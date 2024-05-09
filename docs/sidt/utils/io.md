# Io

[Sidt Index](../../README.md#sidt-index) / [Sidt](../index.md#sidt) / [Utils](./index.md#utils) / Io

> Auto-generated documentation for [sidt.utils.io](../../../sidt/utils/io.py) module.

- [Io](#io)
  - [CLIF](#clif)
    - [CLIF.fmt](#cliffmt)
  - [dfs_to_xlsx](#dfs_to_xlsx)
  - [dump](#dump)
  - [get_current_path](#get_current_path)
  - [open_dir](#open_dir)
  - [xlsx_to_dfs](#xlsx_to_dfs)

## CLIF

[Show source in io.py:12](../../../sidt/utils/io.py#L12)

Command line interface formatter. Use CLIF.fmt() to format a string
with specified colors and formats in sequence.

Example usage:
    print(CLIF.fmt("Hello, World!", CLIF.Color.RED, CLIF.Format.BOLD))

#### Signature

```python
class CLIF(Enum, Enum): ...
```

### CLIF.fmt

[Show source in io.py:51](../../../sidt/utils/io.py#L51)

Format text with specified color and styles applied in sequence.

#### Arguments

- `text` *str* - The text to format.
- `*args` - Arbitrary list of CLIF.Color and CLIF.Format to apply.

#### Returns

- `str` - The formatted text.

#### Signature

```python
@staticmethod
def fmt(text, *args): ...
```



## dfs_to_xlsx

[Show source in io.py:108](../../../sidt/utils/io.py#L108)

Writes a dictionary of DataFrames to an Excel file, with each DataFrame as a separate sheet.

#### Arguments

- `dfs` *dict* - A dictionary where keys are sheet names and values are DataFrames.
- `file_path` *str* - The path where the Excel (.xlsx) file will be saved.

#### Signature

```python
def dfs_to_xlsx(dfs, file_path): ...
```



## dump

[Show source in io.py:67](../../../sidt/utils/io.py#L67)

#### Signature

```python
def dump(data, filename): ...
```



## get_current_path

[Show source in io.py:83](../../../sidt/utils/io.py#L83)

Returns the absolute directory path of the python file from which this function is called.

#### Signature

```python
def get_current_path(): ...
```



## open_dir

[Show source in io.py:122](../../../sidt/utils/io.py#L122)

Opens a directory or file in the system's default file explorer or associated application.
Supports Windows, macOS, and Linux operating systems.

#### Arguments

- `target_dir` *str* - The directory path to open.
- `return_pid` *bool* - If True, returns the process ID (int) of the file explorer.

#### Signature

```python
def open_dir(target_dir, return_pid=False): ...
```



## xlsx_to_dfs

[Show source in io.py:94](../../../sidt/utils/io.py#L94)

Reads an Excel file and returns a dictionary of DataFrames, one for each sheet.

#### Arguments

- `file_path` *str* - The path to the Excel (.xlsx) file.

#### Returns

- `dict` - A dictionary where keys are sheet names and values are DataFrames corresponding to each sheet.

#### Signature

```python
def xlsx_to_dfs(file_path): ...
```