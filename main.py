import sys
from PyQt6.QtWidgets import QApplication
from stickerNote import stickerNote
from database import iniciar_banco_de_dados, carregar_notas

ativar_notas = []

def create_new_sticker(note_id=None, content="", color="#fff9b1", x=200, y=200, w=200, h=200):
    notas = stickerNote(create_new_sticker, note_id, content, color, x, y, w, h)
    notas.show()
    ativar_notas.append(notas)
    return notas

def load_notes():
    linhas = carregar_notas()
    if not linhas:
        create_new_sticker(content="Bem vinda Querida.")
    else: 
        for linha in linhas:
            create_new_sticker(
                note_id=linha[0],
                content=linha[1],
                color=linha[2],
                x=linha[3],
                y=linha[4],
                w=linha[5],
                h=linha[6]
            )

if __name__ == "__main__":
    iniciar_banco_de_dados()
    app = QApplication(sys.argv)
    load_notes()
    sys.exit(app.exec())