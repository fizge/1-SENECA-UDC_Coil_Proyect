import PySimpleGUI as sg
import os
import file_reader as fr 

def files_in_same_folder():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir(current_folder)
    valid_ext = ('.xls', '.xlsx', '.db', '.sqlite', '.csv')
    valid_files = [file for file in files if file.endswith(valid_ext)]    
    return valid_files, current_folder

def show_data(data):
    if data is None or data.empty:
        sg.popup_error("No data to display")
        return

    headings = list(data.columns)
    values = data.values.tolist()

    layout = [
        [sg.Table(values=values, headings=headings, display_row_numbers=True, auto_size_columns=True,
                  num_rows=min(25, len(values)), alternating_row_color='lightblue')]
    ]
    
    window = sg.Window("Data Table", layout, finalize=True)
    window.read()
    window.close()

sg.theme('LightBlue')

layout = [
    [sg.Button('Select dataset', font=('Courier New', 12), button_color=('white', 'blue'), size=(16, 2), border_width=8),
     sg.InputText(key='-INPUT-', size=(60, 1)),
     sg.Button('Confirm', font=('Courier New', 10), size=(10, 1))],
    [sg.Listbox(values=[], size=(50, 10), key='-FILES-', enable_events=True)]
]

window = sg.Window('Select data file', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == 'Select dataset': 
        files, current_folder = files_in_same_folder()
        window['-FILES-'].update(files)
    elif event == '-FILES-':  
        selected_file = values['-FILES-'][0]
        full_rute = os.path.join(current_folder, selected_file)
        window['-INPUT-'].update(full_rute)
    elif event == 'Confirm':
        file_path = values['-INPUT-']
        data = fr.import_data(file_path)

        if data is None:
            sg.popup_error("The file is corrupted or not compatible")
        else:
            window.close()
            show_data(data)

window.close()


