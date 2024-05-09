# Imdb

[Sidt Index](../../README.md#sidt-index) / [Sidt](../index.md#sidt) / [Interfaces](./index.md#interfaces) / Imdb

> Auto-generated documentation for [sidt.interfaces.imdb](../../../sidt/interfaces/imdb.py) module.

- [Imdb](#imdb)
  - [searchResult](#searchresult)
  - [get_actor_filmography](#get_actor_filmography)
  - [get_film_info](#get_film_info)
  - [make_search](#make_search)

## searchResult

[Show source in imdb.py:6](../../../sidt/interfaces/imdb.py#L6)

#### Signature

```python
class searchResult: ...
```



## get_actor_filmography

[Show source in imdb.py:57](../../../sidt/interfaces/imdb.py#L57)

Retrieves the filmography of an actor from IMDb.

#### Arguments

- `actor_id` *str* - The IMDb ID of the actor.

#### Returns

- `dict` - A dictionary containing the filmography of the actor, organized by table name.
      The keys are the table names and the values are lists of film IDs.

#### Signature

```python
def get_actor_filmography(actor_id: str) -> dict: ...
```



## get_film_info

[Show source in imdb.py:91](../../../sidt/interfaces/imdb.py#L91)

Retrieves information about a film from IMDb based on the film ID.

#### Arguments

- `film_id` *str* - The IMDb ID of the film.

#### Returns

- `dict` - A dictionary containing the following film information:
    - title (str): The title of the film.
    - year (str): The release year of the film.
    - age_rating (str): The age rating of the film.
    - run_time (str): The duration of the film.
    - rating (str): The IMDb rating of the film.
    - review_count (str): The number of reviews for the film.

#### Signature

```python
def get_film_info(film_id: str) -> dict: ...
```



## make_search

[Show source in imdb.py:14](../../../sidt/interfaces/imdb.py#L14)

Perform a search on IMDb based on the given term and type.

#### Arguments

- `term` *str* - The search term.
- `type` *str, optional* - The type of search. Can be "titles" or "names". Defaults to None.

#### Returns

- `list[searchResult]` - A list of search results.

#### Raises

- `ValueError` - If the type is provided but not one of the accepted types.

#### Signature

```python
def make_search(term: str, type: str = None) -> list[searchResult]: ...
```

#### See also

- [searchResult](#searchresult)