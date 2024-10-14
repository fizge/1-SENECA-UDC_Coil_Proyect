import PySimpleGUI as sg
import file_reader as fr


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


sg.theme('NeutralBlue')

layout = [
    [sg.Push(), sg.Button('Select dataset', font=('Courier New', 12, 'bold'),
                          button_color=('black', 'seagreen'), size=(16, 2), border_width=8), sg.Push()],
    [sg.InputText(key='-FILE-', size=(60, 1), readonly=True, pad=(10, 10))],
    [sg.Button('Confirm', font=('Courier New', 10), size=(10, 1),
               button_color=('black', 'seagreen'), border_width=4)]
]

window = sg.Window('Select data file', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == 'Select dataset':
        file_path = sg.popup_get_file('Select a data file', no_window=True, file_types=(
            ("CSV Files", "*.csv"), ("Excel Files", "*.xls;*.xlsx"), ("SQLite Database", "*.db;*.sqlite")))
        if file_path:
            window['-FILE-'].update(file_path)
    elif event == 'Confirm':
        file_path = values['-FILE-']
        data = fr.import_data(file_path)

        if data is None:
            sg.popup_error("The file is corrupted or not compatible")
        else:
            window.close()
            show_data(data)

window.close()
