import tkinter as tk
from tkinter import messagebox
import random


class MainMenu:
    """Главное меню приложения"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Крестики-Нолики")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)
        self.root.minsize(500, 400)

        self.center_window(600, 500)
        self.setup_menu()

    def center_window(self, width, height):
        """Центрирование окна на экране ПК"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_menu(self):
        """Создание главного меню"""
        tk.Label(
            self.root,
            text="КРЕСТИКИ-НОЛИКИ",
            font=('Arial', 28, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(pady=(80, 20))

        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack()

        button_style = {
            'font': ('Arial', 16, 'bold'),
            'bg': '#3498db',
            'fg': 'white',
            'activebackground': '#2980b9',
            'activeforeground': 'white',
            'width': 30,
            'height': 2,
            'bd': 0,
            'cursor': 'hand2'
        }

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
                **button_style
            )
            btn.pack(pady=8)

    def start_game(self):
        """Запуск игры"""
        self.root.destroy()
        game = GameWindow()
        game.root.mainloop()

    def open_settings(self):
        """Открыть окно настроек"""
        SettingsWindow(self.root)

    def show_rules(self):
        """Показать правила игры"""
        rules = """
        ПРАВИЛА ИГРЫ "КРЕСТИКИ-НОЛИКИ"

        1. ЦЕЛЬ ИГРЫ:
           Первым выстроить в ряд (горизонтально, вертикально 
           или по диагонали) свои символы (X или O).

        2. ХОД ИГРЫ:
           - Игроки ходят по очереди
           - На каждом ходе ставится один символ
           - Символ ставится в пустую клетку

        3. ПОБЕДА:
           - Побеждает игрок, первым собравший линию
           - Длина линии равна размеру поля

        4. НИЧЬЯ:
           - Если все клетки заполнены, и никто из игроков не собрал линию, то нет победителя

        """
        messagebox.showinfo("Правила игры", rules)

    def exit_game(self):
        """Выход из игры"""
        self.root.destroy()


class SettingsWindow:
    """Окно настроек"""

    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Настройки")
        self.window.configure(bg='#ecf0f1')
        self.window.resizable(True, True)

        self.update_min_size()

        self.center_window(550, 500)

        self.window.transient(parent)
        self.window.grab_set()

        self.setup_ui()

    def update_min_size(self):
        """Обновляем минимальный размер окна в зависимости от видимых элементов"""
        if self.mode_var.get() == 'PvP' if hasattr(self, 'mode_var') else GAME_SETTINGS['mode'] == 'PvP':
            self.window.minsize(500, 420)
        else:
            self.window.minsize(500, 500)

    def center_window(self, width, height):
        """Центрирование окна настроек"""
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2

        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Создание интерфейса настроек"""
        self.title_label = tk.Label(
            self.window,
            text="Настройки игры",
            font=('Arial', 20, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        self.title_label.pack(pady=20)

        self.settings_container = tk.Frame(self.window, bg='#ecf0f1')
        self.settings_container.pack(fill='both', expand=True, padx=20, pady=10)

        self.size_frame = tk.Frame(self.settings_container, bg='#ecf0f1')
        self.size_frame.pack(pady=15)

        tk.Label(
            self.size_frame,
            text="Размер поля:",
            font=('Arial', 14, 'bold'),
            bg='#ecf0f1',
            fg='#34495e'
        ).pack()

        self.size_var = tk.StringVar(value=str(GAME_SETTINGS['size']))

        self.sizes_frame = tk.Frame(self.size_frame, bg='#ecf0f1')
        self.sizes_frame.pack(pady=10)

        sizes = [("3x3", "3"), ("4x4", "4"), ("5x5", "5")]
        for text, value in sizes:
            tk.Radiobutton(
                self.sizes_frame,
                text=text,
                variable=self.size_var,
                value=value,
                font=('Arial', 12),
                bg='#ecf0f1',
                fg='#34495e',
                selectcolor='#3498db'
            ).pack(side='left', padx=15)

        self.mode_frame = tk.Frame(self.settings_container, bg='#ecf0f1')
        self.mode_frame.pack(pady=15)

        tk.Label(
            self.mode_frame,
            text="Режим игры:",
            font=('Arial', 14, 'bold'),
            bg='#ecf0f1',
            fg='#34495e'
        ).pack()

        self.mode_var = tk.StringVar(value=GAME_SETTINGS['mode'])

        self.modes_frame = tk.Frame(self.mode_frame, bg='#ecf0f1')
        self.modes_frame.pack(pady=10)

        modes = [("Игрок vs Игрок", "PvP"), ("Игрок vs Компьютер", "PvC")]
        for text, value in modes:
            tk.Radiobutton(
                self.modes_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                font=('Arial', 12),
                bg='#ecf0f1',
                fg='#34495e',
                selectcolor='#3498db'
            ).pack(side='left', padx=15)

        self.ai_frame = tk.Frame(self.settings_container, bg='#ecf0f1')
        self.ai_frame.pack(pady=15)

        self.ai_label = tk.Label(
            self.ai_frame,
            text="Сложность компьютера:",
            font=('Arial', 14, 'bold'),
            bg='#ecf0f1',
            fg='#34495e'
        )
        self.ai_label.pack()

        self.difficulty_var = tk.StringVar(value=GAME_SETTINGS['difficulty'])

        self.difficulties_frame = tk.Frame(self.ai_frame, bg='#ecf0f1')
        self.difficulties_frame.pack(pady=10)

        difficulties = [("Легкий", "Easy"), ("Средний", "Medium"), ("Сложный", "Hard")]
        for text, value in difficulties:
            tk.Radiobutton(
                self.difficulties_frame,
                text=text,
                variable=self.difficulty_var,
                value=value,
                font=('Arial', 12),
                bg='#ecf0f1',
                fg='#34495e',
                selectcolor='#3498db'
            ).pack(side='left', padx=15)

        self.mode_var.trace('w', self.on_mode_change)
        self.on_mode_change()

        self.button_frame = tk.Frame(self.window, bg='#ecf0f1')
        self.button_frame.pack(side='bottom', pady=20)

        tk.Button(
            self.button_frame,
            text="Сохранить",
            command=self.save_settings,
            font=('Arial', 12, 'bold'),
            bg='#2ecc71',
            fg='white',
            padx=25,
            pady=8
        ).pack(side='left', padx=10)

        tk.Button(
            self.button_frame,
            text="Отмена",
            command=self.window.destroy,
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=25,
            pady=8
        ).pack(side='left', padx=10)

    def on_mode_change(self, *args):
        """Обработка изменения режима игры"""
        if self.mode_var.get() == 'PvP':
            self.ai_frame.pack_forget()
        else:
            self.ai_frame.pack(pady=15)

        self.update_min_size()

        self.window.update_idletasks()
        current_height = self.window.winfo_height()
        min_height = 510

        if current_height < min_height:
            current_width = self.window.winfo_width()
            current_x = self.window.winfo_x()
            current_y = self.window.winfo_y()

            self.window.geometry(f"{current_width}x{min_height}+{current_x}+{current_y}")

    def save_settings(self):
        """Сохранение настроек"""
        try:
            size = int(self.size_var.get())
            GAME_SETTINGS['size'] = size
            GAME_SETTINGS['mode'] = self.mode_var.get()
            GAME_SETTINGS['difficulty'] = self.difficulty_var.get()

            self.window.destroy()

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
        self.root.resizable(True, True)
        self.root.minsize(650, 550)

        self.load_settings()

        self.colors = {
            'bg': '#2c3e50',
            'fg': '#ecf0f1',
            'accent': '#3498db',
            'success': '#2ecc71',
            'danger': '#e74c3c',
            'cell_bg': '#34495e',
            'cell_hover': '#3d566e',
            'text': 'white'
        }

        self.scores = {'X': 0, 'O': 0, 'Draw': 0}
        self.players = ['X', 'O']
        self.current_player = 0
        self.game_active = True
        self.board = []
        self.buttons = []

        self.center_window(850, 650)
        self.setup_ui()
        self.create_board()

    def load_settings(self):
        """Загрузка настроек"""
        global GAME_SETTINGS
        try:
            self.board_size = GAME_SETTINGS['size']
            self.game_mode = GAME_SETTINGS['mode']
            self.ai_difficulty = GAME_SETTINGS['difficulty']
        except Exception:
            self.board_size = 3
            self.game_mode = 'PvP'
            self.ai_difficulty = 'Medium'

    def center_window(self, width, height):
        """Центрирование окна игры"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Создание интерфейса игры """
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        top_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        top_frame.pack(fill='x', pady=(0, 10))

        tk.Button(
            top_frame,
            text="Меню",
            command=self.back_to_menu,
            bg='#95a5a6',
            fg=self.colors['text'],
            font=('Arial', 12, 'bold'),
            padx=15,
            pady=5
        ).pack(side='left')

        center_top = tk.Frame(top_frame, bg=self.colors['bg'])
        center_top.pack(side='left', fill='x', expand=True, padx=20)

        self.score_label = tk.Label(
            center_top,
            text=f"Счет: X - {self.scores['X']} | O - {self.scores['O']} | Ничьи - {self.scores['Draw']}",
            font=('Arial', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.score_label.pack()

        self.status_label = tk.Label(
            center_top,
            text="Ходит: X",
            font=('Arial', 16, 'bold'),
            bg=self.colors['bg'],
            fg='#e74c3c'
        )
        self.status_label.pack()

        if self.game_mode == 'PvP':
            mode_text = f"Режим: Игрок vs Игрок | Размер поля: {self.board_size}x{self.board_size}"
        else:
            difficulty_names = {
                'Easy': 'Легкий',
                'Medium': 'Средний',
                'Hard': 'Сложный'
            }
            difficulty_name = difficulty_names.get(self.ai_difficulty, self.ai_difficulty)
            mode_text = f"Режим: Игрок vs Компьютер | Размер: {self.board_size}x{self.board_size} | Сложность: {difficulty_name}"

        self.mode_label = tk.Label(
            center_top,
            text=mode_text,
            font=('Arial', 12),
            bg=self.colors['bg'],
            fg='#bdc3c7'
        )
        self.mode_label.pack()

        tk.Button(
            top_frame,
            text="Новая игра",
            command=self.new_game,
            bg=self.colors['accent'],
            fg=self.colors['text'],
            font=('Arial', 12, 'bold'),
            padx=15,
            pady=5
        ).pack(side='right')

        self.center_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        self.center_frame.pack(fill='both', expand=True)

        self.board_container = tk.Frame(self.center_frame, bg=self.colors['bg'])
        self.board_container.pack(expand=True, fill='both')

    def get_difficulty_name(self):
        """Получение названия сложности"""
        names = {
            'Easy': 'Легкий',
            'Medium': 'Средний',
            'Hard': 'Сложный'
        }
        return names.get(self.ai_difficulty, self.ai_difficulty)

    def create_board(self):
        """Создание игрового поля"""
        for widget in self.board_container.winfo_children():
            widget.destroy()

        board_frame = tk.Frame(self.board_container, bg=self.colors['bg'])
        board_frame.pack(expand=True)

        self.buttons = []
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]

        if self.board_size == 3:
            font_size = 40
            btn_width = 8
            btn_height = 4
        elif self.board_size == 4:
            font_size = 32
            btn_width = 6
            btn_height = 3
        else:
            font_size = 28
            btn_width = 5
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
                    fg=self.colors['text'],
                    activebackground=self.colors['cell_hover'],
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                btn.grid(row=i, column=j, padx=2, pady=2, sticky='nsew')
                board_frame.grid_rowconfigure(i, weight=1, uniform='row')
                board_frame.grid_columnconfigure(j, weight=1, uniform='col')

                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def make_move(self, row, col):
        """Обработка хода"""
        if not self.game_active or self.board[row][col] != '':
            return

        player = self.players[self.current_player]
        self.board[row][col] = player

        color = '#e74c3c' if player == 'X' else '#3498db'
        self.buttons[row][col].config(
            text=player,
            fg=color,
            disabledforeground=color,
            state='disabled'
        )

        if self.check_winner(player):
            self.game_active = False
            self.scores[player] += 1
            self.update_score()
            self.highlight_winner()
            messagebox.showinfo("Победа!", f"Игрок {player} победил!")
            return

        if self.check_draw():
            self.game_active = False
            self.scores['Draw'] += 1
            self.update_score()
            messagebox.showinfo("Ничья!", "Игра закончилась вничью!")
            return

        self.current_player = 1 - self.current_player
        self.status_label.config(
            text=f"Ходит: {self.players[self.current_player]}",
            fg='#e74c3c' if self.players[self.current_player] == 'X' else '#3498db'
        )

        if self.game_mode == "PvC" and self.players[self.current_player] == 'O':
            self.root.after(500, self.computer_move)

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
        """Ход средней сложности"""
        for row, col in empty_cells:
            self.board[row][col] = 'O'
            if self.check_winner('O'):
                self.board[row][col] = ''
                return row, col
            self.board[row][col] = ''

        for row, col in empty_cells:
            self.board[row][col] = 'X'
            if self.check_winner('X'):
                self.board[row][col] = ''
                return row, col
            self.board[row][col] = ''

        center = self.board_size // 2
        if self.board[center][center] == '':
            return center, center

        corners = [(0, 0), (0, self.board_size - 1),
                   (self.board_size - 1, 0), (self.board_size - 1, self.board_size - 1)]
        for row, col in corners:
            if self.board[row][col] == '':
                return row, col

        return random.choice(empty_cells)

    def get_hard_move(self, empty_cells):
        """Ход высокой сложности с мини-макс алгоритмом"""
        for row, col in empty_cells:
            self.board[row][col] = 'O'
            if self.check_winner('O'):
                self.board[row][col] = ''
                return row, col
            self.board[row][col] = ''

        for row, col in empty_cells:
            self.board[row][col] = 'X'
            if self.check_winner('X'):
                self.board[row][col] = ''
                return row, col
            self.board[row][col] = ''

        best_score = -float('inf')
        best_move = None

        for row, col in empty_cells:
            self.board[row][col] = 'O'
            score = self.minimax(3, False, -float('inf'), float('inf'))
            self.board[row][col] = ''

            if score > best_score:
                best_score = score
                best_move = (row, col)

        if best_move:
            return best_move

        center = self.board_size // 2
        if self.board[center][center] == '':
            return center, center

        corners = [(0, 0), (0, self.board_size - 1),
                   (self.board_size - 1, 0), (self.board_size - 1, self.board_size - 1)]
        for row, col in corners:
            if self.board[row][col] == '':
                return row, col

        return random.choice(empty_cells)

    def minimax(self, depth, is_maximizing, alpha, beta):
        """Мини-макс алгоритм"""
        if self.check_winner('O'):
            return 10 + depth
        if self.check_winner('X'):
            return -10 - depth
        if self.check_draw():
            return 0
        if depth == 0:
            return self.evaluate_board()

        if is_maximizing:
            max_eval = -float('inf')

            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.board[i][j] == '':
                        self.board[i][j] = 'O'
                        eval_score = self.minimax(depth - 1, False, alpha, beta)
                        self.board[i][j] = ''

                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)

                        if beta <= alpha:
                            return max_eval

            return max_eval
        else:
            min_eval = float('inf')

            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.board[i][j] == '':
                        self.board[i][j] = 'X'
                        eval_score = self.minimax(depth - 1, True, alpha, beta)
                        self.board[i][j] = ''

                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)

                        if beta <= alpha:
                            return min_eval

            return min_eval

    def evaluate_board(self):
        """Оценка текущей позиции на поле"""
        score = 0

        for i in range(self.board_size):
            score += self.evaluate_line([(i, j) for j in range(self.board_size)])
            score += self.evaluate_line([(j, i) for j in range(self.board_size)])

        score += self.evaluate_line([(i, i) for i in range(self.board_size)])
        score += self.evaluate_line([(i, self.board_size - 1 - i) for i in range(self.board_size)])

        return score

    def evaluate_line(self, cells):
        """Оценка одной линии (строки, столбца или диагонали)"""
        o_count = 0
        x_count = 0

        for row, col in cells:
            if self.board[row][col] == 'O':
                o_count += 1
            elif self.board[row][col] == 'X':
                x_count += 1

        if o_count > 0 and x_count == 0:
            return 10 ** (o_count - 1)
        elif x_count > 0 and o_count == 0:
            return -(10 ** (x_count - 1))
        else:
            return 0

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

        if all(self.board[i][self.board_size - 1 - i] == player for i in range(self.board_size)):
            self.win_cells = [(i, self.board_size - 1 - i) for i in range(self.board_size)]
            return True

        return False

    def check_draw(self):
        """Проверка ничьи"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == '':
                    return False
        return True

    def highlight_winner(self):
        """Подсветка победителя"""
        for row, col in self.win_cells:
            self.buttons[row][col].config(bg=self.colors['success'])

    def update_score(self):
        """Обновление счета"""
        self.score_label.config(
            text=f"Счет: X - {self.scores['X']} | O - {self.scores['O']} | Ничьи - {self.scores['Draw']}"
        )

    def new_game(self):
        """Начать новую игру"""
        self.game_active = True
        self.current_player = 0
        self.board = [['' for _ in range(self.board_size)] for _ in range(self.board_size)]

        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].config(
                    text='',
                    bg=self.colors['cell_bg'],
                    fg=self.colors['text'],
                    state='normal'
                )

        self.status_label.config(
            text=f"Ходит: {self.players[self.current_player]}",
            fg='#e74c3c' if self.players[self.current_player] == 'X' else '#3498db'
        )

        if self.game_mode == 'PvP':
            mode_text = f"Режим: Игрок vs Игрок | Размер поля: {self.board_size}x{self.board_size}"
        else:
            difficulty_names = {
                'Easy': 'Легкий',
                'Medium': 'Средний',
                'Hard': 'Сложный'
            }
            difficulty_name = difficulty_names.get(self.ai_difficulty, self.ai_difficulty)
            mode_text = f"Режим: Игрок vs Компьютер | Размер: {self.board_size}x{self.board_size} | Сложность: {difficulty_name}"

        self.mode_label.config(text=mode_text)

    def back_to_menu(self):
        """Возврат в меню"""
        self.root.destroy()
        menu = MainMenu()
        menu.root.mainloop()


GAME_SETTINGS = {
    'size': 3,
    'mode': 'PvP',
    'difficulty': 'Medium'
}


def main():
    """Запуск приложения"""
    try:
        menu = MainMenu()
        menu.root.mainloop()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")


if __name__ == "__main__":
    main()
