#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QFileDialog, QInputDialog,QColorDialog
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        top = 400
        left = 400
        width = 800
        height = 600
        icon = "1.png"
        self.setWindowTitle("Графический редактор")
        self.setGeometry(top, left, width, height)
        self.setWindowIcon(QIcon(icon))
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.lastPoint = QPoint
        self.brushLineType = Qt.SolidLine
        self.statusBar().showMessage('')
        mainMenu = self.menuBar()
        mainMenu.setStyleSheet("border-bottom:1px solid;")
        fileMenu = mainMenu.addMenu("Файл")
        brushMenu = mainMenu.addMenu("Размер кисти")
        brushColor = mainMenu.addMenu("Цвет кисти")
        brushLine = mainMenu.addMenu("Тип кисти")
        backColor = mainMenu.addMenu("Цвет фона")
        backAction = QAction(QIcon("13.jpg"), "Выбрать цвет фона", self)
        backAction.setShortcut("Shift+4")
        backColor.addAction(backAction)
        backAction.triggered.connect(self.back)
        backPicAction = QAction(QIcon("14.png"), "Выбрать изображение фона", self)
        backPicAction.setShortcut("Shift+5")
        backColor.addAction(backPicAction)
        backPicAction.triggered.connect(self.backPicture)
        brushSolid = QAction(QIcon("10.png"), "Прямая", self)
        brushSolid.setShortcut("Shift+1")
        brushLine.addAction(brushSolid)
        brushSolid.triggered.connect(self.solid)
        brushDash = QAction(QIcon("11.png"), "Штрих", self)
        brushDash.setShortcut("Shift+2")
        brushLine.addAction(brushDash)
        brushDash.triggered.connect(self.dash)
        brushDot = QAction(QIcon("12.png"), "Пунктир", self)
        brushDot.setShortcut("Shift+3")
        brushDot.triggered.connect(self.dot)
        brushLine.addAction(brushDot)
        saveAction = QAction(QIcon("5.png"), "Сохранить", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)
        clearAction = QAction(QIcon("2.png"), "Очистить", self)
        clearAction.setShortcut("Ctrl+С")
        clearAction.triggered.connect(self.clear)
        fileMenu.addAction(clearAction)
        threepxAction = QAction(QIcon("3.jpg"), "3px", self)
        threepxAction.triggered.connect(self.threePx)
        brushMenu.addAction(threepxAction)
        editSize = QAction(QIcon("1.png"), "Выбрать размер", self)
        editSize.triggered.connect(self.editSize)
        fivepxAction = QAction(QIcon("3.jpg"), "5px", self)
        fivepxAction.triggered.connect(self.fivePx)
        brushMenu.addAction(fivepxAction)
        sevenpxAction = QAction(QIcon("3.jpg"), "7px", self)
        sevenpxAction.triggered.connect(self.sevenPx)
        brushMenu.addAction(sevenpxAction)
        ninepxAction = QAction(QIcon("3.jpg"), "9px", self)
        ninepxAction.triggered.connect(self.ninePx)
        brushMenu.addAction(ninepxAction)
        brushMenu.addAction(editSize)
        blackAction = QAction(QIcon("8.png"), "Черный", self)
        brushColor.addAction(blackAction)
        blackAction.triggered.connect(self.blackColor)
        redAction = QAction(QIcon("7.png"), "Красный", self)
        brushColor.addAction(redAction)
        redAction.triggered.connect(self.redColor)
        greenAction = QAction(QIcon("9.png"), "Зеленый", self)
        brushColor.addAction(greenAction)
        greenAction.triggered.connect(self.greenColor)
        yellowAction = QAction(QIcon("6.png"), "Жёлтый", self)
        brushColor.addAction(yellowAction)
        editColor = QAction(QIcon("4.png"), "Выбрать цвет", self)
        editColor.triggered.connect(self.editColor)
        editColor.setShortcut("Ctrl+P")
        brushColor.addAction(editColor)
        yellowAction.triggered.connect(self.yellowColor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(
                QPen(
                    self.brushColor,
                    self.brushSize,
                    self.brushLineType,
                    Qt.RoundCap,
                    Qt.RoundJoin,
                )
            )
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def back(self):
        color = QColorDialog.getColor()
        self.image.fill(color)
        self.statusBar().showMessage(f'Текущий цвет фона {color.name()}')

    def backPicture(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "PNG(*.png);;JPEG(*.jpg);;All files (*.*)"
        )
        if filePath == "":
            return
        self.image.load(filePath)
        self.statusBar().showMessage('Изображение установлено')

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg);;All files (*.*)"
        )
        if filePath == "":
            return
        self.image.save(filePath)
        self.statusBar().showMessage('Сохранено в папке '+ filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()
        self.statusBar().showMessage('Очищено')

    def solid(self):
        self.brushLineType = Qt.SolidLine

    def dash(self):
        self.brushLineType = Qt.DashLine

    def dot(self):
        self.brushLineType = Qt.DotLine

    def threePx(self):
        self.brushSize = 3

    def fivePx(self):
        self.brushSize = 5

    def sevenPx(self):
        self.brushSize = 7

    def ninePx(self):
        self.brushSize = 9

    def editSize(self):
        i, okPressed = QInputDialog.getInt(self, "Введите размер", "Размер:", 15, 2, 100, 1)
        if okPressed:
            self.brushSize = i
        self.statusBar().showMessage(f'Текущий размер кисти -  {i}')

    def blackColor(self):
        self.brushColor = Qt.black

    def whiteColor(self):
        self.brushColor = Qt.white

    def redColor(self):
        self.brushColor = Qt.red

    def greenColor(self):
        self.brushColor = Qt.green

    def yellowColor(self):
        self.brushColor = Qt.yellow

    def editColor(self):
        color = QColorDialog.getColor()
        self.brushColor = color
        self.statusBar().showMessage(f'Текущий цвет кисти -  {color.name()}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
