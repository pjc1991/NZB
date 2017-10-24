import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import QWorker



def trap_exc_during_debug(*args):
    print(args)


sys.excepthook = trap_exc_during_debug
form_class = uic.loadUiType("NZB.ui")[0]

jokes = ["나는 재벌 부자",
         "NZB is an XML-based file format for retrieving posts from NNTP (Usenet) servers.",
         "수정된 검색어에 대한 결과: 임재범",
         "ㅝㅠ 으로 검색하시겠습니까?",
         "NZB 버튼은 제발 한번만 불러주세요.",
         ]
joke = random.choice(jokes)


class MyWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_1)
        self.label_nzb.setText(joke)
        self.threadpool = QThreadPool()

    def gettext(self, text):
        self.textNote.setPlainText(text)

    def btn_1(self):
        self.probar(0)
        self.label_nzb.setText(random.choice(jokes))
        self.gettext("잠시만 기다려주세요.")
        mode = self.checkBox.isChecked()
        print(mode)
        max_s = self.spinBox.value()
        print("최대 감지 별의 갯수는 %d개" % max_s)
        self.pushButton.setDisabled(True)
        adr = self.textAddress.toPlainText()
        obj1 = QWorker.Worker(adr, mode, max_s)
        self.threadpool.start(obj1)
        obj2 = QWorker.Worker2()
        self.threadpool.start(obj2)
        obj2.signals.progress.connect(self.probar)
        obj1.signals.DataReady.connect(self.gettext)
        obj2.signals.finished.connect(self.btn_enable)

    def btn_enable(self):
        self.pushButton.setEnabled(True)

    def probar(self, val):
        self.progressBar.setValue(val)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
