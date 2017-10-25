import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import os
import QWorker


def trap_exc_during_debug(*args):
    print(args)


def res_path(rel_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)


# sys.excepthook = trap_exc_during_debug
form_class = uic.loadUiType(res_path("NZB.ui"))[0]
form_class2 = uic.loadUiType(res_path("Init.ui"))[0]

jokes = ["닌자 좀비 블러드",
         "NZB is an XML-based file format for retrieving posts from NNTP (Usenet) servers.",
         "수정된 검색어에 대한 결과: 임재범",
         "ㅝㅠ 으로 검색하시겠습니까?",
         "NZB 버튼은 제발 한번만 불러주세요.",
         "님 점박",

         ]

joke  = random.choice(jokes)


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


class Init(QFrame, form_class2):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_self.clicked.connect(self.open_main)
        self.btn_go.clicked.connect(self.auto_work)
        self.main_window = None
        self.threadpool = QThreadPool()
        self.v_list = []
        get_list = QWorker.Worker3()
        self.threadpool.start(get_list)
        get_list.signals.ListReady.connect(self.list_show)
        get_list.signals.ListReady.connect(self.enable_self)

    def enable_self(self):
        self.btn_self.setEnabled(True)

    def list_show(self, v_list):
        self.v_list = v_list
        self.listwidget.clear()
        for i in v_list:
            self.listwidget.addItem(i[0])
        self.btn_go.setEnabled(True)

    def auto_work(self):
        if self.main_window is None:
            self.main_window = MyWindow()
        self.main_window.show()
        self.main_window.textAddress.setPlainText(self.v_list[self.listwidget.currentRow()][1])
        self.main_window.btn_1()

    def open_main(self):
        if self.main_window is None:
            self.main_window = MyWindow()
        self.main_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Init = Init()
    Init.show()
    app.exec_()
