import csv

# CONSTANTS

ERROR_MESSAGES = {
    "file_read": "Ошибка чтения файла! {}",
    "file_write": "Ошибка записи файла! {}"
}

CSV_DIALECT_NAME = 'parsertabledialect'
CSV_COLUMN_NAMES = {
    "searchtr": "str_search_track",
    "foundtr": "str_found_track",
    "src": "url_chosen_track",
    "perc": "percent_of_coincide"
}
CSV_COLUMN_DESCRIPTION = {
    "searchtr": "Строка, по которой необходимо найти трек",
    "foundtr": "Строка, наиболее подходящего, найденного трека",
    "src": "Ссылка на аудиофайл, если он был выбран, иначе 'NONE'",
    "perc": "Процент совпадения при сравнении {} и {}".format(CSV_COLUMN_NAMES["searchtr"], CSV_COLUMN_NAMES["foundtr"])
}

SRC_NOT_FOUND = "NONE"
SRC_RE_PARSING = "RE-PARSING"

csv.register_dialect(
    CSV_DIALECT_NAME,
    delimiter=';',
    doublequote=True,
    escapechar='\\',
    lineterminator="\r\n",
    quotechar='"',
    quoting=csv.QUOTE_MINIMAL,
    skipinitialspace=False,
    strict=True
)


def create_csv_file(file_name, data=None):
    if data is None:
        data = []
    try:
        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, dialect=CSV_DIALECT_NAME,
                                    fieldnames=CSV_COLUMN_NAMES.values())
            writer.writeheader()

            for line in data:
                writer.writerow({CSV_COLUMN_NAMES["searchtr"]: line})
    except Exception as e:
        print(ERROR_MESSAGES['file_write'].format(e.__class__.__name__))


def save_csv_file(file_name, data):
    try:
        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, dialect=CSV_DIALECT_NAME, fieldnames=CSV_COLUMN_NAMES.values())
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(ERROR_MESSAGES['file_write'].format(e))


def read_txt_file(file_name):
    try:
        with open(file_name, 'r', newline='', encoding='utf-8') as file:
            return [line.rstrip() for line in file]
    except Exception as e:
        print(ERROR_MESSAGES["file_read"].format(e))


def read_csv_file(file_name):
    try:
        with open(file_name, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, dialect=CSV_DIALECT_NAME)
            return list(reader)
    except Exception as e:
        print(ERROR_MESSAGES['file_read'].format(e))
        return False


def get_info_csv_file(lines):
    total = len(lines)
    parsed = 0
    none_parse = 0
    error_parse = 0

    for line in lines:
        if line[CSV_COLUMN_NAMES['src']]:
            if line[CSV_COLUMN_NAMES['src']] == SRC_NOT_FOUND:
                none_parse += 1
            elif line[CSV_COLUMN_NAMES['src']] == SRC_RE_PARSING:
                error_parse += 1
            else:
                parsed += 1

    return [total, parsed, none_parse, error_parse, total - (parsed + none_parse)]

