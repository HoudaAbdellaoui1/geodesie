import sys

import PyQt5
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMainWindow, QApplication

from designer_wins.home_designer import *
from PyQt5.QtGui import QColor
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtCore import QPropertyAnimation
import designer_wins.transformation
import ellipse1, l_arc6, pb_dir_inv8, three_latitudes4, rcourbure5, surface_part7,home,src.home,conversion_cartgeo2,conversion_geotocart3

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# global value for the src status
WINDOW_SIZE = 0  # CETTE VARIABLE NOUS PERMET DE DEFINIR SI LA FENETRE EST AGRANDIE OU MINIMISEE


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = designer_wins.transformation.Ui_MainWindow()
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
        self.ui.menu_btn.clicked.connect(lambda: self.slideLeftMenu())
        self.ui.carto_to_geo_btn.clicked.connect(lambda: conversion_cartgeo2.Main2().show())
        self.ui.geo_to_carto_btn.clicked.connect(lambda: conversion_geotocart3.Main3().show())
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

        #configurer le menu
            # menu_connections

    # menu_connections
        self.ui.pushButton_4.clicked.connect(lambda: home.MainWindow().show())
        self.ui.Fct1_btn_2.clicked.connect(lambda: ellipse1.MainWindow().show())
        self.ui.Fct2_btn_2.clicked.connect(lambda: self.show())
        self.ui.Fct3_btn_2.clicked.connect(lambda: three_latitudes4.Main4().show())
        self.ui.Fct4_btn_2.clicked.connect(lambda: rcourbure5.Main5().show())
        self.ui.Fct5_btn_2.clicked.connect(lambda: surface_part7.Main7().show())
        self.ui.Fct6_btn_2.clicked.connect(lambda: l_arc6.Main6().show())
        self.ui.Fct7_btn_2.clicked.connect(lambda: pb_dir_inv8.Main8().show())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
