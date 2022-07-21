from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *
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
        self.zoom_range = 100
        self.original = ""

        main_layout = QVBoxLayout()

        self.txter = QsciScintilla()

        self.font = QFont()
        self.font.setFamily("Consolas")
        self.font.setFixedPitch(True)
        self.font.setPointSize(10)
        self.txter.setFont(self.font)
        self.txter.setMarginsFont(self.font)

        fontmetrics = QFontMetrics(self.font)
        self.txter.setMarginsFont(self.font)
        self.txter.setMarginWidth(0, fontmetrics.width("000000") + 6)
        self.txter.setMarginLineNumbers(0, True)
        self.txter.setMarginsBackgroundColor(QColor("#cccccc"))
        self.txter.marginClicked.connect(self.margin_clicked)

        self.txter.setMarginSensitivity(1, True)
        self.txter.markerDefine(QsciScintilla.SC_MARK_CIRCLE, 8)
        self.txter.setMarkerBackgroundColor(QColor("#ee1111"), 8)

        self.txter.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        self.txter.setCaretLineVisible(True)
        self.txter.setCaretLineBackgroundColor(QColor("#dddddd"))

        self.txter.setWrapMode(QsciScintilla.WrapNone)

        self.txter.setAutoIndent(True)
        self.txter

        self.file_path = None

        self.setCentralWidget(self.txter)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.pos_label = QLabel()
        self.pos_label.setText("Row: 1, Column: 1")
        self.status_bar.addWidget(self.pos_label)

        self.zoom_label = QLabel()
        self.zoom_label.setText("Zoom: 100%")
        self.status_bar.addWidget(self.zoom_label)

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

        view_menu.addSeparator()

        self.caret_line = QAction("C&aret line visibility", self)
        self.caret_line.setStatusTip("Caret line: will shown or not shown")
        self.caret_line.setCheckable(True)
        self.caret_line.setChecked(True)
        self.caret_line.triggered.connect(self.view_caret_line)
        view_menu.addAction(self.caret_line)

        view_menu.addSeparator()

        self.zoom_in = QAction("Zoom &in", self)
        self.zoom_in.setStatusTip("Zoom in: zoom your text editor bigger")
        self.zoom_in.triggered.connect(self.view_zoom_in)
        view_menu.addAction(self.zoom_in)

        self.zoom_out = QAction("Zoom &out", self)
        self.zoom_out.setStatusTip("Zoom out: zoom your text editor smaller")
        self.zoom_out.triggered.connect(self.view_zoom_out)
        view_menu.addAction(self.zoom_out)

        view_menu.addSeparator()

        delete_all_markers = QAction("Delete all markers", self)
        delete_all_markers.setStatusTip("Delete all markers: delete all markers on your notepad")
        delete_all_markers.triggered.connect(self.view_delete_all_markers)
        view_menu.addAction(delete_all_markers)

        format_menu = menu_bar.addMenu("&Format")

        language_menu = format_menu.addMenu("&Languages")

        none = QAction("N&one (Normal text)", self)
        none.setCheckable(True)
        none.setChecked(True)
        none.setEnabled(False)
        language_menu.addAction(none)

        help_menu = menu_bar.addMenu("Help")

        help = QAction("&Help online", self)
        help.setStatusTip("Help online: Open Txter official help website")
        help_menu.addAction(help)

        self.setLayout(main_layout)

        self.version = b"0.8.0"
        self.online_bytestring = urllib.urlopen("https://txter.weebly.com/test.html")

        self.bytestring = self.online_bytestring.read()
        self.bytestring = self.bytestring[204:209]

        if self.bytestring != self.version:
            dlg = QMessageBox.question(self, "Txter updater", "Updated version " + str(self.bytestring)[2:-1] + ". Would you like to update?")
            if dlg == QMessageBox.Yes:
                web.open("https://txter.weebly.com/en-download.html")

        self.setWindowTitle("Txter")
        
        try:
            want_to_access = sys.argv[1]
            want_to_access = want_to_access.replace("\\", "/")
            with open(want_to_access, mode="r", encoding="utf-8-sig") as f:
                ctn = f.read()
                self.original = ctn
                self.path = want_to_access
                self.txter.setText(ctn)
        except:
            pass

    def wheelEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            delta = event.angleDelta()
            if delta.y() > 0:
                self.zoom_out.setEnabled(True)
                self.zoom_range += 10
                self.v_zoom_in()
                if self.zoom_range > 150:
                    self.zoom_range = 150
                    self.zoom_label.setText("Zoom: 150%")
                if self.zoom_range == 11:
                    self.zoom_range = 10
                    self.zoom_label.setText("Zoom: 10%")
                if self.zoom_range == 150:
                    self.zoom_in.setEnabled(False)
            else:
                self.zoom_in.setEnabled(True)
                self.zoom_range -= 10
                self.v_zoom_out()
                if self.zoom_range < 1:
                    self.zoom_range = 1
                    self.zoom_label.setText("Zoom: 1%")
                if self.zoom_range == 1:
                    self.zoom_out.setEnabled(False)
        else:
            super().wheelEvent(event)

    def view_delete_all_markers(self):
        self.txter.markerDeleteAll(8)

    def v_zoom_in(self):
        if self.zoom_range >= 1 and self.zoom_range <= 150:
            self.txter.zoomIn(1)
            self.zoom_label.setText("Zoom: " + str(self.zoom_range) + "%")

    def v_zoom_out(self):
        if self.zoom_range >= 1 and self.zoom_range <= 150:
            self.txter.zoomOut(1)
            self.zoom_label.setText("Zoom: " + str(self.zoom_range) + "%")

    def view_zoom_in(self):
        self.zoom_out.setEnabled(True)
        self.zoom_range += 10
        self.v_zoom_in()
        if self.zoom_range > 200:
            self.zoom_range = 200
            self.zoom_label.setText("Zoom: 150%")
        if self.zoom_range == 11:
            self.zoom_range = 10
            self.zoom_label.setText("Zoom: 10%")
        if self.zoom_range == 200:
            self.zoom_in.setEnabled(False)

    def view_zoom_out(self):
        self.zoom_in.setEnabled(True)
        self.zoom_range -= 10
        self.v_zoom_out()
        if self.zoom_range < 1:
            self.zoom_range = 1
            self.zoom_label.setText("Zoom: 1%")
        if self.zoom_range == 1:
            self.zoom_out.setEnabled(False)

    def update_status_bar(self):
        pos_cur = self.txter.getCursorPosition()
        row_num = pos_cur[1] + 1
        col_num = pos_cur[0] + 1
        self.pos_label.setText("Row: " + str(row_num) + ", Column: " + str(col_num))

    def err_msg(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()

    def margin_clicked(self, nmargin, nline, modifiers):
        if self.txter.markersAtLine(nline) != 0:
            self.txter.markerDelete(nline, 8)
        else:
            self.txter.markerAdd(nline, 8)

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
        if not self.txter.text() == self.original:
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
                with open(fp, mode="r", encoding="UTF-8-sig") as f:
                    ctn = f.read()
                    self.original == ctn
            except Exception as e:
                self.err_msg(str(e))
            else:
                self.path = fp
                self.txter.setText(ctn)

    def file_save(self):
        if self.path == None:
            self.file_save_as()
        try:
            ctn = self.txter.text().replace("\n\r", "\n")
            with open(self.path, mode="w", encoding="UTF-8-sig") as f:
                f.write(ctn)
        except Exception as e:
            self.err_msg(str(e))

    def file_save_as(self):
        fp, _ = QFileDialog.getSaveFileName(parent=self, caption="Save to...", filter=";;".join(self.support))
        try:
            ctn = self.txter.text()
            with open(fp, mode="w", encoding="UTF-8-sig") as f:
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

    def view_caret_line(self):
        if not self.caret_line.isChecked():
            self.txter.setCaretLineVisible(False)
        else:
            self.txter.setCaretLineVisible(True)

    def help_online(self):
        web.open("https://www.txter.weebly.com/helps/manual")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    txter = Txter()
    txter.show()
    sys.exit(app.exec_())
