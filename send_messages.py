import asyncio
import aiofiles
import argparse
from environs import Env
import logging
import json


logger = logging.getLogger(__name__)


def read_args():
    env = Env()
    env.read_env()
    token = env.str('CHAT_TOKEN', '1')
    parser = argparse.ArgumentParser(description='Утилита для отправки сообщений в чат ')
    parser.add_argument('message', type=str,
                        help='Отправляемое в чат сообщение, обязательный параметр')
    parser.add_argument('-l', '--loglevel', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Уровень логирования (по умолчанию: INFO)')
    parser.add_argument('-hs', '--host', type=str, default='minechat.dvmn.org',
                        help='Имя хоста (default=minechat.dvmn.org)')
    parser.add_argument('-p', '--port', type=int, default=5050,
                        help='Номер порта (default=5050)')
    parser.add_argument('-t', '--token', type=str, default=token,
                        help='Токен для подключения к чату, по умолчанию берется из файла .env')
    parser.add_argument('-r', '--reg', type=bool, default=False, choices=[False, True],
                        help='Нужна регистрация? (default=False)')
    parser.add_argument('-n', '--name', type=str, default='User',
                        help='Имя пользователя при регистрации (default=User)')

    args = parser.parse_args()
    return args


async def read_message(reader):
    data = await reader.readline()
    text = f'{data.decode()!r}'[1:-3]
    return text


async def write_message(writer, message):
    writer.write(message.encode())
    await writer.drain()


async def register(reader, writer, nickname):
    logger.info('Open the connection')
    text = await read_message(reader)
    logger.info(f'sender: {text}')
    await write_message(writer, '\n')

    text = await read_message(reader)
    logger.info(f'sender: {text}')

    clean_nickname = nickname.replace('\\n', '')
    await write_message(writer, f'{clean_nickname}\n\n')
    await write_message(writer, '\n')

    text = await read_message(reader)
    logger.info(f'sender: {text}')

    if 'account_hash' in text:
        token = json.loads(text)

        async with aiofiles.open('.env', 'w') as token_file:
            account_hash = token['account_hash']
            await token_file.write(f'CHAT_TOKEN={account_hash}\n')
        logger.info(f'Токен: {account_hash} - сохранен в файл .env')
    return writer


async def authorise(reader, writer, token):
    while True:
        text = await read_message(reader)
        logger.info(f'sender: {text}')
        if 'Hello %username%!' in text:
            await write_message(writer, f'{token}\n\n')
        elif 'null' in text:
            logger.info('Неизвестный токен. Проверьте его или зарегистрируйтесь заново.')
            return 0
        else:
            text = await read_message(reader)
            logger.info(f'sender: {text}')
            return writer


async def submit_message(writer, message):
    clean_message = message.replace('\\n', '')
    await write_message(writer, f'{clean_message}\n\n')
    logger.info(f'Сообщение: "{clean_message}" - отправлено')


async def work_connection(args):
    host, port, reg, name = args.host, args.port, args.reg, args.name
    token, message = args.token, args.message
    try:
        reader, writer = await asyncio.open_connection(host, port)
        if reg:
            writer = await register(reader, writer, name)
            await submit_message(writer, message)
        else:
            writer = await authorise(reader, writer, token)
            if writer:
                await submit_message(writer, message)
    finally:
        if writer:
            logger.info('Close the connection')
            writer.close()
            await writer.wait_closed()



async def main():
    args = read_args()
    loglevel = args.loglevel
    logger = logging.getLogger(__name__)
    logger.setLevel(loglevel)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    await work_connection(args)


if __name__ == '__main__':
    asyncio.run(main())
