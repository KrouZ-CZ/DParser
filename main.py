import pickle
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from des import *
from dparse import *


class App(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.list = []
        self.ui.pushButton_4.clicked.connect(self.get)
        self.ui.pushButton.clicked.connect(self.save)
        self.ui.pushButton_2.clicked.connect(self.load)
        self.ui.pushButton_3.clicked.connect(self.clear)

    def get(self):
        self.thread = QtCore.QThread()
        self.signal = DParse(self.ui.lineEdit.text(), self.ui.lineEdit_2.text(), int(self.ui.lineEdit_3.text()))
        self.signal.moveToThread(self.thread)
        self.signal.mysignal.connect(self.signal_handler)
        self.thread.started.connect(self.signal.get_msg)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: self.ui.pushButton_4.setEnabled(True))
        self.ui.pushButton_4.setEnabled(False)
        self.thread.start()

    def signal_handler(self, msg):
        self.thread.quit()
        self.signal.deleteLater()
        for i in msg['messages']:
            self.list.append({'username': i['username'], 'text': i['text'], 'timestamp': i['timestamp']})
        for i in msg['messages']:
            item = QtWidgets.QListWidgetItem()

            size = QtCore.QSize(45, 45)
            pixmap_obj = QtGui.QPixmap()
            pixmap_obj.loadFromData(msg['icons'][i['icon']])
            icon = QtGui.QIcon(pixmap_obj)

            time = i['timestamp'].split('T')[0] +' '+ i['timestamp'].split('T')[1].split('.')[0]
            item.setIcon(icon)
            item.setText(f"{i.get('username')} {time}:\n{i.get('text')}")
            self.ui.listWidget.setIconSize(size)
            self.ui.listWidget.addItem(item)
    def save(self):
        fp, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', filter='DAT files (*.dat)')
        with open(fp, 'wb') as f:
            pickle.dump(self.list, f)

    def load(self):
        fp, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', filter='DAT files (*.dat)')
        with open(fp, 'rb') as f:
            msg = pickle.load(f)

        for i in msg:
            item = QtWidgets.QListWidgetItem()

            size = QtCore.QSize(45, 45)
            icon = QtGui.QIcon('user.png')

            time = i['timestamp'].split('T')[0] +' '+ i['timestamp'].split('T')[1].split('.')[0]
            item.setIcon(icon)
            item.setText(f"{i.get('username')} {time}:\n{i.get('text')}")
            self.ui.listWidget.setIconSize(size)
            self.ui.listWidget.addItem(item)

    
    def clear(self):
        self.list = []
        self.ui.listWidget.clear()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = App()
    myapp.show()
    sys.exit(app.exec_())
