import json
import os
from datetime import datetime

FILE = "C:/Users/shika/OneDrive/Desktop/projects/expense-tracker/data.json"
# ─────────────────────────────────────────
# Data Layer
# ─────────────────────────────────────────

def load_data():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# ─────────────────────────────────────────
# Input Helpers
# ─────────────────────────────────────────

def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  ⚠ Amount must be greater than zero.")
            else:
                return value
        except ValueError:
            print("  ⚠ Invalid input. Please enter a number.")

def get_type():
    while True:
        value = input("Enter type (income/expense): ").strip().lower()
        if value in ("income", "expense"):
            return value
        print("  ⚠ Please enter 'income' or 'expense'.")

def get_category():
    while True:
        value = input("Enter category: ").strip()
        if value:
            return value.lower()
        print("  ⚠ Category cannot be empty.")

# ─────────────────────────────────────────
# Core Functions
# ─────────────────────────────────────────

def add_entry():
    print("\n--- Add Entry ---")
    type_    = get_type()
    amount   = get_float("Enter amount: ")
    category = get_category()
    date     = datetime.now().strftime("%Y-%m-%d %H:%M")

    entry = {
        "type":     type_,
        "amount":   amount,
        "category": category,
        "date":     date,
    }

    data = load_data()
    data.append(entry)
    save_data(data)

    print(f"  ✅ Entry saved — {type_} of {amount:.2f} ({category}) on {date}")

def show_all():
    data = load_data()
    print("\n--- All Transactions ---")

    if not data:
        print("  No transactions found.")
        return

    print(f"  {'#':<4} {'Date':<17} {'Type':<10} {'Category':<15} {'Amount':>10}")
    print("  " + "─" * 58)

    for i, d in enumerate(data):
        date     = d.get("date", "N/A")
        type_    = d["type"].capitalize()
        category = d["category"].capitalize()
        amount   = d["amount"]
        sign     = "+" if d["type"] == "income" else "-"
        print(f"  {i:<4} {date:<17} {type_:<10} {category:<15} {sign}{amount:>9.2f}")

    print("  " + "─" * 58)

def delete_entry():
    data = load_data()
    show_all()

    if not data:
        return

    try:
        index = int(input("\nEnter index to delete: "))
        if index < 0 or index >= len(data):
            print("  ⚠ Index out of range.")
            return
        removed = data.pop(index)
        save_data(data)
        print(f"  ❌ Deleted: {removed['type']} | {removed['amount']:.2f} | {removed['category']}")
    except ValueError:
        print("  ⚠ Please enter a valid number.")

def show_summary():
    data = load_data()
    income  = sum(d["amount"] for d in data if d["type"] == "income")
    expense = sum(d["amount"] for d in data if d["type"] == "expense")
    balance = income - expense

    print("\n--- Summary ---")
    print(f"  Total Income:   +{income:>10.2f}")
    print(f"  Total Expenses: -{expense:>10.2f}")
    print("  " + "─" * 26)

    status = "✅ Surplus" if balance >= 0 else "⚠ Deficit"
    print(f"  Balance:         {balance:>10.2f}  {status}")

def category_summary():
    data = load_data()
    summary = {}

    for d in data:
        if d["type"] == "expense":
            cat = d["category"]
            summary[cat] = summary.get(cat, 0) + d["amount"]

    print("\n--- Category Summary (Expenses) ---")

    if not summary:
        print("  No expense entries found.")
        return

    total = sum(summary.values())
    print(f"  {'Category':<20} {'Amount':>10}  {'Share':>7}")
    print("  " + "─" * 42)

    for cat, amount in sorted(summary.items(), key=lambda x: x[1], reverse=True):
        share = (amount / total) * 100
        print(f"  {cat.capitalize():<20} {amount:>10.2f}  {share:>6.1f}%")

    print("  " + "─" * 42)
    print(f"  {'Total':<20} {total:>10.2f}  100.0%")

# ─────────────────────────────────────────
# Main Menu
# ─────────────────────────────────────────

def main():
    menu = """
╔══════════════════════════════╗
║      💰 Expense Tracker      ║
╠══════════════════════════════╣
║  1. Add Entry                ║
║  2. Show All Transactions    ║
║  3. Delete Entry             ║
║  4. Show Summary             ║
║  5. Category Summary         ║
║  6. Exit                     ║
╚══════════════════════════════╝"""

    actions = {
        "1": add_entry,
        "2": show_all,
        "3": delete_entry,
        "4": show_summary,
        "5": category_summary,
    }

    while True:
        print(menu)
        choice = input("Choose an option: ").strip()

        if choice == "6":
            print("\n  Goodbye! 👋\n")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("  ⚠ Invalid choice. Please enter 1–6.")

if __name__ == "__main__":
    main()