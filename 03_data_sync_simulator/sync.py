import csv
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

MOCK_SERVER = os.getenv("MOCK_SERVER")
INPUT_CSV = "sample_input.csv"
REPORT_CSV = "sync_report.csv"

MOCK_API_URL = MOCK_SERVER + "/renter/ledger/update"

def clean_row(row):
    cleaned = {
        "renter_id": row.get("renter_id", "").strip(),
        "property_id": row.get("property_id", "").strip(),
        "balance_due": None,
        "last_payment_date": None
    }

    # Validate and sanitize balance
    try:
        balance = float(row["balance_due"])
        cleaned["balance_due"] = round(max(balance, 0), 2)  # ensure non-negative, rounded
    except ValueError:
        return cleaned, "Invalid balance"

    # Sanitize date
    try:
        datetime.strptime(row["last_payment_date"], "%Y-%m-%d")
        cleaned["last_payment_date"] = row["last_payment_date"]
    except ValueError:
        cleaned["last_payment_date"] = None  # Set to None if invalid

    if not cleaned["renter_id"] or not cleaned["property_id"]:
        return cleaned, "Missing renter_id or property_id"

    return cleaned, "OK"

def sync_ledger(payload):
    try:
        response = requests.post(MOCK_API_URL, json=payload)
        return response.status_code == 200, response.status_code
    except Exception as e:
        print(f"❌ Failed to sync {payload['renter_id']}: {e}")
        return False, "Exception"

def write_report(report_data):
    with open(REPORT_CSV, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["renter_id", "property_id", "balance_due", "last_payment_date", "status", "message"])
        writer.writeheader()
        writer.writerows(report_data)

def main():
    print("🚀 Starting ledger sync with reporting...\n")
    report_data = []
    stats = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "issues": {}
    }

    with open(INPUT_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stats["total"] += 1
            cleaned, message = clean_row(row)
            status = "SKIPPED"

            if message == "OK":
                success, resp_code = sync_ledger(cleaned)
                status = "SUCCESS" if success else "FAILED"
                message = f"HTTP {resp_code}"
                if success:
                    print(f"✅ Synced: {cleaned['renter_id']} - {message}")
                    stats["success"] += 1
                else:
                    stats["failed"] += 1
            else:
                print(f"⚠️ Skipped: {cleaned['renter_id']} - {message}")
                stats["skipped"] += 1
                stats["issues"][message] = stats["issues"].get(message, 0) + 1

            report_data.append({
                "renter_id": cleaned.get("renter_id"),
                "property_id": cleaned.get("property_id"),
                "balance_due": cleaned.get("balance_due"),
                "last_payment_date": cleaned.get("last_payment_date"),
                "status": status,
                "message": message
            })

    write_report(report_data)

    # 🎉 Print Summary
    print("\n📊 Sync Summary")
    print("-" * 30)
    print(f"Total records processed : {stats['total']}")
    print(f"✅ Successful syncs      : {stats['success']}")
    print(f"❌ Failed syncs          : {stats['failed']}")
    print(f"🚫 Skipped due to errors : {stats['skipped']}")

    if stats["issues"]:
        print("\n🧹 Common Issues:")
        for issue, count in stats["issues"].items():
            print(f" - {issue}: {count}")

    print(f"\n📄 Sync report saved to: {REPORT_CSV}")

    print("🚀 Starting ledger sync...")
    report_data = []

if __name__ == "__main__":
    main()
# This script reads a CSV file, cleans the data, syncs it with a mock API, and generates a report.