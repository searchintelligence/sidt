# Linkedin

[Sidt Index](../../README.md#sidt-index) / [Sidt](../index.md#sidt) / [Interfaces](./index.md#interfaces) / Linkedin

> Auto-generated documentation for [sidt.interfaces.linkedin](../../../sidt/interfaces/linkedin.py) module.

- [Linkedin](#linkedin)
  - [pageData](#pagedata)
  - [searchResult](#searchresult)
  - [login](#login)
  - [make_search](#make_search)
  - [temp](#temp)

## pageData

[Show source in linkedin.py:34](../../../sidt/interfaces/linkedin.py#L34)

#### Signature

```python
class pageData: ...
```



## searchResult

[Show source in linkedin.py:28](../../../sidt/interfaces/linkedin.py#L28)

#### Signature

```python
class searchResult: ...
```



## login

[Show source in linkedin.py:74](../../../sidt/interfaces/linkedin.py#L74)

#### Signature

```python
def login(driver, username, password): ...
```



## make_search

[Show source in linkedin.py:37](../../../sidt/interfaces/linkedin.py#L37)

#### Signature

```python
def make_search(search: str, category: int, page: int): ...
```



## temp

[Show source in linkedin.py:52](../../../sidt/interfaces/linkedin.py#L52)

#### Signature

```python
def temp(term: str, category: int, top_n: int): ...
```