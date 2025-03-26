import ai_es_utils
import os

from setuptools import setup

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(this_directory, "requirements.txt"), "r") as f:
    requirements = [line for line in f]

setup(
    name='ai-es-utils',
    version=ai_es_utils.__version__,
    packages=[
        'ai_es_utils',
        'ai_es_utils.queries',
        'ai_es_utils.queries.models',
        'ai_es_utils.queries.components',
        'ai_es_utils.queries.composers',
        'ai_es_utils.queries.interfaces',
        'ai_es_utils.queries.utils',
        'ai_es_utils.search',
        'ai_es_utils.search.result_parsers',
        'ai_es_utils.services',
        'ai_es_utils.services.enrichment',
        'ai_es_utils.services.search'
    ],
    install_requires=requirements,
    package_data={'': ['README.md']},
    include_package_data=True,
    license='',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
