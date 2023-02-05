import os
import shutil


def is_numeration(file_name: str) -> bool:
    if file_name.count('.') > 1:
        return file_name[:file_name.find('.')].isdigit()
    return False


def remove_numeration():
    current_dir = os.getcwd()
    output_dir_name = 'Original Tracklist'
    output_dir = os.path.join(current_dir, output_dir_name)

    try:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        for file in os.listdir(current_dir):
            if file.endswith('.txt'):
                with open(os.path.join(current_dir, file), 'r') as input_file, \
                        open(os.path.join(output_dir, file), 'w') as outfile:
                    for line in map(str.strip, input_file.readlines()):
                        print(line)
                        if is_numeration(line):
                            shutil.copy(os.path.join(current_dir, file[:-4], line), os.path.join(output_dir, line))
                        else:
                            shutil.move(os.path.join(current_dir, file[:-4], line), os.path.join(current_dir, line))
    except OSError as e:
        print("Can't create directory or file:", e.__class__.__name__)

