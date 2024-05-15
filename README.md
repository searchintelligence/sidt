# SI Data Tools

[![Build](https://github.com/searchintelligence/sidt/actions/workflows/build.yml/badge.svg)](https://github.com/searchintelligence/sidt/actions/workflows/build.yml)
[![Test interfaces/trustpilot](https://github.com/searchintelligence/sidt/actions/workflows/test-trustpilot.yml/badge.svg)](https://github.com/searchintelligence/sidt/actions/workflows/test-trustpilot.yml)

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

### Tripadvisor [![Test interfaces/trustpilot](https://github.com/searchintelligence/sidt/actions/workflows/test-trustpilot.yml/badge.svg)](https://github.com/searchintelligence/sidt/actions/workflows/test-trustpilot.yml)

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