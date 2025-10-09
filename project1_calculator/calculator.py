def show_menu():
    print("\n===== Калькулятор =====")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")
    print("5. Возведение в степень")
    print("6. Остаток от деления")
    print("7. Целочисленное деление")
    print("8. Показать историю")
    print("9. Очистить историю")
    print("0. Выход")


def get_numbers():
    """Запрашивает у пользователя два числа"""
    while True:
        try:
            a = float(input("Введите первое число: "))
            b = float(input("Введите второе число: "))
            return a, b
        except ValueError:
            print("Ошибка: нужно ввести числа!")


def main():
    history = []

    while True:
        show_menu()
        choice = input("Выберите пункт меню: ")

        if choice == "1":
            a, b = get_numbers()
            result = a + b
            record = f"{a} + {b} = {result}"
            print(record)
            history.append(record)

        elif choice == "2":
            a, b = get_numbers()
            result = a - b
            record = f"{a} - {b} = {result}"
            print(record)
            history.append(record)

        elif choice == "3":
            a, b = get_numbers()
            result = a * b
            record = f"{a} * {b} = {result}"
            print(record)
            history.append(record)

        elif choice == "4":
            a, b = get_numbers()
            try:
                result = a / b
                record = f"{a} / {b} = {result}"
            except ZeroDivisionError:
                record = f"Ошибка: деление {a} / {b} на ноль!"
            print(record)
            history.append(record)

        elif choice == "5":
            a, b = get_numbers()
            result = a ** b
            record = f"{a} ^ {b} = {result}"
            print(record)
            history.append(record)

        elif choice == "6":
            a, b = get_numbers()
            try:
                result = a % b
                record = f"{a} % {b} = {result}"
            except ZeroDivisionError:
                record = f"Ошибка: остаток от деления {a} % {b} на ноль!"
            print(record)
            history.append(record)

        elif choice == "7":
            a, b = get_numbers()
            try:
                result = a // b
                record = f"{a} // {b} = {result}"
            except ZeroDivisionError:
                record = f"Ошибка: целочисленное деление {a} // {b} на ноль!"
            print(record)
            history.append(record)

        elif choice == "8":
            if history:
                print("\nИстория вычислений:")
                for h in history:
                    print(h)
            else:
                print("История пуста.")

        elif choice == "9":
            history.clear()
            print("История очищена.")

        elif choice == "0":
            print("Выход из программы...")
            break

        else:
            print("Ошибка: нет такого пункта меню!")


if __name__ == "__main__":
    main()