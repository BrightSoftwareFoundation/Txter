from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
import sys
import os
import webbrowser as web
import urllib.request as urllib


class Txter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.support = ["Text documents (*.txt)",
                        "All files (*.*)"]
        self.path = None

        main_layout = QVBoxLayout()

        self.txter = QPlainTextEdit()

        font = QFont()

        font.setFamily("Consolas")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setOverline(False)
        font.setUnderline(False)

        self.txter.setFont(font)

        self.file_path = None

        self.setCentralWidget(self.txter)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.pos_label = QLabel()
        self.pos_label.setText("Position: 0, Row: 1, Column: 1")
        self.status_bar.addWidget(self.pos_label)

        self.txter.cursorPositionChanged.connect(self.update_status_bar)

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")

        new_file = QAction("&New file", self)
        new_file.setShortcut(Qt.CTRL + Qt.Key_N)
        new_file.setStatusTip("New file: creates a new file")
        new_file.triggered.connect(self.file_new)
        file_menu.addAction(new_file)

        open_file = QAction("&Open file", self)
        open_file.setShortcut(Qt.CTRL + Qt.Key_O)
        open_file.setStatusTip("Open file: opens an old file")
        open_file.triggered.connect(self.file_open)
        file_menu.addAction(open_file)

        save_file = QAction("&Save file", self)
        save_file.setShortcut(Qt.CTRL + Qt.Key_S)
        save_file.setStatusTip("Save file: saves the current file")
        save_file.triggered.connect(self.file_save)
        file_menu.addAction(save_file)

        save_as_file = QAction("Save &as file", self)
        save_as_file.setShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_S)
        save_as_file.setStatusTip("Save as file: saves the current file in new filepath file")
        save_as_file.triggered.connect(self.file_save_as)
        file_menu.addAction(save_as_file)

        file_menu.addSeparator()

        print_file = QAction("&Print file", self)
        print_file.setShortcut(Qt.CTRL + Qt.Key_P)
        print_file.setStatusTip("Print file: prints current file on your printer")
        print_file.triggered.connect(self.file_print)
        file_menu.addAction(print_file)

        edit_menu = menu_bar.addMenu("&Edit")

        undo_text = QAction("&Undo", self)
        undo_text.setShortcut(Qt.CTRL + Qt.Key_Z)
        undo_text.setStatusTip("Undo: Undoes your text")
        undo_text.triggered.connect(self.txter.undo)
        edit_menu.addAction(undo_text)

        redo_text = QAction("&Redo", self)
        redo_text.setShortcut(Qt.CTRL + Qt.Key_Y)
        redo_text.setStatusTip("Redo: Redoes your text")
        redo_text.triggered.connect(self.txter.redo)
        edit_menu.addAction(redo_text)

        edit_menu.addSeparator()

        cut_text = QAction("&Cut", self)
        cut_text.setShortcut(Qt.CTRL + Qt.Key_X)
        cut_text.setStatusTip("Cut: Cuts your selected text")
        cut_text.triggered.connect(self.txter.cut)
        edit_menu.addAction(cut_text)

        copy_text = QAction("&Copy", self)
        copy_text.setShortcut(Qt.CTRL + Qt.Key_C)
        copy_text.setStatusTip("Copy: Copies your text")
        copy_text.triggered.connect(self.txter.copy)
        edit_menu.addAction(copy_text)

        paste_text = QAction("&Paste", self)
        paste_text.setShortcut(Qt.CTRL + Qt.Key_V)
        paste_text.setStatusTip("Paste: Pastes text from clipboard")
        paste_text.triggered.connect(self.txter.paste)
        edit_menu.addAction(paste_text)

        view_menu = menu_bar.addMenu("&View")

        change_font = QAction("&Change font", self)
        change_font.setStatusTip("Change the font view in the text area")
        change_font.triggered.connect(self.view_font_changed)
        view_menu.addAction(change_font)

        self.setLayout(main_layout)

        self.version = b"0.5.0"
        self.online_bytestring = urllib.urlopen("https://txter.weebly.com/test.html")

        self.bytestring = self.online_bytestring.read()
        self.bytestring = self.bytestring[204:209]

        if self.bytestring != self.version:
            dlg = QMessageBox.question(self, "Txter updater", "Updated version " + str(self.bytestring)[2:-1] + ". Would you like to update?")
            if dlg == QMessageBox.Yes:
                web.open("https://txter.weebly.com/en-download.html")

        self.setWindowTitle("Txter")

        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "main.png")))

        try:
            try:
                with open(sys.argv[1], 'r') as f:
                    ctn = f.read()
            except:
                pass
            else:
                self.path = sys.argv[0]
                self.txter.setPlainText(ctn)
        except Exception as e:
            pass

    def update_status_bar(self):
        pos_cur = self.txter.textCursor()
        self.txter.setTextCursor(pos_cur)
        position = pos_cur.position()
        row_num = int(self.txter.toPlainText().count("\n")) + 1
        col_num = int(pos_cur.columnNumber()) + 1
        self.pos_label.setText("Position: " + str(position) + ", Row: " + str(row_num) + ", Column: " + str(col_num))



    def err_msg(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()

    def file_new(self):
        msg = QMessageBox.question(self, "Sure to close", "Are you sure to close without saving your file?",
                                   QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel)
        if msg == QMessageBox.Save:
            self.file_save()
            self.txter.clear()
        elif msg == QMessageBox.No:
            self.txter.clear()
        else:
            pass

    def closeEvent(self, event):
        msg = QMessageBox.question(self, "Sure to close", "Are you sure to close without saving your file?",
                                   QMessageBox.Save | QMessageBox.No | QMessageBox.Cancel)
        if msg == QMessageBox.Save:
            self.file_save()
            event.accept()
        elif msg == QMessageBox.No:
            event.accept()
        else:
            event.ignore()


    def file_open(self):
        fp, _ = QFileDialog.getOpenFileName(parent=self, caption="Open file", filter=";;".join(self.support))
        if fp:
            try:
                with open(fp, "r") as f:
                    ctn = f.read()
            except Exception as e:
                self.err_msg(str(e))
            else:
                self.path = fp
                self.txter.setPlainText(ctn)

    def file_save(self):
        if self.path == None:
            self.file_save_as()
        try:
            ctn = self.txter.toPlainText()
            with open(self.path, "w") as f:
                f.write(ctn)
        except Exception as e:
            self.err_msg(str(e))

    def file_save_as(self):
        fp, _ = QFileDialog.getSaveFileName(parent=self, caption="Save to...", filter=";;".join(self.support))
        try:
            ctn = self.txter.toPlainText()
            with open(fp, "w") as f:
                f.write(ctn)
        except Exception as e:
            self.err_msg(str(e))
        else:
            self.path = fp

    def file_print(self):
        prtdlg = QPrintDialog()
        if prtdlg.exec_():
            self.txter.print_(prtdlg.printer())

    def view_font_changed(self):
        font, yes = QFontDialog.getFont(parent = self)
        if yes:
            self.txter.setFont(font)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    txter = Txter()
    txter.show()
    sys.exit(app.exec_())
