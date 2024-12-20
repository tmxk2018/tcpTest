import asyncio

# TCP服务器的主机名和端口
HOST = '127.0.0.1'
PORT = 8081

class TCPClient:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
    
    async def handle_client(self, reader, writer):
        # 无限循环，持续接收服务器发送的数据
        while True:
            # 读取数据，最多100字节
            data = await reader.read(100)
            if not data:
                # 如果没有数据，表示连接已关闭
                print('Connection closed by server')
                break
            # 将字节数据解码为字符串，并处理转义字符
            message = self.unescape_special_chars(data.decode())
            print(f'Received: {message}')
            
            # 检查是否接收到了特定的关闭指令
            if message.strip().lower() == 'close':
                print('Received close command')
                break

        # 关闭连接
        writer.close()
        await writer.wait_closed()
        print('Connection closed')

    # def unescape_special_chars(self, data):
    #     # 处理转义字符
    #     # 将转义序列替换为实际字符
    #     escaped_chars = {
    #         '\\n': '\n',
    #         '\\r': '\r',
    #         '\\t': '\t'
    #     }
    #     for escaped, char in escaped_chars.items():
    #         data = data.replace(escaped, char)
    #     return data
    
    def unescape_special_chars(self, data):
    # 处理转义字符
    # 使用字典和str.translate方法高效替换转义序列
        escaped_chars = {
            '\\n': '\n',
            '\\r': '\r',
            '\\t': '\t'
        }
        # 创建一个转换表
        translation_table = {ord(k): v for k, v in escaped_chars.items()}
        # 使用str.translate方法一次性替换所有转义字符
        return data.translate(translation_table)

    async def connect(self):
        # 创建TCP客户端连接
        reader, writer = await asyncio.open_connection(HOST, PORT)
        print(f'Connected to {HOST} on port {PORT}')
        
        # 使用handle_client函数处理接收和发送数据
        await self.handle_client(reader, writer)

    def run(self):
        # 运行客户端
        self.loop.run_until_complete(self.connect())
        self.loop.close()

# 创建TCP客户端实例
client = TCPClient()

# 启动客户端
client.run()