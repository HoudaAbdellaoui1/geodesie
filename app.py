import sys

from PyQt5.QtGui import QColor
from PySide2.QtWidgets import *
from designer_wins.loading_designer import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import home
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

progressBarValue = 0


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Home_Window()
        self.ui.setupUi(self)

        #Enlever la barre du titre de la fenetre
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        #Definir l arriere plan a transaprent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #Appliquer les effets d'ombre
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 150))

        #Appliquer l'ombre au central widget
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        #let's use QTIMER to delay the progress bar
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.app_progress)

        #Time interval in Milliseconds for the progressbar to change value
        self.timer.start(100)

        self.show()

    def app_progress(self):
        global progressBarValue
            #apply progressValue to the progressBar
        self.ui.my_progressBar.setValue(progressBarValue)

        if progressBarValue > 100:
            #reset / stop timer
            self.timer.stop()

            #close the app screen after the progress is complete
            self.close()
            home.window = home.MainWindow()
            home.window.show()

            #Change the loading status text
            QtCore.QTimer.singleShot(0, lambda: self.ui.label_3.
                                     setText("Chargement terminé!"))


        # Lets update the loading status text as the progress changes
        elif progressBarValue < 10:
            QtCore.QTimer.singleShot(0, lambda: self.ui.label_3.setText("Chargement de la calculatrice"))

        elif progressBarValue < 20:
            QtCore.QTimer.singleShot(0, lambda: self.ui.label_3.setText("Connexion..."))

        elif progressBarValue < 35:
            QtCore.QTimer.singleShot(0, lambda: self.ui.label_3.setText("Connexion réussie !"))

        elif progressBarValue < 55:
            QtCore.QTimer.singleShot(0, lambda: self.ui.label_3.setText("Demande des données ..."))

        elif progressBarValue < 65:
            QtCore.QTimer.singleShot(0, lambda: self.ui.label_3.setText("Finalisation ..."))

        elif progressBarValue < 85:
            QtCore.QTimer.singleShot(0, lambda: self.ui.label_3.setText("Presque là...."))

                # Change loadingstatus text
            QtCore.QTimer.singleShot(0, lambda: self.ui.loading_progress_label.setText("BIENVENUE !"))

        #increase progressBarValue by 1 after every time interval we set of 100 milliseconds;
        progressBarValue+=1




def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()