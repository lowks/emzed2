import time
import sys
from guidata import qapplication
from PyQt4.QtCore import Qt, SIGNAL, QThread
from PyQt4.QtGui import (QTableWidget, QTableWidgetItem, QDialog, QTextEdit, QPushButton,
                         QVBoxLayout, QHBoxLayout, QHeaderView, QApplication, QCursor)


class UpdateDialog(QDialog):

    def __init__(self, update_script):
        super(UpdateDialog, self).__init__(None, Qt.Window)
        self.updates_to_run = []
        self.setWindowTitle("emzed updates")
        self.setWindowModality(Qt.WindowModal)
        self.setMinimumWidth(600)
        self.update_script = update_script
        self.setup_widgets()
        self.setup_layout()
        self.connect_signals()

    def showEvent(self, evt):

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        class WorkerThread(QThread):

            def run(self, script=self.update_script, parent=self):
                for _ in script(parent):
                    pass
                self.emit(SIGNAL("update_query_finished()"))

        self.t = WorkerThread()
        self.connect(self.t, SIGNAL("update_query_finished()"), self.start_to_interact)
        self.t.start()

    def start_to_interact(self):
        self.ok_button.setEnabled(True)
        QApplication.restoreOverrideCursor()

    def setup_widgets(self):
        self.info = QTextEdit(self)
        self.info.setReadOnly(1)
        self.updates = QTableWidget(0, 3)
        self.updates.setHorizontalHeaderLabels(["updater", "info", "do_update ?"])
        self.updates.verticalHeader().hide()
        self.updates.horizontalHeader().setResizeMode(0, QHeaderView.Stretch)
        self.updates.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)
        self.ok_button = QPushButton("OK")
        self.ok_button.setEnabled(False)

    def setup_layout(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.info)
        layout.addWidget(self.updates)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        layout.addLayout(button_layout)

    def connect_signals(self):
        self.connect(self.ok_button, SIGNAL("pressed()"), self.accept)

    def ok_button_pressed(self):
        self.info.append("hi")
        self.add_update_info("updater", "info")

    def _item(self, content, is_checkable):
        item = QTableWidgetItem(content)
        if is_checkable:
            item.setCheckState(Qt.Unchecked)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable)
        return item

    def add_update_info(self, updater_id, info, with_checkbox=True):
        i = self.updates.rowCount()
        self.updates.insertRow(i)
        self.updates.setItem(i, 0, self._item(updater_id, False))
        self.updates.setItem(i, 1, self._item(info, False))
        if with_checkbox:
            self.updates.setItem(i, 2, self._item("", True))

    def add_info_line(self, txt):
        self.info.append(txt)

    def get_updates_to_run(self):
        return self.updates_to_run

    def accept(self):
        for i in range(self.updates.rowCount()):
            updater_id = str(self.updates.item(i, 0).text())
            item = self.updates.item(i, 2)
            if item is not None:  # some cells in column are empty
                checked = self.updates.item(i, 2).checkState() == Qt.Checked
                if checked:
                    self.updates_to_run.append(updater_id)
        super(UpdateDialog, self).accept()

if __name__ == "__main__":
    app = qapplication()
    dlg = UpdateDialog()
    dlg.exec_()
    dlg.get_updates_to_run()