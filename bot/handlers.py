import telebot
from telebot import types
import calendar
from datetime import datetime
import time


from schedule import ScheduleManager
from config import schedule_manager, path_to_file
from excel_parser import parse_schedule_from_directory



def register_handlers(bot):
    @bot.message_handler(commands=['schedule'])
    def handle_schedule(message):

        # Пытаемся загрузить расписание из каталога, где лежат Excel-файлы
        employees, schedules = parse_schedule_from_directory(path_to_file)
        if employees is None or schedules is None:
            print('none')
            bot.send_message(message.chat.id, "Расписание для текущего месяца не найдено. Добавьте файл в папку excel_parser/data/M.")
            return  # Прерываем обработку, если файл не найден
        
        now = datetime.now()
        year = now.year
        month = now.month

        markup = types.InlineKeyboardMarkup()

        # Первая строка: заголовок с днями недели
        days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        header_buttons = [
            types.InlineKeyboardButton(text=day, callback_data="ignore")
            for day in days_of_week
        ]
        markup.row(*header_buttons)

        # Получаем календарь месяца: список недель, где 0 означает отсутствие дня
        weeks = calendar.monthcalendar(year, month)
        for week in weeks:
            row_buttons = []
            for day in week:
                if day == 0:
                    # Пустая кнопка для выравнивания
                    row_buttons.append(types.InlineKeyboardButton(text=" ", callback_data="ignore"))
                else:
                    row_buttons.append(types.InlineKeyboardButton(text=str(day), callback_data=f"day_{day}"))
            markup.row(*row_buttons)

        bot.send_message(message.chat.id, "Choose date:", reply_markup=markup)


    @bot.callback_query_handler(func=lambda call: call.data.startswith("day_"))
    def handle_day_callback(call):

        day_str = call.data.split("_")[1]
        try:
            day = int(day_str)
        except ValueError:
            bot.answer_callback_query(call.id, text="Неверное значение дня.")
            return

        schedule = schedule_manager.get_day_schedule(int(day))
        if not schedule:
            bot.answer_callback_query(call.id, text="Расписание на этот день не найдено.")
            return

        employees = []

        for employee, shift in schedule.items():
            if shift == "Д":
                employees.append(employee)
        

        # Предполагаем, что расписание для текущего месяца,
        # получаем текущий год и месяц
        now = datetime.now()
        year = now.year
        month = now.month
        try:
            chosen_date = datetime(year, month, day)
        except ValueError:
            bot.answer_callback_query(call.id, text="Неверная дата.")
            return

        # В Python weekday() возвращает 0 для понедельника, 6 для воскресенья
        weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        weekday_abbr = weekdays[chosen_date.weekday()]

        result = f"({day},{weekday_abbr}) деж:\n" + "\n".join(employees)

        bot.send_message(call.message.chat.id, result)

        time.sleep(1)

        bot.delete_message(call.message.chat.id, call.message.message_id)



