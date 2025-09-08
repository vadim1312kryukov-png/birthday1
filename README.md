[Uploading birthday_bot.py…]()
import asyncio
import logging
from datetime import datetime, timedelta
import os
from telegram import Bot
from telegram.error import TelegramError

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# НАСТРОЙКИ БОТА - ЗАПОЛНИТЕ СВОИМИ ДАННЫМИ
BOT_TOKEN = os.environ.get('BOT_TOKEN', "8288059895:AAHwniisVwhP8fBmPTUJNTTCNOUKFC0r2Ws")
CHAT_ID = os.environ.get('CHAT_ID', "1068102645")

# База данных сотрудников
EMPLOYEES = {
    "Степанцев Егор Петрович": "16.01",
    "Гончаров Григорий Евгеньевич": "21.01",
    "Добролюбцева Светлана Александровна": "21.01",
    "Шумкин Алексей Максимович": "28.01",
    "Щеблакова Валерия Александровна": "31.01",
    "Герасимова Анна Валерьевна": "03.02",
    "Ермолов Алексей Андреевич": "07.02",
    "Гааг Виктор Викторович": "07.03",
    "Пальчикова Александра Александровна": "10.04",
    "Грабов Иван Владимирович": "12.05",
    "Медведева Екатерина Андреевна": "21.07",
    "Сергеева Ольга Сергеевна": "23.08",
    "Басалаев Владислав Александрович": "27.09",
    "Прохорова Виктория Алексеевна": "17.10",
    "Глухов Никита Геннадьевич": "05.11",
    "Павлова Екатерина Сергеевна": "23.11",
    "Крюков Вадим Владимирович": "13.12"
}

def get_upcoming_birthdays():
    """Получить список именинников через 5 дней"""
    today = datetime.now()
    target_date = today + timedelta(days=5)
    target_day_month = target_date.strftime("%d.%m")
    
    upcoming = []
    for name, birthday in EMPLOYEES.items():
        if birthday == target_day_month:
            upcoming.append(name)
    
    return upcoming

def get_birthday_message(names):
    """Сформировать сообщение о предстоящих днях рождения"""
    if len(names) == 1:
        return f"🎉 Напоминание: через 5 дней день рождения у {names[0]}!"
    else:
        names_str = ", ".join(names[:-1]) + f" и {names[-1]}"
        return f"🎉 Напоминание: через 5 дней день рождения у {names_str}!"

async def send_birthday_notification():
    """Отправить уведомление о днях рождения"""
    bot = Bot(token=BOT_TOKEN)
    
    try:
        upcoming_birthdays = get_upcoming_birthdays()
        
        if upcoming_birthdays:
            message = get_birthday_message(upcoming_birthdays)
            await bot.send_message(chat_id=CHAT_ID, text=message)
            logger.info(f"✅ Отправлено уведомление: {message}")
        else:
            logger.info("📅 Сегодня никто не празднует через 5 дней")
    
    except TelegramError as e:
        logger.error(f"❌ Ошибка Telegram: {e}")
    except Exception as e:
        logger.error(f"❌ Общая ошибка: {e}")

async def main():
    """Основная функция для облачного хостинга"""
    logger.info("🤖 Бот запущен в облаке")
    
    # Для Railway, Heroku и других платформ - запуск по расписанию
    while True:
        current_time = datetime.now()
        logger.info(f"🕐 Текущее время: {current_time.strftime('%H:%M:%S %d.%m.%Y')}")
        
        # Проверяем каждый день в 9:00 утра (московское время)
        if current_time.hour == 6:  # UTC+3 для Москвы = 9:00 MSK
            await send_birthday_notification()
            # Ждем час, чтобы не отправлять дубли
            await asyncio.sleep(3600)
        
        # Проверяем каждые 10 минут
        await asyncio.sleep(600)

# Для разовой проверки (подходит для GitHub Actions)
async def check_once():
    """Разовая проверка для планировщика задач"""
    logger.info("🔍 Разовая проверка дней рождения")
    await send_birthday_notification()

if __name__ == "__main__":
    # Проверяем, нужна ли разовая проверка или постоянная работа
    run_once = os.environ.get('RUN_ONCE', 'false').lower() == 'true'
    
    if run_once:
        print("🔍 Запуск разовой проверки...")
        asyncio.run(check_once())
    else:
        print("🤖 Запуск бота в режиме непрерывной работы...")
        print("📅 Проверка дней рождения каждый день в 9:00 МСК")
        print("⏰ Уведомления за 5 дней до дня рождения")
        
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\n🛑 Бот остановлен")
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            # В облачной среде пытаемся продолжить работу
            asyncio.run(main())
