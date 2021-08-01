import dearpygui.dearpygui as dpg

import db
import gui

selected = None
selected_text = None


def start_gui():
    # add a font registry
    with dpg.font_registry():
        # add font (set as default for entire app)
        dpg.add_font("IBMPlexMono-Regular.ttf", 20, default_font=True)

    with dpg.window(label="Scale") as main_window:
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Quit", callback=dpg.stop_dearpygui)

        # with dpg.table(label="Operazioni", row_background=True, borders_innerH=True, borders_outerH=True,
        #                borders_innerV=True, borders_outerV=True, delay_search=True):
        #     dpg.add_table_column(label="Data", width_fixed=True, init_width_or_weight=100)
        #     dpg.add_table_column(label="Contabile", width_fixed=True, init_width_or_weight=100)
        #     dpg.add_table_column(label="Causale")
        #     operazioni = db.get_operazioni()
        #     operazioni_len = len(operazioni)
        #     for i, o in enumerate(operazioni):
        #         dpg.add_text(o[0])
        #         dpg.add_table_next_column()
        #         color: list[int] = [255, 0, 0, 255] if o[1] < 0 else [0, 255, 0, 255]
        #         dpg.add_text('{:>10}'.format(str(o[1])), color=color)
        #         dpg.add_table_next_column()
        #         dpg.add_text(o[2])
        #         if i != operazioni_len - 1:
        #             dpg.add_table_next_column()

        def selectable_callback(sender, app_data, user_data):
            print(f"sender is: {sender}")
            print(f"app_data is: {app_data}")
            print(f"user_data is: {user_data}")
            print(f"Selected: {gui.selected}")
            if gui.selected is None:
                gui.selected = sender
            else:
                dpg.set_value(gui.selected, False)
                gui.selected = sender
            dpg.set_value( gui.selected_text, f"My Object Id: {user_data}")

        dpg.add_text("Operazioni")
        with dpg.child(label="left panel", height=0, width=450, border=True):
            operazioni = db.get_operazioni()
            for o in operazioni:
                label = o[1]
                dpg.add_selectable(label=label, user_data=o[0], callback=selectable_callback)
        dpg.add_same_line()
        with dpg.group():
            with dpg.child(label="item view"):
                gui.selected_text = dpg.add_text(f"My Object Id: {selected}")
                with dpg.tab_bar(label="##Tabs"):
                    with dpg.tab(label="Description"):
                        dpg.add_text("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
                                     "incididunt ut labore et dolore magna aliqua. ")
                    with dpg.tab(label="Details"):
                        dpg.add_text("ID: 0123456789")
            dpg.add_button(label="Revert")
            dpg.add_button(label="Save")

    dpg.set_primary_window(main_window, True)
    dpg.start_dearpygui()
