import sqlite3
from sqlite3 import Error
import csv
import pickle
import numpy as np
import io
from database_component.encryption import encrypt_heart_recording, decrypt_heart_recording
from database_component.hashing import sign, verify


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)


def create_health_data_tables():
    sql_create_patients_table = """CREATE TABLE IF NOT EXISTS patients (
                                    id integer PRIMARY KEY,
                                    age integer,
                                    contact varchar,
                                    physician_id integer,
                                    FOREIGN KEY (physician_id) REFERENCES physicians (id)
                                );"""

    sql_create_health_records_table = """CREATE TABLE IF NOT EXISTS healthrecords (
                                    id integer PRIMARY KEY,
                                    health_record varchar,
                                    patient_id integer,
                                    FOREIGN KEY (patient_id) REFERENCES patients (id)
                                );"""

    sql_create_auscultations_table = """CREATE TABLE IF NOT EXISTS auscultations (
                                    id integer PRIMARY KEY,
                                    heart_recording varchar,
                                    recording_information varchar,
                                    patient_id integer,
                                    FOREIGN KEY (patient_id) REFERENCES patients (id)
                                );"""

    sql_create_physicians_table = """CREATE TABLE IF NOT EXISTS physicians (
                                    id integer PRIMARY KEY,
                                    contact varchar
                                );"""

    database = "heart_sound.db"

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_patients_table)
        create_table(conn, sql_create_health_records_table)
        create_table(conn, sql_create_auscultations_table)
        create_table(conn, sql_create_physicians_table)
    else:
        print("Error! Cannot create database connection.")

    conn.commit()
    conn.close()


def fill_tables_with_mock_data():
    with open('../heart_sound_classification/heart_sound_data.pickle', "rb") as recordings:
        db_recordings = pickle.load(recordings)[0:5]

    data = 'mock_data.csv'
    patient_ids = []
    patient_ages = []
    patient_contact = []
    patient_phys_ids = []
    record_ids = []
    health_records = []
    health_patient_ids = []
    auscultation_ids = []
    auscultation_info = []
    auscultation_patient_ids = []
    physician_ids = []
    physician_contact = []

    with open (data) as data_file:
        csv_reader = csv.reader(data_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                patient_ids.append(row[0])
                patient_ages.append(row[1])
                patient_contact.append(row[2])
                patient_phys_ids.append(row[3])
                record_ids.append(row[4])
                health_records.append(row[5])
                health_patient_ids.append(row[6])
                auscultation_ids.append(row[7])
                auscultation_info.append(row[8])
                auscultation_patient_ids.append(row[9])
                physician_ids.append(row[10])
                physician_contact.append(row[11])
            line_count += 1

    conn = create_connection('heart_sound.db')
    cursor = conn.cursor()
    for i in range(len(patient_ids)):
        id = patient_ids[i]
        age = patient_ages[i]
        contact = patient_contact[i]
        phys_id = patient_phys_ids[i]
        cursor.execute("INSERT INTO patients VALUES (? ,?, ?, ?)", (id, age, contact, phys_id))

    for i in range(len(record_ids)):
        id = record_ids[i]
        records = health_records[i]
        patient_ids = health_patient_ids[i]
        cursor.execute("INSERT INTO healthrecords VALUES (? ,?, ?)", (id, records, patient_ids))

    for i in range(len(auscultation_ids)):
        id = auscultation_ids[i]
        recording = encrypt_heart_recording(db_recordings[i])
        info = auscultation_info[i]
        patient_id = auscultation_patient_ids[i]
        cursor.execute("INSERT INTO auscultations VALUES (? ,?, ?, ?)", (id, recording, info, patient_id))

    for i in range(len(phys_id)):
        id = phys_id[i]
        contact = physician_contact[i]
        cursor.execute("INSERT INTO physicians VALUES (? ,?)", (id, contact))

    conn.commit()
    conn.close()


def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


def main():

    # HASHING: Changing the heart sound data we send into a an encoded string or other representation so that we
    # can check that the same heart sound we retrieve from the database is the indeed the same array. This is done
    # by hashing the heart sound data BEFORE we send it, and then hashing the retrieved data. If the two hashes
    # match, we know the data was not messed with.

    # ENCRYPTION: This is actually making sure the heart sound data is sent in a form that can only be unlocked
    # by a secret key that we set on our side. So the data stored in the database is an encrypted version which
    # will be of no use to a hacker unless they can decrypt our data - which can only be done if they have our
    # secret key.

    # REPLACE YOUR heart_sound.db WITH THE NEW ONE PROVIDED
    # REPLACE THIS LINE WITH A SOUND FILE OF YOUR OWN TO TEST ENCRYPTION AND HASHING.
    with open('../heart_sound_classification/heart_sound_data.pickle', "rb") as recordings:
        heart_recording = pickle.load(recordings)[0]

    encrypted = encrypt_heart_recording(heart_recording)

    # Hash it to verify data integrity after retrieval
    hashed = sign(heart_recording)

    # Test inserting and retrieving encrypted heart sound data
    conn = create_connection('heart_sound.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO auscultations (id, heart_recording, recording_information, patient_id) VALUES (?, ?, ?, ?)", (21, encrypted, "healthy", 1))
    cursor.execute("SELECT heart_recording FROM auscultations WHERE id = 21")
    data = cursor.fetchone()[0]
    retrieved_heart_sound = decrypt_heart_recording(data)
    print(retrieved_heart_sound)

    conn.commit()
    conn.close()

    # Verify data integrity
    integrity_maintained = verify(retrieved_heart_sound, hashed)
    print(integrity_maintained)


if __name__ == '__main__':
    main()
