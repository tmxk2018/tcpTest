import asyncio

# TCP服务器的主机名和端口
HOST = '127.0.0.1'
PORT = 8081

# 异步函数，处理客户端连接
async def handle_client(reader, writer):
    # 无限循环，持续接收服务器发送的数据
    while True:
        # 读取数据，最多100字节,阻塞等待直到有数据可读100个分片
        data = await reader.read(100)
        if not data:
            # 如果没有数据，表示连接已关闭
            print('Connection closed by server')
            break
        # 将字节数据解码为字符串
        message = data.decode()
        print(f'Received: {message}')
        
        # 检查是否接收到了特定的关闭指令
        if message.strip().lower() == 'close':
            print('Received close command')
            break

    # 关闭连接
    writer.close()
    await writer.wait_closed()
    print('Connection closed')

# 主函数，启动客户端并连接到服务器
async def main():
    # 创建TCP客户端连接
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print(f'Connected to {HOST} on port {PORT}')
    
    # 使用handle_client函数处理接收和发送数据
    await handle_client(reader, writer)

# 运行客户端
asyncio.run(main())