class SQLiteConnector:
    def __init__(self, db_dir):
        import sqlite3
        self.connection = sqlite3.connect(db_dir)

    def get_cursor(self):
        return self.connection.cursor()

    def close_connection(self):
        self.connection.commit()
        self.connection.close()


class MySQLConnector():
    """Example of config
    config = {'user': 'root', 'passwd': '', 'host': 'localhost', 'port': 3306, 'db': 'ejudge_db'}
    """

    def __init__(self, config):
        import pymysql
        self.connection = pymysql.connect(**config)

    def get_cursor(self):
        return self.connection.cursor()

    def close_connection(self):
        self.connection.close()

def parse_ejudge(sqlite_dir, mysql_config):
    ejudge_status = {0: 'OK',
                     1: 'CE',
                     2: 'RT',
                     3: 'TL',
                     4: 'PE',
                     5: 'WA',
                     6: 'CF',
                     7: 'PT',
                     8: 'AC',
                     9: 'IG',
                     10: 'DQ',
                     11: 'PD',
                     12: 'ML',
                     13: 'SE',
                     14: 'SV',
                     15: 'WT',
                     16: 'PR',
                     17: 'RJ',
                     18: 'SK'}

    sqlite_db = SQLiteConnector(sqlite_dir)
    mysql_db = MySQLConnector(mysql_config)
    mysql_cur = mysql_db.get_cursor()
    sqlite_cur = sqlite_db.get_cursor()

    mysql_cur.execute('SELECT contest_id, prob_id, lang_id, status, user_id FROM runs')

    ids = {}
    first_l = []
    second_l = []
    third_l = []

    for i in mysql_cur:
        first_l.append( (i[0], i[1]) )
        second_l.append(i)
        third_l.append(i[0])

    for i in list(set(first_l)):
        sqlite_cur.execute('INSERT INTO stats_problem (contest_id, prob_id, polygon_id, name) VALUES ({0}, {1}, 0, 0)'.format(i[0], i[1]))
        ids[i] = sqlite_cur.lastrowid

    import logging
    for i in second_l:
        try:
            sqlite_cur.execute("INSERT INTO stats_submit (outcome, lang_id, problem_id, user_id) VALUES ('{0}', {1}, {2}, {3})".format(ejudge_status[i[3]], i[2], ids[i[0], i[1]], i[4]))
        except KeyError:
            pass
            # logging('fuck the ' + i[3].__str__())

    for i in list(set(third_l)):
        sqlite_cur.execute('INSERT INTO stats_contest (contest_id) VALUES ({0})'.format(i))

    sqlite_db.close_connection()
    mysql_db.close_connection()

