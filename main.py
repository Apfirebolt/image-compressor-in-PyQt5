import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QObject, QRectF, Qt
from PySide2.QtWidgets import QMainWindow, QFileDialog, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, \
    QDialog, QLabel, QComboBox, QLineEdit, QHBoxLayout
from PySide2.QtGui import QPixmap
from PIL import Image


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.file_Select_Btn = QtWidgets.QPushButton(self.centralWidget)
        self.file_Select_Btn.setGeometry(QtCore.QRect(1082, 80, 121, 28))
        self.file_Select_Btn.setObjectName("file_Select_Btn")
        self.headingLabel = QtWidgets.QLabel('Image Compressor Tool in Python')
        self.headingLabel.setAlignment(Qt.AlignCenter)
        self.headingLabel.setStyleSheet("text-align: center; font-size: 20px;")
        self.file_Select_Btn.setText("Load Image")
        self.setWindowTitle("Image Compressor Python")
        self.setMinimumSize(400, 300)
        self.gridLayout.addWidget(self.headingLabel)
        self.gridLayout.addWidget(self.file_Select_Btn)
        MainWindow.setCentralWidget(self.centralWidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self)
        QMainWindow.__init__(self)

        # Initialize UI
        self.setupUi(self)
        self.file_Select_Btn.clicked.connect(self.showImage)

    def tr(self, text):
        return QObject.tr(self, text)

    def showImage(self):
        path_to_file, _ = QFileDialog.getOpenFileName(self, self.tr("Load Image"), self.tr("~/Desktop/"), self.tr("Images (*.jpg)"))

        if path_to_file:
            self.image_viewer = ImageViewer(path_to_file)
            self.image_viewer.show()
        else:
            self.show_info_dialog()

    
    def show_info_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Info!")
        dlg.layout = QVBoxLayout()
        message = QLabel("Please select a file")
        dlg.layout.addWidget(message)
        dlg.setLayout(dlg.layout)
        dlg.exec_()
        return


class ImageViewer(QWidget):
    def __init__(self, image_path):
        super().__init__()

        self.scene = QGraphicsScene()
        self.image_path = image_path
        self.view = QGraphicsView(self.scene)
        self.setWindowTitle("Image Compressor Python")
        self.setMinimumSize(800, 600)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.file_Compress_Btn = QtWidgets.QPushButton()
        self.file_Compress_Btn.setObjectName("file_Compress_Btn")
        self.file_Compress_Btn.setText("Compress Image")
        self.file_Compress_Btn.setStyleSheet("color: #FFF; background-color: #427ef5; padding: 5px")
        self.file_Compress_Btn.clicked.connect(self.compress_image)
        self.selectQuality = QComboBox()
        self.selectQuality.setStyleSheet("padding: 5px; background-color: #427ef5")
        for i in range(10, 100, 10):
	        self.selectQuality.addItem(str(i))

        self.fileName = QLineEdit('filename')
        self.fileName.setStyleSheet("padding: 5px")
        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addWidget(self.file_Compress_Btn, 1)
        self.bottomLayout.addWidget(self.selectQuality, 1)
        self.bottomLayout.addWidget(self.fileName, 1)

        layout.addLayout(self.bottomLayout)

        self.setLayout(layout)

        self.load_image(image_path)


    def load_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.scene.addPixmap(pixmap)
        self.view.fitInView(QRectF(0, 0, pixmap.width(), pixmap.height()), Qt.KeepAspectRatio)
        self.scene.update()
            

    
    def compress_image(self):

            # open the image
        picture = Image.open(self.image_path)
        
        picture.save(self.fileName.text() + '.jpg', 
                    "JPEG", 
                    optimize = True, 
                    quality = int(self.selectQuality.currentText()))
        
        dlg = QDialog(self)
        dlg.setWindowTitle("Info!")
        dlg.layout = QVBoxLayout()
        message = QLabel("Image just compressed and saved")
        dlg.layout.addWidget(message)
        dlg.setLayout(dlg.layout)
        dlg.exec_()
        return


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())