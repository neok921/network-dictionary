import sys
import json
import socket
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


# ========== ЛОКАЛИЗАЦИЯ ==========
class Localization:
    translations = {
        'en': {
            # Основные
            'app_title': 'Network Dictionary',
            'connect': 'Connect',
            'disconnect': 'Disconnect',
            'connected': 'Connected',
            'disconnected': 'Disconnected',
            'search': 'Search',
            'search_placeholder': 'Search for terms...',
            'add_term': 'Add Term',
            'list_all': 'List All',
            'favorites': 'Favorites',
            'settings': 'Settings',
            'statistics': 'Statistics',

            # Форма добавления
            'term': 'Term',
            'definition': 'Definition',
            'category': 'Category',
            'add': 'Add',
            'clear': 'Clear',
            'term_placeholder': 'Enter term...',
            'definition_placeholder': 'Enter definition...',

            # Меню
            'browse': 'Browse',
            'add_new': 'Add New',
            'all_terms': 'All Terms',
            'favorites_menu': 'Favorites',
            'settings_menu': 'Settings',
            'stats_menu': 'Statistics',

            # Темы
            'theme': 'Theme',
            'light': 'Light',
            'dark': 'Dark',
            'blue': 'Blue',
            'green': 'Green',

            # Сервер
            'server_host': 'Server Host',
            'server_port': 'Server Port',
            'connect_server': 'Connect to Server',
            'host_label': 'Host:',
            'port_label': 'Port:',

            # Сообщения
            'success': 'Success',
            'error': 'Error',
            'warning': 'Warning',
            'info': 'Info',
            'loading': 'Loading...',
            'searching': 'Searching...',
            'saving': 'Saving...',

            # Результаты
            'results': 'Results',
            'no_results': 'No results found',
            'found_terms': 'Found {count} terms',
            'total_terms': 'Total terms: {count}',
            'chars': 'chars',

            # Действия
            'get_definition': 'Get Definition',
            'copy': 'Copy',
            'delete': 'Delete',
            'close': 'Close',
            'cancel': 'Cancel',
            'confirm': 'Confirm',

            # Категории
            'general': 'General',
            'programming': 'Programming',
            'science': 'Science',
            'technology': 'Technology',
            'business': 'Business',
            'other': 'Other',

            # Статистика
            'stats_title': 'Statistics',
            'total_terms_stat': 'Total Terms',
            'favorites_stat': 'Favorites',
            'avg_term_length': 'Avg. Term Length',
            'avg_def_length': 'Avg. Definition Length',
            'server_status': 'Server Status',
            'connection': 'Connection',
        },
        'ru': {
            # Основные
            'app_title': 'Сетевой Словарь',
            'connect': 'Подключиться',
            'disconnect': 'Отключиться',
            'connected': 'Подключено',
            'disconnected': 'Отключено',
            'search': 'Поиск',
            'search_placeholder': 'Поиск терминов...',
            'add_term': 'Добавить термин',
            'list_all': 'Все термины',
            'favorites': 'Избранное',
            'settings': 'Настройки',
            'statistics': 'Статистика',

            # Форма добавления
            'term': 'Термин',
            'definition': 'Определение',
            'category': 'Категория',
            'add': 'Добавить',
            'clear': 'Очистить',
            'term_placeholder': 'Введите термин...',
            'definition_placeholder': 'Введите определение...',

            # Меню
            'browse': 'Просмотр',
            'add_new': 'Добавить',
            'all_terms': 'Все термины',
            'favorites_menu': 'Избранное',
            'settings_menu': 'Настройки',
            'stats_menu': 'Статистика',

            # Темы
            'theme': 'Тема',
            'light': 'Светлая',
            'dark': 'Темная',
            'blue': 'Синяя',
            'green': 'Зеленая',

            # Сервер
            'server_host': 'Сервер',
            'server_port': 'Порт',
            'connect_server': 'Подключиться к серверу',
            'host_label': 'Хост:',
            'port_label': 'Порт:',

            # Сообщения
            'success': 'Успешно',
            'error': 'Ошибка',
            'warning': 'Предупреждение',
            'info': 'Информация',
            'loading': 'Загрузка...',
            'searching': 'Поиск...',
            'saving': 'Сохранение...',

            # Результаты
            'results': 'Результаты',
            'no_results': 'Результаты не найдены',
            'found_terms': 'Найдено {count} терминов',
            'total_terms': 'Всего терминов: {count}',
            'chars': 'симв.',

            # Действия
            'get_definition': 'Получить определение',
            'copy': 'Копировать',
            'delete': 'Удалить',
            'close': 'Закрыть',
            'cancel': 'Отмена',
            'confirm': 'Подтвердить',

            # Категории
            'general': 'Общее',
            'programming': 'Программирование',
            'science': 'Наука',
            'technology': 'Технологии',
            'business': 'Бизнес',
            'other': 'Другое',

            # Статистика
            'stats_title': 'Статистика',
            'total_terms_stat': 'Всего терминов',
            'favorites_stat': 'В избранном',
            'avg_term_length': 'Ср. длина термина',
            'avg_def_length': 'Ср. длина определения',
            'server_status': 'Статус сервера',
            'connection': 'Подключение',
        }
    }

    @classmethod
    def tr(cls, key, lang='en', **kwargs):
        text = cls.translations.get(lang, {}).get(key, key)
        # Безопасное форматирование
        try:
            if kwargs:
                return text.format(**kwargs)
            return text
        except (KeyError, IndexError):
            return text


# ========== СЕТЕВОЙ МЕНЕДЖЕР ==========
class FixedNetworkManager:
    @staticmethod
    def send_message(sock, message):
        """Отправка сообщения с указанием длины"""
        message_bytes = message.encode('utf-8')
        message_length = len(message_bytes)

        # Отправляем длину сообщения (4 байта)
        length_bytes = message_length.to_bytes(4, byteorder='big')
        sock.send(length_bytes)

        # Отправляем само сообщение
        sock.send(message_bytes)

    @staticmethod
    def receive_message(sock):
        """Получение сообщения с указанием длины"""
        try:
            # Получаем длину сообщения
            length_bytes = sock.recv(4)
            if not length_bytes:
                return None

            message_length = int.from_bytes(length_bytes, byteorder='big')

            # Получаем само сообщение
            message_bytes = b""
            remaining = message_length
            while remaining > 0:
                chunk = sock.recv(min(4096, remaining))
                if not chunk:
                    break
                message_bytes += chunk
                remaining -= len(chunk)

            if len(message_bytes) != message_length:
                return None

            return message_bytes.decode('utf-8')

        except Exception as e:
            print(f"[CLIENT ERROR] Receiving: {e}")
            return None

    @staticmethod
    def send_request(host, port, request_data, timeout=5):
        """Отправка запроса на сервер"""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(timeout)
            client_socket.connect((host, port))

            # Отправляем запрос
            FixedNetworkManager.send_message(client_socket, json.dumps(request_data))

            # Получаем ответ
            response_str = FixedNetworkManager.receive_message(client_socket)
            client_socket.close()

            if response_str:
                return json.loads(response_str)
            else:
                return {'status': 'error', 'message': 'No response from server'}

        except socket.timeout:
            return {'status': 'error', 'message': 'Connection timeout'}
        except ConnectionRefusedError:
            return {'status': 'error', 'message': 'Connection refused'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


# ========== ТЕМЫ ==========
class ThemeManager:
    themes = {
        "light": {
            "primary": "#4361ee",
            "secondary": "#3a0ca3",
            "accent": "#4cc9f0",
            "background": "#ffffff",
            "surface": "#f8f9fa",
            "text_primary": "#212529",
            "text_secondary": "#6c757d",
            "border": "#dee2e6",
            "success": "#4CAF50",
            "warning": "#FF9800",
            "error": "#f44336",
            "shadow": "rgba(0,0,0,0.1)",
            "sidebar_bg": "#f8f9fa",
            "sidebar_hover": "#e9ecef",
        },
        "dark": {
            "primary": "#7209b7",
            "secondary": "#3a0ca3",
            "accent": "#4cc9f0",
            "background": "#121212",
            "surface": "#1e1e1e",
            "text_primary": "#ffffff",
            "text_secondary": "#b0b0b0",
            "border": "#333333",
            "success": "#4CAF50",
            "warning": "#FF9800",
            "error": "#f44336",
            "shadow": "rgba(255,255,255,0.05)",
            "sidebar_bg": "#1a1a1a",
            "sidebar_hover": "#2d2d2d",
        },
        "blue": {
            "primary": "#2196F3",
            "secondary": "#1976D2",
            "accent": "#03A9F4",
            "background": "#E3F2FD",
            "surface": "#FFFFFF",
            "text_primary": "#0D47A1",
            "text_secondary": "#1E88E5",
            "border": "#90CAF9",
            "success": "#4CAF50",
            "warning": "#FF9800",
            "error": "#f44336",
            "shadow": "rgba(33,150,243,0.1)",
            "sidebar_bg": "#bbdefb",
            "sidebar_hover": "#90caf9",
        },
        "green": {
            "primary": "#2E7D32",
            "secondary": "#1B5E20",
            "accent": "#4CAF50",
            "background": "#E8F5E9",
            "surface": "#FFFFFF",
            "text_primary": "#1B5E20",
            "text_secondary": "#388E3C",
            "border": "#A5D6A7",
            "success": "#2E7D32",
            "warning": "#FF9800",
            "error": "#f44336",
            "shadow": "rgba(46,125,50,0.1)",
            "sidebar_bg": "#c8e6c9",
            "sidebar_hover": "#a5d6a7",
        }
    }

    @staticmethod
    def get_theme(name):
        return ThemeManager.themes.get(name, ThemeManager.themes["light"])


# ========== КАРТОЧКА ТЕРМИНА ==========
class TermCard(QFrame):
    def __init__(self, term, definition, theme, parent=None):
        super().__init__(parent)
        self.term = term
        self.definition = definition
        self.theme = theme
        self.setup_ui()
        self.apply_style()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        # Заголовок термина
        self.term_label = QLabel(self.term)
        self.term_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {self.theme['text_primary']};
            margin-bottom: 5px;
        """)

        # Определение
        self.def_label = QLabel(self.definition)
        self.def_label.setWordWrap(True)
        self.def_label.setStyleSheet(f"""
            font-size: 14px;
            color: {self.theme['text_secondary']};
            margin-top: 5px;
        """)

        # Кнопка действий
        self.action_btn = QPushButton("⚡")
        self.action_btn.setFixedSize(30, 30)
        self.action_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(self.term_label)
        layout.addWidget(self.def_label)
        layout.addStretch()
        layout.addWidget(self.action_btn, 0, Qt.AlignmentFlag.AlignRight)

    def apply_style(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {self.theme['surface']};
                border: 1px solid {self.theme['border']};
                border-radius: 10px;
                padding: 10px;
            }}
            QFrame:hover {{
                border: 2px solid {self.theme['primary']};
                background-color: {self.theme['background']};
            }}
            QPushButton {{
                background-color: {self.theme['primary']};
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {self.theme['secondary']};
            }}
        """)


# ========== САЙДБАР ==========
class Sidebar(QWidget):
    def __init__(self, localization, parent=None):
        super().__init__(parent)
        self.localization = localization
        self.lang = 'en'
        self.theme = 'light'
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Логотип
        self.logo = QLabel("📚")
        self.logo.setStyleSheet("""
            font-size: 40px;
            padding: 30px 20px;
            background-color: transparent;
        """)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo)

        # Контейнер для кнопок меню
        self.menu_container = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_container)
        self.menu_layout.setContentsMargins(10, 0, 10, 0)
        self.menu_layout.setSpacing(5)

        layout.addWidget(self.menu_container)
        layout.addStretch()

        self.menu_buttons = {}

    def update_language(self, lang):
        """Обновление текста меню на выбранный язык"""
        self.lang = lang

        # Очищаем старые кнопки
        for btn in self.menu_buttons.values():
            btn.deleteLater()
        self.menu_buttons.clear()

        # Создаем новые кнопки
        menu_items = [
            ("🔍", "browse", "browse"),
            ("➕", "add_new", "add"),
            ("📋", "all_terms", "list"),
            ("⭐", "favorites_menu", "favorites"),
            ("📊", "stats_menu", "stats"),
            ("⚙️", "settings_menu", "settings")
        ]

        for icon, text_key, key in menu_items:
            text = self.localization.tr(text_key, lang)
            btn = self.create_menu_button(icon, text)
            self.menu_buttons[key] = btn
            self.menu_layout.addWidget(btn)

    def create_menu_button(self, icon, text):
        btn = QPushButton(f"{icon}  {text}")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(50)

        # Стиль для кнопки с анимацией при наведении
        btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 0px 20px;
                border: none;
                background: transparent;
                font-size: 14px;
                color: #666;
                border-radius: 8px;
                margin: 0px;
            }
        """)

        # Добавляем эффект при наведении
        btn.enterEvent = lambda e: self.on_button_hover(btn, True)
        btn.leaveEvent = lambda e: self.on_button_hover(btn, False)

        return btn

    def on_button_hover(self, button, hover):
        """Обработка наведения на кнопку"""
        theme = ThemeManager.get_theme(self.theme)
        if hover:
            button.setStyleSheet(f"""
                QPushButton {{
                    text-align: left;
                    padding: 0px 20px;
                    border: none;
                    background-color: {theme['sidebar_hover']};
                    font-size: 14px;
                    color: {theme['text_primary']};
                    border-radius: 8px;
                    margin: 0px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {theme['sidebar_hover']};
                }}
            """)
        else:
            button.setStyleSheet(f"""
                QPushButton {{
                    text-align: left;
                    padding: 0px 20px;
                    border: none;
                    background: transparent;
                    font-size: 14px;
                    color: {theme['text_secondary']};
                    border-radius: 8px;
                    margin: 0px;
                }}
            """)

    def apply_theme(self, theme):
        """Применение темы к сайдбару"""
        self.theme = theme
        theme_data = ThemeManager.get_theme(theme)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_data['sidebar_bg']};
            }}
        """)

        # Обновляем стиль всех кнопок
        for button in self.menu_buttons.values():
            button.setStyleSheet(f"""
                QPushButton {{
                    text-align: left;
                    padding: 0px 20px;
                    border: none;
                    background: transparent;
                    font-size: 14px;
                    color: {theme_data['text_secondary']};
                    border-radius: 8px;
                    margin: 0px;
                }}
            """)


# ========== ДИАЛОГ НАСТРОЕК ==========
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.parent_app.localization.tr('settings', self.parent_app.current_lang))
        self.setFixedSize(500, 400)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Заголовок
        title = QLabel("⚙️ " + self.parent_app.localization.tr('settings', self.parent_app.current_lang))
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Язык
        lang_group = QGroupBox(self.parent_app.localization.tr('language', self.parent_app.current_lang))
        lang_layout = QVBoxLayout()

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "Русский"])
        self.lang_combo.setCurrentText("English" if self.parent_app.current_lang == 'en' else "Русский")

        lang_layout.addWidget(self.lang_combo)
        lang_group.setLayout(lang_layout)

        # Тема
        theme_group = QGroupBox(self.parent_app.localization.tr('theme', self.parent_app.current_lang))
        theme_layout = QVBoxLayout()

        self.theme_combo = QComboBox()
        theme_names = [
            self.parent_app.localization.tr('light', self.parent_app.current_lang),
            self.parent_app.localization.tr('dark', self.parent_app.current_lang),
            self.parent_app.localization.tr('blue', self.parent_app.current_lang),
            self.parent_app.localization.tr('green', self.parent_app.current_lang)
        ]
        self.theme_combo.addItems(theme_names)

        # Устанавливаем текущую тему
        theme_display_names = {
            'light': self.parent_app.localization.tr('light', self.parent_app.current_lang),
            'dark': self.parent_app.localization.tr('dark', self.parent_app.current_lang),
            'blue': self.parent_app.localization.tr('blue', self.parent_app.current_lang),
            'green': self.parent_app.localization.tr('green', self.parent_app.current_lang)
        }
        current_theme_display = theme_display_names.get(self.parent_app.current_theme, theme_names[0])
        index = self.theme_combo.findText(current_theme_display)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        theme_layout.addWidget(self.theme_combo)
        theme_group.setLayout(theme_layout)

        # Сервер
        server_group = QGroupBox(self.parent_app.localization.tr('server_host', self.parent_app.current_lang))
        server_layout = QFormLayout()

        self.host_input = QLineEdit(self.parent_app.server_host)
        self.port_input = QLineEdit(str(self.parent_app.server_port))

        server_layout.addRow(self.parent_app.localization.tr('host_label', self.parent_app.current_lang),
                             self.host_input)
        server_layout.addRow(self.parent_app.localization.tr('port_label', self.parent_app.current_lang),
                             self.port_input)

        server_group.setLayout(server_layout)

        # Кнопки
        button_layout = QHBoxLayout()
        save_btn = QPushButton(self.parent_app.localization.tr('confirm', self.parent_app.current_lang))
        cancel_btn = QPushButton(self.parent_app.localization.tr('cancel', self.parent_app.current_lang))

        save_btn.clicked.connect(self.save_settings)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        layout.addWidget(title)
        layout.addWidget(lang_group)
        layout.addWidget(theme_group)
        layout.addWidget(server_group)
        layout.addStretch()
        layout.addLayout(button_layout)

    def save_settings(self):
        """Сохранение настроек"""
        # Сохраняем язык
        new_lang = 'en' if self.lang_combo.currentText() == 'English' else 'ru'
        if new_lang != self.parent_app.current_lang:
            self.parent_app.current_lang = new_lang

        # Сохраняем тему
        theme_map = {
            self.parent_app.localization.tr('light', self.parent_app.current_lang): 'light',
            self.parent_app.localization.tr('dark', self.parent_app.current_lang): 'dark',
            self.parent_app.localization.tr('blue', self.parent_app.current_lang): 'blue',
            self.parent_app.localization.tr('green', self.parent_app.current_lang): 'green'
        }
        new_theme = theme_map.get(self.theme_combo.currentText(), 'light')
        if new_theme != self.parent_app.current_theme:
            self.parent_app.current_theme = new_theme

        # Сохраняем настройки сервера
        self.parent_app.server_host = self.host_input.text()
        try:
            self.parent_app.server_port = int(self.port_input.text())
        except ValueError:
            pass

        # Применяем изменения
        self.parent_app.apply_theme()
        self.parent_app.update_ui_texts()

        self.accept()


# ========== ГЛАВНОЕ ОКНО ==========
class ModernDictionaryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = "light"
        self.current_lang = "en"
        self.connected = False
        self.server_host = "localhost"
        self.server_port = 5555
        self.favorites = set()
        self.localization = Localization()

        self.setup_ui()
        self.apply_theme()
        self.update_ui_texts()

    def setup_ui(self):
        """Настройка современного интерфейса"""
        self.setWindowTitle(self.localization.tr('app_title', self.current_lang))
        self.setGeometry(100, 50, 1400, 900)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Левая панель (сайдбар)
        self.sidebar = Sidebar(self.localization)
        self.sidebar.setFixedWidth(280)
        main_layout.addWidget(self.sidebar)

        # Правая часть
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(30, 30, 30, 30)
        right_layout.setSpacing(20)

        # Верхняя панель
        self.top_bar = self.create_top_bar()
        right_layout.addWidget(self.top_bar)

        # Поисковая строка
        search_container = QFrame()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)

        self.search_input = QLineEdit()
        self.search_input.setClearButtonEnabled(True)

        self.search_btn = QPushButton()
        self.search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_btn.clicked.connect(self.search_terms)

        self.list_all_btn = QPushButton()
        self.list_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.list_all_btn.clicked.connect(self.load_all_terms)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.list_all_btn)

        right_layout.addWidget(search_container)

        # Основная область с вкладками
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.setDocumentMode(True)

        # Вкладка Browse
        self.browse_tab = self.create_browse_tab()
        self.tab_widget.addTab(self.browse_tab, "")

        # Вкладка Add
        self.add_tab = self.create_add_tab()
        self.tab_widget.addTab(self.add_tab, "")

        # Вкладка Favorites
        self.fav_tab = self.create_favorites_tab()
        self.tab_widget.addTab(self.fav_tab, "")

        right_layout.addWidget(self.tab_widget)

        main_layout.addWidget(right_widget)

        # Статус бар
        self.setup_status_bar()

        # Подключение сигналов
        self.search_input.returnPressed.connect(self.search_terms)

    def create_top_bar(self):
        """Создание верхней панели"""
        top_bar = QWidget()
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(0, 0, 0, 0)

        # Заголовок
        self.title_label = QLabel()
        self.title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #333;
        """)

        # Виджеты справа
        right_widgets = QWidget()
        self.right_layout = QHBoxLayout(right_widgets)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(10)

        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(right_widgets)

        return top_bar

    def update_top_bar(self):
        """Обновление верхней панели"""
        # Очищаем правую часть
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Кнопка подключения
        self.connect_btn = QPushButton()
        self.connect_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.connect_btn.clicked.connect(self.toggle_connection)
        self.connect_btn.setMinimumWidth(120)

        # Статистика
        self.stats_btn = QPushButton()
        self.stats_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stats_btn.clicked.connect(self.show_stats)
        self.stats_btn.setMinimumWidth(120)

        # Добавляем виджеты
        self.right_layout.addWidget(self.connect_btn)
        self.right_layout.addWidget(self.stats_btn)

    def create_browse_tab(self):
        """Создание вкладки просмотра"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Заголовок
        self.browse_header = QLabel()
        self.browse_header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        """)

        # Контейнер для карточек
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(20)

        scroll.setWidget(self.cards_container)

        layout.addWidget(self.browse_header)
        layout.addWidget(scroll)

        return widget

    def create_add_tab(self):
        """Создание вкладки добавления"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(25)

        # Заголовок
        self.add_header = QLabel()
        self.add_header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
        """)

        # Форма
        form_widget = QFrame()
        form_widget.setMinimumHeight(400)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(20)

        # Термин
        self.term_label = QLabel()
        self.term_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.add_term_input = QLineEdit()
        self.add_term_input.setMinimumHeight(40)

        # Определение
        self.def_label = QLabel()
        self.def_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.add_def_input = QTextEdit()
        self.add_def_input.setMinimumHeight(150)

        # Категория
        self.cat_label = QLabel()
        self.cat_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.category_combo = QComboBox()

        # Кнопки
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton()
        self.add_btn.setMinimumHeight(45)
        self.add_btn.clicked.connect(self.add_new_term)

        self.clear_btn = QPushButton()
        self.clear_btn.setMinimumHeight(45)
        self.clear_btn.clicked.connect(self.clear_form)

        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.clear_btn)

        form_layout.addWidget(self.term_label)
        form_layout.addWidget(self.add_term_input)
        form_layout.addWidget(self.def_label)
        form_layout.addWidget(self.add_def_input)
        form_layout.addWidget(self.cat_label)
        form_layout.addWidget(self.category_combo)
        form_layout.addLayout(button_layout)

        layout.addWidget(self.add_header)
        layout.addWidget(form_widget)
        layout.addStretch()

        return widget

    def create_favorites_tab(self):
        """Создание вкладки избранного"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.fav_header = QLabel()
        self.fav_header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        """)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        self.fav_container = QWidget()
        self.fav_layout = QVBoxLayout(self.fav_container)

        scroll.setWidget(self.fav_container)

        layout.addWidget(self.fav_header)
        layout.addWidget(scroll)

        return widget

    def update_category_combo(self):
        """Обновление комбобокса категорий"""
        self.category_combo.clear()
        categories = [
            self.localization.tr('general', self.current_lang),
            self.localization.tr('programming', self.current_lang),
            self.localization.tr('science', self.current_lang),
            self.localization.tr('technology', self.current_lang),
            self.localization.tr('business', self.current_lang),
            self.localization.tr('other', self.current_lang)
        ]
        self.category_combo.addItems(categories)

    def setup_status_bar(self):
        """Настройка статус бара"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Виджеты в статус баре
        self.status_label = QLabel()
        self.status_icon = QLabel("🔴")

        self.server_label = QLabel()

        self.status_bar.addPermanentWidget(self.status_icon)
        self.status_bar.addPermanentWidget(self.status_label)
        self.status_bar.addPermanentWidget(QLabel(" | "))
        self.status_bar.addPermanentWidget(self.server_label)

    def update_ui_texts(self):
        """Обновление всех текстов интерфейса"""
        # Заголовок окна
        self.setWindowTitle(self.localization.tr('app_title', self.current_lang))

        # Заголовок приложения
        self.title_label.setText("📚 " + self.localization.tr('app_title', self.current_lang))

        # Обновляем верхнюю панель
        self.update_top_bar()

        # Кнопка подключения - теперь полный текст
        if self.connected:
            self.connect_btn.setText("🔗 " + self.localization.tr('disconnect', self.current_lang))
        else:
            self.connect_btn.setText("🔌 " + self.localization.tr('connect', self.current_lang))

        # Кнопка статистики - теперь полный текст
        self.stats_btn.setText("📊 " + self.localization.tr('statistics', self.current_lang))

        # Кнопка поиска
        self.search_btn.setText("🔍 " + self.localization.tr('search', self.current_lang))
        self.list_all_btn.setText("📋 " + self.localization.tr('list_all', self.current_lang))
        self.search_input.setPlaceholderText(self.localization.tr('search_placeholder', self.current_lang))

        # Вкладки
        self.tab_widget.setTabText(0, "🌐 " + self.localization.tr('browse', self.current_lang))
        self.tab_widget.setTabText(1, "➕ " + self.localization.tr('add_new', self.current_lang))
        self.tab_widget.setTabText(2, "⭐ " + self.localization.tr('favorites_menu', self.current_lang))

        # Заголовки вкладок
        self.browse_header.setText(self.localization.tr('browse', self.current_lang))
        self.add_header.setText(self.localization.tr('add_term', self.current_lang))
        self.fav_header.setText("⭐ " + self.localization.tr('favorites_menu', self.current_lang))

        # Форма добавления
        self.term_label.setText(self.localization.tr('term', self.current_lang) + " *")
        self.def_label.setText(self.localization.tr('definition', self.current_lang) + " *")
        self.cat_label.setText(self.localization.tr('category', self.current_lang))
        self.add_term_input.setPlaceholderText(self.localization.tr('term_placeholder', self.current_lang))
        self.add_def_input.setPlaceholderText(self.localization.tr('definition_placeholder', self.current_lang))
        self.add_btn.setText("➕ " + self.localization.tr('add', self.current_lang))
        self.clear_btn.setText("🗑️ " + self.localization.tr('clear', self.current_lang))

        # Обновление комбобокса категорий
        self.update_category_combo()

        # Статус бар
        status_text = self.localization.tr('connected', self.current_lang) if self.connected else self.localization.tr(
            'disconnected', self.current_lang)
        self.status_label.setText(status_text)

        server_text = f"{self.localization.tr('server_host', self.current_lang)}: "
        if self.connected:
            server_text += f"{self.server_host}:{self.server_port}"
        else:
            server_text += self.localization.tr('disconnected', self.current_lang)
        self.server_label.setText(server_text)

        # Обновление сайдбара
        self.sidebar.update_language(self.current_lang)
        self.sidebar.apply_theme(self.current_theme)

        # Подключение сигналов сайдбара
        for key, btn in self.sidebar.menu_buttons.items():
            try:
                btn.clicked.disconnect()
            except:
                pass

            if key == 'browse':
                btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(0))
            elif key == 'add':
                btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(1))
            elif key == 'list':
                btn.clicked.connect(self.load_all_terms)
            elif key == 'favorites':
                btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(2))
            elif key == 'stats':
                btn.clicked.connect(self.show_stats)
            elif key == 'settings':
                btn.clicked.connect(self.show_settings)

    def show_settings(self):
        """Показать диалог настроек"""
        dialog = SettingsDialog(self)
        dialog.exec()

    def apply_theme(self):
        """Применение текущей темы"""
        theme = ThemeManager.get_theme(self.current_theme)

        style = f"""
            QMainWindow {{
                background-color: {theme['background']};
            }}
            QWidget {{
                background-color: {theme['background']};
                color: {theme['text_primary']};
            }}
            QPushButton {{
                background-color: {theme['primary']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {theme['secondary']};
            }}
            QPushButton:pressed {{
                background-color: {theme['accent']};
            }}
            QLineEdit, QTextEdit {{
                background-color: {theme['surface']};
                border: 2px solid {theme['border']};
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: {theme['text_primary']};
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: 2px solid {theme['primary']};
            }}
            QComboBox {{
                background-color: {theme['surface']};
                border: 2px solid {theme['border']};
                border-radius: 8px;
                padding: 8px;
                min-width: 100px;
            }}
            QTabWidget::pane {{
                border: 1px solid {theme['border']};
                border-radius: 10px;
                background-color: {theme['surface']};
            }}
            QTabBar::tab {{
                background-color: {theme['surface']};
                color: {theme['text_secondary']};
                padding: 10px 20px;
                margin-right: 5px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            QTabBar::tab:selected {{
                background-color: {theme['primary']};
                color: white;
                font-weight: bold;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {theme['background']};
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QStatusBar {{
                background-color: {theme['surface']};
                color: {theme['text_secondary']};
                border-top: 1px solid {theme['border']};
            }}
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {theme['border']};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """

        self.setStyleSheet(style)

    def toggle_connection(self):
        """Подключение/отключение от сервера"""
        if not self.connected:
            self.show_connection_dialog()
        else:
            self.disconnect_from_server()

    def show_connection_dialog(self):
        """Диалог подключения"""
        dialog = QDialog(self)
        dialog.setWindowTitle(self.localization.tr('connect_server', self.current_lang))
        dialog.setFixedSize(400, 300)

        layout = QVBoxLayout(dialog)

        # Заголовок
        title = QLabel("🔌 " + self.localization.tr('connect_server', self.current_lang))
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")

        # Форма
        form_layout = QFormLayout()

        host_input = QLineEdit(self.server_host)
        port_input = QLineEdit(str(self.server_port))

        form_layout.addRow(self.localization.tr('host_label', self.current_lang), host_input)
        form_layout.addRow(self.localization.tr('port_label', self.current_lang), port_input)

        # Кнопки
        button_layout = QHBoxLayout()
        connect_btn = QPushButton(self.localization.tr('connect', self.current_lang))
        cancel_btn = QPushButton(self.localization.tr('cancel', self.current_lang))

        connect_btn.clicked.connect(lambda: self.do_connect(
            host_input.text(),
            port_input.text(),
            dialog
        ))
        cancel_btn.clicked.connect(dialog.reject)

        button_layout.addWidget(connect_btn)
        button_layout.addWidget(cancel_btn)

        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addStretch()
        layout.addLayout(button_layout)

        dialog.exec()

    def do_connect(self, host, port, dialog):
        """Выполнение подключения"""
        try:
            port = int(port)

            # Тестовое подключение
            test_response = FixedNetworkManager.send_request(
                host, port,
                {'action': 'ping'},
                timeout=3
            )

            if test_response and test_response.get('status') == 'success':
                self.server_host = host
                self.server_port = port
                self.connected = True
                self.status_icon.setText("🟢")

                # Обновляем UI
                self.update_ui_texts()

                # Загружаем все термины
                self.load_all_terms()

                dialog.accept()

                QMessageBox.information(
                    self,
                    self.localization.tr('success', self.current_lang),
                    f"{self.localization.tr('connected', self.current_lang)}!\n" +
                    self.localization.tr('total_terms', self.current_lang, count=self.get_terms_count())
                )
            else:
                error_msg = test_response.get('message', 'Connection failed') if test_response else 'No response'
                QMessageBox.critical(self, self.localization.tr('error', self.current_lang), error_msg)

        except ValueError:
            QMessageBox.critical(self, self.localization.tr('error', self.current_lang), "Invalid port number")
        except Exception as e:
            QMessageBox.critical(self, self.localization.tr('error', self.current_lang), str(e))

    def disconnect_from_server(self):
        """Отключение от сервера"""
        self.connected = False
        self.status_icon.setText("🔴")
        self.update_ui_texts()

    def get_terms_count(self):
        """Получение количества терминов с сервера"""
        if not self.connected:
            return 0

        response = FixedNetworkManager.send_request(
            self.server_host,
            self.server_port,
            {'action': 'list'}
        )

        if response and response.get('status') == 'success':
            return len(response.get('dictionary', {}))
        return 0

    def send_request(self, request_data):
        """Отправка запроса на сервер"""
        if not self.connected:
            self.show_not_connected_warning()
            return None

        return FixedNetworkManager.send_request(
            self.server_host,
            self.server_port,
            request_data
        )

    def show_not_connected_warning(self):
        """Показать предупреждение о неподключенном состоянии"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(self.localization.tr('warning', self.current_lang))
        msg.setText(self.localization.tr('disconnected', self.current_lang))
        msg.setInformativeText("Please connect to a server first.")

        connect_btn = msg.addButton(self.localization.tr('connect', self.current_lang),
                                    QMessageBox.ButtonRole.AcceptRole)
        cancel_btn = msg.addButton(self.localization.tr('cancel', self.current_lang), QMessageBox.ButtonRole.RejectRole)

        msg.exec()

        if msg.clickedButton() == connect_btn:
            self.toggle_connection()

    def search_terms(self):
        """Поиск терминов"""
        search_text = self.search_input.text().strip()
        if not search_text:
            return

        self.show_loading(self.localization.tr('searching', self.current_lang))

        response = self.send_request({
            'action': 'search',
            'term': search_text
        })

        if response:
            if response.get('status') == 'success':
                results = response.get('results', {})
                self.display_results(results)
            else:
                QMessageBox.critical(self, self.localization.tr('error', self.current_lang),
                                     response.get('message', 'Unknown error'))

        self.hide_loading()

    def load_all_terms(self):
        """Загрузка всех терминов"""
        if not self.connected:
            self.show_not_connected_warning()
            return

        self.show_loading(self.localization.tr('loading', self.current_lang))
        self.tab_widget.setCurrentIndex(0)

        response = self.send_request({'action': 'list'})

        if response:
            if response.get('status') == 'success':
                dictionary = response.get('dictionary', {})
                self.display_results(dictionary)
            else:
                QMessageBox.critical(self, self.localization.tr('error', self.current_lang),
                                     response.get('message', 'Unknown error'))

        self.hide_loading()

    def display_results(self, results):
        """Отображение результатов в виде карточек"""
        # Очищаем старые карточки
        for i in reversed(range(self.cards_layout.count())):
            widget = self.cards_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if not results:
            no_results = QLabel(self.localization.tr('no_results', self.current_lang))
            no_results.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_results.setStyleSheet("font-size: 16px; color: gray; padding: 50px;")
            self.cards_layout.addWidget(no_results, 0, 0, 1, 3)
            return

        theme = ThemeManager.get_theme(self.current_theme)

        # Добавляем информацию о количестве
        count_label = QLabel(self.localization.tr('found_terms', self.current_lang, count=len(results)))
        count_label.setStyleSheet(f"""
            font-size: 14px;
            color: {theme['text_secondary']};
            margin-bottom: 10px;
        """)
        self.cards_layout.addWidget(count_label, 0, 0, 1, 3)

        # Добавляем карточки
        row, col = 1, 0
        max_cols = 3

        for term, definition in sorted(results.items()):
            card = TermCard(term, definition, theme)
            card.action_btn.clicked.connect(
                lambda checked, t=term, d=definition: self.show_term_detail(t, d)
            )

            self.cards_layout.addWidget(card, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # Добавляем растяжку
        self.cards_layout.setRowStretch(row + 1, 1)

    def add_new_term(self):
        """Добавление нового термина"""
        term = self.add_term_input.text().strip()
        definition = self.add_def_input.toPlainText().strip()

        if not term or not definition:
            QMessageBox.warning(self,
                                self.localization.tr('warning', self.current_lang),
                                "Please fill in all required fields")
            return

        self.show_loading(self.localization.tr('saving', self.current_lang))

        response = self.send_request({
            'action': 'add',
            'term': term,
            'definition': definition
        })

        if response:
            if response.get('status') == 'success':
                QMessageBox.information(self,
                                        self.localization.tr('success', self.current_lang),
                                        "Term added successfully!")
                self.clear_form()

                # Обновляем список
                self.load_all_terms()
            else:
                QMessageBox.critical(self,
                                     self.localization.tr('error', self.current_lang),
                                     response.get('message', 'Unknown error'))

        self.hide_loading()

    def clear_form(self):
        """Очистка формы добавления"""
        self.add_term_input.clear()
        self.add_def_input.clear()
        self.category_combo.setCurrentIndex(0)

    def show_term_detail(self, term, definition):
        """Показать детали термина в диалоге"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{self.localization.tr('term', self.current_lang)}: {term}")
        dialog.setFixedSize(500, 400)

        layout = QVBoxLayout(dialog)

        # Заголовок
        title = QLabel(term)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4361ee;
            margin-bottom: 10px;
        """)

        # Определение
        def_text = QTextEdit()
        def_text.setPlainText(definition)
        def_text.setReadOnly(True)
        def_text.setStyleSheet("""
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
        """)

        # Кнопки
        button_layout = QHBoxLayout()

        favorite_btn = QPushButton("⭐ " + self.localization.tr('favorites', self.current_lang))
        favorite_btn.clicked.connect(lambda: self.add_to_favorites(term, definition, dialog))

        copy_btn = QPushButton("📋 " + self.localization.tr('copy', self.current_lang))
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(f"{term}: {definition}"))

        close_btn = QPushButton(self.localization.tr('close', self.current_lang))
        close_btn.clicked.connect(dialog.accept)

        button_layout.addWidget(favorite_btn)
        button_layout.addWidget(copy_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)

        layout.addWidget(title)
        layout.addWidget(def_text)
        layout.addLayout(button_layout)

        dialog.exec()

    def add_to_favorites(self, term, definition, dialog):
        """Добавление в избранное"""
        self.favorites.add((term, definition))
        QMessageBox.information(self,
                                self.localization.tr('success', self.current_lang),
                                f"Added '{term}' to favorites!")
        self.update_favorites_tab()
        dialog.accept()

    def update_favorites_tab(self):
        """Обновление вкладки избранного"""
        # Очищаем старые элементы
        for i in reversed(range(self.fav_layout.count())):
            widget = self.fav_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if not self.favorites:
            label = QLabel(self.localization.tr('no_results', self.current_lang))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("color: gray; font-size: 16px; padding: 50px;")
            self.fav_layout.addWidget(label)
            return

        for term, definition in self.favorites:
            frame = QFrame()
            frame.setFrameShape(QFrame.Shape.StyledPanel)
            frame.setStyleSheet("""
                QFrame {
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 5px;
                }
            """)

            layout = QHBoxLayout(frame)

            term_label = QLabel(f"<b>{term}</b><br>{definition[:100]}...")
            term_label.setWordWrap(True)

            remove_btn = QPushButton("❌")
            remove_btn.setFixedSize(30, 30)
            remove_btn.clicked.connect(lambda checked, t=term: self.remove_from_favorites(t))

            layout.addWidget(term_label)
            layout.addWidget(remove_btn)

            self.fav_layout.addWidget(frame)

        self.fav_layout.addStretch()

    def remove_from_favorites(self, term):
        """Удаление из избранного"""
        self.favorites = {item for item in self.favorites if item[0] != term}
        self.update_favorites_tab()
        QMessageBox.information(self,
                                self.localization.tr('info', self.current_lang),
                                f"Removed '{term}' from favorites")

    def show_stats(self):
        """Показать статистику"""
        if not self.connected:
            self.show_not_connected_warning()
            return

        response = self.send_request({'action': 'list'})

        if response and response.get('status') == 'success':
            dictionary = response.get('dictionary', {})

            # Расчет статистики
            total_terms = len(dictionary)
            favorites_count = len(self.favorites)

            avg_term_length = sum(len(t) for t in dictionary.keys()) / max(1, total_terms)
            avg_def_length = sum(len(d) for d in dictionary.values()) / max(1, total_terms)

            stats_text = f"""
            📊 {self.localization.tr('stats_title', self.current_lang)}

            {self.localization.tr('total_terms_stat', self.current_lang)}: {total_terms}
            {self.localization.tr('favorites_stat', self.current_lang)}: {favorites_count}

            {self.localization.tr('avg_term_length', self.current_lang)}: {avg_term_length:.1f} {self.localization.tr('chars', self.current_lang)}
            {self.localization.tr('avg_def_length', self.current_lang)}: {avg_def_length:.1f} {self.localization.tr('chars', self.current_lang)}

            {self.localization.tr('server_status', self.current_lang)}: {self.server_host}:{self.server_port}
            {self.localization.tr('connection', self.current_lang)}: {'🟢 ' + self.localization.tr('connected', self.current_lang) if self.connected else '🔴 ' + self.localization.tr('disconnected', self.current_lang)}
            """

            QMessageBox.information(self, self.localization.tr('stats_title', self.current_lang), stats_text.strip())

    def show_loading(self, message):
        """Показать индикатор загрузки"""
        self.status_label.setText(message)
        self.status_bar.repaint()
        QApplication.processEvents()

    def hide_loading(self):
        """Скрыть индикатор загрузки"""
        status_text = self.localization.tr('connected', self.current_lang) if self.connected else self.localization.tr(
            'disconnected', self.current_lang)
        self.status_label.setText(status_text)


# ========== ТОЧКА ВХОДА ==========
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Network Dictionary")
    app.setOrganizationName("Dictionary Corp")

    # Устанавливаем стиль Fusion
    app.setStyle("Fusion")

    window = ModernDictionaryApp()
    window.show()

    sys.exit(app.exec())