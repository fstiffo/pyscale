import dearpygui.dearpygui as dpg


def start_gui():
    # add a font registry
    with dpg.font_registry():
        # add font (set as default for entire app)
        dpg.add_font("IBMPlexMono-Regular.ttf", 20, default_font=True)

    with dpg.window(label="Scale") as main_window:
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Quit", callback=dpg.stop_dearpygui)

    dpg.set_primary_window(main_window, True)
    dpg.start_dearpygui()
