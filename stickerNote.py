from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QColorDialog)
from database import salvar_notas, eliminar_notas


class stickerNote(QWidget):
    def __init__(self, create_callback, note_id=None, content="", color="#fff9b1", x=200, y=200, w=200, h=200):
        super().__init__()
        self.note_id = note_id
        self.color = color
        self.old_pos = QPoint()
        self.create_callback = create_callback

        self.iniciar_iu(content, x, y, w, h)

    def iniciar_iu(self, content, x, y, w, h):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(x, y, w, h)

        self.container = QWidget(self)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0,0,0,0)
        layout_principal.addWidget(self.container)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(8, 8, 8, 8)

        header_layout = QHBoxLayout()

        btn_add = QPushButton("+")
        btn_add.setFixedSize(20, 20)
        btn_add.clicked.connect(lambda: self.create_callback())

        btn_color = QPushButton("Cor")
        btn_color.setFixedSize(20, 20)
        btn_color.clicked.connect(self.mudar_cor)

        btn_delete = QPushButton("X")
        btn_delete.setFixedSize(20, 20)
        btn_delete.clicked.connect(self.delete_note)

        header_layout.addWidget(btn_add)
        header_layout.addWidget(btn_color)
        header_layout.addStretch()
        header_layout.addWidget(btn_delete)

        # Texto
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(content)
        self.text_edit.textChanged.connect(self.save_note)

        layout.addLayout(header_layout)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        self.aplicar_estilo()

    def aplicar_estilo(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.color};
                border-radius: 8px;
            }}
            QTextEdit {{
                background-color: transparent;
                border: none;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #333333;
            }}
            QPushButton {{
                background-color: rgba(0, 0, 0, 0.08);
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 0, 0, 0.2);
            }}
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()


    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and not self.old_pos.isNull():
            self.move(event.globalPosition().toPoint() - self.old_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = QPoint()
            self.save_note()

    def resizeEvent(self, event):
        self.save_note()
        super().resizeEvent(event)

    def save_note(self):
        content = self.text_edit.toPlainText()
        self.note_id = salvar_notas(
            self.note_id, content, self.color, self.x(), self.y(), self.width(), self.height()
        )

    def delete_note(self):
        eliminar_notas(self.note_id)
        self.close()

    def mudar_cor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()
            self.aplicar_estilo()
            self.save_note()