import datetime
import os
import time
import tkinter
from threading import Thread
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from beatport_parser import parser_requests
from beatport_parser import parser_csv

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
               columnspan=column_span, rowspan=row_span,
               padx=10, pady=10, sticky=sticky)
    return label


def tk_create_scrolled_text(window, row, column, row_span, column_span):
    scrolled_text = scrolledtext.ScrolledText(window, width=200, height=15)
    scrolled_text.grid(row=row, column=column, columnspan=column_span, rowspan=row_span,
                       padx=10, pady=10, sticky=None)
    return scrolled_text


def tk_create_button(window, text, row, column, function,
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
            parser_csv.create_csv_file(csv_file.name, parser_csv.read_txt_file(text_file))
            set_chosen_playlist(csv_file.name)


def button_choose_playlist():
    csv_file = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if csv_file:
        set_chosen_playlist(csv_file)


def button_parse():
    global parse_state, thread_exit, parsing_thread, buttons, chosen_file_name
    if parse_state:
        thread_exit = True
        buttons['parse'].configure(state=tkinter.DISABLED)
    else:
        buttons['create_playlist'].configure(state=tkinter.DISABLED)
        buttons['choose_playlist'].configure(state=tkinter.DISABLED)
        buttons['parse'].configure(text=BUTTON_NAMES['parse'][1])

        parse_state = True
        file = parser_csv.read_csv_file(chosen_file_name)
        if file:
            parsing_thread = Thread(target=thread_parse, args=(file,))
            parsing_thread.start()


def thread_parse(file):
    global chosen_file_data, thread_exit, counting_time

    chosen_file_data = file
    now = datetime.datetime.now()
    SCROLLED_TEXT_CONSOLE.insert('end', f'Парсинг начат - {now.strftime("%H:%M")}\n')

    for i, line in enumerate(chosen_file_data):
        if thread_exit:
            thread_exit = False
            break

        time_start = time.time()

        if not line[parser_csv.CSV_COLUMN_NAMES['src']] or \
                line[parser_csv.CSV_COLUMN_NAMES['src']] == parser_csv.SRC_RE_PARSING:
            search_req = line[parser_csv.CSV_COLUMN_NAMES['searchtr']]
            res = parser_requests.parse_track(search_req)

            line[parser_csv.CSV_COLUMN_NAMES['foundtr']] = res['smlr']
            line[parser_csv.CSV_COLUMN_NAMES['src']] = res['url']
            line[parser_csv.CSV_COLUMN_NAMES['perc']] = res['perc']

            update_info_ch_playlist(chosen_file_name, chosen_file_data)

            SCROLLED_TEXT_CONSOLE.insert("end", f"{i + 1}. [{res['perc']}] {search_req} - {res['url']}\n")
        counting_time[1] += time.time() - time_start
        counting_time[0] += 1
    now = datetime.datetime.now()
    SCROLLED_TEXT_CONSOLE.insert("end", f"Парсинг завершен - {now.strftime('%H:%M')}")
    thread_parse_finish()


def thread_parse_finish():
    global parse_state, buttons
    parse_state = False

    buttons['parse'].configure(state=tkinter.ACTIVE)
    buttons['create_playlist'].configure(state=tkinter.ACTIVE)
    buttons['choose_playlist'].configure(state=tkinter.ACTIVE)
    buttons['parse'].configure(text=BUTTON_NAMES['parse'][0])

    save_data_parse()


def save_data_parse():
    parser_csv.save_csv_file(chosen_file_name, chosen_file_data)
    create_html_file(chosen_file_name, chosen_file_data)


def set_chosen_playlist(file_name):
    global chosen_file_name, buttons

    chosen_file_name = file_name
    file = parser_csv.read_csv_file(file_name)
    update_info_ch_playlist(file_name, file)

    buttons['parse'].configure(state=tkinter.ACTIVE)
    SCROLLED_TEXT_CONSOLE.delete(1.0, tkinter.END)


def update_info_ch_playlist(file_name, file):
    info = parser_csv.get_info_csv_file(file)
    cells_info_playlist['playlist'].configure(text=CELL_NAMES['playlist'].format(os.path.basename(file_name)))
    cells_info_playlist['total'].configure(text=CELL_NAMES['total'].format(info[0]))
    cells_info_playlist['parsed'].configure(text=CELL_NAMES['parsed'].format(info[1]))
    cells_info_playlist['not_parsed'].configure(text=CELL_NAMES['not_parsed'].format(info[4]))
    cells_info_playlist['not_found'].configure(text=CELL_NAMES['not_found'].format(info[2]))
    time_to_finish = (counting_time[1] / counting_time[0]) * info[4]
    time_to_finish = time.strftime("%H ч %M м %S с", time.gmtime(time_to_finish))

    cells_info_playlist['time_to_finish'].configure(text=CELL_NAMES['time_to_finish'].format(time_to_finish))


def sort_for_html(k):
    try:
        return float(k[parser_csv.CSV_COLUMN_NAMES['perc']])
    except Exception as e:
        return 0


def create_html_file(file_name, data):
    for i, line in enumerate(data):
        line['old__index'] = i + 1

    data = sorted(data, key=sort_for_html, reverse=True)

    try:
        with open(file_name + '.html', 'w', newline='', encoding='utf-8') as file:
            file.write("<html>\r\n<head>")
            file.write("""
            <style type="text/css">
            table {
            width: 100%;
            }
            td {
            border-bottom: 1px dotted black;
            }
            audio {
            height: 40px;
            }
            .green {
            background: lightgreen;
            }
            .yellow {
            background: yellow;
            }
            .red {
            background: Salmon;
            }
            </style>
            """)
            file.write("</head>\r\n<body>\r\n<table cellspacing='0'>\r\n")
            td = "<td>{}</td>"
            a = "<td><a href='{}' target='_blank'>Поиск</a></td>"
            number = "<td>{})</td>"
            perc = "<td>{}%</td>"
            audio = "<td><audio controls src='{}'></audio></td>"
            for i, line in enumerate(data):
                clss = "red"
                sperc = td.format(". . .")
                try:
                    fperc = float(line[parser_csv.CSV_COLUMN_NAMES['perc']])
                    sperc = perc.format(int(fperc))
                    if fperc:
                        if fperc >= 90:
                            clss = "green"
                        elif fperc > 80:
                            clss = "yellow"
                except Exception as e:
                    print(e.__class__.__name__)

                file.write("<tr border='1' class='{}'>".format(clss))
                file.write(number.format(line['old__index']))
                file.write(sperc)
                file.write(td.format(line[parser_csv.CSV_COLUMN_NAMES['searchtr']] + "<br>" +
                                     line[parser_csv.CSV_COLUMN_NAMES['foundtr']]))
                file.write(a.format(parser_requests.get_url_search_track(
                    parser_requests.prepare_str_for_url(line[parser_csv.CSV_COLUMN_NAMES['searchtr']]))))
                file.write(audio.format(line[parser_csv.CSV_COLUMN_NAMES['src']]))
                file.write("</tr>\r\n")
            file.write("</table>\r\n</body>\r\n</html>")
    except Exception as e:
        print(e)


def parse_window_mainloop():
    global buttons, SCROLLED_TEXT_CONSOLE
    root_window = tkinter.Tk()
    root_window.title('Парсер аудиофайлов beatport.com (vds-dev.ru)')

    root_window.grid_columnconfigure(0, weight=1)
    root_window.grid_columnconfigure(1, weight=1)
    root_window.grid_columnconfigure(2, weight=1)
    root_window.grid_columnconfigure(3, weight=1)
    root_window.grid_columnconfigure(4, weight=1)
    root_window.grid_columnconfigure(5, weight=1)

    buttons['create_playlist'] = tk_create_button(root_window, 'Создать плейлист',
                                                  0, 5, button_create_playlist, 1, 1, 'e')
    buttons['choose_playlist'] = tk_create_button(root_window, 'Выбрать плейлист', 2, 5,
                                                  button_choose_playlist, 1, 1, 'e')
    cells_info_playlist['playlist'] = tk_create_label(root_window,
                                                      CELL_NAMES['playlist'].format('Не выбран'), 2, 0, 1, 1, 'w')
    cells_info_playlist['total'] = tk_create_label(root_window, CELL_NAMES['total'].format(''),
                                                   3, 0, 1, 1, 'w')
    cells_info_playlist['parsed'] = tk_create_label(root_window, CELL_NAMES['parsed'].format(''),
                                                    3, 1, 1, 1, 'w')
    cells_info_playlist['not_found'] = tk_create_label(root_window, CELL_NAMES['not_found'].format(''),
                                                       3, 2, 1, 1, 'w')
    cells_info_playlist['not_parsed'] = tk_create_label(root_window, CELL_NAMES['not_parsed'].format(''),
                                                        3, 3, 1, 1, 'w')

    buttons['parse'] = tk_create_button(root_window, BUTTON_NAMES['parse'][0], 4, 0, button_parse, 1, 1, 'w')
    buttons['parse'].configure(state=tkinter.DISABLED)
    cells_info_playlist['time_to_finish'] = tk_create_label(root_window, '', 4, 1, 1, 1, 'w')

    SCROLLED_TEXT_CONSOLE = tk_create_scrolled_text(root_window, 5, 0, 1, 6)

    root_window.mainloop()

    if parse_state:
        save_data_parse()
