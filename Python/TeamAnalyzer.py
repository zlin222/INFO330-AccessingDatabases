import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

conn = sqlite3.connect('../pokemon.sqlite')
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='new3'")
result = cur.fetchone()

if result is None:
        cur.execute("CREATE TABLE new AS SELECT p.id as 'id', \
            p.name as 'pokemon_name', \
            t1.name as 'type1', t2.name as 'type2' \
            FROM pokemon p, type t1, type t2, pokemon_type pt1, \
            pokemon_type pt2 \
            WHERE pt1.pokemon_id = p.id AND pt2.pokemon_id = p.id \
            AND t1.id = pt1.type_id AND pt1.which = 1 \
            AND t2.id = pt2.type_id AND pt2.which = 2"),
        cur.execute("CREATE TABLE new2 AS SELECT t1.name as 'type1_name', \
            t2.name as 'type2_name', \
            against_bug, against_dark, against_dragon, \
            against_electric, against_fairy, \
            against_fight, against_fire, against_flying, \
            against_ghost, against_grass, against_ground, \
            against_ice, against_normal, against_poison, \
            against_psychic,against_rock, against_steel, against_water \
            FROM type t1, type t2, against a \
            WHERE t1.id = a.type_source_id1 AND t2.id = a.type_source_id2;"),
        cur.execute("CREATE TABLE new3 AS \
            SELECT * FROM new n1 \
            LEFT JOIN new2 n2 ON n1.type1 = n2.type1_name \
            and n1.type2 = n2.type2_name;")
else:
    print("Using existing table 'new3' for analysis...")

# All the "against" column suffixes:
types = ["bug", "dark", "dragon", "electric", "fairy", "fight",
         "fire", "flying", "ghost", "grass", "ground", "ice", "normal",
         "poison", "psychic", "rock", "steel", "water"]


# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()


team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
for arg in sys.argv[1:]:
    # Analyze the pokemon whose pokedex_number is in "arg"
    cur.execute("SELECT pokemon_name, type1, type2, id FROM new3 WHERE id = ?", (arg,))
    row = cur.fetchone()
    new3_pokemon_name = row[0]
    new3_type1 = row[1]
    new3_type2 = row[2]
    new3_id = row[3]
    team.append((new3_id, new3_pokemon_name, new3_type1, new3_type2))

    # You will need to write the SQL, extract the results, and compare
    # Remember to look at those "against_NNN" column values; greater than 1
    # means the Pokemon is strong against that type, and less than 1 means
    # the Pokemon is weak against that type
    against_values = []
    for t in types:
        against_column = "against_" + t
        if new3_type2 is None:
            cur.execute("SELECT " + against_column + " FROM new3 WHERE id = ? AND type1 = ?", (new3_id, new3_type1))
        else:
            cur.execute("SELECT " + against_column + " FROM new3 WHERE id = ? AND (type1 = ? OR type2 = ?)", (new3_id, new3_type1, new3_type2))
        against_value = cur.fetchone()[0]
        against_values.append(against_value)
    strong_types = [types[i] for i, v in enumerate(against_values) if v > 1]
    weak_types = [types[i] for i, v in enumerate(against_values) if v < 1]

    print("Analyzing", new3_id)
    print(new3_pokemon_name, "(" + new3_type1 + ("" if new3_type2 is None else " " + new3_type2) + ") is strong against", 
          strong_types, "but weak against", weak_types)

cur.close()
conn.close()