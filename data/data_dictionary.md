# Data Dictionary

Table: `yields` (source: Statistics Canada Table 32-10-0359-01)

| Column | Description |
|---|---|
| year | Crop year, 2000 to 2026 (2026 is preliminary) |
| province | Canadian province (series with at least 15 years of data) |
| crop | Barley, Canola, or Wheat (all wheat) |
| yield_kg_ha | Average yield in kilograms per hectare |

## Derived measures (used in the analysis notebook)

| Measure | Definition |
|---|---|
| Average yield across provinces | Simple mean of `yield_kg_ha` across provinces for each crop and year (not weighted by acreage or production) |
| Period change (%) | (Mean of 2021-2025 minus mean of 2000-2004) divided by mean of 2000-2004, times 100 |
| Year-over-year change (%) | Percent change in the all-province average yield from the previous year |
| Prairie provinces | Alberta, Saskatchewan, and Manitoba |

## SQL outputs
The five queries in `sql/queries.sql` return: average yield by crop and province, year-over-year change, top 3 provinces per crop, best and worst year per crop, and a 5-year moving average.