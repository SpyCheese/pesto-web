from argparse import ArgumentParser
import xml.etree.ElementTree as ETree
import os
import os.path
import sqlite3


def parse_args():
    parser = ArgumentParser(description="db_fill_contest_names - read contest names from xmls ant write it to database.")

    parser.add_argument('xmls', help='directory with xmls')
    parser.add_argument('database', help='sqlite3 database file')

    return vars(parser.parse_args())


def ejudge_get_contest_name(xml_filename):
    try:
        with open(xml_filename, encoding='utf-8') as f:
            data = f.read()
    except UnicodeError:
        return None
    try:
        xml_root = ETree.fromstring(data)
    except ETree.ParseError:
        return None
    try:
        return xml_root.find("name").text
    except AttributeError:
        return None


args = parse_args()
xmls_dir = args['xmls']
if xmls_dir[-1] != '/':
    xmls_dir += '/'
database_file = args['database']

conn = sqlite3.connect(database_file)
cursor = conn.cursor()

for xml_filename in os.listdir(xmls_dir):
    contest_id = xml_filename.split('.')[0]
    contest_name = ejudge_get_contest_name(xmls_dir + xml_filename)
    cursor.execute("UPDATE stats_contest SET name=? WHERE contest_id=?", (contest_name, contest_id))

conn.commit()
conn.close()
