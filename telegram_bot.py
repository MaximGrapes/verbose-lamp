from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import SendMessageRequest
from telethon.sync import TelegramClient
import time
import random
import os

# Значения API ID и API Hash
api_id = 6694331369
api_hash = 'AAH1luDCZFgvSsU7Np57NZMYgN224Tf87yc'

# Имя сессии для сохранения данных
session_name = 'session_name'

# Файл с аккаунтами
account_file = 'accounts.txt'

# Файл с прокси
proxy_file = 'proxies.txt'

# Ссылка на пост для рассылки
post_link = "https://dzen.ru/id/6584961ff79ef86dc1166e9b"

# Список чатов для рассылки
chat_list = ["@chat1", "@chat2", "@chat3"]

# Задержка между действиями
delay = 10

# Количество чатов для вступления за одну сессию
join_limit = 5

# Чтение аккаунтов из файла
with open(account_file, "r") as f:
    accounts = f.readlines()

# Чтение прокси из файла (обработка ошибки)
try:
    with open(proxy_file, "r") as f:
        proxies = f.readlines()
except FileNotFoundError:
    print("Файл с прокси не найден.")
    exit()

# Функция для входа в аккаунт
def login(account):
    # Разделение строки аккаунта на API ID, API Hash и сессию
    api_id, api_hash, session = account.split("+")
    
    # Подключение к клиенту
    client = TelegramClient(session_name, api_id, api_hash)
    
    # Возвращаем клиента
    return client

# Функция для вступления в чаты
def join_chats(client, chat_list, delay, join_limit):
    # Счетчик вступлений
    join_count = 0
    
    # Цикл по чатам
    for chat in chat_list:
        # Вступление в чат
        try:
            client(InviteToChannelRequest(channel=chat, users=[client.get_me().id]))
            time.sleep(delay)
            print(f"{client.get_me().first_name} вступил в {chat}")
            join_count += 1
        except Exception as e:
            # Если не удалось вступить в чат, то выводим ошибку и пропускаем чат
            print(f"Ошибка при вступлении в {chat}: {e}")
            continue
        
        # Если достигли лимита вступлений, то выходим из цикла
        if join_count >= join_limit:
            break

# Функция для рассылки сообщений
def send_messages(client, chat_list, message, delay):
    # Цикл по чатам
    for chat in chat_list:
        # Отправка сообщения
        try:
            client(SendMessageRequest(peer=chat, message=message))
            time.sleep(delay)
            print(f"{client.get_me().first_name} отправил сообщение в {chat}")
        except Exception as e:
            # Если не удалось отправить сообщение, то выводим ошибку и пропускаем чат
            print(f"Ошибка при отправке сообщения в {chat}: {e}")
            continue

# Запуск бота
while True:
    # Выбор режима работы
    choice = input("Введите 1 для запуска режима вступления в чаты, 2 для запуска режима рассылки сообщений: ")
    
   # Запуск режима вступления в чаты
if choice == "1":
    # Цикл по аккаунтам
    for account in accounts:
        # Вход в аккаунт
        client = login(account)

        # Получение списка прокси
        proxy = random.choice(proxies)

        # Подключение к прокси
        client.connect_proxy(proxy)

        # Вступление в чаты
        join_chats(client, chat_list, delay, join_limit)

# Запуск режима рассылки сообщений
elif choice == "2":
    # Цикл по аккаунтам
    for account in accounts:
        # Вход в аккаунт
        client = login(account)

        # Получение списка прокси
        proxy = random.choice(proxies)

        # Подключение к прокси
        client.connect_proxy(proxy)

        # Рассылка сообщений
        send_messages(client, chat_list, post_link, delay)

# Неверный выбор
else:
    print("Неверный выбор")