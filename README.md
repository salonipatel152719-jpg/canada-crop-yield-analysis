@"
# Canadian Crop Yield Analysis Dashboard

## Question
How have wheat, canola, and barley yields changed over time across
Canadian provinces, and which provinces perform best?

## Tools
Python (pandas, matplotlib, seaborn), SQL (SQLite), Streamlit

## Status
In progress
"@ | Set-Content -Encoding utf8 README.md

   ## Data source
   Statistics Canada, Table 32-10-0359-01 (downloaded October 30, 2026)

   - Yield is measured in kilograms per hectare.
- 2026 values are preliminary Statistics Canada estimates and may be revised.
- Rows with no reported yield and zero-yield rows were removed.
- Crop-province series with fewer than 15 years of data were excluded so averages are comparable.
- Rankings are based on yield per hectare, not total production.