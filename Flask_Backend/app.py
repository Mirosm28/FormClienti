import sqlite3
from flask import Flask, render_template, request, redirect, url_for

import os
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "Flask_Backend", "templates"))

# Funzione per connettersi al database
def connessione_db():
    return sqlite3.connect("clienti.db")

# Salva i dati del cliente
def salva_dati_cliente(dati):
    conn = connessione_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clienti (
            nome, data_nascita, sesso, altezza, peso, telefono, email, obiettivi,
            livello_esperienza, lavoro, frequenza_allenamento, sonno, dieta,
            patologie, allenamento, allenamenti_settimanali, durata_sessione,
            giorni_preferiti, note
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dati["nome"], dati["data_nascita"], dati["sesso"], dati["altezza"], dati["peso"],
        dati["telefono"], dati["email"], ", ".join(dati["obiettivi"]),
        dati.get("livello_esperienza", ""), dati.get("lavoro", ""), dati.get("frequenza_allenamento", ""),
        dati["sonno"], dati["dieta"], dati["patologie"], ", ".join(dati["allenamento"]),
        dati["allenamenti_settimanali"], dati["durata_sessione"], dati["giorni_preferiti"],
        dati["note"]
    ))

    conn.commit()
    conn.close()

# Pagina principale con il form
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        dati_cliente = {key: request.form[key] for key in request.form}
        dati_cliente["obiettivi"] = request.form.getlist("obiettivi")
        dati_cliente["allenamento"] = request.form.getlist("allenamento")
        salva_dati_cliente(dati_cliente)
        return "Dati salvati con successo!"

    return render_template("form.html")

# Pagina per visualizzare i clienti
@app.route("/visualizza")
def visualizza():
    conn = connessione_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clienti")
    clienti = cursor.fetchall()
    conn.close()
    return render_template("visualizza.html", clienti=clienti)

# Route per eliminare un cliente
@app.route("/elimina/<int:id_cliente>", methods=["POST"])
def elimina_cliente(id_cliente):
    conn = connessione_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clienti WHERE id = ?", (id_cliente,))
    conn.commit()
    conn.close()
    return redirect(url_for("visualizza"))

# Route per modificare un cliente (mostra il form con i dati pre-compilati)
@app.route("/modifica/<int:id_cliente>", methods=["GET", "POST"])
def modifica_cliente(id_cliente):
    conn = sqlite3.connect("clienti.db")
    cursor = conn.cursor()

    if request.method == "POST":
        dati_modificati = {
            "nome": request.form["nome"],
            "data_nascita": request.form["data_nascita"],
            "sesso": request.form["sesso"],
            "altezza": request.form["altezza"],
            "peso": request.form["peso"],
            "telefono": request.form["telefono"],
            "email": request.form["email"],
            "obiettivi": request.form["obiettivi"],
            "livello_esperienza": request.form["livello_esperienza"],
            "lavoro": request.form["lavoro"],
            "frequenza_allenamento": request.form["frequenza_allenamento"],
            "sonno": request.form["sonno"],
            "dieta": request.form["dieta"],
            "patologie": request.form["patologie"],
            "allenamento": request.form["allenamento"],
            "allenamenti_settimanali": request.form["allenamenti_settimanali"],
            "durata_sessione": request.form["durata_sessione"],
            "giorni_preferiti": request.form["giorni_preferiti"],
            "note": request.form["note"]
        }

        cursor.execute("""
            UPDATE clienti SET nome=?, data_nascita=?, sesso=?, altezza=?, peso=?, telefono=?, 
            email=?, obiettivi=?, livello_esperienza=?, lavoro=?, frequenza_allenamento=?, sonno=?, 
            dieta=?, patologie=?, allenamento=?, allenamenti_settimanali=?, durata_sessione=?, 
            giorni_preferiti=?, note=? WHERE id=?
        """, (
            dati_modificati["nome"], dati_modificati["data_nascita"], dati_modificati["sesso"],
            dati_modificati["altezza"], dati_modificati["peso"], dati_modificati["telefono"],
            dati_modificati["email"], dati_modificati["obiettivi"], dati_modificati["livello_esperienza"],
            dati_modificati["lavoro"], dati_modificati["frequenza_allenamento"], dati_modificati["sonno"],
            dati_modificati["dieta"], dati_modificati["patologie"], dati_modificati["allenamento"],
            dati_modificati["allenamenti_settimanali"], dati_modificati["durata_sessione"],
            dati_modificati["giorni_preferiti"], dati_modificati["note"], id_cliente
        ))

        conn.commit()
        conn.close()
        return redirect(url_for("visualizza"))

    cursor.execute("SELECT * FROM clienti WHERE id = ?", (id_cliente,))
    cliente = cursor.fetchone()
    conn.close()

    return render_template("modifica.html", cliente=cliente)

if __name__ == "__main__":
    app.run(debug=True)
