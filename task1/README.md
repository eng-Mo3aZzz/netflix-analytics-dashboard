# Netflix Analytics Dashboard 🎬

An interactive Netflix data analytics dashboard built with **Python**, **Pandas**, **Streamlit**, and **Plotly**. Includes data cleaning, exploratory data analysis (EDA), and dynamic visualizations.

## Features

- 🔍 Filters by content type, country, rating, and release year
- 📊 KPI cards (total titles, movies, TV shows, countries)
- 📈 Interactive charts: Movies vs TV Shows, rating distribution, release year distribution, content added per year/month, top countries, top directors, top genres
- 🔥 Correlation heatmap
- 🔎 Search by title
- 📥 Download filtered dataset as CSV

## Tech Stack

- Python
- Pandas / NumPy
- Streamlit
- Plotly

## Project Structure

```
├── app.py                  # Streamlit dashboard
├── TASK1.ipynb             # Data cleaning & EDA notebook
├── netflix_titles.csv      # Raw dataset
├── netflix_cleaned.csv     # Cleaned dataset used by the dashboard
├── netflix_logo.png        # Logo used in the UI
└── requirements.txt        # Python dependencies
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data Cleaning

The `TASK1.ipynb` notebook handles:
- Filling missing values (director, cast, country, rating, duration)
- Parsing and standardizing date formats
- Extracting `year_added` and `month_added` from `date_added`
- Exporting the cleaned dataset to `netflix_cleaned.csv`

---

Developed by **MOAAZ ELDEEP**
