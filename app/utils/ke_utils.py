import re
import itertools
from ai_es_utils.queries.models import GeoPoint, RequestPayload
import pickle
import collections

import sacremoses as sm
from ai_es_utils.services.enrichment.internal_job2skills_client import InternalJob2SkillsService
import joblib
import networkx as nx
import numpy as np

from app.config import env_settings


DG = pickle.load(open('app/dependencies/data/knowlege_graph.pickle', 'rb'))
NODES = frozenset(DG.nodes)
skills_all = set(joblib.load("app/dependencies/data/id2skill.joblib").values())
jobs_all = set(joblib.load("app/dependencies/data/job2id.joblib").keys())
FILTER_SET = ["and", "skills", "data", "junior", "engineer", "learning",
        "methods", "platform", "core", "auto", "software", "skill", "methods", "/", "|", "*", ",", "!", "@", "deine",
        "platforms", "softwares", 'engineers', "#", "$", "%", "^", "&", ":", ">", "<", ";", "?", "und", "senior",
        "a", "b", "d", "e", "f", "h", "i", "j", "k", "l", "m", "o", "p", "q", "s", "t", "v", "w", "x", "y", "z", "u"]


def replace_unicode_punct(text: str) -> str:
    text = text.replace("，", ",")
    text = re.sub(r"。\s*", ". ", text)
    text = text.replace("、", ",")
    text = text.replace("»", "")
    text = text.replace("«", "")
    text = text.replace("`", "'")
    text = text.replace("–", "")
    text = text.replace("”", '"')
    text = text.replace("„", '')
    text = text.replace("“", '"')
    text = text.replace("∶", ":")
    text = text.replace("：", ":")
    text = text.replace("？", "?")
    text = text.replace('"', '')
    text = text.replace("'", '')
    text = text.replace("《", '"')
    text = text.replace("》", '"')
    text = text.replace("）", ")")
    text = text.replace("！", "!")
    text = text.replace("（", "(")
    text = text.replace("；", ";")
    text = text.replace("１", "1")
    text = text.replace("」", '"')
    text = text.replace("「", '"')
    text = text.replace("０", "0")
    text = text.replace("３", "3")
    text = text.replace("２", "2")
    text = text.replace("５", "5")
    text = text.replace("６", "6")
    text = text.replace("９", "9")
    text = text.replace("７", "7")
    text = text.replace("８", "8")
    text = text.replace("４", "4")
    text = text.replace("✓", "")
    text = re.sub(r"．\s*", ". ", text)
    text = text.replace("～", "~")
    text = text.replace("’", "'")
    text = text.replace("…", "...")
    text = text.replace("━", "-")
    text = text.replace("—", '-')
    text = text.replace("‐", '-')
    text = text.replace("‑", '-')
    text = text.replace("´", "'")
    text = text.replace("〈", "<")
    text = text.replace("〉", ">")
    text = text.replace("【", "[")
    text = text.replace("】", "]")
    text = text.replace("％", "%")
    text = text.replace("é", "e")
    text = text.replace("‘", "'")
    text = text.replace(" ", '')
    return text


def moses_normalize(text: str) -> str:
    ms_normalizer = sm.MosesPunctNormalizer(lang='en')
    text = replace_unicode_punct(text)
    text = ms_normalizer.normalize(text)
    return text

cities_all = {moses_normalize(item) for item in 
    set(joblib.load("app/dependencies/data/cities_international_from_es.joblib").keys())}
countries_all_de = {moses_normalize(item) for item in 
    set(joblib.load("app/dependencies/data/country_trie_de.joblib").keys())}
countries_all_en = {moses_normalize(item) for item in 
    set(joblib.load("app/dependencies/data/country_trie_en.joblib").keys())}
countries_all = countries_all_de | countries_all_en


def sort_results(results):
    processed = {}
    job_title = results['job-title']
    skills = results['skills']
    processed['jobTitles'] = process_job_titles(job_title, skills)
    processed['mandatorySkills'], processed['optionalSkills'] = process_skills(skills,
                processed['jobTitles'])
    processed['locations'] = normalize_location(list(set([item.lower() for 
                item in results['location']])), cities_all=cities_all)
    processed['companies'] = list(set([item.lower() for item in results['company']]))
    return processed

def process_job_titles(job_titles, skills):
    skills = [skill.lower() for skill in skills if skill.lower() in NODES]
    titles = []
    for skill in skills:
        titles = titles + list(DG.adj[skill])
    counts = collections.Counter(titles)
    if job_titles:
        job_titles = [item.lower() for item in job_titles]
        job_titles = normalize_job_titles(job_titles, items_all=jobs_all)
        jobtitles = [item[0] for item in  counts.most_common(3)] + job_titles
        return list(set(jobtitles))

    else:
        jobtitles = [item[0] for item in  counts.most_common(3)]
        return list(set(jobtitles))



def normalize_location(locations, cities_all=cities_all, countries_all=countries_all):
    normalized = []
    for location in locations:
        if (location in cities_all) and (location not in countries_all):
            normalized.append(location)
        elif "remote" in location:
            normalized.append("remote")
    return list(set(normalized))



def frequency(items):
    frequency_dict = {}
    for item in items:
        if item in frequency_dict:
            frequency_dict[item] += 1
        else:
            frequency_dict.setdefault(item, 1)
    return sorted(list(frequency_dict.items()), key=lambda x: x[1], reverse=True)




def process_skills(skills, job_titles):
    skills = [item.lower().strip() for item in skills if item not in FILTER_SET]
    for idx, item in enumerate(skills):
        item = item.replace("-", " ").replace("(", "").replace(")", "").replace("/", " ")
        skills[idx] = " ".join([x.strip() for x in item.split(" ") if x != ""])
    assumed_skills = []
    for job_title in job_titles:
        if job_title in NODES:
            assumed_skills = assumed_skills + list(DG.adj[job_title])
    must_skills = list(set(skills) & set(assumed_skills))
    optional_skills = np.setdiff1d(skills, must_skills).tolist()

    
    return must_skills, optional_skills
    




def normalize_job_titles(items, items_all):
    items_all = {frozenset(item.split(" ")) for item in items_all if item not in FILTER_SET}
    normalized = []
    for item in items:
        item = item.replace("-", " ").replace("(", "").replace(")", "")
        item = " ".join([x.strip() for x in item.split(" ") if x != ""])
        item_set = set([sub_item.strip() for sub_item in item.split(" ") if sub_item != ""])
        if item_set in items_all:
            normalized.append(item)
        else:
            sub_norms = []
            sub_norms_reduced = []
            sub_items = powerset(item_set)
            for combination in sub_items:
                if combination in items_all:
                    sub_norms.append(combination)
            for sub_norm in sub_norms:
                flag = True
                aux_sub_norms = sub_norms[: ]
                aux_sub_norms.remove(sub_norm)
                for aux_sub_norm in aux_sub_norms:
                    if sub_norm.issubset(aux_sub_norm):
                        flag = False
                        break
                if flag:
                    sub_norms_reduced.append(sub_norm)
            if not sub_norms_reduced:
                continue
            for sub_norm_reduced in sub_norms_reduced:
                aux_item = item
                not_items = sub_norm_reduced ^ item_set
                for not_item in not_items:
                    aux_item = aux_item.replace(not_item, "").strip()
                aux_item = " ".join([x.strip() for x in aux_item.split(" ") if x != ""])
                normalized.append(aux_item)
    return list(set(normalized))


   

def powerset(items_set):
    p_set = []
    sub_len = len(items_set)
    while sub_len > 1:
        sub_item_set = list(map(set, itertools.combinations(items_set, sub_len-1)))
        p_set.extend(sub_item_set)
        sub_len -= 1
    return p_set


if __name__ == "__main__":
    skills = ['Machine Learning', 'Machine Learning Engineer', 'AI', 
              'EdTech', 'AI', 'machine learning', 'AI', 'Learning', 'AI - driven', 'backend', 'AI', 'machine learning models', 'AI - driven tutors', 
              'user experience', 'performance metrics', 'ML development', 'model discovery', 'algorithm development', 'backend', 'frontend', 
              'AI', 'machine learning', 'AI', 'machine learning', 'professional experience', 'AI projects', 'model development', 'experimentation', 
              'AI', 'Self - driven', 'independently', 'fast - paced', 'startup', 'product development', 'AI', 'full - stack development', 
              'backend', 'frontend', 'product metrics', 'user growth', 'retention', 'machine learning models', 'AIs']
    job_titles = ['Engineer', 'Product Manager', 'Machine Learning Engineer', 'Machine Learning Engineer']


    # process_job_titles(job_titles, skills)
    for item in ['machine learning engineer', 'product manager']:
        if item in DG:
            print('yes')
        else:
            print("nooo")