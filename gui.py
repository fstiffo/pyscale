import dearpygui.dearpygui as dpg

import db


def start_gui():
    # add a font registry
    with dpg.font_registry():
        # add font (set as default for entire app)
        dpg.add_font("IBMPlexMono-Regular.ttf", 20, default_font=True)

    with dpg.window(label="Scale") as main_window:
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Quit", callback=dpg.stop_dearpygui)

        with dpg.table(label="Operazioni", row_background=True, borders_innerH=True, borders_outerH=True,
                       borders_innerV=True, borders_outerV=True, delay_search=True):
            dpg.add_table_column(label="Data", width_fixed=True, init_width_or_weight=100)
            dpg.add_table_column(label="Contabile", width_fixed=True, init_width_or_weight=100)
            dpg.add_table_column(label="Causale")
            operazioni = db.get_operazioni()
            operazioni_len = len(operazioni)
            for i, o in enumerate(operazioni):
                dpg.add_text(o[0])
                dpg.add_table_next_column()
                color: list[int] = [255, 0, 0, 255] if o[1] < 0 else [0, 255, 0, 255]
                dpg.add_text('{:>10}'.format(str(o[1])), color=color)
                dpg.add_table_next_column()
                dpg.add_text(o[2])
                if i != operazioni_len - 1:
                    dpg.add_table_next_column()

    dpg.set_primary_window(main_window, True)
    dpg.start_dearpygui()
