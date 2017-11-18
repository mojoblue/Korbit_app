import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, \
    QAction, QTabWidget,QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import getKorbitInfo.korbit_main as kbinfo

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Korbit 조회 프로그램'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()

class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1, "환전가")
        self.tabs.addTab(self.tab2, "최근 거래 정보")
        self.tabs.addTab(self.tab3, "사용자 정보")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("pushButton1")
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab
        self.tab2.layout = QVBoxLayout(self)
        self.pushButton2 = QPushButton("pushButton2")
        self.tab2.layout.addWidget(self.pushButton2)
        self.tab2.setLayout(self.tab2.layout)

        key, sec_key, username, password = kbinfo.getAttributes("../keys.csv")
        token = kbinfo.getToken(username, password, key, sec_key)
        access_token, token_type = token[0], token[2]
        u_info = kbinfo.getUserInfo(access_token, token_type)

        # Create second tab
        self.tab3.layout = QVBoxLayout(self)
        self.text_label1, self.text_label2, self.text_label3, self.text_label4, self.text_label5 = \
            QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)
        self.text_label1.setText("이메일 : {}".format(u_info[5]))
        self.text_label2.setText("이름 : {}".format(u_info[3]))
        self.text_label3.setText("휴대폰 번호 : {}".format(u_info[4]))
        self.text_label4.setText("성별 : {}".format(u_info[1]))
        self.text_label5.setText("User Level : {}".format(u_info[2]))
        self.tab3.layout.addWidget(self.text_label1)
        self.tab3.layout.addWidget(self.text_label2)
        self.tab3.layout.addWidget(self.text_label3)
        self.tab3.layout.addWidget(self.text_label4)
        self.tab3.layout.addWidget(self.text_label5)
        self.tab3.setLayout(self.tab3.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())