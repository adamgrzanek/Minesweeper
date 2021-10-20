import sqlite3
from minesweeper import Saper, play


# create database
connection = sqlite3.connect("minesweeper_results.db")


def create_table(connection):
    '''Create table.'''

    try:
        cur = connection.cursor()
        cur.execute("""CREATE TABLE minesweeper_results
                        (name text, level text, moves text, time real)""")
    except:
        pass


create_table(connection)


def add_result(connection, name, level, moves, time):
    '''Add result to database.'''

    cur = connection.cursor()
    cur.execute(f"""INSERT INTO minesweeper_results VALUES ('{name}', '{level}', '{moves}', '{time}')""")
    connection.commit()
    print('Added your result.')


def show_results(connection, level, name_=None):
    '''Show results order by time in given level.'''

    cur = connection.cursor()
    cur.execute(f"""SELECT * FROM minesweeper_results WHERE level like '{level}' ORDER BY time""") # limit 10?
    result = cur.fetchall()

    print()
    print(f'Results in level {level}:')
    print('pos. | name       | moves | time')
    print('---------------------------------------')
    counter = 1
    for row in result:
        if name_:
            if row[0] == name_:
                print(f" {str(counter):4s}| {(row[0]):11s}| {row[2]:5s} | {str((row[3])).split('.')[0]}")
        else:
            print(f" {str(counter):4s}| {(row[0]):11s}| {row[2]:5s} | {str((row[3])).split('.')[0]}")
        counter += 1
    print()


def winner_name():
    '''The player gives the name.'''

    global w_name
    while True:
        w_name = input(f'Name: (max 10 char) >>>> ')
        if len(w_name) <= 10:
            return w_name
            break
        else:
            print('Too many characters. Try again.')
            continue


def import_data(game_level):
    '''After game (win/lose) import data (time, moves). If win add result to db and show position.'''

    from minesweeper import moves, time_delta
    if game_level.win == True:
        add_result(connection, winner_name(), level, moves, time_delta)
        show_results(connection, level, name_=w_name)



while True:
    print()
    print('  Minesweeper')
    print('1 - Play level easy (10x10 board, 10 mines)')
    print('2 - Play level medium (15x15 board, 40 mines)')
    print('3 - Play level hard (20x20 board, 80 mines)')
    print('4 - Show results')
    print('0 - Exit')
    print()
    user_choice = input('Choose option >>>> ')

    if user_choice == '1':
        level = 'easy'
        n = 10
        game_easy = Saper(10, n)
        play(game_easy)
        import_data(game_easy)


    if user_choice == '2':
        level = 'medium'
        n = 40
        game_medium = Saper(15, n)
        play(game_medium)
        import_data(game_medium)


    if user_choice == '3':
        level = 'hard'
        n = 80
        game_hard = Saper(20, n)
        play(game_hard)
        import_data(game_hard)

    if user_choice == '4':
        show_results(connection, 'easy')
        show_results(connection, 'medium')
        show_results(connection, 'hard')

    if user_choice == '0':
        print('Thank You, see you later!')
        break

