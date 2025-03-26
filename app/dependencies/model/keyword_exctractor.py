from typing import List

import torch
from transformers import BertTokenizer
from hydra import compose, initialize

from app.dependencies.model.ke_model import KeywordExtractionModel, LABELS, device
from app.keyword_extractor_data_types import KeywordExtractorPayload
from app.utils.ke_utils import moses_normalize


with initialize(version_base=None, config_path="."):
    cfg = compose(config_name="model_config.yaml")


RETURNED_LABELS = ['job-title', 'location', 'company', 'skills', 'skill-paragraph']


class KeywordExtractor:
    def __init__(self, model: KeywordExtractionModel, tokenizer: BertTokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def __call__(self, payload: KeywordExtractorPayload):
        job_ad = payload.dict().get("jobAd")
        job_ad = moses_normalize(job_ad)
        preds_str = []
        input_ids = list()
        token_type_ids = list()
        att_masks = list()
        grids = self._gridify(job_ad)
        indecies_list = []
        for item in grids:
            tokens = self.tokenizer(item, return_tensors='pt', padding='max_length', 
            truncation=True, max_length=cfg.max_len)
            input_id = tokens.input_ids[0].tolist()
            _, indecies = self._find_broken_ids(input_ids=input_id)
            indecies_list.append(indecies)
            token_type_id = tokens.token_type_ids[0].tolist()
            att_mask = tokens.attention_mask[0].tolist()
            input_ids.append(input_id)
            token_type_ids.append(token_type_id)
            att_masks.append(att_mask)
        input_ids = torch.IntTensor(input_ids)
        token_type_ids = torch.IntTensor(token_type_ids)
        att_masks = torch.IntTensor(att_masks)
        with torch.no_grad():
            preds = self.model(input_ids=input_ids, att_masks=att_masks, 
                token_type_ids=token_type_ids).tolist()
        for idx in range(len(preds)):
            preds[idx] = arg_max(preds[idx])
            preds[idx] = flag_rest(preds[idx], indecies_list[idx])
            preds_str.append(self._str_label(preds[idx], input_ids[idx]))
        extracted_labels = dict(zip(RETURNED_LABELS, [[] for i in range(len(RETURNED_LABELS))]))
        for grid_label in preds_str:
            for item in RETURNED_LABELS:
                extracted_labels[item].extend(grid_label[LABELS.index(item)])
        return extracted_labels
    
    def _gridify(self, job_ad):
        grids = self._build_grids(job_ad)
        gridified_dt = []
        sub_item_len= [len(self.tokenizer.tokenize(item)) for item in grids]
        for item in join_grids(grids, sub_item_len):
            gridified_dt.append(item)
        gridified_dt = [grid.replace("\n", ", \n") for grid in gridified_dt]
        return gridified_dt
    
    def _build_grids(self, data):
        splited = [item.strip() for item in data.split("\n\n") if item.strip()]
        sub_item_len = [len(self.tokenizer.tokenize(item)) for item in splited]
        gridified = []
        for idx, item in enumerate(splited):
            if sub_item_len[idx] < cfg.max_len - 12:
                gridified.append(item)
            else:
                grids = [grid.strip() for grid in item.split("\n") if grid.strip()]
                for grid in grids:
                    gridified.append(grid)
        sub_item_len = [len(self.tokenizer.tokenize(item)) for item in gridified]
        grids_sentences = []
        for idx, item in enumerate(gridified):
            if sub_item_len[idx] < cfg.max_len - 12:
                grids_sentences.append(item)
            else:
                sentences = [sentence.strip()+'.' if not sentence.strip().endswith('.')\
                    else sentence.strip() for sentence in item.split(". ")]
                for sentence in sentences:
                    grids_sentences.append(sentence)  
        return grids_sentences
    
    def _find_broken_ids(self, input_ids):
        tkns = [self.tokenizer.decode(item) for item in input_ids]
        tkns = [token.replace(" ", "") for token in tkns]
        brokens = []
        for i in range(len(tkns)-1):
            if '##' in tkns[i+1] and '##' not in tkns[i]:
                chunk = []
                chunk.append(i)
            elif '##' in tkns[i+1] and '##' in tkns[i]:
                chunk.append(i)    
            elif '##' not in tkns[i+1] and '##' in tkns[i]:
                chunk.append(i)
                brokens.append(chunk)     
        broken_ids = []
        for item in brokens:
            broken_ids.append([input_ids[idx] for idx in item])        
        return broken_ids, brokens
    
    def _str_label(self, labels, input_ids):
        written_labels = [[] for i in range(len(LABELS))]
        input_ids = input_ids.tolist()
        for step in range(len(labels)):
            for cls in range(len(LABELS)):
                if labels[step][cls] == 1:
                    if labels[step-1][cls] == 0:
                        written_labels[cls].append([step])
                    elif labels[step-1][cls] == 1:
                        written_labels[cls][-1].append(step)            
                else:
                    continue
        string_labels = [[] for i in range(len(LABELS))]
        for idx, item in enumerate(written_labels):
            for sub_item in item:
                string_labels[idx].append(self.tokenizer.decode([input_ids[step] 
                    for step in sub_item]))
        return string_labels

def join_grids(grids, sub_item_len):
    built_grids = []
    sub_grids = []
    ct = 0
    for i in range(len(sub_item_len)):
        if ct + sub_item_len[i] <= cfg.max_len - 12:
            sub_grids.append(grids[i])
            ct += sub_item_len[i]
            if i == len(sub_item_len) - 1:
                built_grids.append(sub_grids)
        else:
            built_grids.append(sub_grids)
            ct = sub_item_len[i]
            sub_grids = [grids[i]]
            if i == len(sub_item_len) - 1:
                built_grids.append(sub_grids)  
    built_grids = ["\n  ".join(item) for item in built_grids]
    return built_grids

def arg_max(preds):
    for step in range(len(preds)):
        for cls in range(len(LABELS)):
            if preds[step][cls] >= cfg.metrics_threshold:
                preds[step][cls] = 1
            else:
                preds[step][cls] = 0
    return preds

def flag_rest(preds, broken_indecies):
    for pred_idx in range(len(preds)):
        for broken_idx, brokens in enumerate(broken_indecies):
            if pred_idx in brokens:
                elementwise_or = [0 for i in range(len(LABELS))]
                for idx in brokens:
                    elementwise_or = [preds[idx][i] | elementwise_or[i] for
                        i in range(len(LABELS))]
                for idx in brokens:
                    preds[idx] = elementwise_or
                broken_indecies.pop(broken_idx)
                break
    return preds





tokenizer = BertTokenizer.from_pretrained(cfg.tokenizer)
model = KeywordExtractionModel()
model.eval()
model.load_state_dict(torch.load(cfg.trained_KE_wts, map_location='cpu'), strict=False)
keyword_extractor = KeywordExtractor(model, tokenizer)

def get_keyword_extractor() -> KeywordExtractor:
    return keyword_extractor