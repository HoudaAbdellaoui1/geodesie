import sys

import PyQt5
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMainWindow, QApplication

from designer_wins.home_designer import *
from PyQt5.QtGui import QColor
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtCore import QPropertyAnimation
import ellipse1, l_arc6, menu_conversion, pb_dir_inv8, three_latitudes4, rcourbure5, surface_part7

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# global value for the src status
WINDOW_SIZE = 0  # CETTE VARIABLE NOUS PERMET DE DEFINIR SI LA FENETRE EST AGRANDIE OU MINIMISEE


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
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
        self.ui.minimizeButton.clicked.connect(lambda: self.showMinimized())
            # Restaurer la fenetre
        self.ui.restoreButton.clicked.connect(lambda: self.restore_or_maximize_window())
            # Fermer la fenetre
        self.ui.closeButton.clicked.connect(lambda: self.close())

        # Deplacer la fenetre si on faire appuyer la souris sur la barre de titre
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
        self.ui.pushButton.clicked.connect(lambda: self.slideLeftMenu())
        self.show()



    # fonction de restaurer/agrandir la fenetre
    def restore_or_maximize_window(self):
        global WINDOW_SIZE
        win_status = WINDOW_SIZE

        if win_status == 0:
        # si la fenetre n est pas agrandie
            WINDOW_SIZE = 1
            self.showMaximized()
            self.ui.restoreButton.setIcon(QtGui.QIcon("/icons/icons/cil-window-maximize.png"))
        else:  # si la fenetre est dans sa taille par defaut
            WINDOW_SIZE = 0
            self.showNormal()
            self.ui.restoreButton.setIcon(QtGui.QIcon(u"/icons/icons/cil-window-restore.png"))

    # Add mouse events to the window
    def mousePressEvent(self, event):
        # position actuelle de la souris
        self.clickPosition = event.globalPos()
         # on va utiliser cette valeur pour deplacer la fenetre

    def slideLeftMenu(self):
    #Obtenir la largeur actuelle du menu
        width = self.ui.left_side_menu.width()
        #Si le menu est minimise
        if width == 45:
            newWidth = 150
        else:
            newWidth = 45

        #ajout de l'animation a la transition
        self.animation = QPropertyAnimation(self.ui.left_side_menu, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

        # menu_connections
        self.ui.Fct1_btn.clicked.connect(lambda: ellipse())
        self.ui.Fct2_btn.clicked.connect(lambda :conversion())
        self.ui.Fct3_btn.clicked.connect(lambda :latitudes())
        self.ui.Fct4_btn.clicked.connect(lambda :courbure())
        self.ui.Fct5_btn.clicked.connect(lambda : surface())
        self.ui.Fct6_btn.clicked.connect(lambda :longueur())
        self.ui.Fct7_btn.clicked.connect(lambda :problemes())

        def ellipse():
            ellipse1.MainWindow().show()
            self.close()

        def conversion():
            menu_conversion.MainWindow().show()
            self.close()

        def latitudes():
            three_latitudes4.Main4().show()
            self.close()

        def courbure():
            rcourbure5.Main5().show()
            self.close()

        def longueur():
            l_arc6.Main6().show()
            self.close()

        def surface():
            surface_part7.Main7().show()
            self.close()

        def problemes():
            pb_dir_inv8.Main8().show()
            self.close()


        # Connect the button "clicked" signal to the first function (l'ellipsoide)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
