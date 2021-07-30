# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import db
import gui


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    db.setup()
    # db.import_from_scale()
    print(f"Cassa: {db.cassa()}")
    print(f"Prestito: {db.prestito()}")
    print(f"Tesoretto: {db.tesoretto()}")
    gui.start_gui()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
