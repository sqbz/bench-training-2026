# Day 7

## What it does

`budget.py` is a CLI budget tracker that stores income and expense transactions in SQLite using Python's built-in `sqlite3`.

Commands:
- `add income <amount> <category>`
- `add expense <amount> <category>`
- `summary`
- `report --month <1-12>`

Data persists between runs in `pre-training/day-7/budget.db`.

## How to run

```bash
python3 pre-training/day-7/budget.py add income 5000 Salary
python3 pre-training/day-7/budget.py add expense 200 Food
python3 pre-training/day-7/budget.py summary
python3 pre-training/day-7/budget.py report --month 3
```

## Example output (actual)

```text
Added income: 5000.00 (Salary)
Added expense: 200.00 (Food)
Added expense: 350.00 (Transport)
Added expense: 120.00 (Food)
Total in: 5000.00
Total out: 670.00
Balance: 4330.00
Top 3 spending categories:
- Transport: 350.00
- Food: 320.00
Report for month 3
id | type    | amount   | category | created_at
 1 | income  |  5000.00 | Salary   | 2026-03-24T18:21:47
 2 | expense |   200.00 | Food     | 2026-03-24T18:21:47
 3 | expense |   350.00 | Transport | 2026-03-24T18:21:47
 4 | expense |   120.00 | Food     | 2026-03-24T18:21:47
Month total in: 5000.00
Month total out: 670.00
Month balance: 4330.00
```

