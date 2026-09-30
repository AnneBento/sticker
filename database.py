import sqlite3

db_name = "notas.db"

def iniciar_banco_de_dados():
    conn = sqlite3.connect("notas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            color TEXT,
            x_pos INTEGER,
            y_pos INTEGER,
            width INTEGER,
            height INTEGER
        )
    """)
    conn.commit()
    conn.close()

def carregar_notas():
    conn = sqlite3.connect("notas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, color, x_pos, y_pos, width, height FROM notas")
    linha = cursor.fetchall()
    conn.close()
    return linha


def salvar_notas(note_id, content, color, x, y, w, h):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    if note_id is None:
        cursor.execute("""
            INSERT INTO notas (content, color, x_pos, y_pos, width, height)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (content, color, x, y, w, h))
        novo_id = cursor.lastrowid
    else:
        cursor.execute("""
            UPDATE notas
            SET content = ?, color = ?, x_pos = ?, y_pos = ?, width = ?, height = ?
            WHERE id = ?
        """, (content, color, x, y, w, h, note_id))
        novo_id = note_id

    conn.commit()
    conn.close()
    return novo_id



def eliminar_notas(note_id):
    if note_id is not None:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notas WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()