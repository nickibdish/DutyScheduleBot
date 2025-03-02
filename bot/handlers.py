import telebot
from telebot import types
import calendar
from datetime import datetime


from schedule import ScheduleManager
from config import schedule_manager



def register_handlers(bot):
    @bot.message_handler(commands=['schedule'])
    def handle_schedule(message):

        now = datetime.now()
        year = now.year
        month = now.month

        num_days = calendar.monthrange(year, month)[1]

        markup = types.InlineKeyboardMarkup(row_width=5)
        buttons = []

        for day in range(1, num_days + 1):
            btn = types.InlineKeyboardButton(str(day), callback_data=f"day_{day}")
            buttons.append(btn)

        markup.add(*buttons)


        bot.send_message(message.chat.id,"choise date:", reply_markup=markup)


    @bot.callback_query_handler(func=lambda call: call.data.startswith("day_"))
    def handle_day_callback(call):
        day = call.data.split("_")[1]

        schedule = schedule_manager.get_day_schedule(int(day))
        
        print(schedule)

