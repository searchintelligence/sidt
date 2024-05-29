import csv
import os
import inspect

from enum import Enum
from typing import Union, List, Dict
from xlsxwriter.workbook import Worksheet
from dataclasses import asdict, fields, dataclass, field

import numpy as np
import pandas as pd

from pandas.api.types import is_datetime64_any_dtype

from ..utils.data import humanise_string, computerise_string, excel_column_converter


class CLIF():
    """
    Command line interface formatter. Use CLIF.fmt() to format a string 
    with specified colors and formats in sequence.

    Example usage:
        print(CLIF.fmt("Hello, World!", CLIF.Color.RED, CLIF.Format.BOLD))
    """

    class Color(Enum):
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"
        BRIGHT_BLACK = "\033[90m"
        BRIGHT_RED = "\033[91m"
        BRIGHT_GREEN = "\033[92m"
        BRIGHT_YELLOW = "\033[93m"
        BRIGHT_BLUE = "\033[94m"
        BRIGHT_MAGENTA = "\033[95m"
        BRIGHT_CYAN = "\033[96m"
        BRIGHT_WHITE = "\033[97m"

    class Format(Enum):
        BOLD = "\033[1m"
        DIM = "\033[2m"
        ITALIC = "\033[3m"
        UNDERLINE = "\033[4m"
        BLINK = "\033[5m"
        REVERSE = "\033[7m"
        HIDDEN = "\033[8m"
        STRIKE = "\033[9m"

    RESET = "\033[0m"

    @staticmethod
    def fmt(text, *args):
        """
        Format text with specified color and styles applied in sequence.
        
        Args:
            text (str): The text to format.
            *args: Arbitrary list of CLIF.Color and CLIF.Format to apply.

        Returns:
            str: The formatted text.
        """
        format_sequence = "".join(arg.value for arg in args)
        return f"{format_sequence}{text}{CLIF.RESET}"


def dump(data, filename="output"):
    # data must be a dataclass object or list of the same dataclass objects

    origin = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    os.makedirs(os.path.join("out", origin), exist_ok=True)
    path = os.path.join("out", origin, filename + ".csv")

    field_names = [f.name for f in fields(data[0])]

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        for item in data:
            writer.writerow(asdict(item))


def xlsx_to_dfs(file_path):
    """
    Reads an Excel file and returns a dictionary of DataFrames, one for each sheet.

    Parameters:
    file_path (str): The path to the Excel (.xlsx) file.

    Returns:
    dict: A dictionary where keys are sheet names and values are DataFrames corresponding to each sheet.
    """

    return pd.read_excel(pd.ExcelFile(file_path), sheet_name=None, index_col=None)


def dfs_to_xlsx(dfs, file_path):
    """
    Writes a dictionary of DataFrames to an Excel file, with each DataFrame as a separate sheet.

    Parameters:
    dfs (dict): A dictionary where keys are sheet names and values are DataFrames.
    file_path (str): The path where the Excel (.xlsx) file will be saved.
    """

    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name)


class XLWriter():
    """
    Class for writing dataframes to Excel with clean formatting, titles, contents, descriptions, and navigation.

    Methods:
        __init__(): Initializes the writer with a specified file path.
        add_sheet(): Adds a DataFrame as a new sheet in the Excel file.
        add_contents(): Adds a contents sheet listing all other sheets. (optional)
        write(): Writes all added sheets to the Excel file and saves it.
    """

    def __init__(self, file_path="xlwriter_output.xlsx"):
        """
        Initialize the XLWriter with a file path.

        Args:
            file_path (str): The file path for the output Excel file. Defaults to "xlwriter_output.xlsx".
        """

        XLWriter._validate_file_path(file_path)
        self.file_path = file_path
        self.has_contents = False
        self.sheets = []


    @dataclass
    class Sheet:
        """Data class representing a sheet in the Excel file."""

        df: pd.DataFrame
        sheet_name: str
        table_name: str
        title: str
        description: str
        no_cols: int
        autofilter: bool = True
        show_index: bool = False
        extra_info: Dict[str, str] = field(default_factory=dict)
        column_widths: Union[int, List[int], Dict[str, int]] = field(default_factory=lambda: 15)
        wrap_cells: bool = False
        worksheet: Worksheet = None
        is_contents: bool = False
        humanise_headers: bool = False
        enum_sheet_name: bool = True

        def __post_init__(self):
            self._validate_sheet_attributes()

        def _validate_sheet_attributes(self):
            if not self.sheet_name:
                raise ValueError("Sheet name cannot be empty.")
            if not self.table_name:
                raise ValueError("Table name cannot be empty.")
            if self.df is None or self.df.empty:
                raise ValueError("DataFrame cannot be empty.")
            if not isinstance(self.column_widths, (int, list, dict)):
                raise TypeError("Column widths must be an integer, list, or dictionary.")
            if self.no_cols != len(self.df.columns):
                raise ValueError("Number of columns in DataFrame does not match 'no_cols'.")
            if not isinstance(self.autofilter, bool):
                raise TypeError("Autofilter must be a boolean value.")
            if not isinstance(self.show_index, bool):
                raise TypeError("Show index must be a boolean value.")
            if not isinstance(self.wrap_cells, bool):
                raise TypeError("Wrap cells must be a boolean value.")
            if not isinstance(self.is_contents, bool):
                raise TypeError("Is contents must be a boolean value.")
            if not isinstance(self.humanise_headers, bool):
                raise TypeError("Humanise headers must be a boolean value.")
            if not isinstance(self.enum_sheet_name, bool):
                raise TypeError("Enum sheet name must be a boolean value.")


    def add_sheet(self, df, sheet_name, title="Data", description="", extra_info={}, autofilter=True, _is_contents=False, 
                  column_widths=None, wrap_cells=False, humanise_headers=True, position=-1, enum_sheet_name=True,
                  default_col_width=15, index=False):
        """
        Adds a DataFrame as a new sheet in the Excel file.

        Args:
            df (pd.DataFrame): DataFrame to be written to the sheet.
            sheet_name (str): Name of the sheet.
            title (str): Title of the sheet. Defaults to 'Data'.
            description (str): Description of the sheet. Defaults to ''.
            extra_info (dict): Additional information for the sheet. Defaults to {}.
            autofilter (bool): Whether to apply autofilter. Defaults to True.
            column_widths (Union[int, List[int], Dict[int, int], None]): Specifies column widths.
                Options are:
                    'int' - Applies the same width to all columns,
                    'List[int]' - Specifies individual widths for each column,
                    'Dict[int, int]' - Specifies widths for columns by their index,
                    'None' - Uses the default column width.
            default_col_width (int): Default column width. Defaults to 15.
            wrap_cells (bool): Whether to wrap text in cells. Defaults to False.
            humanise_headers (bool): Whether to humanize headers. Defaults to True.
            position (int): Position to insert the sheet. Defaults to -1 (append).
            enum_sheet_name (bool): Whether to enumerate the sheet name. Defaults to True.
            index (bool): Whether to include the DataFrame index. Defaults to False.

        Example usage:
            add_sheet(df, sheet_name="Revenue", title="Quarterly Revenue", description="Q1 Analysis",
                    autofilter=True, column_widths=[10, 20, 30], default_col_width=12,
                    wrap_cells=True, humanise_headers=False, position=0, enum_sheet_name=False,
                    index=True)
        """
                
        # Clean sheet name and table name
        sheet_name = humanise_string(sheet_name)
        sheet_name = computerise_string(sheet_name, truncate_length=31, remove_problematic_chars=True, strip_all_whitespace=True)
        table_name = computerise_string(sheet_name, remove_problematic_chars=True, replace_hyphens="_", strip_all_whitespace=True, 
                                        no_leading_digit=True, replace_spaces="_", to_case="lower")
        
        # Convert column headers to human readable format if required
        if humanise_headers:
            df.columns = [humanise_string(col) for col in df.columns]

        # Determine column widths
        no_cols = len(df.columns)
        column_widths = self._get_column_widths(no_cols, column_widths, default_col_width)

        # Create the sheet object
        sheet = XLWriter.Sheet(df=df, sheet_name=sheet_name, table_name=table_name, title=title, description=description, no_cols=no_cols, 
                               extra_info=extra_info, column_widths=column_widths, wrap_cells=wrap_cells, autofilter=autofilter, is_contents=_is_contents,
                               humanise_headers=humanise_headers, show_index=index, enum_sheet_name=enum_sheet_name)
        
        # Insert the sheet at the specified position, defaults to append
        if position < 0:
            position = max(len(self.sheets) + position + 1, 0)
        self.sheets.insert(position, sheet)


    def add_contents(self, title="Contents", sheet_name="Contents", stars=True, column_widths=[30, 60, 100], default_col_width=15):
        """
        Add a contents sheet summarizing all other sheets. Use after adding any required sheets.

        Args:
            title (str): Title of the contents sheet. Defaults to "Contents".
            sheet_name (str): Name of the contents sheet. Defaults to "Contents".
            stars (bool): Whether to include a star column. Defaults to True.
            column_widths (list): List of column widths. Defaults to [30, 60, 100].
            default_col_width (int): Default column width. Defaults to 15.
        """

        # Finalise sheets before generating contents to ensure correct sheet names
        self._finalise_sheets()

        # Get the main body contents df
        contents_df = self._get_contents_df()

        # Add star column if required
        if stars:
            contents_df.insert(1, "★", "")
            column_widths.insert(1, 2)

        # Add contents sheet to the writer
        self.add_sheet(df=contents_df, sheet_name=sheet_name, title=title, default_col_width=default_col_width,
                       description="Contents Sheet", autofilter=False, column_widths=column_widths, 
                       wrap_cells=True, position=0, enum_sheet_name=False, _is_contents=True)
        self.has_contents = True
        self.contents_title = title
        self.contents_sheet_name = sheet_name
        

    def write(self):
        """
        Write all added sheets and the contents to the Excel file and saves it.
        Should be called after adding all required sheets with add_sheet() and add_contents().
        """

        # Explicitly finalise sheets if contents are not added
        if not self.has_contents:
            self._finalise_sheets()

        self._initialise_writer()
        for sheet in self.sheets:

            # Create the worksheet if it doesn't exist
            if sheet.worksheet is None:
                worksheet = self.writer.book.add_worksheet(sheet.sheet_name)
                sheet.worksheet = worksheet

            self._write_sheet_title(sheet)
            self._write_sheet_data(sheet)

        self.writer.close()


    def _finalise_sheets(self):
        """
        Processing for sheets once all have been added.
        """

        # Finalise the sheet names and titles
        for i, sheet in enumerate(self.sheets):
            if sheet.enum_sheet_name:
                sheet.sheet_name = computerise_string(f"{i + 1}. {sheet.sheet_name}", truncate_length=31)


    def _initialise_writer(self):
        """
        Initialise the Excel writer and styles.

        Sets up the Excel writer, output sheets list, and formatting styles for titles, descriptions, and hyperlinks.
        """

        # Initialise writer
        self.writer = pd.ExcelWriter(self.file_path, engine="xlsxwriter")
        
        # Initialise styles and formats
        self.table_style = "Table Style Light 12"
        title_base_style =    {"bold": True, "align": "left", "valign": "vcenter", "text_wrap": True, "fg_color": "#8064a2"}
        hyprlink_base_style = {"bold": True, "align": "left", "valign": "vcenter", "text_wrap": True, "underline": 1}
        self.formats = {
            "title":              self.writer.book.add_format({**title_base_style, "font_size": 16, "font_color": "#FFFFFF"}),
            "description":        self.writer.book.add_format({**title_base_style, "font_size": 11, "font_color": "#FFFFFF"}),
            "hyperlink_sheet":    self.writer.book.add_format({**hyprlink_base_style, "font_size": 12, "font_color": "#FFDE15", "fg_color": "#8064a2"}),
            "hyperlink_contents": self.writer.book.add_format({**hyprlink_base_style, "font_size": 11, "font_color": "#8557ea"}),
        }


    def _get_contents_df(self):
        """
        Create a DataFrame summarizing all sheets' metadata.

        Returns:
            pd.DataFrame: DataFrame containing sheet names, titles, descriptions, and extra information.
        """

        contents_data = []
        for sheet in self.sheets:
            sheet_metadata = {
                "sheet_name": sheet.sheet_name,
                "title": sheet.title,
                "description": sheet.description
            }

            # Add extra information to the metadata
            for key, value in sheet.extra_info.items():
                sheet_metadata[key] = value
            contents_data.append(sheet_metadata)
        
        contents_df = pd.DataFrame(contents_data)        
        return contents_df


    def _write_sheet_data(self, sheet):
        """
        Write data to the specified sheet, including hyperlinks if it is the contents sheet.

        Args:
            sheet (Sheet): The sheet object containing the DataFrame and metadata.
        """

        start_row = 2 + len(sheet.extra_info.keys())

        # If sheet is the contents sheet, write the contents data
        if sheet.is_contents:
            self._df_to_table(sheet.df, sheet, start_row=start_row)

            # Adding hyperlinks to the sheet names in the Contents sheet
            sheet_names = sheet.df["Sheet Name"].tolist()
            for row_num, sheet_name in enumerate(sheet_names): 
                link_sheet_name = f"'{sheet_name}'!A1"
                link_formula = f'=HYPERLINK("#{link_sheet_name}", "{sheet_name}")'
                sheet.worksheet.write_formula(row_num+start_row+1, 0, link_formula, self.formats["hyperlink_contents"])
        
        # If sheet is not the contents sheet, offset by 1 row for back-link to contents
        else:
            if self.has_contents:
                start_row += 1
            self._df_to_table(sheet.df, sheet, start_row=start_row)


    def _write_sheet_title(self, sheet):
        """
        Write the title, description, extra information, and hyperlink to the worksheet.

        Args:
            sheet (Sheet): The Sheet object containing the DataFrame and metadata.
        """

        worksheet = sheet.worksheet
        main_df = sheet.df

        # Determine the last column and row indices for the title section
        end_col_index = len(main_df.columns)
        if sheet.show_index:
            end_col_index += 1
        end_col_name = excel_column_converter(end_col_index)
        end_row_index = 2 + len(sheet.extra_info.keys())
                
        # Write, merge, and format title and description
        if end_col_index > 1:
            worksheet.merge_range(f"A1:{end_col_name}1", sheet.title, self.formats["title"])
            worksheet.merge_range(f"A2:{end_col_name}2", sheet.description, self.formats["description"])

            # Write extra information
            for i, (key, value) in enumerate(sheet.extra_info.items()):
                text = f"{humanise_string(key)} - {value}"
                worksheet.merge_range(f"A{3+i}:{end_col_name}{3+i}", text, self.formats["description"])
        else:
            worksheet.write("A1", sheet.title, self.formats["title"])
            worksheet.write("A2", sheet.description, self.formats["description"])

            # Write extra information
            for i, (key, value) in enumerate(sheet.extra_info.items()):
                text = f"{humanise_string(key)} - {value}"
                worksheet.write(f"A{3+i}", text, self.formats["description"])
            
        # Add hyperlink to return to the contents sheet
        if self.has_contents and not sheet.is_contents:
            if end_col_index > 1:
                worksheet.merge_range(f"A{end_row_index+1}:{end_col_name}{end_row_index+1}", "Return to Contents")
            link_sheet_name = f"'{self.contents_sheet_name}'!A1"
            link_formula = f'=HYPERLINK("#{link_sheet_name}", "Return to Contents")'
            worksheet.write_formula(end_row_index, 0, link_formula, self.formats["hyperlink_sheet"])


    def _df_to_table(self, df, sheet, start_row=0, start_col=0):
        """
        Write the DataFrame to the specified sheet in the Excel file, formatting it as a table.

        Args:
            df (pd.DataFrame): The DataFrame to write to the sheet.
            sheet (Sheet): The sheet object containing metadata and formatting options.
            start_row (int): The starting row for writing the DataFrame. Defaults to 0.
            start_col (int): The starting column for writing the DataFrame. Defaults to 0.
        """

        # Determine the last row and column indices
        end_row = start_row + len(df)
        end_col = start_col + len(df.columns) - 1

        # Handle index
        if sheet.show_index:
            end_col += 1

        # Write the DataFrame to Excel
        df.to_excel(self.writer, sheet_name=sheet.sheet_name, startrow=start_row, startcol=start_col, index=sheet.show_index, header=True)
        worksheet = sheet.worksheet

        # Reformat column headers if configured to do so.
        if sheet.humanise_headers:
            df.columns = [humanise_string(col) for col in df.columns]

        # Set the table formatting config and set the range as a table
        table_config = {
            "columns": [{"header": column} for column in df.columns],
            "style": self.table_style,
            "autofilter": sheet.autofilter,
            "name": sheet.table_name
        }
        worksheet.add_table(first_row=start_row, first_col=start_col, last_row=end_row, last_col=end_col, options=table_config)

        # Apply text wrapping to headers
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(start_row, start_col + col_num, value, self.formats["description"])

        # Combined loop to set column widths and apply data formats
        for i, column_name in enumerate(df.columns, start=start_col):
            
            # Determine the format object for the column
            data_format = self._get_column_data_format(df[column_name])
            format = {}
            if sheet.wrap_cells:
                format["text_wrap"] = True
            format["num_format"] = data_format

            # Apply the format to the column
            format_obj = self.writer.book.add_format(format)
            col_width = sheet.column_widths[i - start_col]
            worksheet.set_column(i, i, col_width, format_obj)

            
    @staticmethod
    def _get_column_data_format(column):
        """
        Determine the appropriate format string for a DataFrame column based on its content.

        Args:
            column (pd.Series): The DataFrame column to analyze.

        Returns:
            str: The format string to use for the column.
        """

        # If all values are missing
        if column.dropna().empty:
            return ""
        
        # If the column is of datetime type
        elif is_datetime64_any_dtype(column):
            # You can customize this format string as needed
            return "mm/dd/yyyy hh:mm:ss"

        # If all values are numeric
        elif column.dropna().apply(lambda x: isinstance(x, (int, float, np.float64, np.int64))).all():
            max_value = column.max()

            # If all values are integers
            if column.dropna().apply(lambda x: float(x).is_integer()).all():
                return "#,##0"
            
            # If some values are floats
            else:
                if max_value > 10000:
                    return "#,##0"
                else:
                    return "#,##0.00"

        # If some values are non-numeric
        else:
            return "@" 


    @staticmethod
    def _get_column_widths(no_cols, column_widths, default_width=15):
        """
        Determine column widths based on the input type.

        Args:
            no_cols (int): Number of columns.
            column_widths (int, List[int], Dict[int, int], or None): The widths to set for columns.
                - int: Same width for all columns.
                - List[int]: Specific width for each column.
                - Dict[int, int]: Width for each column by index.
                - None: Use the default width for all columns.
            default_width (int): Default width to use if not specified. Defaults to 15.

        Returns:
            List[int]: List of column widths.
        """

        if isinstance(column_widths, int):
            column_widths = [column_widths] * no_cols
        elif isinstance(column_widths, list) and len(column_widths) < no_cols:
            column_widths.extend([default_width] * (no_cols - len(column_widths)))
        elif isinstance(column_widths, dict):
            column_widths = [column_widths.get(col, default_width) for col in range(no_cols)]
        elif column_widths is None:
            column_widths = [default_width] * no_cols
        
        return column_widths


    @staticmethod
    def _validate_file_path(file_path):
        """
        Validate the Excel file path's format and directory existence.
        """

        if not isinstance(file_path, str):
            raise ValueError("file_path must be a string.")

        if not file_path.endswith(".xlsx"):
            raise ValueError("The file_path must end with '.xlsx' to indicate an Excel file.")

        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            raise FileNotFoundError(f"The directory {directory} does not exist. Please create it or use an existing directory.")


    @staticmethod
    def df_to_xlsx(df, file_path="xlwriter_output.xlsx", sheet_name="sheet1", **kwargs):
        """
        Simplifies the process of writing a single DataFrame to an Excel file without adding a contents page.

        Args:
            df (pd.DataFrame): DataFrame to be written.
            file_path (str): Path to the output Excel file. Defaults to "xlwriter_output.xlsx".
            sheet_name (str): Name of the Excel sheet. Defaults to "sheet1".

        Keyword Args:
            title (str): Title of the Excel sheet.
            description (str): Description of the Excel sheet.
            column_widths (Union[int, List[int], Dict[str, int]]): Specifies column widths.
                'int' for uniform width, 'List[int]' for specific widths per column, 'Dict[str, int]' for named columns.
            wrap_cells (bool): Whether to wrap text in cells. Defaults to False.
            autofilter (bool): Whether to apply autofilter. Defaults to True.
            humanise_headers (bool): Whether to humanize headers. Defaults to False.
            index (bool): Whether to include the DataFrame index. Defaults to False.

        Example usage:
            df_to_xlsx(df, file_path="data_output.xlsx", sheet_name="Data", title="Summary Data", description="Detailed summary")
        """

        writer = XLWriter(file_path)
        writer.add_sheet(df=df, sheet_name=sheet_name, enum_sheet_name=False, **kwargs)
        writer.write()


    @staticmethod
    def dfs_to_xlsx(dfs, file_path="xlwriter_output.xlsx", with_contents=True, **kwargs):
        """
        Writes multiple DataFrames to a single Excel file, each DataFrame as a separate sheet, optionally including a contents page.

        Args:
            dfs (dict of {str: pd.DataFrame}): A dictionary where each key is the sheet name and each value is a DataFrame to be written to that sheet.
            file_path (str): The file path where the Excel file will be saved. Defaults to 'xlwriter_output.xlsx'.
            with_contents (bool): Whether to include a contents page that lists all sheets. Defaults to True.

        Keyword Args:
            All keyword arguments accepted by 'add_sheet' can be passed through here. For example:
                title (str): Title of the Excel sheet. Defaults to the sheet name if not provided.
                description (str): Description of the Excel sheet. Defaults to an empty string.
                column_widths (Union[int, List[int], Dict[str, int]]): Column widths specification.
                wrap_cells (bool): Whether to enable text wrapping within cells.
                autofilter (bool): Whether to enable autofilter for the sheets.
                humanise_headers (bool): Whether to humanize headers.
                index (bool): Whether to include the DataFrame index.

        Example usage:
            dfs = {'Sales': sales_df, 'Inventory': inventory_df}
            dfs_to_xlsx(dfs, file_path="report.xlsx", with_contents=True, title="Financial Data", autofilter=True)
        """

        writer = XLWriter(file_path)
        for sheet_name, df in dfs.items():
            writer.add_sheet(df=df, sheet_name=sheet_name, enum_sheet_name=True, **kwargs)
        if with_contents:
            writer.add_contents()
        writer.write()