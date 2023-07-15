# +-------------+--------------+-----------------------------------------------------------------+
# |   Author    |     Date     |                            Changed                              |
# +-------------+--------------+-----------------------------------------------------------------+
# |   pyuic5    |  2023/07/15  | Auto-generated (from resources/ui/personal_color_extractor.py   |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A.  |  2023/07/15  | All methods in FacePart() will return cv2.image                 |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A.  |  2023/07/16  | Added: load_image(), take_photo() in MainWindow                 |
# +-------------+--------------+-----------------------------------------------------------------+
# | underconnor |  2023/07/16  | something                                                       |
# +-------------+--------------+-----------------------------------------------------------------+
import cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import sys
from color_extractor.face_detector import FacePart


class CQLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()

class CQLineEdit(QLineEdit):
    clicked = pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()


class ImageLoadWorker(QThread):
    # errors
    # +------+----------------------+------------------------------------------------------+
    # |  #   |     error name       |                    raised when                       |
    # +------+----------------------+------------------------------------------------------+
    # |  0   |    File not found    | file does not exist                                  |
    # +------+----------------------+------------------------------------------------------+
    # |  99  |    Unknown           | unknown exception thrown                             |
    # +------+----------------------+------------------------------------------------------+

    imageSignal = pyqtSignal(QtGui.QPixmap)
    errorSignal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.running = True
        self._width = 0
        self._height = 0

    def run(self):
        while self.running:
            self.msleep(10)

    def update_size(self, w, h):
        self._width = w
        self._height = h

    def load(self, image_path):
        image = QtGui.QPixmap(image_path).scaled(self._width*9, self._height*9, Qt.KeepAspectRatio)

        self.imageSignal.emit(image)

# 만들려 헀으나 너무 졸리고 여러 문제가 발생해서 보류
"""
class WebcamImageLoadWorker(QThread):
    imageSignal = pyqtSignal(QtGui.QPixmap)

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def run(self):
        while True:
            if self.is_running:
                ret, frame = self.cap.read()

                if ret:
                    height, width, channel = frame.shape
                    bytes_per_line = channel * width
                    q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

                    pixmap = QPixmap.fromImage(q_image).scaled(300, 300, Qt.KeepAspectRatio)
                    self.imageSignal.emit(pixmap)

    def start_webcam(self):
        self.is_running = True

    def stop_webcam(self):
        self.is_running = False
        self.cap.release()
        cv2.destroyAllWindows()
"""

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

        self.imagePathLineEdit = CQLineEdit(self.centralwidget)
        self.imagePathLineEdit.setObjectName("imagePathLineEdit")
        self.imagePathLineEdit.clicked.connect(self.path_select)
        self.loadLayout.addWidget(self.imagePathLineEdit)

        self.loadButton = QPushButton(self.centralwidget)
        self.loadButton.setObjectName("loadButton")
        self.loadButton.setText("불러오기")
        self.loadLayout.addWidget(self.loadButton)

        self.loadImgeFromWebcamButton = QPushButton(self.centralwidget)
        self.loadImgeFromWebcamButton.setObjectName("loadImgeFromWebcamButton")
        self.loadImgeFromWebcamButton.setText("사진찍기")
        #self.loadImgeFromWebcamButton.clicked.connect(self.take_photo)
        self.loadLayout.addWidget(self.loadImgeFromWebcamButton)

        #self.webcamWorker = WebcamImageLoadWorker()
        #self.webcamWorker.imageSignal.connect(self.set_faceImageLabel)
        #self.webcamWorker.start()

        self.faceImageLabel = CQLabel(self.centralwidget)
        self.faceImageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.faceImageLabel.setObjectName("faceImageLabel")
        self.faceImageLabel.setText("이미지를 불러와 주세요")
        self.faceImageLabel.clicked.connect(lambda: self.clear_label(self.faceImageLabel, "이미지를 불러와 주세요"))
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

        self.loadWorker = ImageLoadWorker()
        self.loadWorker.imageSignal.connect(self.set_faceImageLabel)
        self.loadWorker.update_size(self.faceImageLabel.width(), self.faceImageLabel.height())
        self.loadWorker.start()

        self.loadButton.clicked.connect(self.load_image)

        self.show()

    def clear_label(self, label, text):
        label.clear()
        label.setText(text)

    def path_select(self):
        path = QFileDialog.getOpenFileName(self, "얼굴 이미지 불러오기", "", "Image file (*.png *.jpg *.jpeg)")[0]
        self.imagePathLineEdit.setText(path)

    def load_image(self):
        path = self.imagePathLineEdit.text()

        if not path:
            return

        try:
            f = open(path, 'rb')
        except FileNotFoundError:
            return
        else:
            f.close()

        self.loadWorker.load(path)

"""
    def take_photo(self):
        if not self.webcamWorker.is_running:
            self.webcamWorker.start_webcam()
        else:
            self.webcamWorker.stop_webcam()

    @pyqtSlot(QtGui.QPixmap)
    def set_faceImageLabel(self, data):
        self.faceImageLabel.setPixmap(data)
"""
    # TODO: 사진찍기 구현
    # *TODO: 퍼스널 컬러 추출하기 구현


app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec_())
