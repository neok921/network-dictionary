import socket
import json


def test_protocol():
    """Тестирование протокола"""
    print("Testing server protocol...")

    # Создаем тестовый сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 5555))

    # Тест 1: Ping
    print("1. Testing ping...")
    request = json.dumps({'action': 'ping'})

    # Отправляем с длиной
    message_bytes = request.encode('utf-8')
    message_length = len(message_bytes)
    sock.send(message_length.to_bytes(4, byteorder='big'))
    sock.send(message_bytes)

    # Получаем ответ
    length_bytes = sock.recv(4)
    response_length = int.from_bytes(length_bytes, byteorder='big')
    response_bytes = sock.recv(response_length)
    response = json.loads(response_bytes.decode('utf-8'))

    print(f"   Response: {response}")

    # Тест 2: List
    print("2. Testing list...")
    request = json.dumps({'action': 'list'})

    message_bytes = request.encode('utf-8')
    message_length = len(message_bytes)
    sock.send(message_length.to_bytes(4, byteorder='big'))
    sock.send(message_bytes)

    length_bytes = sock.recv(4)
    response_length = int.from_bytes(length_bytes, byteorder='big')
    response_bytes = b""
    while len(response_bytes) < response_length:
        chunk = sock.recv(min(4096, response_length - len(response_bytes)))
        response_bytes += chunk

    response = json.loads(response_bytes.decode('utf-8'))

    if response.get('status') == 'success':
        print(f"   Success! Got {len(response.get('dictionary', {}))} terms")
    else:
        print(f"   Error: {response.get('message')}")

    sock.close()
    print("\n✅ Protocol test completed!")


if __name__ == "__main__":
    test_protocol()