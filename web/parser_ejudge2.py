class SQLiteConnector:
    def __init__(self, db_dir):
        import sqlite3
        self.connection = sqlite3.connect(db_dir)

    def get_cursor(self):
        return self.connection.cursor()

    def close_connection(self):
        self.connection.commit()
        self.connection.close()


class MySQLConnector:
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

def parse_ejudge2(sqlite_dir, mysql_config):
    import os.path
    print(os.path.abspath(sqlite_dir))

    print('CONNECTING TO DATA...', end='')
    sqlite_db = SQLiteConnector(sqlite_dir)
    mysql_db = MySQLConnector(mysql_config)

    print('OK\nREADING DATA...', end='')
    mysql_cur = mysql_db.get_cursor()
    mysql_cur.execute('SELECT contest_id, user_id FROM runs')
    ejudge_con_and_usr_id_list = []
    for i in mysql_cur:
        ejudge_con_and_usr_id_list.append(i)
    mysql_cur = mysql_db.get_cursor()
    mysql_cur.execute('SET NAMES utf8')
    mysql_cur.execute('SELECT user_id, contest_id, username FROM users')
    ejudge_usr_id_and_name_list = []
    for i in mysql_cur:
        ejudge_usr_id_and_name_list.append(i)

    sqlite_cur = sqlite_db.get_cursor()
    sqlite_cur.execute('SELECT id, first_name, last_name FROM stats_user')
    sqlite_id_first_second = []
    for i in sqlite_cur:
        sqlite_id_first_second.append(i)
    sqlite_cur = sqlite_db.get_cursor()
    sqlite_cur.execute('SELECT contest_id, parallel_id, season_id FROM stats_contest')
    sqlite_contest_parallel_season = {}
    for contest, parallel, season in sqlite_cur:
        if sqlite_contest_parallel_season.get(contest // 100 * 100, (None, None))[0] is None:
            sqlite_contest_parallel_season[contest // 100 * 100] = (parallel, season)
    sqlite_cur.execute('SELECT id, parallel_id, season_id, user_id FROM stats_participation')
    sqlite_participation = []
    for i in sqlite_cur:
        sqlite_participation.append(i)
    participation_dict = {}
    for id, parallel_id, season_id, user_id in sqlite_participation:
        participation_dict[(parallel_id, season_id, user_id)] = id
    sqlite_cur.execute('SELECT stats_problem.id, stats_contest.parallel_id, stats_contest.season_id FROM stats_problem JOIN stats_contest ON stats_problem.contest_id=stats_contest.id')
    parallel_season_by_problem = {}
    for problem, parallel, season in sqlite_cur:
        parallel_season_by_problem[problem] = (parallel, season)
    submits = []
    sqlite_cur.execute('SELECT stats_submit.id, stats_submit.problem_id, stats_submit.user_id, stats_contest.contest_id FROM stats_submit JOIN stats_problem ON stats_submit.problem_id = stats_problem.id JOIN stats_contest ON stats_problem.contest_id = stats_contest.id')
    for i in sqlite_cur:
        submits.append(i)
    print('OK\nWRITING SUBMITS FIRST...', end='')
    ids_in_ej = {}
    for id, first_name, last_name in sqlite_id_first_second:
        for user_id, contest_id, name in ejudge_usr_id_and_name_list:
            try:
                parallel = sqlite_contest_parallel_season[contest_id // 100 * 100][0]
                season = sqlite_contest_parallel_season[contest_id // 100 * 100][1]
            except KeyError:
                continue
            if name is None:
                continue
            name = ' ' + name + ' '
            if (parallel, season, id) in participation_dict and (' ' + first_name + ' ') in name and (' ' + last_name + ' ') in name and ',' not in name:
                ids_in_ej[(user_id, contest_id // 100 * 100)] = id
    print('OK\nWRITING SUBMITS SECOND...', end='')
    filled = 0
    for id, problem_id, ejudge_user_id, ejudge_contest_id in submits:
        try:
            user_id = ids_in_ej[ejudge_user_id, ejudge_contest_id // 100 * 100]
            parallel, season = parallel_season_by_problem[problem_id]
            participation = participation_dict[parallel, season, user_id]
        except KeyError:
            continue
        sqlite_cur.execute('UPDATE stats_submit SET participation_id = {0} WHERE id={1}'.format(participation, id))
        filled += 1
    print('OK')
    print(filled, 'filled')
    sqlite_db.connection.commit()
    sqlite_db.close_connection()
    mysql_db.close_connection()

if __name__ == "__main__":
    config = {'user': 'root', 'passwd': 'root', 'host': 'localhost', 'port': 3306, 'db': 'ejudgedata'}
    parse_ejudge2('db.sqlite3', config)