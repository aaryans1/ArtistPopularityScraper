import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()

def read_data(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def main():
    json_data = read_data('pokemon.txt')
    cur, conn = open_database('pokemon.db')
    make_types_table(json_data, cur, conn)

    make_pokemon_table(json_data, cur, conn)
    #hp_search(50, cur,conn)
    #hp_speed_attack_search(60, 30, 85,  cur, conn)
    #type_speed_defense_search("Fire", 60, 60, cur, conn)

    #### FEEL FREE TO USE THIS SPACE TO TEST OUT YOUR FUNCTIONS

    conn.close()


if __name__ == "__main__":
   # main()
    unittest.main(verbosity = 2)
    