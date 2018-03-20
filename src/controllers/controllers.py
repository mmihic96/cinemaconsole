"""
Module provide getters and setters, validation,
load menu for each user role and other functions for app.
"""

import data
import constants
import datetime
import json


def set_username(username):
    """
    Function set session username
    """
    data.session_username = username


def get_username():
    """
    Function get session username
    """
    return data.session_username


def set_password(password):
    """
    Function set session password
    """
    data.session_password = password


def get_password():
    """
    Function get session password
    """
    return data.session_password


def set_first_name(first_name):
    """
    Function set session user firstname
    """
    data.session_first_name = first_name


def get_first_name():
    """
    Function get session user firstname
    """
    return data.session_first_name


def set_last_name(last_name):
    """
    Function set session user lastname
    """
    data.session_last_name = last_name


def get_last_name():
    """
    Function get session user lastname
    """
    return data.session_last_name


def validate_user():
    """ Search for session user in hardcoded list of users
        (users are stored i data module)
    """
    users = get_all_users()

    for user in users:
        username = user["username"]
        password = user["password"]
        if username == get_username() and password == get_password():
            return user
    return None


def print_session_message():
    """
    Function show session User First and Last name
    """
    print(constants.SEPARATOR)
    print(constants.SESSION_MESSAGE.format(get_first_name(), get_last_name()))
    print(constants.SEPARATOR)


def print_manager_menu_options():
    """
    Function print manager menu and wait for user selection
    """
    return input(constants.MANAGER_MENU.format(
        constants.MANAGER_MENU_OPTION_1,
        constants.MANAGER_MENU_OPTION_2,
        constants.MANAGER_MENU_OPTION_3,
        constants.MANAGER_MENU_OPTION_4,
        constants.MANAGER_MENU_OPTION_5,
        constants.MANAGER_MENU_OPTION_6))


def print_seller_menu_options():
    """
    Function show menu options for seller and wait for user selection
    """
    return input(constants.SELLER_MENU.format(
        constants.SELLER_MENU_OPTION_1,
        constants.SELLER_MENU_OPTION_2,
        constants.SELLER_MENU_OPTION_3,
        constants.SELLER_MENU_OPTION_4))


def print_search_events_menu_options():
    """
    Function show menu options for events search and wait for user selection
    """
    return input(constants.SEARCH_EVENTS_MENU.format(
        constants.SEARCH_EVENTS_OPTION_1,
        constants.SEARCH_EVENTS_OPTION_2,
        constants.SEARCH_EVENTS_OPTION_3,
        constants.SEARCH_EVENTS_OPTION_4,
        constants.SEARCH_EVENTS_OPTION_5,
        constants.SEARCH_EVENTS_OPTION_6))


def get_events():
    """
    Function get all events from data module
    """
    with open('../data/events.json', 'r') as data:
        return json.load(data)


def all_events():
    """
    Show all available events
    """
    founded_events = []
    for event in get_events():
        if event["deleted"] is not True:
            founded_events.append(event)
    if len(founded_events) > 0:
        print_table(founded_events)
    else:
        print('Ne postoji ni jedna projekcija.')


def find_by_id(id):
    """
    Find event by event ID
    """
    founded_events = []
    for event in get_events():
        if event["deleted"] is not True:
            if event['eventID'] == id:
                founded_events.append(event)
    if len(founded_events) > 0:
        print_table(founded_events)
        return founded_events
    else:
        print('Ne postoji dogadjaj sa tim ID-em.')


def find_by_movie_name(movie_name):
    """
    Find event by movie name
    """
    founded_events = []
    for event in get_events():
        movie = find_movie_by_id(event['movieID'])
        if event["deleted"] is not True:
            if movie_name.lower() in movie["movie_name"].lower():
                founded_events.append(event)
    if len(founded_events) > 0:
        print_table(founded_events)
    else:
        print('Ne postoje projekcije sa tim imenom. ')


def find_event_by_movie_type(movie_type):
    events = get_events()
    founded_events = []
    for e in events:
        movie = find_movie_by_id(e['movieID'])
        if movie['movie_type'].lower() == movie_type:
            founded_events.append(e)
    if len(founded_events) > 0:
        print_table(founded_events)
        return founded_events
    print('Ne postoje filmovi sa tim tipom')
    return []


def find_by_hall(hall_id):
    """
    Find event by hall ID
    """
    founded_events = []
    for event in get_events():
        hall = find_hall_by_id(event["hallID"])
        if event["deleted"] is False:
            if hall_id.lower() == hall["hallID"].lower():
                founded_events.append(event)
    if len(founded_events) > 0:
        print_table(founded_events)
        return founded_events
    else:
        print('Ne postoji dogadjaj sa tom salom.')


def delete_event_by_id(event_id):
    """
    Delete event, set deleted property True
    """
    for e in get_events():
        if e["deleted"] is False:
            if e["eventID"] == event_id:
                if delete_event(e['eventID']) is True:
                    print("Uspjesno ste obrisali projekcija.")
                    return
    print("Projekcija sa tim ID-em nije pronadjena.")


def add_event():
    movie = False
    hall = False
    """
    All dates and months are valid for now,
    in 2and part of project more validate will be provided
    """
    all_e = get_events()
    if len(all_e) < 1:
        event_id = 1
    else:
        event_id = all_e[len(all_e) - 1]['eventID'] + 1
    # OVDE TABELA ZA FILMOVE I PROVJERA DA LI ID POSTOJI
    while movie is False:
        print_table_movies(get_all_movies())
        movie_id = input("Izaberite id filma koji zelite da pustite -  ")
        try:
            movie = find_movie_by_id(int(movie_id))
            if movie is not False:
                break
            print('Ne postoji film sa tim ID-em, pokusajte ponovo. ')
        except:
            print('Pogresan unos. Pokusajte ponovo')
            continue
    # OVDE TABELA SA SALAMA KOJE POSTOJE
    while hall is False:
        print_table_halls(get_all_halls())
        hall_id = input("Unesite ID sale u kojem ce se film odrzati - ")
        hall = find_hall_by_id(hall_id)
        if hall is not False:
            break
        print('Ne postoji sala sa tim ID-em. Pokusajte ponovo.')

    while True:
        try:
            price = float(input("Unesite cijenu karte za taj film - "))
            break
        except:
            print('Pogresan unos. Pokusajte ponovo.')
            continue
    # DATUM I VREME
    while True:
        try:
            now = datetime.datetime.now()
            inputDate = input("Unesite datum u formatu 'dd/mm/yy' : ")
            day, month, year = inputDate.split('/')
            if int(year) < now.year or int(month) < now.month:
                print(
                    "Ne mozete unijeti projekciju na mjesec/godinu koji/koja" +
                    "je prosao/prosla.")
                continue
            if int(month) == now.month and int(day) < now.day:
                print('Ne mozete unijeti projekciju na dan koji je prosao.')
                continue
            datetime.datetime(int(year), int(month), int(day))
            break
        except:
            print("Unijeli ste nevalidan datum. Pokusajte ponovo.")
            continue
    while True:
        inputTime = input('Unesite vreme u kom zelite da pustite film - ')
        if check_time(inputTime) is False:
            print('Unijeli ste nevalidno vrijeme. Pokusajte ponovo')
            continue
        else:
            break
    my_date = inputDate
    my_time = inputTime
    events = get_events()
    event_same_date = find_event_on_same_date(
        events, my_date, hall_id)
    if(len(event_same_date) > 0):
        if (check_events_time(event_same_date,
                              my_time, movie['movie_duration'])) is False:
            print('Ne mozete pustiti film u to vrijeme. Pokusajte neko drugo.')
            return
        else:
            new_event = {}
            new_event["eventID"] = event_id
            new_event["movieID"] = movie['movieID']
            new_event["price"] = price
            new_event["dateTime"] = str(inputDate) + ' ' + str(inputTime)
            new_event["hallID"] = hall['hallID']
            new_event["seat_available"] = hall['seat_number']
            new_event["deleted"] = False
            events = get_events()
            events.append(new_event)
            write_to_file(events)
            print("Uspjesno ste dodali film.")
            return all_events()
    else:
        new_event = {}
        new_event["eventID"] = event_id
        new_event["movieID"] = movie['movieID']
        new_event["price"] = price
        new_event["dateTime"] = str(inputDate) + ' ' + str(inputTime)
        new_event["hallID"] = hall['hallID']
        new_event["seat_available"] = hall['seat_number']
        new_event["deleted"] = False
        events = get_events()
        events.append(new_event)
        write_to_file(events)
        print("Uspjesno ste dodali film.")
        return all_events()


def print_table(data):
    """
    Function print nice table
    """
    titles = ['ID', 'Datum i vrijeme', 'Sala',
              'Film', 'Trajanje', 'Br. mjesta', 'Cijena']
    event_ids = []
    date_and_times = []
    seat_numbers = []
    halls = []
    movies = []
    movie_duration = []
    prices = []

    i = 0
    while i < len(data):
        if data[i]["deleted"] is False:
            movie = find_movie_by_id(data[i]["movieID"])
            event_ids.append(data[i]["eventID"])
            date_and_times.append(data[i]["dateTime"])
            movies.append(movie["movie_name"])
            movie_duration.append(movie["movie_duration"])
            halls.append(data[i]["hallID"])
            seat_numbers.append(data[i]['seat_available'])
            prices.append(data[i]["price"])
        i += 1

    data = [titles] + list(
        zip(event_ids, date_and_times,
            halls, movies, movie_duration, seat_numbers, prices))

    for i, d in enumerate(data):
        line = '|'.join(str(x).ljust(20) for x in d)
        print(line)
        if i == 0:
            print('-' * len(line))


def print_table_movies(movies):
    """
    Function print nice table
    """
    titles = ['ID', 'Ime filma', 'Trajanje',
              'Tip']
    movie_ids = []
    movie_names = []
    movie_durations = []
    movie_types = []

    i = 0
    while i < len(movies):
        movie_ids.append(movies[i]["movieID"])
        movie_names.append(movies[i]["movie_name"])
        movie_durations.append(movies[i]["movie_duration"])
        movie_types.append(movies[i]["movie_type"])
        i += 1

    data = [titles] + list(
        zip(movie_ids, movie_names,
            movie_durations, movie_types))

    for i, d in enumerate(data):
        line = '|'.join(str(x).ljust(10) for x in d)
        print(line)
        if i == 0:
            print('-' * len(line))


def print_table_halls(halls):
    """
    Function print nice table
    """
    titles = ['ID', 'Broj mjesta']
    hall_ids = []
    seat_numbers = []

    i = 0
    while i < len(halls):
        hall_ids.append(halls[i]["hallID"])
        seat_numbers.append(halls[i]["seat_number"])
        i += 1

    data = [titles] + list(
        zip(hall_ids, seat_numbers))

    for i, d in enumerate(data):
        line = '|'.join(str(x).ljust(10) for x in d)
        print(line)
        if i == 0:
            print('-' * len(line))


def get_all_users():
    with open('../data/users.json', 'r') as data:
        return json.load(data)


def find_movie_by_id(movie_id):
    movies = []
    with open('../data/movies.json', 'r') as data:
        movies = json.load(data)
    for m in movies:
        if m['movieID'] == movie_id:
            return m
    return False


def find_hall_by_id(hallID):
    halls = []
    with open('../data/halls.json', 'r') as data:
        halls = json.load(data)
    for h in halls:
        if h['hallID'] == hallID:
            return h
    return False


def delete_event(event_id):
    events = get_events()
    for e in range(0, len(events), 1):
        if event_id == events[e]["eventID"]:
            events[e]['deleted'] = True
            with open('../data/events.json', 'w') as data:
                json_format = json.dumps(events)
                data.write(json_format)
            return True
    return False


def write_to_file(events):
    with open('../data/events.json', 'w') as data:
        json_format = json.dumps(events)
        data.write(json_format)


def sell_ticet():
    events = get_events()
    print_table(events)
    all_tickets = []
    while True:
        event = input('Unesite ID dogadjaja za koji zelite da kupite karte - ')
        e = find_by_id(int(event))
        try:
            len(e)
        except:
            continue

        if len(e) > 0:
            n_tickets = input('Unesite broj karata koji zelite - ')
            if int(n_tickets) < 0:
                print('Morate unijeti broj veci od 0.')
                continue
            if int(n_tickets) <= e[0]['seat_available']:
                print('Cijena iznosi - ' +
                      str(int(n_tickets) * e[0]['price']))
                price = int(n_tickets) * e[0]['price']
                e[0]['seat_available'] = e[0]['seat_available'] - \
                    int(n_tickets)
                tickets = get_all_tickets()
                if len(tickets) < 1:
                    new_ticket_id = 1
                else:
                    new_ticket_id = tickets[len(tickets) - 1]['id'] + 1
                some_data = {
                    "id": new_ticket_id,
                    "dateTime": str(datetime.datetime.now()),
                    "price": price,
                    "seller": get_username()
                }
                tickets.append(some_data)
                _update(e[0])
                with open('../data/tickets.json', 'w') as data:
                    js = json.dumps(tickets)
                    data.write(js)
                print('Uspjesno ste dodali stavku na racun.')
                break
            else:
                print('Nema dovoljno mesta za taj iznos karata.')
                continue
        else:
            continue
    return


def check_time(inputTime):
    insered_time = inputTime.split(':')
    if len(insered_time) == 2:
        if int(insered_time[0]) < 0 or int(insered_time[0]) > 23 or \
                int(insered_time[1]) < 0 or int(insered_time[1]) > 59:
            return False
        else:
            return True
    else:
        return False

# DATE TIME CHECK


def find_event_on_same_date(events, my_date, hall_id, event_id=None):
    events_on_same_date = []
    for e in events:
        if e['eventID'] == event_id:
            continue
        event_date_time_splited = e['dateTime'].split(' ')
        event_date = event_date_time_splited[0]
        event_time = event_date_time_splited[1]
        if event_date == my_date and e['deleted'] is False and \
                e['hallID'] == hall_id:
            movie = find_movie_by_id(e['movieID'])
            e['duration'] = movie["movie_duration"]
            events_on_same_date.append(e)
    return events_on_same_date


def check_events_time(events, my_time, my_movie_duration):
    choosen_time = my_time.split(':')
    choosen_time_in_minutes = (
        int(choosen_time[0]) * 60) + int(choosen_time[1])
    before = check_before(choosen_time_in_minutes, events)
    after = check_after(choosen_time_in_minutes, events)
    if choosen_time_in_minutes >= before and choosen_time_in_minutes +\
            my_movie_duration < after:
        return True
    else:
        return False


def check_before(my_minutes, events):
    before = 0
    duration_movie = 0
    for e in events:
        event_date_time_splited = e['dateTime'].split(' ')
        event_time = event_date_time_splited[1].split(':')
        event_time_in_minutes = int(event_time[0]) * 60 + int(event_time[1])
        if int(event_time_in_minutes) < int(my_minutes) and \
                int(event_time_in_minutes) > int(before):
            before = event_time_in_minutes
            duration_movie = e['duration']
    return int(before) + int(duration_movie)


def check_after(my_minutes, events):
    after = 1500
    duration_movie = 0
    for e in events:
        event_date_time_splited = e['dateTime'].split(' ')
        event_time = event_date_time_splited[1].split(':')
        event_time_in_minutes = int(
            event_time[0]) * 60 + int(event_time[1])
        if int(event_time_in_minutes) > int(my_minutes) and int(after) >\
                int(event_time_in_minutes):
            after = event_time_in_minutes
            duration_movie = e['duration']
    return int(after)


def get_all_movies():
    with open('../data/movies.json', 'r') as data:
        return json.load(data)


def get_all_halls():
    with open('../data/halls.json', 'r') as data:
        return json.load(data)


def update_event():
    events = get_events()
    print_table(events)

    try:
        event_id = input(
            'Unesite ID dogadjaja koji zelite da promijenite - ')
        event = find_by_id(int(event_id))
        if len(event) < 0:
            return
        print('1. Film 2. Cijenu 3. Datum i vrijeme 4. Salu')
        change = input('Izaberite koju stavku zelite da izmenite: ')
        if int(change) == 1:
            print_table_movies(get_all_movies())
            movie_id = input(
                'Unesite id filma koji zelite da izaberete - ')
            movie = find_movie_by_id(int(movie_id))
            print(event[0]['movieID'])
            event[0]['movieID'] = movie['movieID']
            _update(event[0])
            print('Uspjesno ste izmjenili projekciju. ')
            return
        elif int(change) == 2:
            price = input('Unesite novu cijenu filma - ')
            event[0]['price'] = float(price)
            _update(event[0])
            print('Uspjesno ste izmjenili projekciju.')
            return
        elif int(change) == 3:
            movie = find_movie_by_id(event[0]['movieID'])
            # DATUM I VREME
            while True:
                try:
                    now = datetime.datetime.now()
                    inputDate = input(
                        "Unesite datum u formatu 'dd/mm/yy' : ")
                    day, month, year = inputDate.split('/')
                    if int(year) < now.year or int(month) < now.month:
                        print(
                            "Ne mozete unijeti projekciju na mjesec/godinu" +
                            "koji/koja je prosao/prosla.")
                        continue
                    if int(month) == now.month and int(day) < now.day:
                        print(
                            'Ne mozete unijeti projekciju na' +
                            'dan koji je prosao.')
                        continue
                    datetime.datetime(int(year), int(month), int(day))
                    break
                except:
                    print("Unijeli ste nevalidan datum. Pokusajte ponovo.")
                    continue
            while True:
                inputTime = input(
                    'Unesite vreme u kom zelite da pustite film - ')
                if check_time(inputTime) is False:
                    print('Unijeli ste nevalidno vrijeme. Pokusajte ponovo')
                    continue
                else:
                    break
            my_date = inputDate
            my_time = inputTime
            events = get_events()
            event_same_date = find_event_on_same_date(
                events, my_date, event[0]['hallID'], event[0]['eventID'])
            if(len(event_same_date) > 0):
                if (check_events_time(event_same_date,
                                      my_time, movie['movie_duration'])) \
                        is False:
                    print(
                        'Ne mozete pustiti film u to vrijeme. Pokusajte' +
                        'neko drugo.')
                    return
                else:
                    event[0]['dateTime'] = str(my_date) + ' ' + str(my_time)
                    _update(event[0])
                    print('Uspjesno ste izmjenili projekciju')
                    return
            else:
                event[0]['dateTime'] = str(my_date) + ' ' + str(my_time)
                _update(event[0])
                print('Uspjesno ste izmjenili projekciju')
                return

        elif int(change) == 4:
            print_table_halls(get_all_halls())
            hallID = input('Unesite novi ID sale - ')
            hall = find_hall_by_id(hallID)
            event[0]['hallID'] = hall['hallID']
            event[0]['seat_available'] = hall['seat_number']
            _update(event[0])
            print('Uspjesno ste izmjenili projekciju.')
            return
        else:
            print('Ne postoji ta opcija pokusajte ponovo.')
            return
    except Exception as e:
        print(e)
        print('Doslo je do greske prilikom izmjene. Pokusajte ponovo. ')
        return


def _update(event):
    events = get_events()
    for e in range(0, len(events), 1):
        if events[e]['eventID'] == event['eventID']:
            events[e] = event
    with open('../data/events.json', 'w') as data:
        json_data = json.dumps(events)
        data.write(json_data)


def get_all_tickets():
    with open('../data/tickets.json', 'r') as data:
        return json.load(data)


def add_new_user():
    fname = input('Unesite ime - ')
    lname = input('Unesite prezime -')
    while True:
        username = input('Korisinicko ime - ')
        if check_if_username_exist(username) is True or len(username) <= 1:
            print(
                'Korisnicko ime zauzeto ili duzina karaktera manja od 1. ' +
                'Pokusajte neko drugo.')
            continue
        break
    password = input('Unesite sifru - ')
    if len(password) < 1:
        print('Sifra ne moze biti prazna. Pokusajte ponovo.')
        return
    role = input('Unesite rolu - ')
    if len(role) < 1:
        print('Rola ne moze biti prazna. Pokusajte ponovo.')
        return
    users = get_all_users()
    new_user = {
        "id": users[len(users) - 1]['id'] + 1,
        "name": fname,
        "lastname": lname,
        "username": username,
        "password": password,
        "role": role
    }
    users.append(new_user)
    with open('../data/users.json', 'w') as data:
        js = json.dumps(users)
        data.write(js)
    print('Uspjesno ste dodali korisnika')


def check_if_username_exist(username):
    users = get_all_users()
    for u in users:
        if u['username'] == username:
            return True
    return False


def print_table_tickets():
    """
    Function print nice table
    """
    tickets = get_all_tickets()
    titles = ['ID', 'Datum i vreme', 'Cena',
              'Prodavac']
    tickets_ids = []
    tickets_dates = []
    tickets_price = []
    tickets_sellers = []

    i = 0
    while i < len(tickets):
        tickets_ids.append(tickets[i]["id"])
        tickets_dates.append(tickets[i]["dateTime"])
        tickets_price.append(tickets[i]["price"])
        tickets_sellers.append(tickets[i]["seller"])
        i += 1

    data = [titles] + list(
        zip(tickets_ids, tickets_dates,
            tickets_price, tickets_sellers))

    for i, d in enumerate(data):
        line = '|'.join(str(x).ljust(30) for x in d)
        print(line)
        if i == 0:
            print('-' * len(line))
