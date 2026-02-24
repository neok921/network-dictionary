#!/usr/bin/env python3
"""
Запуск сетевого словаря
"""

import subprocess
import sys
import time
import os


def main():
    print("🌐 Network Dictionary Application")
    print("=" * 40)
    print("\nВыберите действие:")
    print("1. Запустить сервер")
    print("2. Запустить клиент")
    print("3. Запустить сервер и клиент")
    print("4. Выход")

    choice = input("\nВведите номер (1-4): ").strip()

    if choice == "1":
        print("\nЗапуск сервера...")
        subprocess.Popen([sys.executable, "server.py"])
        print("✅ Сервер запущен на localhost:5555")
        print("Для остановки нажмите Ctrl+C в этом окне")
        input("\nНажмите Enter для возврата в меню...")
        main()

    elif choice == "2":
        print("\nЗапуск клиента...")
        subprocess.Popen([sys.executable, "client_modern_fxied.py"])
        print("✅ Клиент запущен")
        input("\nНажмите Enter для возврата в меню...")
        main()

    elif choice == "3":
        print("\nЗапуск сервера и клиента...")
        # Запускаем сервер
        server_proc = subprocess.Popen([sys.executable, "server.py"])
        print("⏳ Ожидание запуска сервера...")
        time.sleep(2)

        # Запускаем клиент
        client_proc = subprocess.Popen([sys.executable, "client_modern.py"])
        print("✅ Сервер и клиент запущены")

        try:
            server_proc.wait()
            client_proc.wait()
        except KeyboardInterrupt:
            print("\nЗавершение работы...")
            server_proc.terminate()
            client_proc.terminate()

    elif choice == "4":
        print("Выход из программы...")
        sys.exit(0)
    else:
        print("Неверный выбор")
        main()


if __name__ == "__main__":
    main()