import os
import json
import requests
from datetime import datetime, timedelta

# Данные о днях рождения
BIRTHDAYS = {
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

class GitHubActionsBirthdayBot:
    def __init__(self):
        # Получаем данные из переменных окружения GitHub
        self.bot_token = os.environ.get('BOT_TOKEN')
        self.chat_id = os.environ.get('CHAT_ID')  # ID вашей группы
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        if not self.bot_token:
            raise ValueError("BOT_TOKEN не найден в переменных окружения!")
        if not self.chat_id:
            raise ValueError("CHAT_ID не найден в переменных окружения!")
    
    def send_message(self, text):
        """Отправить сообщение в группу"""
        url = f"{self.api_url}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print(f"✅ Сообщение отправлено успешно")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка отправки сообщения: {e}")
            return False
    
    def get_upcoming_birthdays(self):
        """Найти дни рождения на следующую неделю"""
        target_date = datetime.now() + timedelta(days=7)
        target_date_str = target_date.strftime("%d.%m")
        
        upcoming = []
        for name, birthday in BIRTHDAYS.items():
            if birthday == target_date_str:
                upcoming.append((name, birthday))
        
        return upcoming
    
    def check_and_send_notifications(self):
        """Проверить и отправить уведомления"""
        print(f"🔍 Проверка дней рождения на {datetime.now().strftime('%Y-%m-%d')}")
        
        upcoming_birthdays = self.get_upcoming_birthdays()
        
        if not upcoming_birthdays:
            print("📅 Нет дней рождения на следующую неделю")
            return
        
        for name, date in upcoming_birthdays:
            message = f"""
🎉 <b>НАПОМИНАНИЕ!</b> 🎉

Через неделю (<b>{date}</b>) день рождения у:
👤 <b>{name}</b>

Не забудьте поздравить! 🎂🎁

#ДеньРождения #НеЗабудьПоздравить
            """
            
            success = self.send_message(message.strip())
            if success:
                print(f"✅ Отправлено напоминание для {name}")
            else:
                print(f"❌ Не удалось отправить напоминание для {name}")
    
    def send_test_message(self):
        """Отправить тестовое сообщение"""
        test_message = f"""
🤖 <b>Birthday Bot активен!</b>

📅 Дата проверки: {datetime.now().strftime('%d.%m.%Y %H:%M')}
📊 В базе: {len(BIRTHDAYS)} дней рождения
🔔 Следующая проверка: завтра в 9:00 МСК

✅ Бот работает автоматически!
        """
        
        return self.send_message(test_message.strip())

def main():
    """Основная функция"""
    try:
        bot = GitHubActionsBirthdayBot()
        
        # Проверяем аргументы командной строки
        import sys
        if len(sys.argv) > 1 and sys.argv[1] == 'test':
            # Тестовый режим
            print("🧪 Запуск в тестовом режиме")
            bot.send_test_message()
        else:
            # Обычная проверка
            bot.check_and_send_notifications()
            
    except Exception as e:
        print(f"💥 Критическая ошибка: {e}")
        # Отправляем уведомление об ошибке (если возможно)
        try:
            error_bot = GitHubActionsBirthdayBot()
            error_bot.send_message(f"❌ Ошибка в Birthday Bot: {str(e)}")
        except:
            pass

if __name__ == "__main__":
    main()
