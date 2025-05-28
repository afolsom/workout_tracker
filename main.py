
import sqlite3
import os
import time

##### JupyterHub Path
db_path = "workout_tracker_db.db"

##### PC Path
#db_path = "C:/Users/awfma/DataspellProjects/workout_tracker/workout_tracker_db.db"

##### Android Path
#db_path = "/storage/emulated/0/Documents/workout_tracker/workout_tracker_db.db"

def create_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users "
                   "(user_id INTEGER PRIMARY KEY, "
                   "user_name TEXT, "
                   "password TEXT, "
                   "first_name TEXT, "
                   "last_name TEXT, "
                   "email TEXT, "
                   "created_date DATE, "
                   "modified_date DATE, "
                   "deleted_date DATE)")

    cursor.execute("CREATE TABLE major_muscles "
                   "(major_muscle_id INTEGER PRIMARY KEY, "
                   "user_id INTEGER, "
                   "name TEXT, "
                   "created_date DATE, "
                   "modified_date DATE, "
                   "deleted_date DATE)")

    cursor.execute("CREATE TABLE exercises "
                   "(exercise_id INTEGER PRIMARY KEY, "
                   "user_id INTEGER, "
                   "major_muscle_id INTEGER, "
                   "name TEXT, "
                   "created_date DATE, "
                   "modified_date DATE, "
                   "deleted_date DATE)")

    cursor.execute("CREATE TABLE session "
                   "(session_id INTEGER PRIMARY KEY, "
                   "user_id INTEGER, "
                   "created_date DATE, "
                   "modified_date DATE, "
                   "deleted_date DATE)")

    cursor.execute("CREATE TABLE session_performance "
                   "(performance_id INTEGER PRIMARY KEY, "
                   "session_id INTEGER, "
                   "major_muscle_id INTEGER, "
                   "exercise_id INTEGER, "
                   "user_id INTEGER, "
                   "sets INTEGER, "
                   "reps INTEGER, "
                   "weight INTEGER, "
                   "created_date DATE, "
                   "started_dtm DATE, "
                   "ended_dtm DATE, "
                   "modified_date DATE, "
                   "deleted_date DATE)")

    conn.commit()
    return


if os.path.exists(db_path):
    print("Database ready!")
else:
    create_db()
    print("Database Created.")


user_name = input("Enter your username: ")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
user_id_test = conn.execute("SELECT distinct user_id FROM users WHERE user_name = ?", (user_name,)).fetchone()

if user_id_test is None:
    print("User Name does not exist.")
    check = input("Do you want to create a new user? (y/n): ")
    if check.upper() == "Y":
        user_name = input("Enter Username: ")
        password = input("Enter Password: ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last name: ")
        email = input("Enter Email: ")
        conn.execute("INSERT INTO users(user_name, password, first_name, last_name, email, created_date, modified_date, deleted_date) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL)", (user_name, password, first_name, last_name, email))
        conn.commit()
        print("Please run again to sign in")
    else:
        print("closing Script")
else:
    print(f"Welcome {user_name}!")

user_id = int(list(user_id_test)[0])
print(f"user_id = {user_id}")

major_muscles_test = conn.execute("SELECT DISTINCT name FROM major_muscles WHERE user_id = ?", (user_id,)).fetchone()

default_major_muscles = ['Back', 'Arms', 'Legs', 'Shoulders', 'Core', 'Chest', 'Cardio']
default_exercises = [
    ('Back', 'Weighted Row'),
    ('Back', 'One Arm Dumbbell Row'),
    ('Back', 'Reverse Fly'),
    ('Back', 'Bent Over Row'),
    ('Back', 'Inverted Row'),
    ('Back', 'Pull Downs'),
    ('Back', 'Dead lifts'),
    ('Arms', 'Dumbbell Curls'),
    ('Arms', 'Barbell Curls'),
    ('Arms', 'Hammer Curls'),
    ('Arms', 'Tricep Dips'),
    ('Arms', 'Overhead Tricep Pulls'),
    ('Arms', 'Skull Crushers'),
    ('Arms', 'Overhead Tricep Dumbbell Dips'),
    ('Arms', 'Wrist Curls'),
    ('Legs', 'Leg Press'),
    ('Legs', 'Squats'),
    ('Legs', 'Weighted Calf Raises'),
    ('Legs', 'Leg Extension'),
    ('Legs', 'Weighted Lunges'),
    ('Legs', 'Leg Curls'),
    ('Shoulders', 'Overhead Press'),
    ('Shoulders', 'Dumbbell Side Delt Raises'),
    ('Shoulders', 'Shoulder Lifts'),
    ('Shoulders', 'Cable Side Delt Raises'),
    ('Shoulders', 'Lat Pulls'),
    ('Shoulders', 'Barbell Raise and Lifts'),
    ('Core', 'Crunch'),
    ('Core', 'Plank'),
    ('Core', 'Bicycle Crunch'),
    ('Core', 'Leg Raises'),
    ('Core', 'Weighted Twist'),
    ('Core', 'V-Ups'),
    ('Chest', 'Bench Press'),
    ('Chest', 'Dumbbell Press'),
    ('Chest', 'Incline Bench Press'),
    ('Chest', 'Decline Dumbbell Press'),
    ('Chest', 'Butterflies'),
    ('Chest', 'Cable Press'),
    ('Cardio', 'Elliptical'),
    ('Cardio', 'Treadmill'),
    ('Cardio', 'Jump Rope')
    ]

if major_muscles_test is None:
    default = input("You do not have any muscle groups or exercises in the database, would you like to insert the default major muscle groups and exercises? (y/n)")
    if default.upper() == 'Y':
        for muscle in default_major_muscles:
            conn.execute("INSERT INTO major_muscles (user_id, name, created_date, modified_date, deleted_date) VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL)", (user_id, muscle))
            conn.commit()

        for muscle, exercise in default_exercises:
            muscle_id = int(list(conn.execute("SELECT DISTINCT major_muscle_id FROM major_muscles WHERE name = ?", (muscle,)).fetchone())[0])
            conn.execute("INSERT INTO exercises (user_id, major_muscle_id, name, created_date, modified_date, deleted_date) VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL)", (user_id, muscle_id, exercise))
            conn.commit()



def insert_major_muscle():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    check = input("Would you like to add another major muscle? (y/n) ")
    while check.upper() == "Y":
        major_muscles = conn.execute("SELECT DISTINCT name FROM major_muscles WHERE user_id = ?", (user_id,)).fetchall()

        print("Currently Existing Major Muscles: ")
        for row in major_muscles:
            name = list(row)[0]
            print(f"{name}")

        major_muscle = input("Enter Major Muscle: ")

        conn.execute("INSERT INTO major_muscles(user_id, name, created_date, modified_date, deleted_date) VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL)", (user_id, major_muscle))

        conn.commit()
        print("Major Muscle Added to Database!")
        check = input("Would you like to add another major muscle? (y/n) ")


def insert_exercise():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    check = input("Would you like to add another exercise? (y/n) ")
    while check.upper() == "Y":
        major_muscles = conn.execute("SELECT DISTINCT major_muscle_id, name FROM major_muscles WHERE user_id = ?", (user_id,)).fetchall()

        print("Options for Major Muscle: ")
        for row in major_muscles:
            id = list(row)[0]
            name = list(row)[1]
            print(f"{id} - {name}")

        major_muscle = int(input("Enter the number associated with a major muscle: "))

        exercises = conn.execute("SELECT DISTINCT name FROM exercises WHERE major_muscle_id = (?) AND user_id = ?", (major_muscle, user_id)).fetchall()

        print("Exercises Already Existing for Major Muscle: ")
        for row in exercises:
            name = list(row)[0]
            print(f"{name}")

        exercise = input("Enter the Exercise Name to Add: ")

        conn.execute("INSERT INTO exercises(user_id, major_muscle_id, name, created_date, modified_date, deleted_date) VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL)",(user_id, major_muscle, exercise))

        conn.commit()
        print("Exercise Added to Database!")
        check = input("Would you like to add another exercise? (y/n) ")


mod_input_start = input("Would you like to modify or view sessions, exercises, or major muscles? (y/n) ")
while mod_input_start.upper() == "Y":
    print("1 - View the currently available Major muscles and exercises")
    print("2 - Add another major muscle group")
    print("3 - Add another exercise")
    print("4 - Delete a recent session")
    print("5 - Add an exercise to a recent session")
    print("6 - Cancel")
    mod_input = input("Which option above would you like to do?")
    if mod_input.upper() == "1":
        current_muscles = conn.execute("SELECT DISTINCT m.name, e.name FROM major_muscles m LEFT JOIN exercises e on e.major_muscle_id = m.major_muscle_id WHERE m.user_id = ? ORDER BY m.name, e.name", (user_id,)).fetchall()
        if len(current_muscles) == 0:
            print("No Major Muscles and Exercises Added to Database!")
        else:
            for muscle, exercise in current_muscles:
                print(f"{muscle} - {exercise}")
    elif mod_input.upper() == "2":
        insert_major_muscle()
    elif mod_input.upper() == "3":
        insert_exercise()
    elif mod_input.upper() == "4":
        sessions_delete = conn.execute("SELECT DISTINCT session_id, datetime(created_date, 'localtime') FROM session WHERE user_id = ? ORDER BY created_date DESC LIMIT 6", (user_id,)).fetchall()
        if len(sessions_delete) == 0:
            print("No Sessions to Delete!")
        else:
            print("Six most recent sessions:")
            for row in sessions_delete:
                id = list(row)[0]
                date = list(row)[1]
                print(f"{id} - {date}")
            ss_id_delete = int(input("Enter the id of the session to delete: "))
            conn.execute("DELETE FROM session WHERE session_id = ?", (ss_id_delete,))
            conn.execute("DELETE FROM session_performance WHERE session_id = ?", (ss_id_delete,))
            conn.commit()
    elif mod_input.upper() == "5":
        sessions = conn.execute("SELECT DISTINCT session_id, datetime(created_date, 'localtime') FROM session WHERE user_id = ? ORDER BY created_date DESC LIMIT 6", (user_id,)).fetchall()
        print("Six most recent sessions:")
        for row in sessions:
            id = list(row)[0]
            date = list(row)[1]
            print(f"{id} - {date}")
        ss_id = int(input("Enter the id of the session to modify: "))
        check = input("Would you like to add an exercise to a recent session? (y/n) ")
        while check.upper() == "Y":
            major_muscles = conn.execute("SELECT DISTINCT major_muscle_id, name FROM major_muscles WHERE user_id = ?", (user_id,)).fetchall()

            print("Options for Major Muscle: ")
            for row in major_muscles:
                id = list(row)[0]
                name = list(row)[1]
                print(f"{id} - {name}")

            major_muscle = int(input("Enter the number associated with a major muscle: "))

            exercises = conn.execute("SELECT DISTINCT exercise_id, name FROM exercises WHERE major_muscle_id = (?) AND user_id = ? ORDER BY exercise_id", (major_muscle, user_id)).fetchall()

            print("Exercises for this major muscle: ")
            for row in exercises:
                id = list(row)[0]
                name = list(row)[1]
                print(f"{id} - {name}")

            exercise = input("Enter the Exercise # to Add: ")
            sets = int(input("Enter the number of sets you did: "))
            weight = int(input("Enter the maximum weight you did in a single set: "))
            reps = int(input("Enter the number of reps for the max weight set: "))

            conn.execute("INSERT INTO session_performance(session_id, user_id, major_muscle_id, exercise_id, sets, weight, reps, created_date, modified_date, deleted_date) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL)",(ss_id, user_id, major_muscle, exercise, sets, weight, reps))

            conn.commit()
            print("Exercise Added to Session!")
            check = input("Would you like to add another exercise? (y/n) ")

    else:
        break
    mod_input_start = input("Would you like to modify or view any additional sessions, exercises, or major muscles? (y/n) ")



last_session = conn.execute("SELECT DISTINCT datetime(s.created_date, 'localtime') as last_session_date, m.name FROM session s LEFT JOIN session_performance sp on s.session_id = sp.session_id LEFT JOIN major_muscles m on m.major_muscle_id = sp.major_muscle_id WHERE s.session_id IN (SELECT DISTINCT sl.session_id FROM session sl WHERE sl.user_id = ? ORDER BY sl.created_date DESC LIMIT 1) ORDER BY sp.created_date DESC", (user_id,)).fetchall()
print("In your last session, you worked the following major muscle groups:")
if len(last_session) > 0:
    for ls in last_session:
        ls_date = list(ls)[0]
        ls_muscle = list(ls)[1]
        print(f"Date: {ls_date}, Major Muscle: {ls_muscle}")
else:
    print("No previous session found.")


def session():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    conn.execute("INSERT INTO session(user_id, created_date, modified_date, deleted_date) VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL)", (user_id,))
    conn.commit()
    session_id = int(list(conn.execute("SELECT DISTINCT session_id FROM session where user_id = ? ORDER BY created_date DESC LIMIT 1", (user_id,)).fetchone())[0])

    start_with_cardio = input("Would you like to start with Cardio?  (y/n) ")
    if start_with_cardio.upper() == "Y":
        cardio_muscle_id = list(conn.execute("SELECT distinct major_muscle_id FROM major_muscles m WHERE name = 'Cardio'").fetchone())[0]
        cardio_exercises = conn.execute("SELECT DISTINCT e.exercise_id, e.name FROM exercises e WHERE major_muscle_id IN (?) ORDER BY RANDOM() LIMIT 1", (cardio_muscle_id, )).fetchmany(1)
        for row in cardio_exercises:
            id = list(row)[0]
            name = list(row)[1]
            print(f"Let's do cardio exercise {name}")
            start_date_time = time.time()
            input("Enter y when you are finished: ")
            end_date_time = time.time()
            conn.execute("INSERT INTO session_performance(session_id, major_muscle_id, exercise_id, user_id, created_date, started_dtm, ended_dtm, modified_date, deleted_date) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, CURRENT_TIMESTAMP, NULL)", (session_id, cardio_muscle_id, id, user_id, start_date_time, end_date_time))
            conn.commit()


    #major_muscles = conn.execute("SELECT DISTINCT major_muscle_id, name FROM major_muscles").fetchall()
    major_muscles = conn.execute("SELECT DISTINCT m.major_muscle_id, m.name FROM major_muscles m WHERE m.major_muscle_id NOT IN (SELECT DISTINCT sp.major_muscle_id FROM session_performance sp WHERE DATE(sp.created_date) BETWEEN DATE('now', '-4 day') AND DATE('now'))").fetchall()

    print("Options for Major Muscle: ")
    for row in major_muscles:
        id = list(row)[0]
        name = list(row)[1]
        print(f"{id} - {name}")

    major_muscle_1 = int(input("Enter 1 out of 2 Major Muscle Groups for today's session (#): "))
    major_muscle_2 = int(input("Enter 2 out of 2 Major Muscle Groups for today's session (#): "))
    exercise_count = int(input("Enter number of exercises you would like to do (up to 6): "))

    session_exercises = conn.execute("SELECT distinct e.major_muscle_id, e.exercise_id, e.name FROM exercises e WHERE e.exercise_id IN (SELECT DISTINCT ei.exercise_id from exercises ei WHERE ei.major_muscle_id IN (?, ?) ORDER BY RANDOM() LIMIT 6)", (major_muscle_1, major_muscle_2)).fetchmany(exercise_count)
    for row in session_exercises:
        major_muscle_id = int(list(row)[0])
        exercise_id = int(list(row)[1])
        exercise_name = list(row)[2]
        print(f"Let's do the {exercise_name} exercise!")

        last_time_exercises = conn.execute("SELECT distinct sets, weight, reps, ROUND(((ended_dtm - started_dtm)/60.0),1) as duration FROM session_performance sp where user_id = ? AND exercise_id = ? ORDER BY sp.created_date DESC", (user_id, exercise_id)).fetchone()
        if last_time_exercises is not None:
            last_time_sets = list(last_time_exercises)[0]
            last_time_weight = list(last_time_exercises)[1]
            last_time_reps = list(last_time_exercises)[2]
            last_time_duration = list(last_time_exercises)[3]
            print(f"Last time on this exercise, you did {last_time_sets} sets, {last_time_reps} reps, at a max weight of {last_time_weight} for a duration of {last_time_duration} minutes")
        else:
            print("you have not done this exercise before.")

        start_date_time = time.time()
        sets = int(input("Enter the number of sets you did: "))
        weight = int(input("Enter the maximum weight you did in a single set: "))
        reps = int(input("Enter the number of reps for the max weight set: "))
        end_date_time = time.time()
        conn.execute("INSERT INTO session_performance(session_id, major_muscle_id, exercise_id, user_id, sets, reps, weight, created_date, started_dtm, ended_dtm, modified_date, deleted_date) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, CURRENT_TIMESTAMP, NULL)", (session_id, major_muscle_id, exercise_id, user_id, sets, reps, weight, start_date_time, end_date_time))
        conn.commit()
        print("exercise completed!")

def manual_session():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    conn.execute("INSERT INTO session(user_id, created_date, modified_date, deleted_date) VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL)", (user_id,))
    conn.commit()
    session_id = int(list(conn.execute("SELECT DISTINCT session_id FROM session where user_id = ? ORDER BY created_date DESC LIMIT 1", (user_id,)).fetchone())[0])
    check = input("Would you like to add an exercise to your session? (y/n) ")
    while check.upper() == "Y":
        major_muscles = conn.execute("SELECT DISTINCT major_muscle_id, name FROM major_muscles WHERE user_id = ?", (user_id,)).fetchall()

        print("Options for Major Muscle: ")
        for row in major_muscles:
            id = list(row)[0]
            name = list(row)[1]
            print(f"{id} - {name}")

        major_muscle = int(input("Enter the number associated with a major muscle: "))

        exercises = conn.execute("SELECT DISTINCT exercise_id, name FROM exercises WHERE major_muscle_id = (?) AND user_id = ? ORDER BY exercise_id", (major_muscle, user_id)).fetchall()

        print("Exercises for this major muscle: ")
        for row in exercises:
            id = list(row)[0]
            name = list(row)[1]
            print(f"{id} - {name}")

        exercise = input("Enter the Exercise # to Add: ")
        sets = int(input("Enter the number of sets you did: "))
        weight = int(input("Enter the maximum weight you did in a single set: "))
        reps = int(input("Enter the number of reps for the max weight set: "))

        conn.execute("INSERT INTO session_performance(session_id, user_id, major_muscle_id, exercise_id, sets, weight, reps, created_date, modified_date, deleted_date) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL)",(session_id, user_id, major_muscle, exercise, sets, weight, reps))

        conn.commit()
        print("Exercise Added to Session!")
        check = input("Would you like to add another exercise? (y/n) ")


session_check = input("Would you like to start a session? (y/n) ")
if session_check.upper() == "Y":
    manual_auto = input("Would like to to start an Auto Session (y) or a Manual Session (n)?")
    if manual_auto.upper() == "Y":
        session()
        print("Session Completed!")
    else:
        manual_session()
        print("Session Completed!")
else:
    print("closing Script")

