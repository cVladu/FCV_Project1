import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from main import run_main


dir_path_inp = ''
dir_path_out = ''
config_file_path = ''


def show_error(*args):
    err = args[2]
    messagebox.showerror('Error', err)


def create_handle_browse(button_type, label):
    # noinspection PyUnusedLocal
    def handle_browse(event=None):
        if button_type == 'input':
            global dir_path_inp
            dirname = filedialog.askdirectory()
            dir_path_inp = dirname
            label['text'] = dir_path_inp
        elif button_type == 'output':
            global dir_path_out
            dirname = filedialog.askdirectory()
            dir_path_out = dirname
            label['text'] = dir_path_out
        elif button_type == 'config':
            global config_file_path
            config_file_path = filedialog.askopenfile('r').name
            label['text'] = config_file_path

    return handle_browse


def create_run_command(window_to_destroy, entry, recursive_check):

    # noinspection PyUnusedLocal
    def run_command(event=None):
        run_main(dir_path_inp,
                 dir_path_out,
                 config_file_path,
                 int(entry.get()),
                 recursive_check.get())
        window_to_destroy.destroy()
    return run_command


def init_gui():
    _main_window = tk.Tk()

    label_inp_dir = tk.Label(master=_main_window, text='Input directory: ')
    label_inp_dir.grid(row=0, column=0)

    label_inp_dir_name = tk.Label(master=_main_window)
    label_inp_dir_name.grid(row=0, column=1)

    button_inp_dir = tk.Button(master=_main_window, text='Browse...',
                               command=create_handle_browse('input', label_inp_dir_name))
    button_inp_dir.grid(row=0, column=2)

    recursive_var = tk.BooleanVar()
    checkbox_recursive = tk.Checkbutton(master=_main_window, variable=recursive_var, text='Recursive')
    checkbox_recursive.grid(row=1, column=2)

    label_out_dir = tk.Label(master=_main_window, text='Output directory: ')
    label_out_dir.grid(row=2, column=0)

    label_out_dir_name = tk.Label(master=_main_window)
    label_out_dir_name.grid(row=2, column=1)

    button_out_dir = tk.Button(master=_main_window, text='Browse...',
                               command=create_handle_browse('output', label_out_dir_name))
    button_out_dir.grid(row=2, column=2)

    label_start_count = tk.Label(master=_main_window, text='Start Count:')
    label_start_count.grid(row=3, column=1)

    entry_start_count = tk.Entry(master=_main_window)
    entry_start_count.insert(tk.END, '1')
    entry_start_count.grid(row=3, column=2)

    label_config_file = tk.Label(master=_main_window, text='Config file: ')
    label_config_file.grid(row=4, column=0)

    label_config_file_name = tk.Label(master=_main_window)
    label_config_file_name.grid(row=4, column=1)

    button_config_file = tk.Button(master=_main_window, text='Browse...',
                                   command=create_handle_browse('config', label_config_file_name))
    button_config_file.grid(row=4, column=2)

    button_run = tk.Button(master=_main_window, text='RUN',
                           command=create_run_command(_main_window, entry_start_count, recursive_var))
    button_run.grid(row=5, column=0, columnspan=3, sticky='nsew')
    return _main_window


if __name__ == '__main__':
    tk.Tk.report_callback_exception = show_error
    main_window = init_gui()
    main_window.mainloop()

