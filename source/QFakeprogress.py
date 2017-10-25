from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot
import Core
import random
import re
import time


class WorkerSignals(QObject):
    progress = pyqtSignal(int)


class Worker(QRunnable):

    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        self.jobs_done = 0

    @pyqtSlot()
    def run(self):
        for i in range(80):
            self.signals.progress.emit(i)
            if self.jobs_done:
                break
            time.sleep(0.2)

    # @pyqtSlot()
    # def go_work(self,  data):
        # nzb = Core.superduper_nzb(data)
        # self.DataReady.emit(nzb)
        # self.finished.emit()
