# Trustpilot

[Sidt Index](../../README.md#sidt-index) / [Sidt](../index.md#sidt) / [Interfaces](./index.md#interfaces) / Trustpilot

> Auto-generated documentation for [sidt.interfaces.trustpilot](../../../sidt/interfaces/trustpilot.py) module.

- [Trustpilot](#trustpilot)
  - [Review](#review)
  - [Trustpilot](#trustpilot-1)
  - [get_reviews](#get_reviews)
  - [get_site_info](#get_site_info)
  - [process_reviews](#process_reviews)

## Review

[Show source in trustpilot.py:8](../../../sidt/interfaces/trustpilot.py#L8)

#### Signature

```python
class Review: ...
```



## Trustpilot

[Show source in trustpilot.py:16](../../../sidt/interfaces/trustpilot.py#L16)

#### Signature

```python
class Trustpilot: ...
```



## get_reviews

[Show source in trustpilot.py:35](../../../sidt/interfaces/trustpilot.py#L35)

#### Signature

```python
def get_reviews(id, headers) -> list[Review]: ...
```

#### See also

- [Review](#review)



## get_site_info

[Show source in trustpilot.py:51](../../../sidt/interfaces/trustpilot.py#L51)

#### Signature

```python
def get_site_info(id, headers) -> Trustpilot: ...
```

#### See also

- [Trustpilot](#trustpilot)



## process_reviews

[Show source in trustpilot.py:25](../../../sidt/interfaces/trustpilot.py#L25)

#### Signature

```python
def process_reviews(response) -> list[Review]: ...
```

#### See also

- [Review](#review)