import tkinter as tk
from tkinter import messagebox, ttk, colorchooser
import random
import json
import os

GAME_SETTINGS = {
    'size': 3,
    'mode': 'PvP',
    'difficulty': 'Medium',
    'player1_symbol': 'X',
    'player2_symbol': 'O',
    'player1_color': '#e74c3c',
    'player2_color': '#3498db',
    'theme': 'dark',
    'ai_starts': False,
    'timer_enabled': True,
    'timer_seconds': 30
}

THEMES = {
    'dark': {
        'bg': '#2c3e50',
        'fg': '#ecf0f1',
        'accent': '#3498db',
        'secondary': '#34495e',
        'button_bg': '#3498db',
        'button_fg': 'white',
        'button_active': '#2980b9',
        'cell_bg': '#34495e',
        'cell_hover': '#3d566e',
        'text_primary': '#ecf0f1',
        'text_secondary': '#bdc3c7',
        'success': '#2ecc71',
        'danger': '#e74c3c',
        'warning': '#f39c12',
        'info': '#3498db'
    },
    'light': {
        'bg': '#f8f9fa',
        'fg': '#212529',
        'accent': '#007bff',
        'secondary': '#e9ecef',
        'button_bg': '#007bff',
        'button_fg': 'white',
        'button_active': '#0056b3',
        'cell_bg': '#ffffff',
        'cell_hover': '#e9ecef',
        'text_primary': '#212529',
        'text_secondary': '#6c757d',
        'success': '#28a745',
        'danger': '#dc3545',
        'warning': '#ffc107',
        'info': '#17a2b8'
    }
}


class MainMenu:
    """Главное меню игры"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Крестики-Нолики")
        self.root.geometry("600x500")
        self.apply_theme()
        self.root.resizable(True, True)
        self.root.minsize(500, 400)

        self.center_window(600, 500)
        self.setup_menu()

    def apply_theme(self):
        """Применение текущей темы"""
        theme = THEMES[GAME_SETTINGS['theme']]
        self.root.configure(bg=theme['bg'])

    def load_settings(self):
        """Загрузка настроек из файла"""
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding='utf-8') as f:
                    saved = json.load(f)
                    GAME_SETTINGS.update(saved)
        except Exception:
            pass

    def center_window(self, width, height):
        """Центрирование окна на экране"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_menu(self):
        """Настройка интерфейса главного меню"""
        theme = THEMES[GAME_SETTINGS['theme']]

        main_container = tk.Frame(self.root, bg=theme['bg'])
        main_container.pack(fill='both', expand=True)

        tk.Label(
            main_container,
            text="КРЕСТИКИ-НОЛИКИ",
            font=('Arial', 32, 'bold'),
            bg=theme['bg'],
            fg=theme['text_primary']
        ).pack(pady=(80, 30))

        button_frame = tk.Frame(main_container, bg=theme['bg'])
        button_frame.pack()

        buttons = [
            ("Начать игру", self.start_game),
            ("Настройки", self.open_settings),
            ("Правила игры", self.show_rules),
            ("Выход", self.exit_game)
        ]

        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=('Arial', 14, 'bold'),
                bg=theme['button_bg'],
                fg='white',
                activebackground=theme['button_active'],
                activeforeground='white',
                width=20,
                height=2,
                bd=0,
                cursor='hand2'
            )
            btn.pack(pady=8)

    def toggle_theme(self):
        """Переключение темы"""
        GAME_SETTINGS['theme'] = 'light' if GAME_SETTINGS['theme'] == 'dark' else 'dark'
        try:
            with open("settings.json", "w", encoding='utf-8') as f:
                json.dump(GAME_SETTINGS, f, indent=4)
        except Exception:
            pass

        self.root.destroy()
        menu = MainMenu()
        menu.root.mainloop()

    def start_game(self):
        """Запуск игры"""
        self.root.destroy()
        game = GameWindow()
        game.root.mainloop()

    def open_settings(self):
        """Открытие окна настроек"""
        SettingsWindow(self.root)

    def show_rules(self):
        """Показать правила игры"""
        theme = THEMES[GAME_SETTINGS['theme']]

        rules_window = tk.Toplevel(self.root)
        rules_window.title("Правила игры")
        rules_window.geometry("500x400")
        rules_window.configure(bg=theme['bg'])
        rules_window.resizable(False, False)

        x = self.root.winfo_x() + (self.root.winfo_width() - 500) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 400) // 2
        rules_window.geometry(f'500x400+{x}+{y}')

        text = tk.Text(
            rules_window,
            font=('Arial', 12),
            bg=theme['bg'],
            fg=theme['text_primary'],
            wrap='word',
            padx=20,
            pady=20
        )
        text.pack(fill='both', expand=True)

        rules_text = """
        ПРАВИЛА ИГРЫ "КРЕСТИКИ-НОЛИКИ"

        1. ЦЕЛЬ ИГРЫ:
           Первым выстроить в ряд (горизонтально, вертикально
           или по диагонали) свои символы.

        2. ХОД ИГРЫ:
           - Игроки ходят по очереди
           - На каждом ходе ставится один символ
           - Символ ставится в пустую клетку
           
        4. ПОБЕДА:
            - Побеждает игрок, первым собравший линию
            - Длина линии равна размеру поля

        5. НИЧЬЯ:
           - Если все клетки заполнены, и никто из игроков не собрал линию, то нет победителя
           
        6. РЕЖИМЫ ИГРЫ:
           - Игрок против Игрока
           - Игрок против Компьютера (3 уровня сложности)

        7. НАСТРОЙКИ:
           - Размер поля от 3x3 до 10x10
           - Выбор символов и цветов игроков
           - Темная/светлая тема
           - Таймер на ход

        8. ТАЙМЕР:
           - При включенном таймере у игрока ограниченное время на ход
           - Если время вышло, засчитывается победа противника
        """

        text.insert('1.0', rules_text)
        text.config(state='disabled')

        tk.Button(
            rules_window,
            text="Закрыть",
            command=rules_window.destroy,
            bg=theme['danger'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10
        ).pack(pady=10)

    def exit_game(self):
        """Выход из игры"""
        self.root.destroy()


class SettingsWindow:
    """Окно настроек игры"""

    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Настройки игры")
        self.apply_theme()
        self.window.resizable(True, True)
        self.window.minsize(650, 650)

        self.window.geometry("650x650")

        self.center_window()

        self.window.transient(parent)
        self.window.grab_set()

        self.load_settings()
        self.setup_ui()

        self.window.bind('<Configure>', self.on_window_configure)

    def apply_theme(self):
        """Применение текущей темы"""
        theme = THEMES[GAME_SETTINGS['theme']]
        self.window.configure(bg=theme['bg'])

    def load_settings(self):
        """Загрузка текущих настроек"""
        self.settings = GAME_SETTINGS.copy()

    def save_current_settings(self):
        """Сохранение текущих настроек в глобальный словарь"""
        for key, value in self.settings.items():
            GAME_SETTINGS[key] = value

    def center_window(self):
        """Центрирование окна относительно родительского"""
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        width, height = 650, 650
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2

        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Настройка интерфейса окна настроек"""
        theme = THEMES[GAME_SETTINGS['theme']]

        self.canvas = tk.Canvas(self.window, bg=theme['bg'], highlightthickness=0)

        self.scrollable_frame = tk.Frame(self.canvas, bg=theme['bg'])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        title_label = tk.Label(
            self.scrollable_frame,
            text="НАСТРОКИ ИГРЫ",
            font=('Arial', 22, 'bold'),
            bg=theme['bg'],
            fg=theme['text_primary']
        )
        title_label.pack(pady=(0, 20))

        settings_frame = tk.Frame(self.scrollable_frame, bg=theme['bg'])
        settings_frame.pack(fill='both', expand=True)

        self.size_frame = tk.LabelFrame(
            settings_frame,
            text=" Размер поля ",
            font=('Arial', 12, 'bold'),
            bg=theme['secondary'],
            fg=theme['text_primary'],
            padx=15,
            pady=10
        )
        self.size_frame.pack(fill='x', pady=(0, 15))

        self.size_var = tk.StringVar(value=str(self.settings['size']))

        size_inner_frame = tk.Frame(self.size_frame, bg=theme['secondary'])
        size_inner_frame.pack()

        tk.Label(
            size_inner_frame,
            text="Размер (3-10):",
            font=('Arial', 11),
            bg=theme['secondary'],
            fg=theme['text_primary']
        ).pack(side='left', padx=(0, 10))

        size_spinbox = tk.Spinbox(
            size_inner_frame,
            from_=3,
            to=10,
            textvariable=self.size_var,
            font=('Arial', 11),
            width=8,
            bg='white',
            fg='#2c3e50'
        )
        size_spinbox.pack(side='left')

        self.mode_frame = tk.LabelFrame(
            settings_frame,
            text=" Режим игры ",
            font=('Arial', 12, 'bold'),
            bg=theme['secondary'],
            fg=theme['text_primary'],
            padx=15,
            pady=10
        )
        self.mode_frame.pack(fill='x', pady=(0, 15))

        self.mode_var = tk.StringVar(value=self.settings['mode'])

        mode_inner_frame = tk.Frame(self.mode_frame, bg=theme['secondary'])
        mode_inner_frame.pack()

        modes = [("Игрок vs Игрок", "PvP"), ("Игрок vs Компьютер", "PvC")]
        for text, value in modes:
            tk.Radiobutton(
                mode_inner_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                font=('Arial', 11),
                bg=theme['secondary'],
                fg=theme['text_primary'],
                selectcolor=theme['info'],
                padx=10
            ).pack(side='left', padx=10)

        self.ai_frame = tk.LabelFrame(
            settings_frame,
            text=" Сложность ИИ ",
            font=('Arial', 12, 'bold'),
            bg=theme['secondary'],
            fg=theme['text_primary'],
            padx=15,
            pady=10
        )

        self.difficulty_var = tk.StringVar(value=self.settings['difficulty'])

        ai_inner_frame = tk.Frame(self.ai_frame, bg=theme['secondary'])
        ai_inner_frame.pack()

        difficulties = [("Легкий", "Easy"), ("Средний", "Medium"), ("Сложный", "Hard")]
        for text, value in difficulties:
            tk.Radiobutton(
                ai_inner_frame,
                text=text,
                variable=self.difficulty_var,
                value=value,
                font=('Arial', 11),
                bg=theme['secondary'],
                fg=theme['text_primary'],
                selectcolor=theme['info'],
                padx=10
            ).pack(side='left', padx=10)

        self.ai_starts_frame = tk.Frame(settings_frame, bg=theme['bg'])
        self.ai_starts_frame.pack(fill='x', pady=(0, 15))

        self.ai_starts_var = tk.BooleanVar(value=self.settings.get('ai_starts', False))

        self.ai_starts_check = tk.Checkbutton(
            self.ai_starts_frame,
            text="ИИ ходит первым (в режиме PvC)",
            variable=self.ai_starts_var,
            font=('Arial', 11),
            bg=theme['bg'],
            fg=theme['text_primary'],
            selectcolor=theme['info'],
            activebackground=theme['bg'],
            activeforeground=theme['text_primary']
        )
        self.ai_starts_check.pack(anchor='w')

        timer_frame = tk.LabelFrame(
            settings_frame,
            text=" Таймер ",
            font=('Arial', 12, 'bold'),
            bg=theme['secondary'],
            fg=theme['text_primary'],
            padx=15,
            pady=10
        )
        timer_frame.pack(fill='x', pady=(0, 15))

        self.timer_enabled_var = tk.BooleanVar(
            value=self.settings.get('timer_enabled', True)
        )
        self.timer_seconds_var = tk.StringVar(
            value=str(self.settings.get('timer_seconds', 30))
        )

        timer_check = tk.Checkbutton(
            timer_frame,
            text="Включить таймер на ход",
            variable=self.timer_enabled_var,
            font=('Arial', 11),
            bg=theme['secondary'],
            fg=theme['text_primary'],
            selectcolor=theme['info'],
            activebackground=theme['secondary'],
            activeforeground=theme['text_primary'],
            command=self.toggle_timer_settings
        )
        timer_check.pack(anchor='w', pady=(0, 10))

        self.timer_settings_frame = tk.Frame(timer_frame, bg=theme['secondary'])
        self.timer_settings_frame.pack(fill='x', pady=5)

        tk.Label(
            self.timer_settings_frame,
            text="Секунд на ход:",
            font=('Arial', 11),
            bg=theme['secondary'],
            fg=theme['text_primary']
        ).pack(side='left', padx=(0, 10))

        self.timer_spinbox = tk.Spinbox(
            self.timer_settings_frame,
            from_=5,
            to=300,
            textvariable=self.timer_seconds_var,
            font=('Arial', 11),
            width=8,
            bg='white',
            fg='#2c3e50',
            state='normal' if self.timer_enabled_var.get() else 'disabled'
        )
        self.timer_spinbox.pack(side='left')

        self.players_frame = tk.LabelFrame(
            settings_frame,
            text=" Настройки игроков ",
            font=('Arial', 12, 'bold'),
            bg=theme['secondary'],
            fg=theme['text_primary'],
            padx=15,
            pady=10
        )
        self.players_frame.pack(fill='x', pady=(0, 15))

        players_grid = tk.Frame(self.players_frame, bg=theme['secondary'])
        players_grid.pack()

        headers = ["", "Символ", "Цвет"]
        for col, header in enumerate(headers):
            tk.Label(
                players_grid,
                text=header,
                font=('Arial', 11, 'bold'),
                bg=theme['secondary'],
                fg=theme['text_primary'],
                padx=10
            ).grid(row=0, column=col, pady=5)

        tk.Label(
            players_grid,
            text="Игрок 1:",
            font=('Arial', 11, 'bold'),
            bg=theme['secondary'],
            fg=theme['text_primary'],
            padx=10
        ).grid(row=1, column=0, sticky='w', pady=5)

        self.player1_symbol_var = tk.StringVar(value=self.settings['player1_symbol'])

        def validate_symbol1(new_text):
            if len(new_text) <= 3:
                return True
            return False

        vcmd1 = (self.window.register(validate_symbol1), '%P')
        player1_symbol_entry = tk.Entry(
            players_grid,
            textvariable=self.player1_symbol_var,
            font=('Arial', 11),
            width=5,
            bg='white',
            fg=self.settings['player1_color'],
            justify='center',
            validate='key',
            validatecommand=vcmd1
        )
        player1_symbol_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        self.player1_color_var = tk.StringVar(value=self.settings['player1_color'])

        color_frame1 = tk.Frame(players_grid, bg=theme['secondary'])
        color_frame1.grid(row=1, column=2, padx=10, pady=5, sticky='w')

        self.color_preview1 = tk.Label(
            color_frame1,
            text="   ",
            font=('Arial', 1),
            bg=self.settings['player1_color'],
            width=3,
            height=1,
            relief='sunken',
            bd=1
        )
        self.color_preview1.pack(side='left', padx=(0, 5))

        color_btn1 = tk.Button(
            color_frame1,
            text="Выбрать",
            command=lambda: self.choose_color('player1'),
            font=('Arial', 10),
            bg=theme['accent'],
            fg='white',
            padx=10,
            pady=2
        )
        color_btn1.pack(side='left')

        tk.Label(
            players_grid,
            text="Игрок 2:",
            font=('Arial', 11, 'bold'),
            bg=theme['secondary'],
            fg=theme['text_primary'],
            padx=10
        ).grid(row=2, column=0, sticky='w', pady=5)

        self.player2_symbol_var = tk.StringVar(value=self.settings['player2_symbol'])

        def validate_symbol2(new_text):
            if len(new_text) <= 3:
                return True
            return False

        vcmd2 = (self.window.register(validate_symbol2), '%P')
        player2_symbol_entry = tk.Entry(
            players_grid,
            textvariable=self.player2_symbol_var,
            font=('Arial', 11),
            width=5,
            bg='white',
            fg=self.settings['player2_color'],
            justify='center',
            validate='key',
            validatecommand=vcmd2
        )
        player2_symbol_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        self.player2_color_var = tk.StringVar(value=self.settings['player2_color'])

        color_frame2 = tk.Frame(players_grid, bg=theme['secondary'])
        color_frame2.grid(row=2, column=2, padx=10, pady=5, sticky='w')

        self.color_preview2 = tk.Label(
            color_frame2,
            text="   ",
            font=('Arial', 1),
            bg=self.settings['player2_color'],
            width=3,
            height=1,
            relief='sunken',
            bd=1
        )
        self.color_preview2.pack(side='left', padx=(0, 5))

        color_btn2 = tk.Button(
            color_frame2,
            text="Выбрать",
            command=lambda: self.choose_color('player2'),
            font=('Arial', 10),
            bg=theme['accent'],
            fg='white',
            padx=10,
            pady=2
        )
        color_btn2.pack(side='left')

        theme_frame = tk.LabelFrame(
            settings_frame,
            text=" Тема ",
            font=('Arial', 12, 'bold'),
            bg=theme['secondary'],
            fg=theme['text_primary'],
            padx=15,
            pady=10
        )
        theme_frame.pack(fill='x', pady=(0, 15))

        self.theme_var = tk.StringVar(value=self.settings['theme'])

        theme_inner_frame = tk.Frame(theme_frame, bg=theme['secondary'])
        theme_inner_frame.pack()

        themes = [("Темная", "dark"), ("Светлая", "light")]
        for text, value in themes:
            tk.Radiobutton(
                theme_inner_frame,
                text=text,
                variable=self.theme_var,
                value=value,
                font=('Arial', 11),
                bg=theme['secondary'],
                fg=theme['text_primary'],
                selectcolor=theme['info'],
                padx=10
            ).pack(side='left', padx=10)

        buttons_frame = tk.Frame(self.scrollable_frame, bg=theme['bg'])
        buttons_frame.pack(side='bottom', fill='x', pady=(20, 0))

        button_container = tk.Frame(buttons_frame, bg=theme['bg'])
        button_container.pack()

        default_btn = tk.Button(
            button_container,
            text="По умолчанию",
            command=self.reset_to_default,
            font=('Arial', 12, 'bold'),
            bg=theme['warning'],
            fg='white',
            padx=25,
            pady=8,
            cursor='hand2',
            height=1
        )
        default_btn.pack(side='left', padx=5)

        cancel_btn = tk.Button(
            button_container,
            text="Отмена",
            command=self.window.destroy,
            font=('Arial', 12, 'bold'),
            bg=theme['danger'],
            fg='white',
            padx=25,
            pady=8,
            cursor='hand2',
            height=1
        )
        cancel_btn.pack(side='left', padx=10)

        save_btn = tk.Button(
            button_container,
            text="Сохранить",
            command=self.save_settings,
            font=('Arial', 12, 'bold'),
            bg=theme['success'],
            fg='white',
            padx=25,
            pady=8,
            cursor='hand2',
            width=12,
            height=1
        )
        save_btn.pack(side='left', padx=5)

        self.mode_var.trace('w', self.on_mode_change)
        self.on_mode_change()

    def _on_mousewheel(self, event):
        """Обработка прокрутки колесика мыши"""
        try:
            if self.canvas.winfo_exists():
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass

    def on_window_configure(self, event):
        """Обработка изменения размера окна"""
        if event.widget == self.window:
            try:
                if self.canvas.winfo_exists():
                    self.canvas.itemconfig(1, width=event.width - 40)
            except Exception:
                pass

    def toggle_timer_settings(self):
        """Переключение доступности настроек таймера"""
        state = 'normal' if self.timer_enabled_var.get() else 'disabled'
        self.timer_spinbox.config(state=state)

    def choose_color(self, player):
        """Выбор цвета для игрока"""
        current_color = (
            self.player1_color_var.get()
            if player == 'player1'
            else self.player2_color_var.get()
        )

        color = colorchooser.askcolor(
            initialcolor=current_color,
            title=f"Выберите цвет для {player}"
        )

        if color[1]:
            hex_color = color[1]
            if player == 'player1':
                self.player1_color_var.set(hex_color)
                self.color_preview1.config(bg=hex_color)
            else:
                self.player2_color_var.set(hex_color)
                self.color_preview2.config(bg=hex_color)

    def on_mode_change(self, *args):
        """Обработка изменения режима игры"""
        if self.mode_var.get() == 'PvP':
            self.ai_frame.pack_forget()
            self.ai_starts_frame.pack_forget()
        else:
            self.ai_frame.pack(fill='x', pady=(0, 15))
            self.ai_starts_frame.pack(fill='x', pady=(0, 15))

    def reset_to_default(self):
        """Сброс настроек к значениям по умолчанию"""
        default_settings = {
            'size': 3,
            'mode': 'PvP',
            'difficulty': 'Medium',
            'player1_symbol': 'X',
            'player2_symbol': 'O',
            'player1_color': '#e74c3c',
            'player2_color': '#3498db',
            'theme': 'dark',
            'ai_starts': False,
            'timer_enabled': True,
            'timer_seconds': 30
        }

        self.size_var.set(str(default_settings['size']))
        self.mode_var.set(default_settings['mode'])
        self.difficulty_var.set(default_settings['difficulty'])
        self.player1_symbol_var.set(default_settings['player1_symbol'])
        self.player2_symbol_var.set(default_settings['player2_symbol'])
        self.player1_color_var.set(default_settings['player1_color'])
        self.player2_color_var.set(default_settings['player2_color'])
        self.theme_var.set(default_settings['theme'])
        self.ai_starts_var.set(default_settings['ai_starts'])
        self.timer_enabled_var.set(default_settings['timer_enabled'])
        self.timer_seconds_var.set(str(default_settings['timer_seconds']))

        self.color_preview1.config(bg=default_settings['player1_color'])
        self.color_preview2.config(bg=default_settings['player2_color'])

        messagebox.showinfo("Сброс", "Настройки сброшены к значениям по умолчанию!")

    def collect_settings(self):
        """Сбор всех настроек из интерфейса"""
        player1_symbol = self.player1_symbol_var.get().strip()[:3]
        player2_symbol = self.player2_symbol_var.get().strip()[:3]

        if not player1_symbol or not player2_symbol:
            raise ValueError("Символы игроков не могут быть пустыми!")

        if player1_symbol == player2_symbol:
            raise ValueError("Символы игроков должны быть разными!")

        size = int(self.size_var.get())
        if size < 3 or size > 10:
            raise ValueError("Размер поля должен быть от 3 до 10!")

        timer_seconds = int(self.timer_seconds_var.get())
        if timer_seconds < 5 or timer_seconds > 300:
            raise ValueError("Таймер должен быть от 5 до 300 секунд!")

        self.settings = {
            'size': size,
            'mode': self.mode_var.get(),
            'difficulty': self.difficulty_var.get(),
            'player1_symbol': player1_symbol,
            'player2_symbol': player2_symbol,
            'player1_color': self.player1_color_var.get(),
            'player2_color': self.player2_color_var.get(),
            'theme': self.theme_var.get(),
            'ai_starts': (
                self.ai_starts_var.get()
                if self.mode_var.get() == 'PvC'
                else False
            ),
            'timer_enabled': self.timer_enabled_var.get(),
            'timer_seconds': timer_seconds
        }

    def save_settings(self):
        """Сохранение настроек"""
        try:
            self.collect_settings()

            self.save_current_settings()

            with open("settings.json", "w", encoding='utf-8') as f:
                json.dump(GAME_SETTINGS, f, indent=4)

            messagebox.showinfo("Успех", "Настройки успешно сохранены!")

            try:
                self.canvas.unbind_all("<MouseWheel>")
            except Exception:
                pass

            self.window.destroy()

            self.parent.destroy()
            menu = MainMenu()
            menu.root.mainloop()

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")


class GameWindow:
    """Окно игры"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Крестики-Нолики")
        self.root.geometry("850x650")
        self.apply_theme()
        self.root.resizable(True, True)
        self.root.minsize(650, 550)

        self.load_settings()

        self.timer_seconds = GAME_SETTINGS['timer_seconds']
        self.timer_running = False
        self.timer_id = None

        self.scores = {
            GAME_SETTINGS['player1_symbol']: 0,
            GAME_SETTINGS['player2_symbol']: 0,
            'Ничья': 0
        }
        self.players = [
            GAME_SETTINGS['player1_symbol'],
            GAME_SETTINGS['player2_symbol']
        ]

        if GAME_SETTINGS['mode'] == 'PvC' and GAME_SETTINGS['ai_starts']:
            self.current_player = 1
        else:
            self.current_player = 0

        self.game_active = True
        self.board = []
        self.buttons = []
        self.timeout_player = None

        self.center_window(850, 650)
        self.setup_ui()
        self.create_board()

        if (
            GAME_SETTINGS['mode'] == 'PvC'
            and GAME_SETTINGS['ai_starts']
            and self.current_player == 1
        ):
            self.root.after(1000, self.computer_move)

        if GAME_SETTINGS['timer_enabled']:
            self.start_timer()

    def apply_theme(self):
        """Применение текущей темы"""
        theme = THEMES[GAME_SETTINGS['theme']]
        self.colors = theme
        self.root.configure(bg=theme['bg'])

    def load_settings(self):
        """Загрузка настроек из глобального словаря"""
        try:
            self.board_size = GAME_SETTINGS['size']
            self.game_mode = GAME_SETTINGS['mode']
            self.ai_difficulty = GAME_SETTINGS['difficulty']
            self.player1_color = GAME_SETTINGS['player1_color']
            self.player2_color = GAME_SETTINGS['player2_color']
            self.timer_enabled = GAME_SETTINGS['timer_enabled']
            self.timer_seconds = GAME_SETTINGS['timer_seconds']
        except Exception:
            self.board_size = 3
            self.game_mode = 'PvP'
            self.ai_difficulty = 'Medium'
            self.player1_color = '#e74c3c'
            self.player2_color = '#3498db'
            self.timer_enabled = True
            self.timer_seconds = 30

    def center_window(self, width, height):
        """Центрирование окна на экране"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Настройка интерфейса игры"""
        theme = self.colors

        self.main_frame = tk.Frame(self.root, bg=theme['bg'])
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        top_frame = tk.Frame(self.main_frame, bg=theme['bg'])
        top_frame.pack(fill='x', pady=(0, 10))

        tk.Button(
            top_frame,
            text="Меню",
            command=self.back_to_menu,
            bg=theme['secondary'],
            fg=theme['text_primary'],
            font=('Arial', 12, 'bold'),
            padx=15,
            pady=5
        ).pack(side='left')

        current_symbol = self.players[self.current_player]
        self.status_label = tk.Label(
            top_frame,
            text=f"Ходит: {current_symbol}",
            font=('Arial', 14),
            bg=theme['bg'],
            fg=self.player1_color if current_symbol == self.players[0] else self.player2_color
        )
        self.status_label.pack(side='left', padx=20, fill='x', expand=True)

        if self.timer_enabled:
            self.timer_label = tk.Label(
                top_frame,
                text=f"Таймер: {self.timer_seconds}с",
                font=('Arial', 14, 'bold'),
                bg=theme['warning'],
                fg='white',
                padx=15,
                pady=5
            )
            self.timer_label.pack(side='left', padx=20)

        self.score_label = tk.Label(
            top_frame,
            text=(
                f"Счет: {GAME_SETTINGS['player1_symbol']} - "
                f"{self.scores[GAME_SETTINGS['player1_symbol']]} | "
                f"{GAME_SETTINGS['player2_symbol']} - "
                f"{self.scores[GAME_SETTINGS['player2_symbol']]} | "
                f"Ничьи - {self.scores['Ничья']}"
            ),
            font=('Arial', 14, 'bold'),
            bg=theme['bg'],
            fg=theme['text_primary']
        )
        self.score_label.pack(side='left', padx=20)

        tk.Button(
            top_frame,
            text="Новая игра",
            command=self.new_game,
            bg=theme['accent'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=15,
            pady=5
        ).pack(side='right')

        self.center_frame = tk.Frame(self.main_frame, bg=theme['bg'])
        self.center_frame.pack(fill='both', expand=True)

        self.board_container = tk.Frame(self.center_frame, bg=theme['bg'])
        self.board_container.pack(expand=True, fill='both')

    def start_timer(self):
        """Запуск таймера"""
        if not self.timer_enabled or not self.game_active:
            return

        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        """Остановка таймера"""
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def reset_timer(self):
        """Сброс таймера"""
        self.stop_timer()
        self.timer_seconds = GAME_SETTINGS['timer_seconds']
        if self.timer_enabled:
            self.timer_label.config(
                text=f"Таймер: {self.timer_seconds}с",
                bg=self.colors['warning'],
                fg='white'
            )
            self.start_timer()

    def update_timer(self):
        """Обновление таймера"""
        if not self.timer_running or not self.game_active:
            return

        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            if self.timer_seconds <= 10:
                self.timer_label.config(fg='red', bg='#ffcccc')
            elif self.timer_seconds <= 30:
                self.timer_label.config(fg='orange', bg='#fff0cc')
            else:
                self.timer_label.config(fg='white', bg=self.colors['warning'])

            self.timer_label.config(text=f"Таймер: {self.timer_seconds}с")
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Таймер: 0с", fg='red', bg='#ffcccc')
            self.timeout_player = self.players[self.current_player]
            self.handle_timeout()

    def handle_timeout(self):
        """Обработка истечения времени"""
        if not self.game_active:
            return

        self.game_active = False

        if self.game_mode == 'PvC':
            if self.players[self.current_player] == GAME_SETTINGS['player2_symbol']:
                winner = GAME_SETTINGS['player1_symbol']
            else:
                winner = GAME_SETTINGS['player2_symbol']
        else:
            if self.players[self.current_player] == GAME_SETTINGS['player1_symbol']:
                winner = GAME_SETTINGS['player2_symbol']
            else:
                winner = GAME_SETTINGS['player1_symbol']

        self.scores[winner] += 1
        self.update_score()
        messagebox.showinfo(
            "Время вышло!",
            f"Время на ход вышло! {winner} побеждает!"
        )

    def create_board(self):
        """Создание игрового поля"""
        for widget in self.board_container.winfo_children():
            widget.destroy()

        board_frame = tk.Frame(self.board_container, bg=self.colors['bg'])
        board_frame.pack(expand=True)

        self.buttons = []
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]

        if self.board_size <= 4:
            font_size = 40
            btn_width = 8
            btn_height = 4
        elif self.board_size <= 6:
            font_size = 32
            btn_width = 6
            btn_height = 3
        else:
            font_size = 24
            btn_width = 4
            btn_height = 2

        for i in range(self.board_size):
            row_buttons = []
            for j in range(self.board_size):
                btn = tk.Button(
                    board_frame,
                    text='',
                    font=('Arial', font_size, 'bold'),
                    width=btn_width,
                    height=btn_height,
                    bg=self.colors['cell_bg'],
                    fg=self.colors['text_primary'],
                    activebackground=self.colors['cell_hover'],
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                btn.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')

                board_frame.grid_rowconfigure(i, weight=1, uniform='row')
                board_frame.grid_columnconfigure(j, weight=1, uniform='col')

                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def make_move(self, row, col):
        """Совершение хода"""
        if not self.game_active or self.board[row][col] != '':
            return

        player = self.players[self.current_player]
        self.board[row][col] = player

        symbol_length = len(player)
        if self.board_size <= 4:
            base_size = 40
        elif self.board_size <= 6:
            base_size = 32
        else:
            base_size = 24

        if symbol_length == 2:
            font_size = int(base_size * 0.8)
        elif symbol_length == 3:
            font_size = int(base_size * 0.6)
        else:
            font_size = base_size

        color = self.player1_color if player == self.players[0] else self.player2_color
        self.buttons[row][col].config(
            text=player,
            font=('Arial', font_size, 'bold'),
            fg=color,
            disabledforeground=color,
            state='disabled'
        )

        if self.timer_enabled:
            self.reset_timer()

        if self.check_winner(player):
            self.stop_timer()
            self.game_active = False
            self.scores[player] += 1
            self.update_score()
            self.highlight_winner()
            messagebox.showinfo("Победа!", f"Игрок {player} победил!")
            return

        if self.check_draw():
            self.stop_timer()
            self.game_active = False
            self.scores['Ничья'] += 1
            self.update_score()
            messagebox.showinfo("Ничья!", "Игра закончилась вничью!")
            return

        self.current_player = 1 - self.current_player
        self.update_status()

        if (
            self.game_mode == "PvC"
            and self.players[self.current_player] == GAME_SETTINGS['player2_symbol']
        ):
            self.root.after(500, self.computer_move)

    def update_status(self):
        """Обновление статуса игры"""
        current_symbol = self.players[self.current_player]
        color = (
            self.player1_color
            if current_symbol == self.players[0]
            else self.player2_color
        )
        self.status_label.config(
            text=f"Ходит: {current_symbol}",
            fg=color
        )

    def computer_move(self):
        """Ход компьютера"""
        if not self.game_active:
            return

        empty = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == '':
                    empty.append((i, j))

        if not empty:
            return

        if self.ai_difficulty == "Easy":
            row, col = random.choice(empty)
        elif self.ai_difficulty == "Medium":
            row, col = self.get_medium_move(empty)
        else:
            row, col = self.get_hard_move(empty)

        self.make_move(row, col)

    def get_medium_move(self, empty_cells):
        """Получение хода для среднего уровня сложности"""
        for row, col in empty_cells:
            self.board[row][col] = GAME_SETTINGS['player2_symbol']
            if self.check_winner(GAME_SETTINGS['player2_symbol']):
                self.board[row][col] = ''
                return row, col
            self.board[row][col] = ''

        for row, col in empty_cells:
            self.board[row][col] = GAME_SETTINGS['player1_symbol']
            if self.check_winner(GAME_SETTINGS['player1_symbol']):
                self.board[row][col] = ''
                return row, col
            self.board[row][col] = ''

        center = self.board_size // 2
        if self.board[center][center] == '':
            return center, center

        corners = [
            (0, 0),
            (0, self.board_size - 1),
            (self.board_size - 1, 0),
            (self.board_size - 1, self.board_size - 1)
        ]
        for row, col in corners:
            if self.board[row][col] == '':
                return row, col

        return random.choice(empty_cells)

    def get_hard_move(self, empty_cells):
        """Получение хода для сложного уровня"""
        for row, col in empty_cells:
            self.board[row][col] = GAME_SETTINGS['player2_symbol']
            if self.check_winner(GAME_SETTINGS['player2_symbol']):
                self.board[row][col] = ''
                return row, col
            self.board[row][col] = ''

        for row, col in empty_cells:
            self.board[row][col] = GAME_SETTINGS['player1_symbol']
            if self.check_winner(GAME_SETTINGS['player1_symbol']):
                self.board[row][col] = ''
                return row, col
            self.board[row][col] = ''

        center = self.board_size // 2
        if self.board[center][center] == '':
            return center, center

        corners = [
            (0, 0),
            (0, self.board_size - 1),
            (self.board_size - 1, 0),
            (self.board_size - 1, self.board_size - 1)
        ]
        for row, col in corners:
            if self.board[row][col] == '':
                return row, col

        return random.choice(empty_cells)

    def check_winner(self, player):
        """Проверка победы"""
        for i in range(self.board_size):
            if all(self.board[i][j] == player for j in range(self.board_size)):
                self.win_cells = [(i, j) for j in range(self.board_size)]
                return True

        for j in range(self.board_size):
            if all(self.board[i][j] == player for i in range(self.board_size)):
                self.win_cells = [(i, j) for i in range(self.board_size)]
                return True

        if all(self.board[i][i] == player for i in range(self.board_size)):
            self.win_cells = [(i, i) for i in range(self.board_size)]
            return True

        if all(
            self.board[i][self.board_size - 1 - i] == player
            for i in range(self.board_size)
        ):
            self.win_cells = [(i, self.board_size - 1 - i) for i in range(self.board_size)]
            return True

        return False

    def check_draw(self):
        """Проверка ничьей"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == '':
                    return False
        return True

    def highlight_winner(self):
        """Выделение победной комбинации"""
        for row, col in self.win_cells:
            self.buttons[row][col].config(bg=self.colors['success'])

    def update_score(self):
        """Обновление счета"""
        self.score_label.config(
            text=(
                f"Счет: {GAME_SETTINGS['player1_symbol']} - "
                f"{self.scores[GAME_SETTINGS['player1_symbol']]} | "
                f"{GAME_SETTINGS['player2_symbol']} - "
                f"{self.scores[GAME_SETTINGS['player2_symbol']]} | "
                f"Ничьи - {self.scores['Ничья']}"
            )
        )

    def new_game(self):
        """Начать новую игру"""
        self.stop_timer()
        self.game_active = True
        self.timeout_player = None

        if GAME_SETTINGS['mode'] == 'PvC' and GAME_SETTINGS['ai_starts']:
            self.current_player = 1
        else:
            self.current_player = 0

        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]

        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].config(
                    text='',
                    bg=self.colors['cell_bg'],
                    fg=self.colors['text_primary'],
                    state='normal'
                )

        self.update_status()

        if self.timer_enabled:
            self.reset_timer()

        if (
            GAME_SETTINGS['mode'] == 'PvC'
            and GAME_SETTINGS['ai_starts']
            and self.current_player == 1
        ):
            self.root.after(1000, self.computer_move)

    def back_to_menu(self):
        """Возврат в главное меню"""
        self.stop_timer()
        self.root.destroy()
        menu = MainMenu()
        menu.root.mainloop()


def main():
    """Главная функция приложения"""
    try:
        menu = MainMenu()
        menu.root.mainloop()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")


if __name__ == "__main__":
    main()
