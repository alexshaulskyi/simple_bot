import os
import time
import sys

from dotenv import load_dotenv
import requests
import telegram

load_dotenv()

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

proxy = telegram.utils.request.Request(proxy_url='https://212.115.235.12:81')
bot = telegram.Bot(token=TELEGRAM_TOKEN, request=proxy)

def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    if homework.get('status') != 'approved':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    params = {'from_date': current_timestamp}
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
    homework_statuses = requests.get(url=url, headers=headers, params=params)
    return homework_statuses.json()

def send_message(message):
    return bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    current_timestamp = int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            hw_list = new_homework.get('homeworks', [])
            if hw_list:
                send_message(parse_homework_status(hw_list[0]))
            current_timestamp = new_homework.get('current_date')
            time.sleep(300)
        
        except KeyboardInterrupt:
            print('Action was interrupted manually')
            sys.exit(0)

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)


if __name__ == '__main__':
    main()
