import asyncio
import aiofiles
import argparse
from datetime import datetime


def read_args():
    parser = argparse.ArgumentParser(description='Утилита для чтения сообщений чата ')
    parser.add_argument('-host', type=str, default='minechat.dvmn.org', help='Имя хоста (default=minechat.dvmn.org)')
    parser.add_argument('-port', type=int, default=5000, help='Номер порта (default=5000)')
    parser.add_argument('-logfile', type=str, default='logfile.txt', help='Имя файла логов (default=logfile.txt)')
    args = parser.parse_args()
    return args


async def tcp_client():
    args = read_args()
    host, port, logfile = args.host, args.port, args.logfile
    try:
        reader, writer = await asyncio.open_connection(host, port)
        async with aiofiles.open(logfile, 'w') as chat_log:
            while True:
                log_time = datetime.now()
                log_time = log_time.strftime('%Y-%m-%d %H:%M:%S')
                data = await reader.readline()
                text = f'{data.decode()!r}'[1:-3]
                text.rstrip()
                text = f'{log_time} - {text}'
                print( text)
                await chat_log.write(f'{text}\n')
    finally:
        print('Close the connection')
        writer.close()
        await writer.wait_closed()

def main():
    asyncio.run(tcp_client())

if __name__ == '__main__':
    main()
