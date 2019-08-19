from backend.values import *
from datetime import datetime, timedelta
from backend.models import User, Course, db

FIRST_NAME = "Test"
LAST_NAME = "User"
EMAIL = "@test.com"
UNIQUE_USERS = [
    ("admin", "test", "admin@test.com", ACCESS[ADMIN], True, True, True),
    ("organizer", "test", "organizer@test.com", ACCESS[ORGANIZER], True, True, True),
    ("treasurer", "test", "treasurer@test.com", ACCESS[TREASURER], False, False, False)
]
USERS = [
    ("S", LAST_NAME, EMAIL, ACCESS[MEMBER], True, False, False),
    ("S", LAST_NAME, EMAIL, ACCESS[MEMBER], True, False, False),
    ("S", LAST_NAME, EMAIL, ACCESS[MEMBER], True, False, False),
    ("SI", LAST_NAME, EMAIL, ACCESS[MEMBER], True, True, False),
    ("SI", LAST_NAME, EMAIL, ACCESS[MEMBER], True, True, False),
    ("SI", LAST_NAME, EMAIL, ACCESS[MEMBER], True, True, False),
    ("SM", LAST_NAME, EMAIL, ACCESS[MEMBER], True, False, True),
    ("SM", LAST_NAME, EMAIL, ACCESS[MEMBER], True, False, True),
    ("SM", LAST_NAME, EMAIL, ACCESS[MEMBER], True, False, True),
    ("SIM", LAST_NAME, EMAIL, ACCESS[MEMBER], True, True, True),
    ("SIM", LAST_NAME, EMAIL, ACCESS[MEMBER], True, True, True),
    ("SIM", LAST_NAME, EMAIL, ACCESS[MEMBER], True, True, True),
    ("I", LAST_NAME, EMAIL, ACCESS[MEMBER], False, True, False),
    ("I", LAST_NAME, EMAIL, ACCESS[MEMBER], False, True, False),
    ("I", LAST_NAME, EMAIL, ACCESS[MEMBER], False, True, False),
    ("IM", LAST_NAME, EMAIL, ACCESS[MEMBER], False, True, True),
    ("IM", LAST_NAME, EMAIL, ACCESS[MEMBER], False, True, True),
    ("IM", LAST_NAME, EMAIL, ACCESS[MEMBER], False, True, True),
    ("M", LAST_NAME, EMAIL, ACCESS[MEMBER], False, False, True),
    ("M", LAST_NAME, EMAIL, ACCESS[MEMBER], False, False, True),
    ("M", LAST_NAME, EMAIL, ACCESS[MEMBER], False, False, True)
]


def test_users():
    for d in UNIQUE_USERS:
        user = User()
        user.first_name = d[0]
        user.last_name = d[1]
        user.email = d[2]
        user.access = d[3]
        user.salcie = d[4]
        user.incie = d[5]
        user.mucie = d[6]
        user.is_active = True
        user.set_password(user.first_name)
        db.session.add(user)
        db.session.commit()
    for i, d in enumerate(USERS):
        user = User()
        user.first_name = f"{d[0]}{i}"
        user.last_name = d[1]
        user.email = f"{user.first_name}{d[2]}"
        user.access = d[3]
        user.salcie = d[4]
        user.incie = d[5]
        user.mucie = d[6]
        user.is_active = True
        user.set_password(user.first_name)
        db.session.add(user)
        db.session.commit()


START_YEAR = 2019

COURSES = [
    ("NSE", datetime(START_YEAR, 11, 21, 20, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Horstkantine", "nl", "incie", "EW, CC", ""),
    ("Harambee", datetime(START_YEAR, 11, 22, 20, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Ravelijn", "nl", "incie", "No preference", ""),
    ("Skeuvel", datetime(START_YEAR + 1, 1, 16, 21, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Sportzaal Helmerhoek", "en", "incie", "QS, CC", ""),
    ("ConcepT", datetime(START_YEAR + 1, 1, 30, 19, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Horstkantine", "nl", "incie", "QS", "Openingsdans voor gala QS walking on sunshine"),
    ("Arago (1)", datetime(START_YEAR + 1, 2, 4, 20, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Horstkantine", "nl", "incie", "QS, CC", "1 van 3, geen mic"),
    ("Abacus, Inter-Actief, Scintilla", datetime(START_YEAR + 1, 2, 11, 19, 0, 0, 0), timedelta(hours=1, minutes=30),
     "SmartXP", "en", "incie", "QS, CC", "geen mic, oude laptop audio crackelt"),
    ("Arago (2)", datetime(START_YEAR + 1, 2, 13, 20, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Horstkantine", "nl", "incie", "QS, CC (Herhaling), SS", "2 van 3"),
    ("Communiqué, Dimensie, Sirius", datetime(START_YEAR + 1, 2, 14, 20, 30, 0, 0), timedelta(hours=1, minutes=30),
     "Mystiek Theater Enschede", "en", "incie", "EW, RB", "onduidelijkheden rondom organisatie"),
    ("Arago (3)", datetime(START_YEAR + 1, 2, 25, 20, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Horstkantine", "unknown", "incie", "QS, CC, SS (Herhaling)", "3 van 3"),
    ("Stress (1)", datetime(START_YEAR + 1, 2, 27, 20, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Ravelijn", "unknown", "incie", "QS, CC", "1 dans als openingsdans, tweede 'tussendoor'"),
    ("Stress (2)", datetime(START_YEAR + 1, 3, 6, 20, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Ravelijn", "unknown", "incie", "Herhaling", "nadruk op CC"),
    ("Astatine, Proto", datetime(START_YEAR + 1, 3, 7, 19, 0, 0, 0), timedelta(hours=1, minutes=30),
     "SmartXP", "en", "incie", "CC, JV", "vb nummers beatles - twist and shout en monkeys - i am a believer"),
    ("Divide et Medica", datetime(START_YEAR + 1, 3, 20, 21, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Spinnerstraat 27, Gymzaal", "unknown", "incie", "QS, CC", ""),
    ("4 happy feet", datetime(START_YEAR + 1, 3, 25, 21, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Audiozaal", "unknown", "incie", "QS, CC", ""),
    ("NSK podiumdans", datetime(START_YEAR + 1, 3, 31, 12, 0, 0, 0), timedelta(hours=1, minutes=0),
     "Sportzaal 4", "unknown", "incie", "QS, CC", "voor podiumdansers"),
    ("AEGEE", datetime(START_YEAR + 1, 4, 3, 19, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Horstkantine", "unknown", "incie", "QS, CC", ""),
    ("Daedalus", datetime(START_YEAR + 1, 4, 10, 19, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Horstkantine", "unknown", "incie", "QS, CC", "1 of 2"),
    ("Daedalus", datetime(START_YEAR + 1, 4, 17, 19, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Horstkantine", "unknown", "incie", "QS, CC", "2 of 2"),
    ("MISC", datetime(START_YEAR + 1, 4, 18, 20, 15, 0, 0), timedelta(hours=1, minutes=30),
     "Mina Krusemanstraat, gymzaal", "unknown", "incie", "QS, JV", ""),
    ("Phoenix Lacrosse", datetime(START_YEAR + 1, 4, 25, 20, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Unknown", "unknown", "incie", "QS, CC", ""),
    ("Atlantis", datetime(START_YEAR + 1, 4, 29, 20, 0, 0, 0), timedelta(hours=1, minutes=30),
     "SmartXP", "unknown", "incie", "QS, CC", ""),

    ("Communiqué", datetime(START_YEAR, 11, 23, 16, 30, 0, 0), timedelta(hours=1, minutes=30),
     "", "en", "salcie", "", ""),
    ("Damesdispuut MonduDamo", datetime(START_YEAR, 11, 28, 21, 0, 0, 0), timedelta(hours=1, minutes=30),
     "", "en", "salcie", "", ""),
    ("Dance Fever", datetime(START_YEAR + 1, 1, 23, 20, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Nijmegen", "en", "salcie", "", ""),
    ("4 happy feet", datetime(START_YEAR + 1, 3, 21, 18, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Audiozaal", "en", "salcie", "", ""),
    ("Damesdispuut Spooky", datetime(START_YEAR + 1, 3, 30, 16, 0, 0, 0), timedelta(hours=1, minutes=30),
     "Pakkerij, Oude markt 24", "nl", "salcie", "", ""),
    ("NSK podiumdans", datetime(START_YEAR + 1, 3, 31, 13, 30, 0, 0), timedelta(hours=1, minutes=0),
     "Sportzaal 4", "nl", "salcie", "", ""),
]


def course_request_data(data):
    return {
        "requested_by": data[0],
        "date": data[1],
        "duration": data[2],
        "location": data[3],
        "language": data[4],
        "committee": data[5],
        "dances": data[6],
        "notes": data[7],
    }


def test_courses():
    for c in COURSES:
        Course.create(course_request_data(c))
