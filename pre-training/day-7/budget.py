import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


class BudgetDB:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                        amount REAL NOT NULL CHECK(amount > 0),
                        category TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )
                    """
                )
        except sqlite3.Error as e:
            raise RuntimeError(f"Database init failed: {e}") from e

    def add_transaction(self, tx_type, amount, category):
        now = datetime.now().isoformat(timespec="seconds")
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO transactions(type, amount, category, created_at) VALUES (?, ?, ?, ?)",
                    (tx_type, amount, category, now),
                )
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to add transaction: {e}") from e

    def totals(self):
        try:
            with self._connect() as conn:
                income = conn.execute(
                    "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'income'"
                ).fetchone()[0]
                expense = conn.execute(
                    "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'expense'"
                ).fetchone()[0]
                top_categories = conn.execute(
                    """
                    SELECT category, SUM(amount) AS total
                    FROM transactions
                    WHERE type = 'expense'
                    GROUP BY category
                    ORDER BY total DESC
                    LIMIT 3
                    """
                ).fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to read summary: {e}") from e
        return income, expense, top_categories

    def monthly_report(self, month):
        try:
            with self._connect() as conn:
                rows = conn.execute(
                    """
                    SELECT id, type, amount, category, created_at
                    FROM transactions
                    WHERE CAST(strftime('%m', created_at) AS INTEGER) = ?
                    ORDER BY created_at ASC
                    """,
                    (month,),
                ).fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"Failed to read report: {e}") from e
        return rows


def build_parser():
    parser = argparse.ArgumentParser(prog="budget.py", description="Track income and expenses in SQLite.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a transaction")
    add_parser.add_argument("type", choices=["income", "expense"])
    add_parser.add_argument("amount", type=float)
    add_parser.add_argument("category")

    subparsers.add_parser("summary", help="Show overall summary")

    report_parser = subparsers.add_parser("report", help="Show monthly report")
    report_parser.add_argument("--month", type=int, required=True)

    return parser


def print_summary(db):
    income, expense, top_categories = db.totals()
    balance = income - expense
    print(f"Total in: {income:.2f}")
    print(f"Total out: {expense:.2f}")
    print(f"Balance: {balance:.2f}")
    print("Top 3 spending categories:")
    if not top_categories:
        print("- No expense data")
        return
    for category, total in top_categories:
        print(f"- {category}: {total:.2f}")


def print_report(rows, month):
    print(f"Report for month {month}")
    if not rows:
        print("No transactions found.")
        return
    print("id | type    | amount   | category | created_at")
    total_in = 0.0
    total_out = 0.0
    for tx_id, tx_type, amount, category, created_at in rows:
        print(f"{tx_id:>2} | {tx_type:<7} | {amount:>8.2f} | {category:<8} | {created_at}")
        if tx_type == "income":
            total_in += amount
        else:
            total_out += amount
    print(f"Month total in: {total_in:.2f}")
    print(f"Month total out: {total_out:.2f}")
    print(f"Month balance: {total_in - total_out:.2f}")


def main():
    parser = build_parser()
    args = parser.parse_args()
    db = BudgetDB(Path(__file__).with_name("budget.db"))

    try:
        if args.command == "add":
            if args.amount <= 0:
                print("Error: amount must be greater than 0.", file=sys.stderr)
                return 1
            db.add_transaction(args.type, args.amount, args.category)
            print(f"Added {args.type}: {args.amount:.2f} ({args.category})")
            return 0

        if args.command == "summary":
            print_summary(db)
            return 0

        if args.command == "report":
            if args.month < 1 or args.month > 12:
                print("Error: --month must be between 1 and 12.", file=sys.stderr)
                return 1
            rows = db.monthly_report(args.month)
            print_report(rows, args.month)
            return 0
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())

