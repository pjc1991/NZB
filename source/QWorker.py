from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot
import Core
import re
import time
import math

jobs_done = 0


class WorkerSignals(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    DataReady = pyqtSignal(str)
    ListReady = pyqtSignal(list)


class Worker(QRunnable):

    def __init__(self, data, mode, max_s):
        super().__init__()
        self.signals = WorkerSignals()
        self.data = data
        self.mode = mode
        self.max_s = max_s


    @pyqtSlot()
    def run(self):
        global jobs_done
        jobs_done = 0
        time.sleep(1)
        if self.mode:
            Core.wstars = re.compile("[☆](?=\s)?.+(?=\W)?")
            Core.bstars = re.compile("[★](?=\s)?.+(?=\W)?")
        else:
            Core.wstars = re.compile("[☆]\s?\w+")
            Core.bstars = re.compile("[★]\s?\w+")
        print(Core.wolf(self.data))
        if Core.wolf(self.data) is None:
            output = "올바른 주소를 입력해주세요."
        else:
            print("바른 주소는...%s" % Core.wolf(self.data))
            address = Core.wolf(self.data)
            self.signals.DataReady.emit("주소 획득 완료 %s" % Core.wolf(self.data))
            log_data = Core.getsoup(address)
            print(log_data)
            if log_data == "WARNING":
                output = "올바른 주소를 입력해주세요..."
            else:
                self.signals.DataReady.emit("웹 페이지 획득 완료")
                data = Core.working(log_data)
                print("데이터를 확인합니다. \n %s" % data)
                self.signals.DataReady.emit("로그 획득 완료")
                print("데이터를 확인합니다. \n %s" % data)
                zt = "".join(Core.nzb(Core.bstars, data, self.max_s))
                tc = "".join(Core.nzb(Core.wstars, data, self.max_s))
                self.signals.DataReady.emit("집계 완료")
                print(zt)
                print(tc)
                output = "---------------점 추천---------------\n\n%s\n---------------투표 추천---------------\n\n%s" \
                         % (zt, tc)

        time.sleep(0.5)
        self.signals.DataReady.emit(output)
        jobs_done = 1


class Worker2(QRunnable):

    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        for i in range(1, 100):
            fake = int(math.log(i)*20)
            self.signals.progress.emit(fake)
            if jobs_done:
                break
            time.sleep(0.1)
        while jobs_done < 1:
            time.sleep(0.1)
        self.signals.progress.emit(100)
        time.sleep(0.2)
        self.signals.finished.emit()


class Worker3(QRunnable):


    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        Core.on_drv()
        list1 = Core.get_vil_list("http://werewolf.co.kr")
        list3 = Core.get_vil_list("http://werewolf6.cafe24.com")
        vil_list = list1 + list3
        self.signals.ListReady.emit(vil_list)
        print(vil_list)
        len(vil_list)
