import pandas as pd
import math

def parse_schedule(file_path: str):
    """
    Предположим:
    1) Ячейка со значением "1" — это начало (по вертикали).
    2) Таблица с сотрудниками (ФИО) на строку выше (target_row - 1), 
       начиная справа на 2 столбца от найденной "1".
    3) Горизонтально таблица заканчивается, когда в строке с ФИО встретим пустую ячейку.
    4) Вертикально таблица заканчивается, когда в столбце с датами встретим пустую ячейку.
    """

    # 1. Считываем лист целиком, без заголовков
    raw_df = pd.read_excel(file_path, header=None)

    # 2. Ищем координаты ячейки со значением "1"
    target_row, target_col = None, None
    for i, row in raw_df.iterrows():
        for j, val in enumerate(row):
            if val == 1 or str(val).strip() == "1":
                target_row, target_col = i, j
                break
        if target_row is not None:
            break

    if target_row is None:
        print("Не нашли ячейку со значением '1'.")
        return None, None

    # 3. Смотрим, где у нас «ФИО сотрудников»:
    #    - они на строку выше (target_row - 1)
    #    - начинаются со столбца (target_col + 2)
    #    - тянутся вправо, пока ячейки не пустые
    employees = []
    if target_row - 1 < 0:
        print("Нельзя взять строку выше — target_row - 1 < 0.")
        return None, None

    row_above = raw_df.iloc[target_row - 1]  # строка выше
    # Пробегаемся по столбцам, начиная с (target_col + 2), пока не встретим пустую ячейку
    col_index = target_col + 2
    while col_index < len(row_above):
        val = row_above[col_index]
        # Условие конца таблицы по горизонтали:
        # как только ячейка None или пустая строка — выходим из цикла
        if val is None or str(val).strip() == "":
            break
        employees.append(str(val).strip())
        col_index += 1

    if not employees:
        print("Не удалось определить сотрудников. Проверяйте структуру.")
        return None, None

    # Теперь мы знаем, что столбцы с данными идут до col_index - 1 включительно.
    # Следовательно, "интересующие" столбцы — это диапазон [target_col+2, col_index).

    schedules = []
    current_row = target_row

    # 4. Идём вниз по столбцу с датами (target_col),
    #    пока не встретим пустую/нечисловую ячейку.
    while current_row < len(raw_df):
        val_date = raw_df.iat[current_row, target_col]

        # Проверяем, что val_date — это число (int/float), не NaN
        if isinstance(val_date, (int, float)) and not math.isnan(val_date):
            day_of_month = int(val_date)  # предполагаем, что там целое (1,2,3...)
            
            # Получаем срез столбцов по количеству сотрудников
            # Диапазон [target_col+2, col_index)
            row_values = raw_df.iloc[current_row, target_col+2 : col_index]
            # Превращаем в список, чтобы по индексам мапить к employees
            row_values_list = row_values.tolist()

            # Собираем словарь вида {"Иванов": "В", "Петров": "О", ...}
            day_shifts = {}
            for idx_emp, emp_name in enumerate(employees):
                shift_val = row_values_list[idx_emp]
                day_shifts[emp_name] = shift_val
            
            schedules.append({
                "day": day_of_month,
                "shifts": day_shifts
            })

            current_row += 1

        else:
            # Как только встретили нечисловое значение (пустую ячейку),
            # считаем, что таблица по вертикали кончилась
            break

    return employees, schedules

