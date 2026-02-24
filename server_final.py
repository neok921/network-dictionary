import socket
import threading
import json
import os
import sys
from datetime import datetime


class DictionaryServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.dictionary = {}
        self.load_dictionary()
        self.lock = threading.Lock()
        self.running = True
        print(f"[INFO] Server initialized on {self.host}:{self.port}")

    def load_dictionary(self):
        """Загрузка словаря из файла"""
        try:
            if os.path.exists('dictionary.json'):
                with open('dictionary.json', 'r', encoding='utf-8') as f:
                    self.dictionary = json.load(f)
                print(f"[INFO] Loaded dictionary with {len(self.dictionary)} terms")
            else:
                self.dictionary = {
                    'python': 'A high-level programming language',
                    'oop': 'Object-Oriented Programming',
                    'api': 'Application Programming Interface',
                    'json': 'JavaScript Object Notation',
                    'socket': 'An endpoint for sending or receiving data across a computer network',
                    'server': 'A computer or system that provides resources or services',
                    'client': 'A computer or program that requests services from a server'
                }
                self.save_dictionary()
                print("[INFO] Created default dictionary")
        except Exception as e:
            print(f"[ERROR] Loading dictionary: {e}")
            self.dictionary = {}

    def save_dictionary(self):
        """Сохранение словаря в файл"""
        try:
            with open('dictionary.json', 'w', encoding='utf-8') as f:
                json.dump(self.dictionary, f, ensure_ascii=False, indent=2)
            print(f"[INFO] Dictionary saved with {len(self.dictionary)} terms")
        except Exception as e:
            print(f"[ERROR] Saving dictionary: {e}")

    def receive_message(self, client_socket):
        """Получение полного сообщения от клиента с обработкой длины"""
        try:
            # Получаем длину сообщения (первые 4 байта)
            length_bytes = client_socket.recv(4)
            if not length_bytes:
                return None

            message_length = int.from_bytes(length_bytes, byteorder='big')

            # Получаем само сообщение
            message_bytes = b""
            remaining = message_length
            while remaining > 0:
                chunk = client_socket.recv(min(4096, remaining))
                if not chunk:
                    break
                message_bytes += chunk
                remaining -= len(chunk)

            if len(message_bytes) != message_length:
                print(f"[ERROR] Incomplete message received")
                return None

            return message_bytes.decode('utf-8')

        except Exception as e:
            print(f"[ERROR] Receiving message: {e}")
            return None

    def send_message(self, client_socket, message):
        """Отправка сообщения клиенту с указанием длины"""
        try:
            message_bytes = message.encode('utf-8')
            message_length = len(message_bytes)

            # Отправляем длину сообщения (4 байта)
            length_bytes = message_length.to_bytes(4, byteorder='big')
            client_socket.send(length_bytes)

            # Отправляем само сообщение
            client_socket.send(message_bytes)
            return True

        except Exception as e:
            print(f"[ERROR] Sending message: {e}")
            return False

    def handle_client(self, client_socket, address):
        """Обработка клиентского подключения"""
        print(f"[+] New connection from {address}")

        try:
            while True:
                # Получаем сообщение
                message = self.receive_message(client_socket)
                if message is None:
                    print(f"[-] Client {address} disconnected")
                    break

                print(f"[DEBUG] Received from {address}: {message[:100]}...")

                try:
                    request = json.loads(message)
                except json.JSONDecodeError as e:
                    print(f"[ERROR] Invalid JSON from {address}: {e}")
                    response = {'status': 'error', 'message': 'Invalid JSON format'}
                    self.send_message(client_socket, json.dumps(response))
                    continue

                # Обрабатываем запрос
                response = self.process_request(request)
                print(f"[DEBUG] Sending response to {address}")

                # Отправляем ответ
                self.send_message(client_socket, json.dumps(response))

        except ConnectionResetError:
            print(f"[-] Connection reset by {address}")
        except Exception as e:
            print(f"[ERROR] Handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"[-] Connection closed from {address}")

    def process_request(self, request):
        """Обработка запроса от клиента"""
        action = request.get('action')
        term = request.get('term', '').lower()
        definition = request.get('definition', '')

        print(f"[PROCESS] Action: {action}, Term: {term}")

        with self.lock:
            if action == 'get':
                definition = self.dictionary.get(term, '')
                return {'status': 'success', 'definition': definition}

            elif action == 'add':
                if term and definition:
                    self.dictionary[term] = definition
                    self.save_dictionary()
                    return {'status': 'success', 'message': 'Term added successfully'}
                else:
                    return {'status': 'error', 'message': 'Term and definition are required'}

            elif action == 'search':
                results = {}
                search_term = term.lower()
                for key, value in self.dictionary.items():
                    if search_term in key.lower() or search_term in value.lower():
                        results[key] = value
                return {'status': 'success', 'results': results}

            elif action == 'list':
                return {'status': 'success', 'dictionary': self.dictionary}

            elif action == 'delete':
                if term in self.dictionary:
                    del self.dictionary[term]
                    self.save_dictionary()
                    return {'status': 'success', 'message': 'Term deleted successfully'}
                else:
                    return {'status': 'error', 'message': 'Term not found'}

            elif action == 'ping':
                return {'status': 'success', 'message': 'pong', 'timestamp': datetime.now().isoformat()}

            else:
                return {'status': 'error', 'message': 'Unknown action'}

    def start(self):
        """Запуск сервера"""
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            print(f"[*] Server started on {self.host}:{self.port}")
            print(f"[*] Listening for connections...")
            print(f"[*] Dictionary contains {len(self.dictionary)} terms")
            print("[*] Press Ctrl+C to stop the server\n")

            while self.running:
                try:
                    client_socket, address = self.server.accept()
                    print(f"[+] Accepted connection from {address}")

                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()
                    self.clients.append((client_socket, client_thread))

                except Exception as e:
                    if self.running:
                        print(f"[ERROR] Accepting connection: {e}")

        except Exception as e:
            print(f"[ERROR] Starting server: {e}")
            self.stop()

    def stop(self):
        """Остановка сервера"""
        print("\n[*] Shutting down server...")
        self.running = False

        # Закрыть все клиентские подключения
        for client_socket, thread in self.clients:
            try:
                client_socket.close()
            except:
                pass

        try:
            self.server.close()
        except:
            pass

        print("[*] Server stopped")


if __name__ == "__main__":
    print("=" * 50)
    print("NETWORK DICTIONARY SERVER (Fixed Protocol)")
    print("=" * 50)

    server = DictionaryServer()

    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[*] Interrupted by user")
        server.stop()
    except Exception as e:
        print(f"[ERROR] Server crashed: {e}")
        server.stop()