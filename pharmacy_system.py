"""Pharmacy management system module for handling stock, prescriptions, and patients."""

from datetime import datetime
import json
import sqlite3

# Global state
CONN = sqlite3.connect(":memory:")
STOCK = {}
PRESCRIPTIONS = []


def setup_database():
    """Set up the in-memory SQLite database with initial patient data."""
    cur = CONN.cursor()
    cur.execute("CREATE TABLE patients (id TEXT, name TEXT, allergy TEXT)")
    cur.execute("INSERT INTO patients VALUES ('P1', 'Kavya', 'penicillin')")
    cur.execute("INSERT INTO patients VALUES ('P2', 'Arjun', 'none')")
    cur.execute("INSERT INTO patients VALUES ('P3', 'Meena', 'ibuprofen')")
    CONN.commit()


def find_patient(name):
    """Find patient details by name using parameterized queries to prevent SQL injection."""
    cur = CONN.cursor()
    query = "SELECT id, allergy FROM patients WHERE name = ?"
    return cur.execute(query, (name,)).fetchall()


def add_stock(drug, units, expiry, batch_log=None):
    """Add stock units for a specific drug and log the batch."""
    if batch_log is None:
        batch_log = []
    STOCK[drug] = {
        "units": STOCK.get(drug, {}).get("units", 0) + units,
        "expiry": expiry,
    }
    batch_log.append((drug, units))
    return len(batch_log)


def dispense(patient_name, drug, units):
    """Dispense a drug to a patient if no allergy and sufficient stock exists."""
    try:
        patients = find_patient(patient_name)
        if not patients:
            return False
        patient = patients[0]
        if drug.lower() in patient[1].lower():
            print("Allergy warning for", patient_name)
            return False
        if drug not in STOCK or STOCK[drug]["units"] < units:
            return False
        STOCK[drug]["units"] -= units
        PRESCRIPTIONS.append(
            {
                "patient": patient[0],
                "drug": drug,
                "units": units,
                "time": str(datetime.now()),
            }
        )
        return True
    except (IndexError, KeyError, sqlite3.Error):
        return False


def expiring_soon(days=30):
    """Return a list of drugs expiring within the specified number of days."""
    soon = []
    for d, data in STOCK.items():
        exp = datetime.strptime(data["expiry"], "%Y-%m-%d")
        if (exp - datetime.now()).days < days:
            soon.append(d)
    return soon


def export_prescriptions(file_name="prescriptions.json"):
    """Export prescriptions list to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(json.dumps(PRESCRIPTIONS))


def load_stock(file_name="stock.json"):
    """Load stock data from a JSON file if it exists."""
    global STOCK
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            STOCK = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass


def print_stock():
    """Print the current pharmacy stock."""
    print("Pharmacy Stock")
    for d, data in STOCK.items():
        print(d, "->", data["units"], "units, expires", data["expiry"])


def main():
    """Main execution function for the pharmacy system."""
    setup_database()
    load_stock()
    add_stock("Paracetamol", 100, "2027-03-01")
    add_stock("Amoxicillin", 20, "2025-12-31")
    add_stock("Penicillin", 50, "2027-01-15")
    add_stock("Ibuprofen", 15, "2026-11-30")
    print("Arjun gets Amoxicillin:", dispense("Arjun", "Amoxicillin", 10))
    print("Kavya gets Penicillin:", dispense("Kavya", "Penicillin", 10))
    print("Meena gets ibuprofen:", dispense("Meena", "ibuprofen", 2))
    print("Unknown patient:", dispense("Ghost", "Paracetamol", 5))
    name = input("Patient name to look up (Enter for Arjun): ") or "Arjun"
    print("Lookup result:", find_patient(name))
    print("Expiring within 30 days:", expiring_soon())
    export_prescriptions()
    print_stock()


if __name__ == "__main__":
    main()
