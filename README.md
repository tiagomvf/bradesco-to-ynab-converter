# Bradesco-to-YNAB Converter

A Python script to convert Bradesco credit card statements (CSV) into YNAB-compatible format.

## Features
- Automatically processes multiple CSV files
- Handles character encoding conversion (Latin-1 → UTF-8)
- Smart date year detection
- Filters out non-transaction rows
- Converts Brazilian currency format to YNAB-compatible amounts
- Generates output files with `_ynab_ready.csv` suffix

## Date Handling Logic
The year detection algorithm uses the current system date (January 25, 2025) as reference:
1. Parses transaction day/month from CSV
2. Creates tentative date with current date (January 25, 2025)
3. Compares tentative date to current date
4. If tentative date is in the future, uses previous year (2024)

**Examples:**
- 15/01 → 2025-01-15 (within current month)
- 05/02 → 2024-02-05 (future month in current year)
- 31/12 → 2024-12-31 (year maintained)

## Requirements
- Python 3.6+
- No external dependencies

## Usage
1. Place Bradesco CSV files in the `input-files/` directory
2. Run the converter:
```bash
python3 bradesco_to_ynab.py
```
3. Find converted files in the root directory with `_ynab_ready.csv` suffix

## Input File Requirements
- CSV files downloaded from Bradesco Internet Banking
- Must have ";" as delimiter
- Expected columns: Date, Payee, _, Amount

## Output Format
- YNAB-compatible CSV with columns:
  - Date (MM/DD/YYYY)
  - Payee
  - Category (empty)
  - Memo
  - Amount

## Troubleshooting
**Common issues:**
- Encoding errors: Ensure original files are Latin-1 encoded
- Future dates: Transactions dated after current date will use previous year
- Amount formatting: Handles values like "1.234,56" → 1234.56