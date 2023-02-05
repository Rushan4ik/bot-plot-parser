import os
import threading
import time
import tkinter.ttk as ttk
import tkinter


def parse_directories():
    current_dir = os.getcwd()

    root = tkinter.Tk()
    root.geometry('600x100')

    i = 0
    for directory, folder, files in os.walk(current_dir):
        if directory == current_dir:
            continue
        elif not os.path.basename(directory) in os.listdir(current_dir):
            continue
        elif os.path.basename(directory) == 'Original Tracklist':
            continue
        else:
            i += 1

    progress_bar = ttk.Progressbar(root, maximum=i, mode='determinate', length=400)
    progress_bar.pack()
    label = tkinter.Label(root)
    label.pack()

    progress_thread = threading.Thread(target=progress, args=[progress_bar, label, current_dir])
    progress_thread.start()
    root.mainloop()


def progress(progress_bar, label, current_dir):
    try:
        for directory, folder, files in os.walk(current_dir):
            if directory == current_dir:
                continue
            elif not os.path.basename(directory) in os.listdir(current_dir):
                continue
            elif os.path.basename(directory) == 'Original Tracklist':
                continue
            else:
                name = os.path.basename(directory)
                res = sorted(filter(lambda file_name: file_name[0] != '.' and file_name.endswith('.mp3'), files))
                label['text'] = f'Генерирую {name}.txt'
                with open(f'{os.path.join(current_dir, name)}.txt', 'w', encoding='utf-8') as file:
                    file.write('\n'.join(res))
                progress_bar['value'] += 1
                time.sleep(0.5)
        label['text'] = 'Генерация закончена'
    except Exception as e:
        label['text'] = f"Ошибка\n{e.__class__.__name__}: {e}"
