# +-------------+--------------+-----------------------------------------------------------------+
# |   Author    |     Date     |                            Changed                              |
# +-------------+--------------+-----------------------------------------------------------------+
# |   pyuic5    |  2023/07/15  | Auto-generated (from resources/ui/personal_color_extractor.py)  |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A.  |  2023/07/15  | All methods in FacePart() will return cv2.image                 |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A.  |  2023/07/16  | Added: load_image(), take_photo() in MainWindow                 |
# +-------------+--------------+-----------------------------------------------------------------+
# | underconnor |  2023/07/16  | something                                                       |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A.  |  2023/07/23  | Added feature: taking photo via webcam                          |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A.  |  2023/08/16  | WIP: writing ExtractWorker                                      |
# +-------------+--------------+-----------------------------------------------------------------+
# |   pyuic5    |  2023/10/19  | Auto-generated (resources/ui/personal_color_extractor_form.py)  |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A.  |  2023/10/19  | Connected with color_extractor, implemented ProcessWorker       |
# +-------------+--------------+-----------------------------------------------------------------+
# |   pyuic5    |  2023/10/20  | Auto-generated (from resources/ui/personal_color_result.py)     |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A.  |  2023/10/20  | Implemented ResultForm                                          |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A.  |  2023/10/23  | Implemented gacha                                               |
# +-------------+--------------+-----------------------------------------------------------------+
# |  Andrew A.  |  2023/10/25  | Refactored (on branch personal_color/refactor)                  |
# +-------------+--------------+-----------------------------------------------------------------+

from colormath.color_objects import LabColor, HSVColor, sRGBColor
from colormath.color_conversions import convert_color
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import color_extractor.colors as colors
import client.client as client
import color_extractor
import numpy as np
import pyqrcode
import logging
import cv2
import sys
import os

logging.basicConfig(
    level=logging.DEBUG,
    format="%(funcName)s %(levelname)s: %(message)s"
)
logging.getLogger("PC_main")


# -- Clickable QT Objects --
class CQLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()


class CQLineEdit(QLineEdit):
    clicked = pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()
# ---------------------------


class ImageLoadWorker(QThread):
    """
    ImageLoadWorker <- PyQt5.QtCore.QThread
    인수로 주어진 이미지를 불러옵니다.

    imageSignal(PyQt5.QtGui.QPixmap): 이미지를 내보내는 시그널입니다. 반드시 연결되어 있어야 합니다.
    errorSignal(int): 오류가 발생했을 떄 오류 코드를 전송하는 시그널입니다. 연결되지 않아도 괜찮습니다.
    """
    imageSignal = pyqtSignal(QtGui.QPixmap)
    errorSignal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.running = True
        self._width = 0
        self._height = 0

    def run(self):
        # 대기 상태로 계속 실행
        while self.running:
            self.msleep(10)

    def update_size(self, w, h):
        """
        돌려줄 이미지의 사이즈를 정합니다.

        :param w: 돌려줄 이미지의 폭입니다.
        :param h: 돌려줄 이미지의 높이입니디.
        """
        self._width = w
        self._height = h

    def load(self, image_path):
        """
        이미지를 불러와 imageSignal로 전송합니다.

        :param image_path: 로드할 이미지의 위치입니다.
        """
        image = QtGui.QPixmap(image_path).scaled(self._width * 9, self._height * 9, Qt.KeepAspectRatio)

        self.imageSignal.emit(image)


class WebcamImageLoadWorker(QThread):
    imageSignal = pyqtSignal(QtGui.QPixmap)

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_AUTO_WB, 0.0)
        self._width = 0
        self._height = 0
        self.frame = None  # 현재 프레임이나 바로 이전 프레임이 저장됩니다.

    def run(self):
        while True:
            # 웹캠에서 사진을 불러오지 않는 경우 대기
            if not self.is_running:
                self.msleep(100)
                continue

            ret, frame = self.cap.read()

            if ret:
                # cv2.image -> QPixmap 형식으로 변환
                height, width, channel = frame.shape
                bytes_per_line = channel * width
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame = cv2.flip(frame, 1)
                q_image = QtGui.QImage(self.frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)

                pixmap = QtGui.QPixmap.fromImage(q_image).scaled(self._width * 9, self._height * 9, Qt.KeepAspectRatio)
                self.imageSignal.emit(pixmap)

    def start_webcam(self):
        self.is_running = True

    def stop_webcam(self):
        self.is_running = False

    def update_size(self, w, h):
        self._width = w
        self._height = h

    def get_last_image(self):
        return self.frame


class StartForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(741, 371)
        self.setWindowTitle("프론 - 퍼스널 컬러 측정 - 시작하기")

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.pronLogoLabel = QLabel(self.centralwidget)
        self.pronLogoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.pronLogoLabel.setObjectName("pronLogoLabel")
        self.verticalLayout.addWidget(self.pronLogoLabel)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.nameEdit = QLineEdit(self.centralwidget)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 1, 1, 1, 1)
        self.nameEdit.setPlaceholderText("이름(혹은 별명)을 입력하세요")

        self.chromebookIDEdit = QLineEdit(self.centralwidget)
        self.chromebookIDEdit.setEnabled(False)
        self.chromebookIDEdit.setObjectName("chromebookIDEdit")
        self.gridLayout.addWidget(self.chromebookIDEdit, 0, 1, 1, 1)
        self.chromebookIDEdit.setPlaceholderText("크롬북 ID가 표시됩니다. ")

        self.chromebookIDLabel = QLabel(self.centralwidget)
        self.chromebookIDLabel.setObjectName("chromebookIDLabel")
        self.gridLayout.addWidget(self.chromebookIDLabel, 0, 0, 1, 1)
        self.chromebookIDLabel.setText("크롬북 ID")

        self.nameLabel = QLabel(self.centralwidget)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout.addWidget(self.nameLabel, 1, 0, 1, 1)
        self.nameLabel.setText("이름(별명)")

        self.verticalLayout.addLayout(self.gridLayout)

        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName("startButton")
        self.verticalLayout.addWidget(self.startButton)
        self.startButton.setText("시작하기")
        self.startButton.clicked.connect(self.start)

        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.setCentralWidget(self.centralwidget)

        self.show()
        self.display()

    def display(self):
        # 상단 그림 설정, CHROMEBOOK_ID fill
        pixmap = QtGui.QPixmap(os.path.join(os.path.dirname(__file__), "resources", "image", "logo.png")).scaled(666,
                                                                                                                 212)
        self.pronLogoLabel.setPixmap(pixmap)
        self.chromebookIDEdit.setText(client.get_chromebook_id())

    def start(self):
        if not self.nameEdit.text().strip():
            QMessageBox.critical(self, "오류",
                                 "이름을 입력해주세요!", QMessageBox.Yes, QMessageBox.Yes)
            return

        name = self.nameEdit.text().strip()
        client.update_name(name)  # client/data.dat 첫 번쨰 줄에 이름이 입력됩니다.

        self.__next__ = MainApp()
        self.close()


class ResultForm(QMainWindow):
    def __init__(self, tone):
        super().__init__()
        self.tone = tone
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(500, 500)
        self.setWindowTitle("퍼스널컬러 - 결과")

        color_label_font = QtGui.QFont()
        color_label_font.setFamily("Disket Mono")
        color_label_font.setPointSize(36)

        font_colorDescription = QtGui.QFont()
        font_colorDescription.setFamily("Nanum Gothic")
        font_colorDescription.setPointSize(13)

        font_clientID = QtGui.QFont()
        font_clientID.setFamily("Disket Mono")
        font_clientID.setPointSize(9)

        font_customerName = QtGui.QFont()
        font_customerName.setFamily("Nanum Gothic")
        font_customerName.setPointSize(9)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.setMinimumSize(QtCore.QSize(500, 500))
        self.setMaximumSize(QtCore.QSize(500, 500))

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.colorCodeLabel = QLabel(self.centralwidget)
        self.colorCodeLabel.setGeometry(QtCore.QRect(20, 325, 200, 61))
        self.colorCodeLabel.setFont(color_label_font)
        self.colorCodeLabel.setObjectName("colorCodeLabel")
        self.colorCodeLabel.setText("#######")

        self.colorDescription = QLabel(self.centralwidget)
        self.colorDescription.setGeometry(QtCore.QRect(25, 385, 450, 70))
        self.colorDescription.setWordWrap(True)
        self.colorDescription.setFont(font_colorDescription)
        self.colorDescription.setObjectName("colorDescription")
        self.colorDescription.setStyleSheet("background-color: transparent;")
        self.colorDescription.setWindowOpacity(1)

        self.clientID = QLabel(self.centralwidget)
        self.clientID.setGeometry(QtCore.QRect(10, 10, 121, 16))
        self.clientID.setFont(font_clientID)
        self.clientID.setObjectName("clientID")
        self.clientID.setText("CHROMEBOOK_##")

        self.customerName = QLabel(self.centralwidget)
        self.customerName.setGeometry(QtCore.QRect(430, 10, 60, 16))
        self.customerName.setFont(font_customerName)
        self.customerName.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.customerName.setObjectName("customerName")
        self.customerName.setText("NAME")

        self.qrlabel = QLabel(self.centralwidget)
        self.qrlabel.setGeometry(QtCore.QRect(125, 60, 250, 250))
        self.qrlabel.setStyleSheet("background-color: transparent;")

        self.webForFurtherInformation = QLabel(self.centralwidget)
        self.webForFurtherInformation.setFont(font_customerName)
        self.webForFurtherInformation.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.webForFurtherInformation.setStyleSheet("background-color: transparent;")
        self.webForFurtherInformation.setGeometry(QtCore.QRect(125, 290, 250, 10))
        self.webForFurtherInformation.setText("자세한 결과는 웹에서 확인해주세요!")

        self.setCentralWidget(self.centralwidget)
        self.display()

    def display(self):
        # 랜덤 판단
        if open(os.path.join(os.path.dirname(__file__), "gacha"), 'r').read().strip() == "true":
            color = colors.get_random_color()
        else:
            color = colors.get_random_color_from_tone(self.tone)

        description = colors.get_color_description(color)

        self.colorCodeLabel.setText("#" + color)
        # 일반적인 QLabel은 행간 설정을 지원하지 않아
        # 직접 스타일을 지정해줘야 합니다.
        self.colorDescription.setText(f"<p style='line-height: 150%'>{description}</p>")
        self.setStyleSheet(f'background-color: #{color}')

        # 퍼스널컬러 결과를 바탕으로 QR생성 및 불러오기
        # TODO: 여기서 버벅인다면 QThread로 처리할 것
        name = client.get_client_name()
        qr = pyqrcode.create(f"https://shinsungpron.github.io/colorresult?color={color}&name={name}", error="L", encoding='utf-8')
        qr.png("result.png", module_color=[0, 0, 0, 178], background=[255, 255, 255, 0], scale=10)  # 저장 후 다시 불러옴
        pixmap = QtGui.QPixmap("result.png").scaled(250, 250)
        self.qrlabel.setPixmap(pixmap)

        self.clientID.setText(client.get_chromebook_id())
        self.customerName.setText(client.get_client_name())

        client.update_color(color)  # client/data.dat 두 번쨰 줄에 퍼스널컬러 코드가 들어갑니다.
        client.send()  # 데이터베이스 서버로 데이터 전송


class ProcessWorker(QThread):
    setImageSignal = pyqtSignal(QtGui.QPixmap, int)
    messageSignal = pyqtSignal(str)
    done = pyqtSignal(str)
    error = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.extract = False

    def run(self):
        while True:
            self.msleep(100)
            if self.extract:
                print(self.image.shape)
                self.messageSignal.emit("화이트밸런싱 중")
                self.image = color_extractor.personal_color_extract.white_balance(self.image)
                self.messageSignal.emit("얼굴인식 중")

                # 얼굴이 인식되지 않으면 오류를 반환합니다. (pyqtSignal error 트리거)
                try:
                    face_parts = color_extractor.face_detector.FacePart(self.image)
                except ValueError:
                    self.error.emit()
                    return

                # TODO: _show_entire_points() 공개 메소드로 전환
                # _show_entire_points() 로 불러온 얼굴 인식 결과를
                # QPixmap으로 변환 -> ProcessingForm의 라벨에 넣습니다.
                face_points = face_parts._show_entire_points()
                height, width, channel = face_points.shape
                bytes_per_line = channel * width
                q_image = QtGui.QImage(face_points.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(q_image).scaled(self._facial_width * 9, self._facial_height * 9,
                                                                 Qt.KeepAspectRatio)
                self.setImageSignal.emit(pixmap, 0)

                # 인식된 얼굴 부위를 cv2.image -> QPixmap으로 케스팅해 facepart 라벨에 넣습니다.
                for i, part in enumerate(face_parts.available_parts):
                    img = face_parts.get_part(part)
                    height, width, channel = img.shape
                    bytes_per_line = channel * width
                    q_image = QtGui.QImage(img.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(q_image).scaled(self._height * 2, self._width * 2,
                                                                     Qt.KeepAspectRatio)
                    self.setImageSignal.emit(pixmap, i + 1)
                    self.msleep(300)

                # 얼굴의 각 부분별 주요 색상을 추출합니다.
                self.messageSignal.emit("각 부분별 주요 색상 추출 중")
                dominant_colors = [
                    color_extractor.dominant_color.DominantColor(face_parts.get_part(part)).get_dominant_color()
                    for part in face_parts.available_parts]

                # 왼쪽과 오른쪽의 평균으로 최종 결과를 계산합니다.
                cheek = np.mean([dominant_colors[0], dominant_colors[1]], axis=0)
                eye = np.mean([dominant_colors[2], dominant_colors[3]], axis=0)
                eyebrow = np.mean([dominant_colors[4], dominant_colors[5]], axis=0)

                self.messageSignal.emit("퍼스널 컬러 찾는 중")
                Lab_b = []
                hsv_s = []

                for part in (cheek, eyebrow, eye):
                    rgb = sRGBColor(part[0], part[1], part[2], is_upscaled=True)  # RGB로 변환
                    lab = convert_color(rgb, LabColor, through_rgb_type=sRGBColor)  # LAB으로 변환
                    hsv = convert_color(rgb, HSVColor, through_rgb_type=sRGBColor)  # HSV로 변환
                    Lab_b.append(float(format(lab.lab_b, ".2f")))
                    hsv_s.append(float(format(hsv.hsv_s, ".2f")) * 100)

                Lab_weight = [1, 1, 1]
                hsv_weight = [1, 1, 1]

                if color_extractor.personal_color_extract.is_warm(Lab_b, Lab_weight):
                    if color_extractor.personal_color_extract.is_spr(hsv_s, hsv_weight):
                        tone = '봄웜톤 (spring)'
                    else:
                        tone = '가을웜톤 (fall)'
                else:
                    if color_extractor.personal_color_extract.is_smr(hsv_s, hsv_weight):
                        tone = '여름쿨톤 (summer)'
                    else:
                        tone = '겨울쿨톤 (winter)'

                print(tone)
                self.messageSignal.emit(f"퍼스널컬러 유형: {tone}")
                self.done.emit(tone)  # 결과 반환
                self.extract = False  # 쓰레드 대기상태로 전환

    def extract_color_from_image(self, image):
        """
        이미지로부터 얼굴을 인식해 퍼스널컬러를 반환합니다.

        :param image: 퍼스널컬러를 추출할 이미지입니다. (numpy array 형식의 이미지)
        :return: done(str) <- pyqtSignal 로 추출된 퍼스널컬러의 톤 결과를 반환합니다.
        """
        self.image = image
        self.extract = True  # 쓰레드 작업상태로 전환

    def update_size_facial_landmarks(self, w, h):
        self._facial_width = w
        self._facial_height = h

    def update_size(self, w, h):
        self._width = w
        self._height = h


class ProcessingForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(870, 646)

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.baseHorizontal = QHBoxLayout()
        self.baseHorizontal.setObjectName("baseHorizontal")

        self.facialRecogResultLabel = QLabel(self.centralwidget)
        self.facialRecogResultLabel.setObjectName("facialRecogResultLabel")
        self.baseHorizontal.addWidget(self.facialRecogResultLabel)

        self.baseGrid = QGridLayout()
        self.baseGrid.setObjectName("baseGrid")

        self.rightEyeLabel = QLabel(self.centralwidget)
        self.rightEyeLabel.setObjectName("rightEyeLabel")
        self.baseGrid.addWidget(self.rightEyeLabel, 1, 1, 1, 1)

        self.leftCheekLabel = QLabel(self.centralwidget)
        self.leftCheekLabel.setObjectName("leftCheekLabel")
        self.baseGrid.addWidget(self.leftCheekLabel, 0, 0, 1, 1)

        self.rightCheekLabel = QLabel(self.centralwidget)
        self.rightCheekLabel.setObjectName("rightCheekLabel")
        self.baseGrid.addWidget(self.rightCheekLabel, 0, 1, 1, 1)

        self.leftEyeLabel = QLabel(self.centralwidget)
        self.leftEyeLabel.setObjectName("leftEyeLabel")
        self.baseGrid.addWidget(self.leftEyeLabel, 1, 0, 1, 1)

        self.leftEyebrowLabel = QLabel(self.centralwidget)
        self.leftEyebrowLabel.setObjectName("leftEyebrowLabel")
        self.baseGrid.addWidget(self.leftEyebrowLabel, 2, 0, 1, 1)

        self.rightEyebrowLabel = QLabel(self.centralwidget)
        self.rightEyebrowLabel.setObjectName("rightEyebrowLabel")
        self.baseGrid.addWidget(self.rightEyebrowLabel, 2, 1, 1, 1)

        self.baseHorizontal.addLayout(self.baseGrid)
        self.horizontalLayout_2.addLayout(self.baseHorizontal)

        self.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.worker = ProcessWorker()
        self.worker.setImageSignal.connect(self.set_image)
        self.worker.messageSignal.connect(self.set_message)
        self.worker.done.connect(self.done)
        self.worker.update_size_facial_landmarks(self.facialRecogResultLabel.width(),
                                                 self.facialRecogResultLabel.height())
        self.worker.update_size(self.leftEyeLabel.height(), self.leftEyeLabel.width())
        self.worker.error.connect(self.error)
        self.worker.start()

    def extract(self, image):
        self.worker.extract_color_from_image(image)

    @pyqtSlot(QtGui.QPixmap, int)
    def set_image(self, image, at):
        if at == 0:
            self.facialRecogResultLabel.setPixmap(image)
        elif at == 1:
            self.leftEyeLabel.setPixmap(image)
        elif at == 2:
            self.rightEyeLabel.setPixmap(image)
        elif at == 3:
            self.leftCheekLabel.setPixmap(image)
        elif at == 4:
            self.rightCheekLabel.setPixmap(image)
        elif at == 5:
            self.leftEyebrowLabel.setPixmap(image)
        elif at == 6:
            self.rightEyebrowLabel.setPixmap(image)

    @pyqtSlot(str)
    def set_message(self, message):
        self.statusbar.showMessage(message)

    @pyqtSlot(str)
    def done(self, color):
        self.w = ResultForm(color)
        self.w.show()
        self.close()

    @pyqtSlot()
    def error(self):
        QMessageBox.critical(self, "오류", "얼굴 인식을 실패했습니다.\n사진을 다시 찍어주세요.",
                             QMessageBox.Yes, QMessageBox.Yes)
        self.close()
        return


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.isTakingPhoto = False

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
        self.loadLayout.addWidget(self.loadImgeFromWebcamButton)

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
        self.extractButton.clicked.connect(self.extract)
        self.baseVerticalLayout.addWidget(self.extractButton)

        self.baseVerticalLayout.setStretch(1, 1)
        self.baseVerticalLayout.setStretch(2, 1)
        self.horizontalLayout.addLayout(self.baseVerticalLayout)
        self.setCentralWidget(self.centralwidget)

        self.loadWorker = ImageLoadWorker()
        self.loadWorker.imageSignal.connect(self.set_faceImageLabel)
        self.loadWorker.update_size(self.faceImageLabel.width(), self.faceImageLabel.height())
        self.loadWorker.start()

        self.webcamWorker = WebcamImageLoadWorker()
        self.webcamWorker.update_size(self.faceImageLabel.width(), self.faceImageLabel.height())
        self.loadImgeFromWebcamButton.clicked.connect(self.take_photo)
        self.webcamWorker.imageSignal.connect(self.set_faceImageLabel)
        self.webcamWorker.start()

        self.loadButton.clicked.connect(self.load_image)

        self.show()

    def clear_label(self, label, text):
        if self.isTakingPhoto:
            self.webcamWorker.stop_webcam()
            self.isTakingPhoto = False
        else:
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

    def take_photo(self):
        self.isTakingPhoto = True
        self.webcamWorker.start_webcam()

    @pyqtSlot(QtGui.QPixmap)
    def set_faceImageLabel(self, data):
        self.faceImageLabel.setPixmap(data)

    def extract(self):
        self.w = ProcessingForm()
        self.w.show()
        self.w.extract(self.webcamWorker.get_last_image())


app = QApplication(sys.argv)
QtGui.QFontDatabase.addApplicationFont("./resources/fonts/Disket-Mono-Regular.ttf")
QtGui.QFontDatabase.addApplicationFont("./resources/fonts/NanumGothic.otf")
main_window = StartForm()
main_window.show()
sys.exit(app.exec_())
