import re
import os
from db.session import Session
from db.models import Employee, Schedule
from excel_parser.parser import parse_schedule
from typing import Tuple

def extract_period_from_filename(filename: str) -> Tuple[int, int]:
    # реализация функции

    """
    Извлекает месяц и год из имени файла.
    
    Ожидаемый формат имени файла: "[номер месяца]...год.xlsx"
    Пример: "02...2025.xlsx" — возвращает (2, 2025)
    
    :param filename: Имя файла (например, "02...2025.xlsx")
    :return: Кортеж (month, year) в виде целых чисел.
    :raises ValueError: если имя файла не соответствует ожидаемому формату.
    """
    # Регулярное выражение:
    # - (\d{1,2}) — от 1 до 2 цифр для месяца
    # - .*?       — любой символ (нежадно)
    # - (\d{4})   — ровно 4 цифры для года
    pattern = r"(\d{1,2}).*?(\d{4})"
    match = re.search(pattern, filename)
    if match:
        try:
            month = int(match.group(1))
            year = int(match.group(2))
            return month, year
        except ValueError:
            raise ValueError("Невозможно преобразовать извлеченные значения в числа.")
    else:
        raise ValueError("Имя файла не соответствует ожидаемому формату.")

def import_excel_to_db(excel_file: str):
    """
    Импортирует данные из Excel-файла в базу данных.
    
    Файл должен иметь имя вида "[номер месяца]...год.xlsx", например "02...2025.xlsx".
    Функция автоматически извлекает месяц и год из имени файла,
    затем с помощью функции parse_schedule получает данные из Excel,
    и сохраняет их в базу данных с использованием SQLAlchemy.
    
    :param excel_file: Путь к Excel-файлу, например "excel_parser/data/02...2025.xlsx"
    """
    # Извлекаем базовое имя файла и определяем месяц и год
    base_filename = os.path.basename(excel_file)
    try:
        month, year = extract_period_from_filename(base_filename)
    except ValueError as e:
        print(f"Ошибка извлечения периода из имени файла: {e}")
        return
    print(f"Извлечено: месяц = {month}, год = {year}")
    
    # Получаем данные из Excel с помощью парсера
    employees_list, schedule_data = parse_schedule(excel_file)
    if not employees_list or not schedule_data:
        print("Ошибка: не удалось получить данные из Excel.")
        return
    
    session = Session()
    
    # Обработка списка сотрудников: для каждого сотрудника проверяем, есть ли он в базе,
    # и если нет – добавляем его.
    for emp_name in employees_list:
        employee = session.query(Employee).filter_by(name=emp_name).first()
        if not employee:
            employee = Employee(name=emp_name)
            session.add(employee)
            session.commit()  # Коммитим сразу для получения employee.id
    
    # Обработка расписания: schedule_data – список записей вида:
    # { "day": <число дня>, "shifts": { "<employee>": "<shift_code>", ... } }
    for record in schedule_data:
        day = record["day"]
        shifts = record["shifts"]
        for emp_name, shift in shifts.items():
            # Получаем сотрудника из базы (он уже должен быть добавлен)
            employee = session.query(Employee).filter_by(name=emp_name).first()
            if not employee:
                # Обычно этого не должно случаться, так как сотрудники обработаны выше
                employee = Employee(name=emp_name)
                session.add(employee)
                session.commit()
            # Создаем новую запись расписания для каждого сотрудника на соответствующий день
            new_schedule = Schedule(
                year=year,
                month=month,
                day=day,
                employee_id=employee.id,
                shift=shift
            )
            session.add(new_schedule)
    
    # Фиксируем изменения в базе данных
    session.commit()
    session.close()
    print("Импорт данных завершен успешно.")

if __name__ == "__main__":
    # Пример вызова: файл находится в "excel_parser/data" и имеет имя "02...2025.xlsx"
    import_excel_to_db("excel_parser/data/02...2025.xlsx")
