from argparse import ArgumentParser
import xml.etree.ElementTree as ETree
import os
import os.path
import sqlite3


def parse_args():
    parser = ArgumentParser(description="db_fill_from_poldnev - read user names and participations from poldnev")

    parser.add_argument('tsv', help='tsv file from poldnev')
    parser.add_argument('database', help='sqlite3 database file')

    return vars(parser.parse_args())

args = parse_args()
tsv_filename = args['tsv']
database_file = args['database']

tsv = open(tsv_filename, "r")
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

user_id_convert = dict()
season_to_id = dict()
parallel_to_id = dict()

cursor.execute("DELETE FROM stats_user")
cursor.execute("DELETE FROM stats_participation")
cursor.execute("DELETE FROM stats_season")
cursor.execute("DELETE FROM stats_parallel")
is_first = True
for line in tsv:
    if is_first:
        is_first = False
        continue
    try:
        poldnev_id, last_name, first_name, middle_name, season, parallel = line.strip().split("\t")
    except ValueError:
        continue
    poldnev_id = int(poldnev_id)

    if poldnev_id not in user_id_convert:
        cursor.execute("INSERT INTO stats_user (first_name, last_name) VALUES (?,?)", (first_name, last_name))
        user_id_convert[poldnev_id] = cursor.lastrowid
    user_id = user_id_convert[poldnev_id]

    if season not in season_to_id:
        year = int(season[:4])
        order = 0
        season_lower = season.lower()
        name_to_order = (
            ("июль", 1),
            ("август", 2),
            ("кострома", 3),
            ("николаев", 4),
            ("подмосковье", 5),
            ("зима", 6)
        )
        for p in name_to_order:
            if p[0] in season_lower:
                order = p[1]
                break
        cursor.execute("INSERT INTO stats_season (name, year, \"order\") VALUES (?,?,?)", (season, year, order))
        season_to_id[season] = cursor.lastrowid
    season_id = season_to_id[season]

    parallel = parallel.replace("+", "")
    if parallel not in parallel_to_id:
        cursor.execute("INSERT INTO stats_parallel (name) VALUES (?)", (parallel,))
        parallel_to_id[parallel] = cursor.lastrowid
    parallel_id = parallel_to_id[parallel]

    cursor.execute("INSERT INTO stats_participation (parallel_id, season_id, user_id) VALUES (?,?,?)",
        (parallel_id,season_id,user_id))

conn.commit()
conn.close()
tsv.close()
