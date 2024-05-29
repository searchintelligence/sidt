# SI Data Tools

[![Build](https://github.com/searchintelligence/sidt/actions/workflows/build.yml/badge.svg)](https://github.com/searchintelligence/sidt/actions/workflows/build.yml)
[![Test interfaces/trustpilot](https://github.com/searchintelligence/sidt/actions/workflows/test-trustpilot.yml/badge.svg)](https://github.com/searchintelligence/sidt/actions/workflows/test-trustpilot.yml)
[![Test interfaces/expatistan](https://github.com/searchintelligence/sidt/actions/workflows/test-expatistan.yml/badge.svg)](https://github.com/searchintelligence/sidt/actions/workflows/test-expatistan.yml)

### Usage

Install Using:
```bash
pip install git+https://github.com/searchintelligence/sidt.git
```

Update Using:
```bash
pip install git+https://github.com/searchintelligence/sidt.git --force-reinstall --no-deps
```

### Development

Clone this repo and install it with the edit flag:
```bash
git clone https://github.com/searchintelligence/sidt
pip install -e /path/to/local/repo
```

Create a personal development branch and switch to it:
```bash
git checkout -b arek-dev
```

### Project Structure

<pre>
<b>sidt/</b>
├─ <b>.github/</b>
│  └─ <b>workflows/</b>
│     <i>Store for all Github workflows.</i>
├─ <b>.vscode/</b>
│  <i>Config for the VSCode testing panel.</i>
├─ <b>sidt/</b>
│  <i>The package root directory.</i>
│  ├─ <b>data/</b>
│  │  <i>Store for reusable data.</i>
│  ├─ <b>interfaces/</b>
│  │  <i>Code that interfaces with websites to collect data.</i>
│  └─ <b>utils/</b>
│     <i>Reusable code for common functions.</i>
├─ <b>docs/</b>
│  <i>Package documentation auto-generated from docstrings.</i>
├─ <b>tests/</b>
│  <i>Unit tests for code in the sidt package.</i>
├─ <b>requirements.txt</b>
│  <i>List of required Python dependencies, auto generated with pipreqs.</i>
├─ <b>setup.py</b>
│  <i>Script that initialises the Python package upon installation.</i>
├─ <b>README.md</b>
└─ <b>LICENSE</b>
</pre>

## Examples

### Trustpilot [![Test interfaces/trustpilot](https://github.com/searchintelligence/sidt/actions/workflows/test-trustpilot.yml/badge.svg)](https://github.com/searchintelligence/sidt/actions/workflows/test-trustpilot.yml)

```python
from sidt.interfaces import trustpilot

sites = [
    "Zara.com",
    "Uniqlo.com",
    "Nike.com",
    "Lululemon.com"
]

# Collect review count and score for each site

output = []
for site in sites:
    trustpilot_id = trustpilot.make_search(query=site)[0]["id"]
    info = trustpilot.get_site_info(trustpilot_id)
    output.append({
        "site": site,
        "review_count": info["review_count"],
        "score": info["score"]
    })

# Collect every review for each site

output = []
for site in sites:
    trustpilot_id = trustpilot.make_search(query=site)[0]["id"]
    reviews = trustpilot.get_reviews(trustpilot_id)
    for review in reviews:
        output.append({
            "site": site,
            "reviewTitle": review["title"],
            "reviewBody": review["body"],
            "reviewRating": review["rating"]
        })
```

## XLWriter
### Writes dataframes to clean excel files with advanced sheet-wise formatting options and an automatically generated contents page with navigation. Three examples of differing complexity given below.

```python
import pandas as pd
from sidt.utils.io import XLWriter

# Dataframes to write

df0 = pd.DataFrame({"Methodology": [""]})
df1 = pd.DataFrame({"Index": [0, 1, 2], "Value": ["a", "b", "c"]})
df2 = pd.DataFrame({
    "Integers": range(1, 6),
    "Big Numbers": [10000, 500000, 1000000, 5000000, 10000000],
    "Text": ["Hello", "World", "This", "Is", "Example"]
})


""" Simple examples """

# Write all three dataframes to a single file, using the same custom formatting for all sheets

XLWriter.dfs_to_xlsx(
    {"Methodology": df0, "Summary": df1, "Raw Data": df2},
    with_contents=True,
    file_path="output.xlsx",
    humanise_headers=True,
    column_widths=20
    )

# Write a single dataframe to a file, using the default formatting

XLWriter.df_to_xlsx(df0)


""" Advanced example """

# Initialise writer with a filename

writer = XLWriter("output.xlsx")

# Add dataframes to writer one at a time, with unique formatting for each sheet

writer.add_sheet(
    df0, 
    sheet_name="Methodology", 
    title="Methodology", 
    description="A sheet with a 'Methodology' header, with an empty cell to manually write a methodology into.",
    column_widths=[250],
    wrap_cells=True,
    position=0,
    enum_sheet_name=False
    )
writer.add_sheet(
    df1, 
    sheet_name="Summary", 
    title="Summary",
    column_widths=25, 
    extra_info={"Analysis by": "John Doe"}
    )
writer.add_sheet(
    df2, 
    sheet_name="Raw Data", 
    autofilter=False
    )

# Generate a contents page and write the data

writer.add_contents(stars=True)
writer.write()
```

![XLWriter Output](/resources/readme-files/xlwriter_output_contents.png)
![XLWriter Output](/resources/readme-files/xlwriter_output_raw_data.png)