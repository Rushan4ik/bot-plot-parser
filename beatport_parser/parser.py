import os
import tkinter
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
# CONSTANTS


CELL_NAMES = {
    'playlist': "Плейлист: {}",
    'total': "Всего треков: {}",
    'parsed': "Парс выполнен: {}",
    'not_parsed': "Нужен парс: {}",
    'not_found': "Не найдено: {}",
    'time_to_finish': "Осталось примерно: {}"
}

BUTTON_NAMES = {
    "create_playlist": "",
    "choose_playlist": '',
    'parse': ['Начать парсинг', "Остановить парсинг"]
}

SCROLLED_TEXT_CONSOLE = None

# VARIABLES
cells_info_playlist = {
    'playlist': None,
    'total': None,
    'parsed': None,
    'not_parsed': None,
    'not_found': None,
    'time_to_finish': None
}

buttons = {
    "create_playlist": None,
    "choose_playlist": None,
    'parse': None
}

chosen_file_name = ''
chosen_file_data = []

parse_state = False
thread_exit = False

parsing_thread = None

counting_time = [700, 4260]


def tk_create_label(window, text, row, column, row_span, column_span, sticky=None):
    label = tkinter.Label(window, text=text)
    label.grid(row=row, column=column,
               columnspan=column_span, row_span=row_span,
               padx=10, pady=10, sticky=sticky)
    return label


def tk_create_scrolled_text(window, row, column, row_span, column_span):
    scrolled_text = scrolledtext.ScrolledText(window, width=200, height=15)
    scrolled_text.grid(row=row, column=column, columnspan=column_span, row_span=row_span,
                       padx=10, pady=10, sticky=None)
    return scrolled_text


def tkCreateButton(window, text, row, column, function,
                   row_span=1, column_span=1, sticky=None):
    button = tkinter.Button(window, text=text, padx=5, pady=5, command=function)
    button.grid(row=row, column=column, columnspan=column_span, rowspan=row_span, padx=10, pady=10, sticky=sticky)
    return button


def button_create_playlist():
    text_file = filedialog.askopenfilename(filetypes=[("TXT Files", "*.txt")])

    if text_file:
        file_name = os.path.splitext(os.path.basename(text_file))
        dir_name = os.path.dirname(text_file)

        messagebox.showinfo("Предупреждение",
                            """
                            Сейчас откроется сохранение .csv файла
                            Вам нужно выбрать место, где вы хотите сохранить его.
                            """)

        csv_file = filedialog.asksaveasfile(filetypes=[('CSV Files', '*.csv')],
                                            initialdir=dir_name, initialfile=file_name[0],
                                            defaultextension='.csv')

        if csv_file:
            # TODO
            pass


def parse_window_mainloop():
    pass
