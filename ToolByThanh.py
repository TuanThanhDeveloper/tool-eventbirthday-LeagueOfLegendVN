import sys

import pyautogui
from PyQt5.QtWidgets import (QWidget,
                             QPushButton, QApplication, QGridLayout, QTextBrowser)
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5 import QtCore


class Worker(QObject):
    finished = pyqtSignal()  # give worker class a finished signal

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        self.continue_run = True  # provide a bool run condition for the class

    def do_work(self):
        f = open("birthday_code_league_of_legends.txt", 'r', encoding='utf-8')
        x, y, h, w = pyautogui.locateOnScreen('code.png')
        pyautogui.click(x + h / 2, y + w / 2)
        pyautogui.write(f.readline())
        pyautogui.press('enter')
        pyautogui.sleep(1)
        x1, y1, h1, t1 = pyautogui.locateOnScreen('ok.png')
        pyautogui.click(x1 + 30, y1 + 30)
        pyautogui.sleep(1)
        pyautogui.click(x1 + 30, y1 + 30)
        pyautogui.sleep(1)
        pyautogui.click(x + h / 2, y + w / 2)
        pyautogui.press('backspace', presses=13)
        while self.continue_run:  # give the loop a stoppable condition
            pyautogui.click(x + h / 2, y + w / 2)
            pyautogui.write(f.readline())
            pyautogui.press('enter')
            pyautogui.sleep(1)
            pyautogui.click(x1 + 30, y1 + 30)
            pyautogui.sleep(1)
            pyautogui.click(x1 + 30, y1 + 30)
            pyautogui.sleep(1)
            pyautogui.click(x + h / 2, y + w / 2)
            pyautogui.press('backspace', presses=13)
            pyautogui.sleep(2)
        self.finished.emit()  # emit the finished signal when the loop is done

    def stop(self):
        self.continue_run = False  # set the run condition to false on stop


class Gui(QWidget):
    stop_signal = pyqtSignal()  # make a stop signal to communicate with the worker in another thread

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        _translate = QtCore.QCoreApplication.translate
        # Buttons:
        self.btn_start = QPushButton('Start')
        self.btn_start.resize(self.btn_start.sizeHint())
        self.btn_start.move(50, 50)
        self.btn_stop = QPushButton('Stop')
        self.btn_stop.resize(self.btn_stop.sizeHint())
        self.btn_stop.move(150, 50)
        self.textBrowser = QTextBrowser()
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
                                                          "\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n "
                                                          "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                          "p, li { white-space: pre-wrap; }\n"
                                                          "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                          "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                                          "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; "
                                                          "-qt-block-indent:0; text-indent:0px;\"><br /></p>\n "
                                                          "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Yêu cầu:     + Kích thước màn hình Full HD</p>\n"
                                                          "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">                  + kích thước client 1280 * 720</p>\n"
                                                          "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                                          "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                                          "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Lưu ý: máy sẽ không thể sử dụng lúc đang auto</p>\n"
                                                          "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                                          "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                                          "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; "
                                                          "text-indent:0px;\">Tool được viết bởi Trần Tuấn Thành</p>\n "
                                                          "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Liên hệ: https://www.facebook.com/trantuanthanh0803/</p></body></html>"))

        # GUI title, size, etc...
        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle('Tool by Thành')
        self.layout = QGridLayout()
        self.layout1 = QGridLayout()
        self.layout.addWidget(self.textBrowser, 0, 0)
        self.layout.addLayout(self.layout1, 1, 0)
        self.layout1.addWidget(self.btn_start, 0, 0)
        self.layout1.addWidget(self.btn_stop, 0, 50)
        self.setLayout(self.layout)

        # Thread:
        self.thread = QThread()
        self.worker = Worker()
        self.stop_signal.connect(self.worker.stop)  # connect stop signal to worker stop method
        self.worker.moveToThread(self.thread)

        self.worker.finished.connect(self.thread.quit)  # connect the workers finished signal to stop thread
        self.worker.finished.connect(self.worker.deleteLater)  # connect the workers finished signal to clean up worker
        self.thread.finished.connect(self.thread.deleteLater)  # connect threads finished signal to clean up thread

        self.thread.started.connect(self.worker.do_work)
        self.thread.finished.connect(self.worker.stop)

        # Start Button action:
        self.btn_start.clicked.connect(self.thread.start)

        # Stop Button action:
        self.btn_stop.clicked.connect(self.stop_thread)

        self.show()

    # When stop_btn is clicked this runs. Terminates the worker and the thread.
    def stop_thread(self):
        self.stop_signal.emit()  # emit the finished signal on stop


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())
