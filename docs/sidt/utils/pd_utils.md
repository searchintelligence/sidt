# Pd Utils

[Sidt Index](../../README.md#sidt-index) / [Sidt](../index.md#sidt) / [Utils](./index.md#utils) / Pd Utils

> Auto-generated documentation for [sidt.utils.pd_utils](../../../sidt/utils/pd_utils.py) module.

- [Pd Utils](#pd-utils)
  - [explode_by_cols](#explode_by_cols)
  - [merge_dfs](#merge_dfs)
  - [move_cols](#move_cols)

## explode_by_cols

[Show source in pd_utils.py:4](../../../sidt/utils/pd_utils.py#L4)

Expands DataFrame by exploding lists in specified columns into separate rows.

#### Arguments

- `df` *pd.DataFrame* - The DataFrame to modify.
explode_on (list of str): Column names containing lists to explode into rows.

#### Returns

- `pd.DataFrame` - DataFrame with each list in specified columns expanded into rows.

#### Signature

```python
def explode_by_cols(df, explode_on): ...
```



## merge_dfs

[Show source in pd_utils.py:20](../../../sidt/utils/pd_utils.py#L20)

Merges a list of pandas DataFrames on a specified column using an outer merge strategy. Optionally fills NaN
values and sorts the resulting DataFrame by the merge key.

#### Arguments

dfs (list of pd.DataFrame): DataFrames to merge.
- `merge_on` *str* - Column name to merge on, must be present in all DataFrames.
fill_na (numeric, str, or dict, optional): Value(s) to fill NaN, can be a single value or a dict of column fills.
- `sort_by_merge_col` *bool, optional* - If True, sorts the merged DataFrame by the merge column.

#### Signature

```python
def merge_dfs(dfs, merge_on, fill_na=None, sort_by_merge_col=False): ...
```



## move_cols

[Show source in pd_utils.py:44](../../../sidt/utils/pd_utils.py#L44)

Moves specified columns to specified positions in a DataFrame.

#### Arguments

- `df` *pd.DataFrame* - The DataFrame to modify.
cols_to_move (dict or list): If a dict, keys are column names and values are the target positions.
                            If a list, all columns in the list will be moved to the position specified
                            by the `position` argument.
- `position` *int, optional* - The position to move all columns to if `cols_to_move` is a list.
                          Required if `cols_to_move` is a list.

#### Returns

- `pd.DataFrame` - A DataFrame with columns moved to the specified positions.

#### Examples

df = pd.DataFrame({
    - `'A'` - [1, 2, 3],
    - `'index'` - [4, 5, 6],
    - `'state'` - [7, 8, 9],
    - `'city'` - [10, 11, 12],
    - `'B'` - [13, 14, 15]
})
- `move_cols(df,` *{'index'* - 0, 'state': 1, 'city': -1})
move_cols(df, ['index', 'state', 'city'], 0)

#### Signature

```python
def move_cols(
    df, cols_to_move, position=None, inplace=False, ignore_missing_cols=False
): ...
```