# Data Dictionary

## Source
Statistics Canada, Table 32-10-0359-01: Estimated areas, yield, production,
average farm price and total farm value of principal field crops, in metric
and imperial units (annual). Downloaded October 30, 2026.

## Clean dataset
File: `data/clean/crop_yield_clean.csv`
Database table: `yields` in `data/crop.db`
Rows: 648 (one row per crop, province, and year)

| Column | Type | Description | Example |
|---|---|---|---|
| year | integer | Crop year, 2000 to 2026. 2026 is preliminary. | 2019 |
| province | text | Canadian province (series with at least 15 years of data). Nine provinces for barley and wheat, six for canola. | Alberta |
| crop | text | Barley, Canola, or Wheat (all wheat). | Barley |
| yield_kg_ha | float | Average yield in kilograms per hectare. | 3000.0 |

## Mapping from the raw file

| Raw column | Clean column | Notes |
|---|---|---|
| REF_DATE | year | Converted to integer |
| GEO | province | Canada and regional totals removed |
| Type of crop | crop | "Canola (rapeseed)" renamed Canola; "Wheat, all" renamed Wheat |
| VALUE | yield_kg_ha | Only the "Kilograms per hectare" unit kept |

## Cleaning rules
- Kept only rows with unit "Kilograms per hectare" (the raw file repeats each yield in bushels per acre).
- Kept three crops: Barley, Canola (rapeseed), and Wheat (all wheat). Wheat sub-types were excluded to avoid double counting.
- Kept ten provinces only. Removed Canada, Maritime provinces, East, Prairie provinces, and West.
- Dropped rows with no reported yield (flagged `..`, `F`, or `x` by Statistics Canada).
- Dropped zero yields, which do not represent real harvests.
- Excluded crop-province series with fewer than 15 years of data.

## Derived measures (used in the analysis notebook)

| Measure | Definition |
|---|---|
| Average yield across provinces | Simple mean of `yield_kg_ha` across provinces for each crop and year (not weighted by acreage or production) |
| Period change (%) | (Mean of 2021-2025 minus mean of 2000-2004) divided by mean of 2000-2004, times 100 |
| Year-over-year change (%) | Percent change in the all-province average yield from the previous year |
| Prairie provinces | Alberta, Saskatchewan, and Manitoba |

## SQL outputs
The five queries in `sql/queries.sql` return: average yield by crop and province, year-over-year change, top 3 provinces per crop, best and worst year per crop, and a 5-year moving average.

## Notes
- 2026 values are preliminary and may be revised.
- Averages in the analysis are simple means across provinces, not weighted by acreage or production.
- Yield per hectare is not total production.