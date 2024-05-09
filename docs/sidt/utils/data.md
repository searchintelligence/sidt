# Data

[Sidt Index](../../README.md#sidt-index) / [Sidt](../index.md#sidt) / [Utils](./index.md#utils) / Data

> Auto-generated documentation for [sidt.utils.data](../../../sidt/utils/data.py) module.

- [Data](#data)
  - [computerise_string](#computerise_string)
  - [excel_column_converter](#excel_column_converter)
  - [flatten_structure](#flatten_structure)
  - [humanise_string](#humanise_string)
  - [nested_lookup](#nested_lookup)

## computerise_string

[Show source in data.py:94](../../../sidt/utils/data.py#L94)

Formats a string based on specified parameters to make it computer-readable and ensures consistent encoding.

#### Arguments

- `s` *str* - The input string to clean.
replace_spaces (str, None): If specified, replaces spaces with the given string.
replace_hyphens (str, None): If specified, replaces hyphens with the given string.
- `no_leading_digit` *bool* - If True, adds an underscore in front of leading digits.
- `strip_all_whitespace` *bool* - If True, removes all extra internal and external whitespace.
remove_problematic_chars (bool, str, None): Controls removal of problematic characters.
    - `-` *True* - Removes a default set of problematic characters.
    - False or None: Does not remove any problematic characters.
    - `-` *str* - Removes characters specified in the provided string, e.g., "#$%&".
truncate_length (int, None): If specified, truncates the string to this length.
to_case (str, None): If 'lower' or 'upper', converts the string to the specified case.

#### Signature

```python
def computerise_string(
    s,
    replace_spaces=None,
    replace_hyphens=None,
    no_leading_digit=False,
    strip_all_whitespace=False,
    remove_problematic_chars=True,
    truncate_length=None,
    to_case=None,
): ...
```



## excel_column_converter

[Show source in data.py:57](../../../sidt/utils/data.py#L57)

Converts between a bijective base-26 number and its corresponding alphabetic string and vice versa.

#### Arguments

value (int or str): Numeric index or alphabetic string to be converted.

#### Examples

- excel_column_converter(1) -> 'A'
- excel_column_converter('A') -> 1
- excel_column_converter(28) -> 'AB'
- excel_column_converter('AB') -> 28

#### Signature

```python
def excel_column_converter(value): ...
```



## flatten_structure

[Show source in data.py:37](../../../sidt/utils/data.py#L37)

Recursively flattens a nested list of lists and dictionaries to a single-level list.

#### Examples

flatten([1, [2, [3, 4]], 5, {'a': 6}])
    [1, 2, 3, 4, 5, {'a': 6}]

#### Signature

```python
def flatten_structure(structure): ...
```



## humanise_string

[Show source in data.py:144](../../../sidt/utils/data.py#L144)

Converts a string to a human-readable format, with options to replace abbreviations,
skip capitalisation of certain words, and adjust formatting.

#### Arguments

- `s` *str* - The string to be humanised.
- `replace_underscores` *bool* - If True, replaces underscores with spaces.
- `uncapitalised_words` *set, optional* - A set of words not to capitalise if capitalise is True.
    Defaults to common English articles and prepositions.
- `replacements` *dict, optional* - A dictionary mapping abbreviations to their desired expansions.
    Defaults to common abbreviations.
- `capitalise` *bool* - If True, capitalises each word excluding uncapitalised words.

#### Signature

```python
def humanise_string(
    s,
    replace_underscores=True,
    uncapitalised_words=None,
    replacements=None,
    capitalise=True,
): ...
```



## nested_lookup

[Show source in data.py:5](../../../sidt/utils/data.py#L5)

Safely navigates through a nested dictionary/list structure and retrieves
a value using a specified list of keys/indices.

#### Arguments

nested_item (dict or list): The nested dictionary or list.
- `lookup_keys` *list* - A list of keys or indices specifying the path to the desired value.

#### Returns

The value found at the path, or None if the path is invalid or an error occurs.

#### Examples

data = response.json()  # Assume response.json() returns a list or dict
result = Tools.nested_lookup(data, [0, "key", 5, "title", "value"])

#### Signature

```python
def nested_lookup(nested_item, lookup_keys): ...
```