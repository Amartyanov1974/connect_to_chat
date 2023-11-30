import asyncio

async def tcp_echo_client():
    try:
        reader, writer = await asyncio.open_connection(
            'minechat.dvmn.org', 5000)
        while True:
            data = await reader.readline()
            text = f'{data.decode()!r}'[1:-3]
            text.rstrip()
            print(text)
    finally:
        print('Close the connection')
        writer.close()
        await writer.wait_closed()

def main():
    asyncio.run(tcp_echo_client())

if __name__ == '__main__':
    main()
