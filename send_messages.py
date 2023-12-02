import asyncio
import aiofiles
import argparse
from datetime import datetime
import logging
import json
from pprint import pprint
import string
import re


def read_args():
    parser = argparse.ArgumentParser(description='Утилита для отправки сообщений в чат ')
    parser.add_argument('-loglevel', default='WARNING',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Уровень логирования (по умолчанию: WARNING)')
    parser.add_argument('-host', type=str, default='minechat.dvmn.org',
                        help='Имя хоста (default=minechat.dvmn.org)')
    parser.add_argument('-port', type=int, default=5050,
                        help='Номер порта (default=5050)')
    parser.add_argument('-reg', type=bool, default=False, choices=[False, True],
                        help='Нужна регистрация? (default=False')
    args = parser.parse_args()
    return args

logger = logging.getLogger(__name__)


async def authorise(reader, writer):
    while True:
        data = await reader.readline()
        text = f'{data.decode()!r}'
        text = text[1:-3]
        logger.info(f'sender: {text}')
        if 'Hello %username%!' in text:
            message = input('Введите Ваш персональный токен: ')
            writer.write(f'{message}\n\n'.encode())
            await writer.drain()
            break
        elif 'null' in text:
            message = input('Неизвестный токен. Проверьте его или зарегистрируйтесь заново.')
            writer.write(f'{message}\n\n'.encode())
            await writer.drain()
            break
    return reader, writer


async def submit_message(reader, writer):
    while True:
        message = input('Введите сообщение: ')
        clean_message = re.sub(r'\n', '', message)
        writer.write(f'{clean_message}\n\n'.encode())
        await writer.drain()


async def register(reader, writer):
    logger.info('Open the connection')

    data = await reader.readline()
    text = f'{data.decode()!r}'[1:-3]
    logger.info(f'sender: {text}')

    writer.write('\n'.encode())
    await writer.drain()

    data = await reader.readline()
    text = f'{data.decode()!r}'[1:-3]
    logger.info(f'sender: {text}')

    nickname = str(input('Введите Ваш будущий ник: '))

    clean_nickname = nickname.replace('\n', '')
    writer.write(f'{clean_nickname}\n\n'.encode())
    await writer.drain()
    writer.write('\n'.encode())
    await writer.drain()

    data = await reader.readline()
    text = f'{data.decode()!r}'[1:-3]
    logger.info(f'sender: {text}')

    if 'account_hash' in text:
        token = json.loads(text)

        async with aiofiles.open('.env', 'a') as token_file:
            await token_file.write(f'account_hash={token["account_hash"]}\n')
        print('Токен сохранен в файл .env')
    return reader, writer



async def main():
    loglevel = 'INFO'
    logger = logging.getLogger(__name__)
    logger.setLevel(loglevel)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    args = read_args()
    host, port, reg = args.host, args.port, args.reg
    try:
        reader, writer = await asyncio.open_connection(host, port)
        if reg:
            reader, writer = await register(reader, writer)
            await submit_message(reader, writer)
        else:
            reader, writer = await authorise(reader, writer)
            await submit_message(reader, writer)
    finally:
        logger.info('Close the connection')
        writer.close()
        await writer.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
