import pandas as pd


def explode_by_multiple(df, explode_on):
    """
    Expands DataFrame by exploding lists in specified columns into separate rows.

    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    explode_on (list of str): Column names containing lists to explode into rows.
    
    Returns:
    pd.DataFrame: DataFrame with each list in specified columns expanded into rows.
    """
    for col in explode_on:
        df = df.explode(col)
    return df


def merge_dfs(dfs, merge_on, fill_na=None, sort_by_merge_col=False):
    """
    Merges a list of pandas DataFrames on a specified column using an outer merge strategy. Optionally fills NaN 
    values and sorts the resulting DataFrame by the merge key.

    Parameters:
    dfs (list of pd.DataFrame): DataFrames to merge.
    merge_on (str): Column name to merge on, must be present in all DataFrames.
    fill_na (numeric, str, or dict, optional): Value(s) to fill NaN, can be a single value or a dict of column fills.
    sort_by_merge_col (bool, optional): If True, sorts the merged DataFrame by the merge column.
    """

    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(left=merged_df, right=df, how="outer", left_on=merge_on, right_on=merge_on, suffixes=("", "_drop"))
    merged_df = merged_df[[col for col in merged_df.columns if not col.endswith("_drop")]]
    if fill_na is not None:
        merged_df.fillna(fill_na, inplace=True)
    if sort_by_merge_col:
        merged_df.sort_values(by=merge_on, ascending=True, inplace=True)
    
    return merged_df


def move_cols(df, cols_to_move, position=None):
    """
    Moves specified columns to specified positions in a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    cols_to_move (dict or list): If a dict, keys are column names and values are the target positions.
                                If a list, all columns in the list will be moved to the position specified
                                by the `position` argument.
    position (int, optional): The position to move all columns to if `cols_to_move` is a list.
                              Required if `cols_to_move` is a list.

    Returns:
    pd.DataFrame: A DataFrame with columns moved to the specified positions.

    Example:
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'index': [4, 5, 6],
        'state': [7, 8, 9],
        'city': [10, 11, 12],
        'B': [13, 14, 15]
    })
    move_cols(df, {'index': 0, 'state': 1, 'city': -1})
    move_cols(df, ['index', 'state', 'city'], 0)
    """
    if isinstance(cols_to_move, list):
        if position is None:
            raise ValueError("Position must be provided when cols_to_move is a list.")
        cols_to_move = {col: position for col in cols_to_move}

    # Ensure all column names exist in the DataFrame
    if not all(col in df.columns for col in cols_to_move):
        raise ValueError("One or more columns specified do not exist in the DataFrame.")

    # Create a new column order
    current_cols = list(df.columns)
    # Remove the columns to move from their current positions
    for col in cols_to_move:
        if col in current_cols:
            current_cols.remove(col)

    # Insert each column in its new position, handling negative indices
    for col, pos in sorted(cols_to_move.items(), key=lambda x: x[1] if x[1] >= 0 else len(current_cols) + x[1] + 1):
        if pos < 0:
            pos += len(current_cols) + 1
        current_cols.insert(pos, col)

    return df[current_cols]

