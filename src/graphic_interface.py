import PySimpleGUI as sg
import file_reader as fr

def create_window(headings, values):
    layout = [
        [sg.Push(), sg.Button('Select dataset', font=('Courier New', 12, 'bold'),button_color=('black', 'seagreen'), size=(16, 2), border_width=8), sg.Push()],
        [sg.Push(), sg.InputText(key='-FILE-', size=(70, 1), readonly=True, pad=(10, 10)), sg.Push()],
        [sg.Button('Confirm', font=('Courier New', 10), size=(10, 1), button_color=('black', 'seagreen'), border_width=4),
         sg.Button('Clean table', font=('Courier New', 10, 'bold'), size=(13, 1), button_color=('black', 'white'), border_width=4)],
        [sg.Table(values=values, headings=headings, display_row_numbers=True, auto_size_columns=False, col_widths=[15] * len(headings), num_rows=15, 
                  vertical_scroll_only=False, alternating_row_color='lightblue', key='-TABLE-', visible=True if values else False)]
              ]

    return sg.Window('Select data file', layout, finalize=True, resizable=True)

headings = []
values = []

sg.theme('NeutralBlue')
window = create_window(headings, values)

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

        if not file_path:
            sg.popup_error("Please select a file first.")
            continue

        try:
            data = fr.import_data(file_path)
            if data is None or data.empty:
                sg.popup_error("The file is corrupted or not compatible")
            else:
                headings = list(data.columns)
                values = data.values.tolist()

                window.close()
                window = create_window(headings, values)
        except Exception as e:
            sg.popup_error(f"An error occurred while importing the data: {e}")
    elif event == 'Clean table':
        headings = []
        values = []
        
        window.close()
        window = create_window(headings, values)

window.close()
