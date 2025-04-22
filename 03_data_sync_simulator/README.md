# 🔄 Ledger Balance Sync Simulator

This module simulates a real-world data integration scenario where tenant financial data from a Property Management System (PMS) is validated, transformed, and synced to a mock version of a renter API — specifically targeting the `/renter/ledger/update` endpoint.

---

## 📦 What This Does

- Reads a CSV of tenant ledger balances from a PMS export
- Cleans and sanitizes messy or incomplete data (e.g. invalid dates, negative balances, missing IDs)
- Transforms data into API-ready JSON payloads
- Sends records to a mock REST endpoint
- Logs activity to the console
- Generates a detailed CSV sync report with statuses and errors
- Tracks key sync analytics (success/fail/skip/issue breakdown)

---

## 🚀 This project demonstrates:
- API fluency (POST requests, error handling)
- Data wrangling (type coercion, validation)
- Real-world logic (field cleaning, idempotency prep)
- CLI-style feedback and diagnostics

---

## 📁 Files

| File | Description |
|------|-------------|
| `ledger_input.csv` | Raw tenant ledger data (can be dirty or malformed) |
| `sync_ledger.py` | Main script for validating, transforming, and syncing |
| `sync_report.csv` | Output report of all records and their sync results |
| `README.md` | This file — setup, documentation, and concepts |

---

## 🧪 Sample CSV Input

```csv
renter_id,property_id,balance_due,last_payment_date
10001,U101,1130.5,2023-09-27
10002,U102,invalid,2023-12-19
10003,U103,1440.36,not-a-date
