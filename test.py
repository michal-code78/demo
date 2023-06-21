# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QProgressBar
from PyQt5.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
import time
#========================================================================================================

# class Api to connect with OANDA
class Api:
#addr part of address exp https://api-fxpractice.oanda.com, inst exp DE30_EUR,
# gran exp M1
	def __init__(self, addr, inst, gran, count, token):		
		self.addr = addr
		self.inst = inst
		self.gran = gran
		self.count = count
		self.token = token
		
	
	def get_cand(self):
		import requests
		from requests.structures import CaseInsensitiveDict		
		url = "%s/v3/instruments/%s/candles?granularity=%s&count=%s" %(self.addr,
															self.inst, self.gran, self.count)
		headers = CaseInsensitiveDict()
		headers["Authorization"] = "Bearer %s" %(self.token)
		headers["Accept-Datetime-Format"] = "UNIX"
		headers["Content-Type"]= "application/json"
		try:
			resp = requests.get(url, headers=headers)
			
		except:
			wdict = {'errorMessage': 'Problem z internetem'}
		else:
			wdict=resp.json()

		return wdict

#funtion  to connect with oanda and generate string
def moja(ininst):
	from datetime import datetime
	ap = Api(
				addr = "https://api-fxpractice.oanda.com",
				inst = ininst, #"DE30_EUR", 'EUR_GBP', #'EUR_USD', #"DE30_EUR",
				gran = "S5",
				count = "2",
				token="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
						+ "xxxxxxxxxxxxxxxxxxxxxxxxxxx")
	
	cand = ap.get_cand()

	try:
		check = cand['candles'][0]['time']
	except:
		text_1 = cand['errorMessage']
	else:
		#this string looks like float can not be change directly to int 
		last_index =len(cand['candles']) -1
		tunix = int(float(cand['candles'][last_index]['time']))
		time1 = datetime.fromtimestamp(tunix)
		wtime = time1.strftime("%d-%m-%Y, Time %H:%M:%S")		
		text_1 = f"{wtime} Open: {cand['candles'][last_index]['mid']['o']}"
		
	return text_1
# class worker with metode do_work loop is activate and deactivating by
#global run_run
class Worker(QObject):
	progress = Signal(str)
	@Slot(int)
	def do_work(self,n):
		while run_run:
			text = moja("DE30_EUR")
			self.progress.emit(text)
			time.sleep(0.5)


		#self.completed.emit(i)


class Ui_MainWindow(QMainWindow):
	
	work_requested = Signal(int)
	button_1_stage = False
	
	def setupUi(self, MainWindow):
		#code genrated by qt disiner
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(800, 600)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		
		self.button_1 = QtWidgets.QPushButton(self.centralwidget)
		self.button_1.setGeometry(QtCore.QRect(190, 270, 141, 31))        
		self.button_1.setObjectName("button_1")
		
		self.Label_1 = QtWidgets.QLabel(self.centralwidget)
		self.Label_1.setGeometry(QtCore.QRect(170, 140, 401, 91))
		
		palette = QtGui.QPalette()
		brush = QtGui.QBrush(QtGui.QColor(204, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(204, 0, 0))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
		brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
		brush.setStyle(QtCore.Qt.SolidPattern)
		palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
		self.Label_1.setPalette(palette)
		font = QtGui.QFont()
		font.setFamily("DejaVu Sans")
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.Label_1.setFont(font)
		self.Label_1.setAutoFillBackground(False)
		self.Label_1.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.Label_1.setFrameShadow(QtWidgets.QFrame.Plain)
		self.Label_1.setTextFormat(QtCore.Qt.AutoText)
		self.Label_1.setAlignment(QtCore.Qt.AlignCenter)
		self.Label_1.setWordWrap(True)
		self.Label_1.setObjectName("Label_1")
		self.button_2 = QtWidgets.QPushButton(self.centralwidget)
		self.button_2.setGeometry(QtCore.QRect(390, 270, 141, 31))
		self.button_2.setObjectName("button_2")
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		
		self.retranslateUi(MainWindow)
		#uruchumienie funkcji button_1,button_2 po kliknieciu
		self.button_1.clicked.connect(self.button_1_click)
		self.button_2.clicked.connect(self.button_2_click)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		
		
		self.worker = Worker()
		self.worker_thread = QThread()
		
		
		#self.worker.progress.connect(self.update_label_1)
		#self.worker.completed.connect(self.update_label_1)

		self.work_requested.connect(self.worker.do_work)

		self.worker.moveToThread(self.worker_thread)

		# start the thread
		self.worker_thread.start()

		
	def update_label_1(self,text):
		_translate = QtCore.QCoreApplication.translate
		self.Label_1.setText(_translate("MainWindow", str(text)))


	def retranslateUi(self, MainWindow):
		text_0 = 'Market -Michal Bogacz'
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Market -Michal Bogacz "))
		self.button_1.setText(_translate("MainWindow", "DAX-30"))
		self.Label_1.setText(_translate("MainWindow", text_0))
		self.button_2.setText(_translate("MainWindow", "Off"))
		
	def button_1_click(self):
		if not self.button_1_stage:
			global run_run
			global gininst
			run_run = True
			self.work_requested.emit(True)
			self.worker.progress.connect(self.update_label_1)
			self.button_1_stage = True

			

		
	def button_2_click(self):
		if self.button_1_stage:
			self.worker.progress.disconnect(self.update_label_1)
			self.button_1_stage = False
		global run_run
		run_run = False
		text = 'OFF'
		_translate = QtCore.QCoreApplication.translate
		self.Label_1.setText(_translate("MainWindow", text))
		#self.work_re2.emit(False)
		#self.work_requested.disconnect(self.worker.do_work)
	




if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	#app.setStyleSheet(Path('login.qss').read_text())
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys_info = app.exec_()
	run_run = False
	sys.exit(sys_info)

