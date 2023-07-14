# +------------+--------------+-----------------------------------------------------------------+
# |   Author   |     Date     |                            Changed                              |
# +------------+--------------+-----------------------------------------------------------------+
# |   pyuic5   |  2023/07/15  | Auto-generated (from resources/ui/personal_color_extractor.py   |
# +------------+--------------+-----------------------------------------------------------------+
# |  Andrew A. |  2023/07/14  | All methods in FacePart() will return cv2.image                 |
# +------------+--------------+-----------------------------------------------------------------+

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(570, 707)
        self.setMaximumSize(QtCore.QSize(16777204, 16777215))
        self.setWindowTitle("퍼스널 컬러 찾기")

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.baseVerticalLayout = QVBoxLayout()
        self.baseVerticalLayout.setObjectName("baseVerticalLayout")

        self.loadLayout = QHBoxLayout()
        self.loadLayout.setContentsMargins(-1, 0, -1, -1)
        self.loadLayout.setObjectName("loadLayout")
        self.baseVerticalLayout.addLayout(self.loadLayout)

        self.imagePathLineEdit = QLineEdit(self.centralwidget)
        self.imagePathLineEdit.setObjectName("imagePathLineEdit")
        self.loadLayout.addWidget(self.imagePathLineEdit)

        self.loadButton = QPushButton(self.centralwidget)
        self.loadButton.setObjectName("loadButton")
        self.loadButton.setText("불러오기")
        self.loadLayout.addWidget(self.loadButton)

        self.loadImgeFromWebcamButton = QPushButton(self.centralwidget)
        self.loadImgeFromWebcamButton.setObjectName("loadImgeFromWebcamButton")
        self.loadImgeFromWebcamButton.setText("사진찍기")
        self.loadLayout.addWidget(self.loadImgeFromWebcamButton)

        self.faceImageLabel = QLabel(self.centralwidget)
        self.faceImageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.faceImageLabel.setObjectName("faceImageLabel")
        self.faceImageLabel.setText("이미지를 불러와 주세요")
        self.baseVerticalLayout.addWidget(self.faceImageLabel)

        self.personalColorLabel = QLabel(self.centralwidget)
        self.personalColorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.personalColorLabel.setObjectName("personalColorLabel")
        self.personalColorLabel.setText("이미지를 불러온 후 \"추출하기\" 버튼을 누르세요.")
        self.baseVerticalLayout.addWidget(self.personalColorLabel)

        self.extractButton = QPushButton(self.centralwidget)
        self.extractButton.setObjectName("pushButton")
        self.extractButton.setText("퍼스널 컬러 추출하기")
        self.baseVerticalLayout.addWidget(self.extractButton)

        self.baseVerticalLayout.setStretch(1, 1)
        self.baseVerticalLayout.setStretch(2, 1)
        self.horizontalLayout.addLayout(self.baseVerticalLayout)
        self.setCentralWidget(self.centralwidget)

        self.show()

    # TODO: 파일 선택 기능 구현
    # TODO: 이미지 불러오기 기능 구현
    # TODO: 사진찍기 기능 구현
    # *TODO: 퍼스널 컬러 추출하기 구현


app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
