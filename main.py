import json
import PySimpleGUI as sg
import re
import operator
import os
from VideoGame import VideoGame 

fVideoGame = 'VideoGame.json'
lVideoGame = []

pattern_ID = r"\d{3}"

def saveVideoGameJSON(file_path, video_games):
    data = []
    for game in video_games:
        if not game.erased:
            data.append({
                "ID": game.ID,
                "Name": game.name,
                "Company": game.company,
                "Platform": game.platform,
                "Year": game.year,
                "Price": game.price
            })

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def readVideoGameJSON(file_path, lG):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for game_data in data:
                video_game = VideoGame(game_data["ID"], game_data["Name"], game_data["Company"],
                                       game_data["Platform"], game_data["Year"], game_data["Price"])
                lG.append(video_game)
    except FileNotFoundError:
        pass

def addVideoGame(l_VideoGame, t_VideoGameInterfaz, oVideoGame):
    l_VideoGame.append(oVideoGame)
    saveVideoGameJSON(fVideoGame, l_VideoGame)
    t_VideoGameInterfaz.append([oVideoGame.ID, oVideoGame.name, oVideoGame.company, oVideoGame.platform, oVideoGame.year, oVideoGame.price])

def sort_table(table, cols):
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table

def delVideoGame(l_VideoGame, t_VideoGameInterfaz, posinTable):
    posinFile = t_VideoGameInterfaz[posinTable][0]
    cdel = None
    for o in l_VideoGame:
        if o.ID == posinFile:
            cdel = o
            break
    if cdel is not None:
        l_VideoGame.remove(cdel)
        t_VideoGameInterfaz.remove(t_VideoGameInterfaz[posinTable])
        cdel.erased = True
        saveVideoGameJSON(fVideoGame, l_VideoGame)

def updateVideoGame(l_VideoGame, t_row_VideoGameInterfaz, posinFile, window):
    cdel = None
    for o in l_VideoGame:
        if o.ID == posinFile:
            cdel = o
            break
    if cdel is not None:
        # Actualizar datos del VideoGame
        cdel.setGameInfo(t_row_VideoGameInterfaz[1], t_row_VideoGameInterfaz[2], t_row_VideoGameInterfaz[3],
                         t_row_VideoGameInterfaz[4], t_row_VideoGameInterfaz[5])
        saveVideoGameJSON(fVideoGame, l_VideoGame)

        # Actualizar la tabla en la interfaz
        t_row_VideoGameInterfaz[0] = cdel.ID
        window['-Table-'].update(values=[t_row_VideoGameInterfaz], append=False)

def purgeVideoGame():
    file_path_new = 'nuevoVideoGame.json'
    data_new = []
    for game in lVideoGame:
        if not game.erased:
            data_new.append({
                "ID": game.ID,
                "Name": game.name,
                "Company": game.company,
                "Platform": game.platform,
                "Year": game.year,
                "Price": game.price
            })

    with open(file_path_new, 'w') as file_new:
        json.dump(data_new, file_new, indent=2)

    os.remove(fVideoGame)
    os.rename(file_path_new, fVideoGame)

def interfaz():
    font1, font2 = ('Arial', 14), ('Arial', 16)
    sg.theme('Purple')
    sg.set_options(font=font1)
    table_data = []
    rowToUpdate = []
    readVideoGameJSON(fVideoGame, lVideoGame)
    for o in lVideoGame:
        if not o.erased:
            table_data.append([o.ID, o.name, o.company, o.platform, o.year, o.price])

    layout = [
        [sg.Push(), sg.Text('Video Game'), sg.Push()]] + [
        [sg.Text(text), sg.Push(), sg.Input(key=key)] for key, text in VideoGame.fields.items()] + [
        [sg.Push()] +
        [sg.Button(button) for button in ('Add', 'Delete', 'Modify', 'Clear', 'Purge')] +
        [sg.Push()],
        [sg.Table(values=table_data, headings=VideoGame.headings, max_col_width=50, num_rows=10,
                  display_row_numbers=False, justification='center', enable_events=True,
                  enable_click_events=True,
                  vertical_scroll_only=False, select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                  expand_x=True, bind_return_key=True, key='-Table-')],
        [sg.Button('Purge'), sg.Push(), sg.Button('Sort File')],
    ]
    sg.theme('Dark')
    window = sg.Window('Video Game Management with Files', layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Add':
            valida = False
            if re.match(pattern_ID, values['-ID-']):
                valida = True
            if valida:
                addVideoGame(lVideoGame, table_data, VideoGame(values['-ID-'], values['-Name-'], values['-Company-'],
                                                               values['-Platform-'], values['-Year-'],
                                                               values['-Price-']))
                window['-Table-'].update(table_data)
        if event == 'Delete':
            if len(values['-Table-']) > 0:
                delVideoGame(lVideoGame, table_data, values['-Table-'][0])
                window['-Table-'].update(table_data)

        if event == 'Clear':
            window['-ID-'].update('')
            window['-Name-'].update('')
            window['-Company-'].update('')
            window['-Platform-'].update('')
            window['-Year-'].update('')
            window['-Price-'].update('')

        if event == 'Modify':
            valida = False
            if re.match(pattern_ID, values['-ID-']):
                valida = True
            if valida:
                for t in table_data:
                    if t[0] == int(values['-ID-']):
                        rowToUpdate = t
                        t[1], t[2], t[3], t[4], t[5] = values['-Name-'], values['-Company-'], values['-Platform-'], \
                                                         values['-Year-'], values['-Price-']
                        break
                updateVideoGame(lVideoGame, rowToUpdate, int(values['-ID-']), window)
                window['-Table-'].update(table_data)

        if event == 'Purge':
            purgeVideoGame()
            window['-Table-'].update(table_data)
            sg.popup('Purge complete.')

        if isinstance(event, tuple):
            print(event)
            print(values)
        if event[0] == '-Table-':
            if event[2][0] == -1:
                col_num_clicked = event[2][1]
                table_data = sort_table(table_data, (col_num_clicked, 0))
                window['-Table-'].update(table_data)

    window.close()

interfaz()
