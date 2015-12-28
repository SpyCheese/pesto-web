def parse_poldnev(file_name, db_name):
    import sqlite3
    sqlite_connection = sqlite3.connect(db_name)

    f = open(file_name)
    f.readline()
    for i in f:
        person_id, person_last_names, person_first_names, person_middle_name, session_name, parallel = f.readline().split('\t')
        sqlite_connection.cursor().execute('INSERT INTO stats_users (person_id, person_last_names, person_first_names, person_middle_name, session_name, parallel) '
                                           'VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}")'
                                           .format(person_id, person_last_names, person_first_names, person_middle_name, session_name, parallel))

    f.close()
    sqlite_connection.commit()
    sqlite_connection.close()
