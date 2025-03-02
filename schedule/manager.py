# Импортируем функцию parse_schedule из вашего модуля парсера Excel.
from excel_parser import parse_schedule

class ScheduleManager:
    # Допустимые коды смен.
    # Р – например, рабочий день (рабочий), В – выходной, К – конкурс, О – отпуск, Д – дежурство.
    # Здесь "Д" означает именно дежурство.
    ALLOWED_CODES = {"Р", "В", "К", "О", "Д"}

    def __init__(self, file_path: str):
        """
        Конструктор класса ScheduleManager.
        
        При инициализации происходит вызов функции parse_schedule для загрузки расписания
        из Excel-файла. Если данные успешно загружены, они сохраняются в атрибутах:
          - self.employees: список сотрудников (ФИО);
          - self.schedules: список записей расписания, где каждая запись имеет вид:
            {"day": <число>, "shifts": {<сотрудник>: <код смены>, ...}}.
        
        :param file_path: строка с путем к Excel-файлу.
        """
        employees, schedules = parse_schedule(file_path)
        if not employees or not schedules:
            raise ValueError("Не удалось получить расписание из файла!")
        
        self.employees = employees
        self.schedules = schedules

    def get_full_schedule(self):
        """
        Возвращает полное расписание.
        
        :return: список всех записей расписания.
        """
        return self.schedules

    def get_day_schedule(self, day: int):
        """
        Возвращает расписание для конкретного дня.
        
        Проходим по списку записей расписания (self.schedules) и ищем запись, где ключ "day" равен переданному дню.
        
        :param day: число дня (например, 1, 2, 3, ...).
        :return: словарь соответствия сотрудник → код смены или None, если запись для данного дня не найдена.
        """
        for record in self.schedules:
            if record["day"] == day:
                return record["shifts"]
        return None

    def swap_shifts(self, day1: int, day2: int, user1: str, user2: str) -> bool:
        """
        Меняет местами дежурства двух сотрудников, которые дежурят на разных днях.
        
        Например, если сотрудник user1 дежурит на day1, а сотрудник user2 дежурит на day2,
        то после вызова этого метода:
          - user1 получит смену, которая была назначена на day2,
          - user2 получит смену, которая была назначена на day1.
        
        Алгоритм:
          1. Получаем расписание для day1 и day2 с помощью метода get_day_schedule.
          2. Если для любого из дней нет расписания или в нем отсутствует соответствующий сотрудник, возвращаем False.
          3. Меняем местами значения (коды смен) для user1 в day1 и для user2 в day2.
        
        :param day1: День, на котором исходно дежурит user1.
        :param day2: День, на котором исходно дежурит user2.
        :param user1: Имя первого сотрудника.
        :param user2: Имя второго сотрудника.
        :return: True, если обмен выполнен успешно, иначе False.
        """
        # Получаем расписание для первого и второго дня.
        day1_schedule = self.get_day_schedule(day1)
        day2_schedule = self.get_day_schedule(day2)
        
        # Если расписание хотя бы для одного из дней не найдено, обмен невозможен.
        if day1_schedule is None or day2_schedule is None:
            return False
        
        # Проверяем, что в расписаниях присутствуют указанные сотрудники.
        if user1 not in day1_schedule or user2 not in day2_schedule:
            return False
        
        # Меняем местами коды смен:
        day1_schedule[user1], day2_schedule[user2] = day2_schedule[user2], day1_schedule[user1]
        return True

    def change_status(self, day: int, user: str, new_status: str) -> bool:
        """
        Позволяет сотруднику изменить статус своей смены на выбранный.
        
        Допустимые коды смен: "Р", "В", "К", "О", "Д" (где "Д" означает дежурство).
        Если новый статус не входит в этот набор, операция не выполняется.
        
        Алгоритм:
          1. Проверяем, что new_status является одним из допустимых кодов.
          2. Получаем расписание для указанного дня.
          3. Если расписание или сотрудник не найдены, возвращаем False.
          4. Обновляем статус смены для указанного сотрудника на new_status и возвращаем True.
        
        :param day: Число дня, для которого производится изменение статуса.
        :param user: Имя сотрудника, чей статус изменяется.
        :param new_status: Новый код смены (например, "Р", "В", "К", "О" или "Д").
        :return: True, если изменение выполнено успешно, иначе False.
        """
        # Проверяем, что новый статус входит в набор допустимых кодов.
        if new_status not in self.ALLOWED_CODES:
            return False
        
        # Получаем расписание для указанного дня.
        day_schedule = self.get_day_schedule(day)
        if day_schedule is None:
            return False
        
        # Проверяем, что указанный сотрудник присутствует в расписании этого дня.
        if user not in day_schedule:
            return False
        
        # Обновляем статус смены для сотрудника.
        day_schedule[user] = new_status
        return True
