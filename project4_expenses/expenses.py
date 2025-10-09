import sqlite3
import csv
import os
from datetime import datetime
from typing import Optional

DB_FILENAME = "expenses.db"
VALID_CATEGORIES = ["еда", "транспорт", "развлечения", "прочее"]  # можно расширять


def get_conn(db_path: Optional[str] = None):
    if db_path:
        return sqlite3.connect(db_path)
    return sqlite3.connect(DB_FILENAME)


def init_db(db_path: Optional[str] = None):
    with get_conn(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL, -- YYYY-MM-DD
                description TEXT
            )
            """
        )
        conn.commit()


def validate_date(date_str: str) -> str:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Неверный формат даты. Ожидается ГГГГ-ММ-ДД")


def add_expense(amount: float, category: str, date_str: str, description: Optional[str] = None, db_path: Optional[str] = None):
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Неверная категория. Доступные: {', '.join(VALID_CATEGORIES)}")
    date_norm = validate_date(date_str)
    with get_conn(db_path) as conn:
        conn.execute(
            "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
            (amount, category, date_norm, description),
        )
        conn.commit()


def fetch_all(db_path: Optional[str] = None):
    with get_conn(db_path) as conn:
        return conn.execute("SELECT id, amount, category, date, description FROM expenses ORDER BY date DESC, id DESC").fetchall()


def fetch_by_date(date_str: str, db_path: Optional[str] = None):
    date_norm = validate_date(date_str)
    with get_conn(db_path) as conn:
        return conn.execute("SELECT id, amount, category, date, description FROM expenses WHERE date = ? ORDER BY id DESC", (date_norm,)).fetchall()


def fetch_by_category(category: str, db_path: Optional[str] = None):
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Неверная категория. Доступные: {', '.join(VALID_CATEGORIES)}")
    with get_conn(db_path) as conn:
        return conn.execute("SELECT id, amount, category, date, description FROM expenses WHERE category = ? ORDER BY date DESC, id DESC", (category,)).fetchall()


def export_csv(filepath: str, db_path: Optional[str] = None):
    rows = fetch_all(db_path)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "amount", "category", "date", "description"])
        for r in rows:
            writer.writerow(r)
    return len(rows)


def print_rows(rows):
    if not rows:
        print("Записей нет.")
        return
    print(f"\n{'ID':<4} {'Сумма':<10} {'Категория':<15} {'Дата':<12} Описание")
    print("-" * 70)
    for r in rows:
        id_, amount, category, date, desc = r
        print(f"{id_:<4} {amount:<10.2f} {category:<15} {date:<12} {desc or ''}")
    print()


def prompt_amount() -> float:
    while True:
        s = input("Сумма (например 12.50): ").strip()
        try:
            val = float(s)
            return val
        except ValueError:
            print("Некорректная сумма. Попробуйте ещё раз.")


def prompt_category() -> str:
    print("Категории:", ", ".join(VALID_CATEGORIES))
    while True:
        c = input("Категория: ").strip().lower()
        if c in VALID_CATEGORIES:
            return c
        else:
            print("Неверная категория. Повторите ввод.")


def prompt_date(default_today: bool = True) -> str:
    default = datetime.now().strftime("%Y-%m-%d") if default_today else ""
    while True:
        s = input(f"Дата (ГГГГ-ММ-ДД){' ['+default+']' if default else ''}: ").strip()
        if s == "" and default:
            return default
        try:
            return validate_date(s)
        except ValueError as e:
            print(e)


def main_menu():
    print("""
===== Дневник расходов =====
1. Добавить запись
2. Показать все записи
3. Показать записи по дате
4. Показать записи по категории
5. Экспорт в CSV
0. Выход
""")


def main(db_path: Optional[str] = None):
    init_db(db_path)
    while True:
        main_menu()
        choice = input("Выберите пункт: ").strip()
        try:
            if choice == "1":
                amount = prompt_amount()
                category = prompt_category()
                date_str = prompt_date()
                desc = input("Описание (необязательно): ").strip() or None
                add_expense(amount, category, date_str, desc, db_path)
                print("Запись добавлена.")

            elif choice == "2":
                rows = fetch_all(db_path)
                print_rows(rows)

            elif choice == "3":
                date_str = prompt_date(default_today=False)
                rows = fetch_by_date(date_str, db_path)
                print_rows(rows)

            elif choice == "4":
                cat = prompt_category()
                rows = fetch_by_category(cat, db_path)
                print_rows(rows)

            elif choice == "5":
                default_path = os.path.join(os.getcwd(), "expenses_export.csv")
                path = input(f"Путь для CSV (по умолчанию {default_path}): ").strip() or default_path
                count = export_csv(path, db_path)
                print(f"Экспортировано {count} записей в {path}")

            elif choice == "0":
                print("Выход.")
                break

            else:
                print("Неверный пункт меню.")
        except Exception as exc:
            print("Ошибка:", exc)


if __name__ == "__main__":
    main()
