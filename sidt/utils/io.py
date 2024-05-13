import csv
import os
import inspect

from enum import Enum
from typing import Union, List, Dict
from xlsxwriter.workbook import Worksheet
from dataclasses import asdict, fields, dataclass, field

import numpy as np
import pandas as pd

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


def dump(data, filename):
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
    """Class for writing dataframes to Excel with clean formatting, titles, contents and descriptions"""


    def __init__(self, file_path="xlwriter_output.xlsx"):
        self.file_path = file_path
        self.has_contents = False
        self.sheets = []


    @dataclass
    class Sheet:
        df: pd.DataFrame
        sheet_name: str
        table_name: str
        title: str
        description: str
        no_cols: int
        autofilter: bool = True
        include_headers: bool = True
        include_index: bool = False
        extra_info: Dict[str, str] = field(default_factory=dict)
        column_widths: Union[int, List[int], Dict[str, int]] = field(default_factory=lambda: 15)
        wrap_cells: bool = False
        worksheet: Worksheet = None
        is_contents: bool = False


    def add_sheet(self, df, sheet_name, title, description, extra_info={}, autofilter=False, is_contents=False, column_widths=None, wrap_cells=False, humanise_headers=True, position=-1, enum_sheet_name=True):
        """"""
        
        # Computerise sheet name
        if enum_sheet_name:
            num_sheets = len(self.sheets)
            sheet_name = f"{num_sheets + 1}. {sheet_name}"
        sheet_name = computerise_string(sheet_name, truncate_length=31, remove_problematic_chars=True, strip_all_whitespace=True)
        table_name = computerise_string(sheet_name, remove_problematic_chars=True, replace_hyphens="_", strip_all_whitespace=True, 
                                        no_leading_digit=True, replace_spaces="_", to_case="lower")
        
        # Convert column headers to human readable format
        if humanise_headers:
            df.columns = [humanise_string(col) for col in df.columns]

        # Get sheet metadata
        no_cols = len(df.columns)

        # Add the sheet to the list
        sheet = XLWriter.Sheet(df=df, sheet_name=sheet_name, table_name=table_name, title=title, description=description, no_cols=no_cols, 
                               extra_info=extra_info, column_widths=column_widths, wrap_cells=wrap_cells, autofilter=autofilter, is_contents=is_contents)
        if position < 0:
            position = max(len(self.sheets) + position + 1, 0)
        self.sheets.insert(position, sheet)


    def add_contents(self, title="Contents", sheet_name="Contents", stars=True, col_widths=[30, 60, 100], default_col_width=15):
        self.contents_stars = stars
        self.contents_title = title
        self.contents_sheet_name = sheet_name
        self.contents_col_widths = col_widths
        self.contents_default_col_width = default_col_width
        
        # Get the main body contents df
        contents_df = self._get_contents_df()
        no_cols = len(contents_df.columns)
        col_widths = self.contents_col_widths
        
        # Determine column widths
        if isinstance(col_widths, int):
            col_widths = [col_widths] * no_cols
        elif isinstance(col_widths, list) and len(col_widths) < no_cols:
            col_widths.extend([self.contents_default_col_width] * (no_cols - len(col_widths)))
        elif isinstance(col_widths, dict):
            col_widths = [col_widths.get(col, self.contents_default_col_width) for col in contents_df.columns]
        
        # Add star column if required
        if self.contents_stars:
            contents_df.insert(1, "★", "")
            col_widths.insert(1, 2)
        self.contents_col_widths = col_widths
        
        # Add contents sheet to the writer
        self.add_sheet(df=contents_df, sheet_name=self.contents_sheet_name, title=self.contents_title, 
                       description="Contents Sheet", autofilter=False, column_widths=col_widths, 
                       wrap_cells=True, position=0, enum_sheet_name=False, is_contents=True)
        self.has_contents = True


    def write(self):

        self._initialise_writer()
        
        for sheet in self.sheets:

            # Create the worksheet if it doesn't exist
            if sheet.worksheet is None:
                worksheet = self.writer.book.add_worksheet(sheet.sheet_name)
                sheet.worksheet = worksheet

            self._sheet_to_excel(sheet)

        self.writer.close()


    def _get_contents_df(self):

        contents_data = []
        
        for sheet in self.sheets:
            sheet_metadata = {
                "sheet_name": sheet.sheet_name,
                "title": sheet.title,
                "description": sheet.description
            }
            for key, value in sheet.extra_info.items():
                sheet_metadata[key] = value
            contents_data.append(sheet_metadata)
        
        contents_df = pd.DataFrame(contents_data)        
        return contents_df


    def _initialise_writer(self):

        # Initialise writer
        self.writer = pd.ExcelWriter(self.file_path, engine="xlsxwriter")
        self.out_sheets = []
        
        # Initialise styles
        self.table_style = "Table Style Light 12"
        self.formats = {
            "title": self.writer.book.add_format({"bold": True, "font_size": 16, "font_color": "#FFFFFF", "align": "left", "valign": "vcenter", "text_wrap": True, "fg_color": "#8064a2"}),
            "description": self.writer.book.add_format({"bold": True, "font_size": 11, "font_color": "#FFFFFF", "align": "left", "valign": "vcenter", "text_wrap": True, "fg_color": "#8064a2"}),
            "header_hyperlink": self.writer.book.add_format({"bold": True, "font_size": 12, "font_color": "#FFDE15", "align": "left", "valign": "vcenter", "text_wrap": True, "fg_color": "#8064a2", "underline": 1}),
            "contents_hyperlink": self.writer.book.add_format({"bold": True, "underline": 1, "font_color": "#8557ea"}),
            "wrap_text": self.writer.book.add_format({"text_wrap": True})
        }


    def _sheet_to_excel(self, sheet):

        # Write title and description using merged cells, if applicable
        self._write_sheet_title(sheet)

            
    def _write_sheet_title(self, sheet):
        worksheet = sheet.worksheet
        main_df = sheet.df

        last_col_index = len(main_df.columns)
        last_col_name = excel_column_converter(last_col_index)
        last_row_index = 2 + len(sheet.extra_info.keys())
        
        # Merge and format title and description
        if last_col_index > 1:
            worksheet.merge_range(f"A1:{last_col_name}1", sheet.title, self.formats["title"])
            worksheet.merge_range(f"A2:{last_col_name}2", sheet.description, self.formats["description"])

            for i, (key, value) in enumerate(sheet.extra_info.items()):
                text = f"{humanise_string(key)} - {value}"
                worksheet.merge_range(f"A{3+i}:{last_col_name}{3+i}", text, self.formats["description"])
        else:
            # Write without merging if only one column
            worksheet.write("A1", sheet.title, self.formats["title"])
            worksheet.write("A2", sheet.description, self.formats["description"])
            
        # Hyperlink to return to the contents sheet
        if self.has_contents and not sheet.is_contents:
            if last_col_index > 1:
                worksheet.merge_range(f"A{last_row_index+1}:{last_col_name}{last_row_index+1}", "Return to Contents")
            link_sheet_name = f"'Contents'!A1"
            link_formula = f'=HYPERLINK("#{link_sheet_name}", "Return to Contents")'
            worksheet.write_formula(last_row_index, 0, link_formula, self.formats["header_hyperlink"])
