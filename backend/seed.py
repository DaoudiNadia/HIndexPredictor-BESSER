import sqlite3
import os

DB_PATH = "data/Class_Diagram.db"

fields = [
    ("COMPUTER_SCIENCE", 3.53),
    ("PHYSICS",          7.35),
    ("MATHEMATICS",      5.48),
    ("MEDICINE",         9.75),
    ("CHEMISTRY",        9.59),
    ("BIOLOGY",         10.12),
    ("ECONOMICS",        4.96),
    ("SOCIOLOGY",        5.76),
]

def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM researchfield")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO researchfield (name, averageHIndex) VALUES (?, ?)",
            fields
        )
        conn.commit()
        print("ResearchField records seeded.")
    else:
        print("Already seeded, skipping.")
    conn.close()

if __name__ == "__main__":
    seed()