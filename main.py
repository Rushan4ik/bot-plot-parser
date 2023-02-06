from tracklist import parse_directories
from numeration_remover import remove_all_numeration
from beatport_parser.parser import parse_window_mainloop


parse_directories()
remove_all_numeration()
parse_window_mainloop()
