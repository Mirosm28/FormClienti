import sqlite3

# Connessione al database (se non esiste, viene creato)
conn = sqlite3.connect("clienti.db")
cursor = conn.cursor()

# Creazione della tabella per i clienti
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clienti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_nascita TEXT NOT NULL,
        sesso TEXT NOT NULL,
        altezza INTEGER,
        peso INTEGER,
        telefono TEXT,
        email TEXT,
        obiettivi TEXT,
        livello_esperienza TEXT,
        lavoro TEXT,
        frequenza_allenamento TEXT,
        sonno INTEGER,
        dieta TEXT,
        patologie TEXT,
        allenamento TEXT,
        allenamenti_settimanali INTEGER,
        durata_sessione TEXT,
        giorni_preferiti TEXT,
        note TEXT
    )
""")

# Salva e chiudi la connessione
conn.commit()
conn.close()

print("Database e tabella creati con successo!")
