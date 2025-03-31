# 📺 TVMaze Episodes ETL Pipeline

This repository contains a data engineering pipeline built to extract, transform, analyze, and load (ETL) TV show and episode data from the [TVMaze](https://www.tvmaze.com/api) API Rest.

---

## 🧱 **Data Model**

The data is structured using a **Star Schema** design, composed of the following tables:

- **Fact Table**: 
  - `fact_episodes` (episode-level data)

- **Dimension Tables**:
  - `dim_shows` (show-level details)
  - `dim_genres` (genres associated with shows)

- **Bridge Table** (for many-to-many relationship):
  - `show_genres` (mapping between shows and genres)

![SQLite Data Model](model/tvmaze%20SQLite%20Data%20Model.png)

---

## ⚙️ **Technologies and Libraries**

- **Python** (3.9 or higher)
- **Flask** (used minimally for API structure)
- **Pandas** (data manipulation)
- **Requests** (API calls)
- **YData-Profiling** (Data profiling and analysis)
- **PyArrow** (Parquet file handling)
- **SQLite3** (Relational database storage)

---

## 📂 **Repository Structure**

tvmaze-episodes-etl-pipeline/ │ ├── 📂 data/ # Parquet files storage ├── 📂 db/ # SQLite database ├── 📂 json/ # Raw JSON files from API ├── 📂 model/ # Data model diagram ├── 📂 profiling/ # Profiling reports and analyses ├── 📂 src/ # Python scripts │ ├── extract.py │ ├── main.py │ ├── process.py │ ├── queries.py │ └── utils.py │ ├── .gitignore ├── requirements.txt └── README.md

---

## 🧪 **Execution Instructions**

### 1. Clone the repository

```bash
git clone https://github.com/manuel-alejandro429/lulo-bank-data-engineer-tech-test.git
cd lulo-bank-data-engineer-tech-test
```

### 2. Create and activate your virtual environment
```bash
python -m venv env
# For Windows:
env\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Execute the ETL pipeline
```bash
python src/main.py
```
This script will extract data from the API, transform, profile, and save data into Parquet files and a SQLite database (tvmaze.db)

---

## 🔎 **Data Quality Analysis**

A detailed analysis and conclusions regarding data quality, profiling insights, and necessary actions are available in:

- [`profiling/profiling_analysis.md`](profiling/profiling_analysis.md)

Additional profiling reports (HTML files) are provided under the `profiling/` directory.


## 📊 **Aggregations and Analysis**

After execution, the pipeline performs SQL queries to obtain requested calculated metrics:

- **Average Runtime per Show**
- **Count of TV Shows per Genre**
- **Unique Official Website Domains**

SQL queries are defined in [`queries.py`](src/queries.py).

---

## 📁 **Generated Files**

The pipeline generates:

- **JSON**: Raw API data stored under `/json`
- **Parquet**: Structured files stored in `/data`
- **SQLite DB**: Relational database (`tvmaze.db`) stored in `/db`
- **Profiling**: HTML reports and markdown analysis stored under `/profiling`

---

## 🚧 **Future Enhancements**

- Add unit tests for core functions
- Upload this pipeline to a cloud base platform: GCP, AWS
- Generate reporting with tools like: power BI, Tableau, Looker Studio


---

## 📞 **Author**

- **Data Engineer : Manuel Alejandro Orejuela Garcés**
- [LinkedIn](https://www.linkedin.com/in/manuel-alejandro-orejuela-garc%C3%A9s-05bb2817a/)  

---

✨ **Good luck and happy coding!**


