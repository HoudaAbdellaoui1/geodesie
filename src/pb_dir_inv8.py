import designer_wins.ellipse1
from PyQt5.QtGui import QColor
from PySide2.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets

from functions import *
import designer_wins.images_rc
import designer_wins.pb_dir_inverse
import home,ellipse1,menu_conversion,three_latitudes4,rcourbure5,l_arc6,surface_part7

#Pour adapter la fenetre aux ecrans a haute resolution
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
# valeur globale pour l etat de la fenetre
WINDOW_SIZE = 0  # CETTE VARIABLE NOUS PERMET DE DEFINIR SI LA FENETRE EST AGRANDIE OU MINIMISEE

class Main8(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = designer_wins.pb_dir_inverse.Ui_MainWindow()
        self.ui.setupUi(self)

        # Remove window title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Set main background to transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Apply shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 150))
        # Appy shadow to central widget
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        # Button click events for top bar buttons
        # Minimiser la fenetre
        self.ui.minimizeButton_2.clicked.connect(lambda: self.showMinimized())
        # Restaurer la fenetre
        self.ui.restoreButton_2.clicked.connect(lambda: self.restore_or_maximize_window())
        # Fermer la fenetre
        self.ui.closeButton_2.clicked.connect(lambda: self.close())

        # Deplacer la fenetre si on fait appuyer la souris sur la barre de titre
        def move_window(e):
            # Detecter si la fentere est dans sa taille normale
            if self.isMaximized() == False:
                # deplacer la fenetre seulement si elle est dans sa taille normale
                if e.buttons() == QtCore.Qt.LeftButton:  # si le bouton gauche est appuye
                    # Deplacer la fenetre
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()

        # ajouter l'evenement click a l entete pour deplacer la fenetre
        self.ui.main_header.mouseMoveEvent = move_window
        self.ui.btn_calculer.clicked.connect(lambda :self.direct())
        self.ui.btn_calculer_2.clicked.connect(lambda : self.inverse())
        self.ui.pushButton_3.clicked.connect(lambda: self.slideLeftMenu())
        self.show()

        # fonction de restaurer/agrandir la fenetre

    def restore_or_maximize_window(self):
        global WINDOW_SIZE
        win_status = WINDOW_SIZE

        if win_status == 0:
            # si la fenetre n est pas agrandie
            WINDOW_SIZE = 1
            self.showMaximized()
            self.ui.restoreButton_2.setIcon(QtGui.QIcon("/icons/icons/cil-window-maximize.png"))
        else:  # si la fenetre est dans sa taille par defaut
            WINDOW_SIZE = 0
            self.showNormal()
            self.ui.restoreButton_2.setIcon(QtGui.QIcon(u"/icons/icons/cil-window-restore.png"))

        # Add mouse events to the window

    def mousePressEvent(self, event):
        # position actuelle de la souris
        self.clickPosition = event.globalPos()
        # on va utiliser cette valeur pour deplacer la fenetre

    def slideLeftMenu(self):
        # Obtenir la largeur actuelle du menu
        width = self.ui.left_side_menu.width()
        # Si le menu est minimise
        if width == 45:
            newWidth = 145
        else:
            newWidth = 45

        self.animation = QPropertyAnimation(self.ui.left_side_menu, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

        # menu_connections
        self.ui.pushButton_4.clicked.connect(lambda: home.MainWindow().show())
        self.ui.Fct1_btn_2.clicked.connect(lambda: ellipse1.MainWindow().show())
        self.ui.Fct2_btn_2.clicked.connect(lambda:menu_conversion.MainWindow().show())
        self.ui.Fct3_btn_2.clicked.connect(lambda: three_latitudes4.Main4().show())
        self.ui.Fct4_btn_2.clicked.connect(lambda: rcourbure5.Main5().show())
        self.ui.Fct5_btn_2.clicked.connect(lambda: surface_part7.Main7().show())
        self.ui.Fct6_btn_2.clicked.connect(lambda: l_arc6.Main6().show())
        self.ui.Fct7_btn_2.clicked.connect(lambda: self.show())

    def direct(self):
        phi = float(self.ui.phi1.text())
        lamb= float(self.ui.lambda1.text())
        a = float(self.ui.azimut_dep.text())
        s = float(self.ui.distance.text())
        self.ui.phi2_output.setText(str(pb_direct(phi,lamb,s,a)[0]))
        self.ui.lambda2output.setText(str(pb_direct(phi,lamb,s,a)[1]))
        self.ui.a21_output.setText(str(pb_direct(phi,lamb,s,a)[2]))

    def inverse(self):
        phi1 = float(self.ui.phi1_2.text())
        lambda1 = float(self.ui.lambda1_2.text())
        phi2 = float(self.ui.phi2.text())
        lambda2 = float(self.ui.lambda2.text())
        self.ui.a12_output.setText(str(pb_inverse(phi1,lambda1,phi2,lambda2)[0]))
        self.ui.a21_output_2.setText(str(pb_inverse(phi1,lambda1,phi2,lambda2)[1]))
        self.ui.s12_output.setText(str(pb_inverse(phi1,lambda1,phi2,lambda2)[2]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main8()
    app.exec_()