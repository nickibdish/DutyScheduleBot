from excel_parser.parser import parse_schedule
from schedule import ScheduleManager

def main():



    schedule_manager = ScheduleManager("excel_parser/data/02...2025.xlsx")
    schedule_manager.print_schedule()



# Проверяем, что файл запущен как скрипт, а не импортирован как модуль
if __name__ == "__main__":
    main()
