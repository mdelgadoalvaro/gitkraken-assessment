# GitKraken Data Engineer Assessment

This project demonstrates a full data pipeline to ingest, process, analyze, and report on sales data from multiple months and store the final results in AWS S3.

---

## Objective

Build a pipeline that:
- Ingests and merges multiple CSV files
- Cleans and transforms raw data
- Calculates business metrics
- Generates visualizations and a PDF report
- Uploads the cleaned dataset and report to AWS S3

---

## Project structure

```
.
├── data/                   # Raw monthly CSV files
├── reports/                # Output charts & PDF report
├── sales_pipeline/         # Source code
│   ├── explore.py          # Step 0: Explore and inspect raw data
│   ├── ingest.py           # Step 1: Load & merge CSVs
│   ├── process.py          # Step 2: Clean and transform data
│   ├── analyze.py          # Step 3: Metrics, plots, report
│   ├── upload_to_s3.py     # Step 4: Upload results to S3
│   ├── main.py             # Orchestration script
│   └── utils/              # Utility functions (envs, logger, constants)
├── tests/                  # Unit tests
├── .env.example            # Sample environment variables
├── pyproject.toml          # Poetry project file
└── README.md
```

---

## How to run

1. Place all monthly CSVs in the `data/` folder.

2. Install poetry and dependencies
```bash
pip install poetry
poetry install
```

3. Copy `.env.example` to `.env` and customize:
```bash
cp .env.example .env
```

4. (Optional) Run the data exploration script to understand the raw input:
```bash
poetry run explore
```

5. Run the full pipeline:
```bash
poetry run pipeline
```

This will:
- Execute the pipeline
- Optionally upload results to AWS S3

6. Clean generated output files:
```bash
poetry run clean
```

---

## Thought process and approach

### Step 0: Data exploration
- Reviewed each CSV file for structure and nulls
- Identified repeated header rows and invalid types
- Combined datasets and summarized statistics
- Detected residual 2020 data and excluded it

### Step 1: Ingestion
- Loaded and concatenated 12 monthly sales CSVs using pandas
- Ensured column consistency and correct types

### Step 2: Cleaning and transformation
- Removed NaNs and erroneous rows
- Converted prices, quantities, and dates to proper types
- Extracted `Month`, `City`, `Sales`, and `YearMonth`
- Optimized date parsing for speed

### Step 3: Analysis and insights
- Found best-performing month, city, and product
- Used bundling analysis to explain best-seller behavior
- Generated visualizations and a detailed PDF report

### Step 4: Loading to S3
- Uploaded cleaned data and report to AWS S3 using `boto3`

### Step 5: Testing
- Unit tests added for helper functions like `get_bool_env()` and S3 upload
- Tests are located in the `tests/` directory

To run tests:
```bash
pytest
```

---

## Key metrics extracted

- Best month for sales with revenue
- Top-performing city
- Most sold product and co-purchase reasoning

---

## Trade-offs & design choices

- Dates parsed with specified format to improve efficiency
- Temporary PNGs are saved for use in PDF (FPDF requires file paths)
- S3 upload is modular and optional via environment variables
- Pipeline was optimized for readability and modularity
- Clean-up step is optional to preserve local output

---

## Code quality & practices

- Type annotations added to all core functions
- Logging used instead of print statements
- Modular functions separated by concern (ingest, process, analyze, etc.)
- Environment-driven behavior with `.env` support

---

## Environment Variables

| Variable         | Description                                     |
|------------------|-------------------------------------------------|
| `AWS_S3_BUCKET`  | Name of your S3 bucket                          |
| `AWS_UPLOAD`     | If true, upload cleaned CSV + report to S3      |       |
| `CLEAN_OUTPUT`   | If true, deletes local PNGs, PDF, and CSV files |

---

## Example Outputs

### Charts
The following charts are generated and saved in the `reports/` folder:

- `monthly_sales.png`: Total sales by month
- `city_sales.png`: Total sales by city
- `best_selling_products.png`: Quantity sold by product
- `batteries_bundling.png`: Most frequent product bundles with AAA Batteries

### PDF report

A full PDF report is generated as `reports/Sales_Report.pdf`, which includes:
- Summary of sales performance
- Visual charts embedded
- Reasoning for top-selling product

This file is uploaded to S3 if `AWS_UPLOAD=true`.

### Cleaned data

A merged and cleaned version of the raw input is saved as:
- `cleaned_sales_data_2019.csv`

This includes additional fields like:
- `Month`
- `YearMonth`
- `City`
- `Sales`

---

## Final Notes

- Data comes from simulated sales in 2019. Residual 2020 data was filtered out.
- Project is designed to be extensible (e.g., database support, dashboards)
- Built and delivered in under 4 hours, balancing clarity and functionality

## Potential improvements
- Continuous deployment: create a CD pipeline to deploy to staging/production environments
- Monitoring: create a monitor that let us know if the process fails
