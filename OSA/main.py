import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
from PyQt5.QtSvg import QSvgWidget

from gui import Ui_MainWindow
from resources_rc import *
import threading

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)
        self.ui.check_account()

    ## Function for searching

    ## Function for changing page to user page
    def on_user_btn_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                    + self.ui.full_menu_widget.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
            
    ## functions for changing menu page
    def on_home_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.clear_video_player()

    def on_home_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.clear_video_player()
    #stats
    def on_dashborad_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.clear_video_player()
        self.ui.update_best_score_table()
        thread = threading.Thread(target=self.ui.update_worlds_best_table())
        thread.start()


    def on_dashborad_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.clear_video_player()

    def on_orders_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.clear_video_player()

    def on_orders_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.clear_video_player()

    def on_products_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.clear_video_player()

    def on_products_btn_2_toggled(self, ):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.ui.clear_video_player()




if __name__ == "__main__":
    app = QApplication(sys.argv)

    ## loading style file
    # with open("style.qss", "r") as style_file:
    #     style_str = style_file.read()
    # app.setStyleSheet(style_str)

    ## loading style file, Example 2
    style_file = QFile("style.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    style_stream = QTextStream(style_file)
    app.setStyleSheet(style_stream.readAll())


    window = MainWindow()
    window.show()

    sys.exit(app.exec())


'''
from PyQt5.QtWidgets import QApplication, QDesktopWidget
screen = QDesktopWidget().screenGeometry()

screen_width = screen.width()
screen_height = screen.height()
app_width = int(screen_width/2)
app_height = int(screen_height/2)
'''
