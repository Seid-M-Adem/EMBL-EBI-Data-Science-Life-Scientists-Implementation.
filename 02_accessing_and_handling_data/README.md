# 02 · Accessing & Handling Data

Getting public biological data out of databases with code, and turning it into clean,
analysis-ready tables and figures. Every later module depends on this.

## 🗺️ Learning Path
| Step | Folder | Session | You learn to… |
|------|--------|---------|---------------|
| 1 | [01_apis_and_data_collection](01_apis_and_data_collection/) | Intro to APIs & Python for data collection | Query MGnify and ENA REST APIs from the shell (`curl`, `jq`) and from Python (`requests`, `MGnipy`) |
| 2 | [02_handling_and_visualisation](02_handling_and_visualisation/) | Handling & visualising data in Python | Clean, reshape, anonymise and plot tabular data with pandas, NumPy and seaborn |

## 🔍 What to Look For
- **API clients that cope with failure**: pagination, rate limiting, retries and error handling.
- **Reproducible data flow**: raw responses saved to `data/raw/`, transformed outputs to `data/processed/`. Nothing is edited by hand.
- **Idiomatic pandas**: vectorised operations, tidy reshaping, joins across data sources, and explicit handling of missing values.
- **Publication-quality figures** with Matplotlib/Seaborn, each with a written interpretation.

## 📚 Course Materials
Slides and practical notebooks are in each subfolder's `course_materials/`. The three practical notebooks for
this module and the ML intro all come from one tutorial repo:
[`python-data-tutorials`](01_apis_and_data_collection/course_materials/python-data-tutorials/) (Apache-2.0).
