# ai-es-utils

This module provides high-level access to the elastic search client. 
The focus is to aid and stream-line the building of queries specific for TW.

## Workflow

We designed the workflow with various interfaces in mind:

### Search Executor
The search executor is a high level object that combines all the other interfaces. The search executor accepts a payload and returns processed search results. To this end, the object needs to be initialized with the respective query-components, query-composer, search-service, and post-processor.

### Query Component
A query component is a self-sufficient object that takes a payload and returns a valid elasticsearch query. A list of query-components defines the search logic of the search executor. Usually the list of queries produced by a list of query components need to be joined using a query composer.

### Query Composer

A query composer handles the merging of a list of single self-sufficient queries, such as produced by query-components. This joining tends to have a large impact on the final search logic. One approach is for example to join only queries that are grouped via the same "name". However, one can think of many more composing strategies.

### Post Processor

The post-processor does various things important for the TW Frontend. One important task is to apply the highlighting. In general, the post-processor takes a result as dict and returns modified results, according to the specified post-processing steps.

## Usage

First, define the search logic that you want to use. You do this by instantiating the query-components that needs to be used:

```python
query_stack = [
    IncludePortalsQuery(),
    GenderQuery(),
    ...,
    SortQuery(),
    SizeAndOffsetQuery(),
    HighlightQuery()
]
```
Second, you need to instatiate a query-composer:
```python
query_composer = DecayLastScrapedGroupedComposer()
```
Finally, we can already put together a search executor, if we use the default post-processor:
```python
smart_search = SearchExecutor(
    ElasticSearchService("prod", hosts=[{"host": "es-dev.internal.talentwunder.com", "port": 80}]),
    query_stack=query_stack,
    query_composer=query_composer,
    verbose=1
)
```
Firing a search is as simple as passing the payload and bearer token to the search executor:
```python
smart_search(request, bearer_token=bearer_token, history_id="1")
```
## Notes

- Current, jobtitle and skill logic is very limited with respect to the fields searched
- The current elasticsearch version (6.8) does allow for span_near/span_multi/fuzzy queries that allow for phrase-queries, i.e. aknowledging the order of terms, as well as apply fuzzy search, i.e. accounting for misspelling. However, the scores will wierd, sometimes rating misspelled terms 4 times higher than the original query word.
- One idea is to have different search logic for different networks. This should be accomplished by a query-composer