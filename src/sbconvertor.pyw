#!/usr/bin/env python
# coding: utf-8
#
#       Copyright 2010 Olivier Berten <olivier.berten@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#

from sbcommon import *

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		
		self.setWindowTitle(_('SwatchBooker Batch Convertor'))
		self.setWindowIcon(QIcon(":/swatchbooker.svg"))

		mainWidget = QWidget()

		self.threads = []
		self.tobeadded = 0
		self.added = 0
		self.tobeconverted = []
		self.list = QTableWidget()
		self.list.horizontalHeader().setStretchLastSection(True)
		self.list.verticalHeader().hide()
		self.list.horizontalHeader().hide()
		self.list.setColumnCount(2)
		self.list.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.list.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.list.setColumnWidth(0,32)
		self.list.setShowGrid(False)

		self.addFile = QPushButton(_("Add files"))
		self.addWeb = QPushButton(_("Add from web"))
		self.removeButton = QPushButton(_("Remove"))
		self.removeButton.setEnabled(False)
		self.removeAllButton = QPushButton(_("Remove all"))
		self.removeAllButton.setEnabled(False)
		self.progress = QProgressBar()
		self.progress.setFormat("%v/%m")
		self.progress.hide()

		inputLayout = QGridLayout()
		inputLayout.addWidget(self.list,0,0,6,1)
		inputLayout.setColumnStretch(0,1)
		inputLayout.addWidget(self.addFile,0,1)
		inputLayout.addWidget(self.addWeb,1,1)
		inputLayout.addWidget(self.removeButton,2,1)
		inputLayout.addWidget(self.removeAllButton,3,1)
		inputLayout.setRowStretch(4,1)
		inputLayout.addWidget(self.progress,5,1)

		if settings.contains('lastSaveDir'):
			self.path = unicode(settings.value('lastSaveDir').toString())
		else:
			self.path = unicode(QDir.homePath())

		self.pathLabel = QLabel(self.path)
		self.pathLabel.setFrameStyle(QFrame.StyledPanel|
										 QFrame.Sunken)
		self.pathButton = QPushButton(_("Choose output directory"))

		outputLayout = QHBoxLayout()
		outputLayout.addWidget(QLabel(_("Output directory:")))
		outputLayout.addWidget(self.pathLabel, 1)
		outputLayout.addWidget(self.pathButton)

		self.formatCombo = QComboBox()
		for codec in sorted(codecs.writes):
			codec_exts = []
			for ext in eval('codecs.'+codec).ext:
				codec_exts.append('*.'+ext)
			self.formatCombo.addItem(eval('codecs.'+codec).__doc__ +' ('+" ".join(codec_exts)+')',QVariant(codec))
		
		if settings.contains('lastSaveCodec'):
			self.formatCombo.setCurrentIndex(self.formatCombo.findText(settings.value('lastSaveCodec').toString()))

		formatLayout = QHBoxLayout()
		formatLayout.addWidget(QLabel(_("Output format:")))
		formatLayout.addWidget(self.formatCombo)
		
		self.convertButton = QPushButton(_("Convert"))
		self.convertButton.setEnabled(False)

		layout = QVBoxLayout()
		layout.addLayout(inputLayout)
		layout.addLayout(outputLayout)
		layout.addLayout(formatLayout)
		layout.addWidget(self.convertButton)
		mainWidget.setLayout(layout)
		
		self.setCentralWidget(mainWidget)

		self.connect(self.addFile, SIGNAL("clicked()"),
					 self.fileOpen)
		self.connect(self.addWeb, SIGNAL("clicked()"),
					 self.webOpen)
		self.connect(self.removeButton, SIGNAL("clicked()"),
					 self.remove)
		self.connect(self.removeAllButton, SIGNAL("clicked()"),
					 self.removeAll)
		self.connect(self.convertButton, SIGNAL("clicked()"),
					 self.convert)
		self.connect(self.pathButton, SIGNAL("clicked()"),
					 self.setPath)
		self.connect(self.list, SIGNAL("itemSelectionChanged()"),
					 self.toggleRemove)
		self.connect(self.formatCombo, SIGNAL("currentIndexChanged(int)"),
					 self.paramsChanged)
		
	def setPath(self):
		path = unicode(QDir.toNativeSeparators(QFileDialog.getExistingDirectory(self,
					_("Choose output directory"), self.path)))
		if path > '' and path != self.path:
			self.path = path
			self.pathLabel.setText(self.path)
			self.paramsChanged()
		
	def paramsChanged(self):
		if self.list.rowCount() > 0:
			self.convertButton.setEnabled(True)
			for index in range(self.list.rowCount()):
				self.list.setCellWidget(index,0,QWidget())
				self.tobeconverted[index][1] = False

	def fileOpen(self):
		dir = settings.value('lastOpenDir').toString() if settings.contains('lastOpenDir') else QDir.homePath()
		filetypes = []
		for codec in codecs.reads:
			codec_exts = []
			for ext in eval('codecs.'+codec).ext:
				codec_exts.append('*.'+ext)
			codec_txt = eval('codecs.'+codec).__doc__ +' ('+" ".join(codec_exts)+')'
			filetypes.append(codec_txt)
		allexts = ["*.%s" % unicode(format).lower() \
				   for format in codecs.readexts.keys()]
		if settings.contains('lastOpenCodec'):
			filetype = settings.value('lastOpenCodec').toString()
		else:
			filetype = QString()
		flist = QFileDialog.getOpenFileNames(self,
							_("Add files"), dir,
							(unicode(_("All supported files (%s)")) % " ".join(allexts))+";;"+(";;".join(sorted(filetypes)))+";;"+_("All files (*)"),filetype)
		if flist.count() > 0:
			settings.setValue('lastOpenCodec',QVariant(filetype))
			settings.setValue('lastOpenDir',QVariant(os.path.dirname(unicode(flist[0]))))
			self.tobeadded += flist.count()
			self.progress.setMaximum(self.tobeadded)
			self.progress.setValue(self.added)
			self.progress.show()
			self.convertButton.setEnabled(False)
			self.removeAllButton.setEnabled(False)
			for fname in flist:
				thread = fileOpenThread(fname,self)
				self.connect(thread, SIGNAL("added()"), self.updateProgressBar)
				self.connect(thread, SIGNAL("finished()"), self.toggleAdding)
				self.connect(thread, SIGNAL("terminated()"), self.toggleAdding)
				self.threads.append(thread)
				thread.start()

	def webOpen(self):
		try:
			dialog = webOpenDlg(self,settings,True)
			if dialog.exec_() and dialog.svc and dialog.ids:
				self.tobeadded += len(dialog.ids)
				self.progress.setMaximum(self.tobeadded)
				self.progress.setValue(self.added)
				self.progress.show()
				self.convertButton.setEnabled(False)
				self.removeAllButton.setEnabled(False)
				for id in dialog.ids:
					thread = webOpenThread(dialog.svc,id,self)
					self.connect(thread, SIGNAL("added()"), self.updateProgressBar)
					self.connect(thread, SIGNAL("finished()"), self.toggleAdding)
					self.connect(thread, SIGNAL("terminated()"), self.toggleAdding)
					self.threads.append(thread)
					thread.start()
		except IOError:
			QMessageBox.critical(self, _('Error'), _("No internet connexion has been found"))

	def toggleAdding(self):
		self.threads.remove(self.sender())
		if len(self.threads) == 0:
			if  len(self.tobeconverted) > 0:
				self.removeAllButton.setEnabled(True)
				self.convertButton.setEnabled(True)
			self.progress.hide()
			self.tobeadded = 0
			self.added = 0

	def updateProgressBar(self):
		self.added += 1
		self.progress.setValue(self.added)

	def remove(self):
		itemIndexes = []
		for item in self.list.selectedItems():
			itemIndexes.append(self.list.row(item))
		for i in sorted(itemIndexes,reverse=True):
			self.list.removeRow(i)
			del self.tobeconverted[i]
		self.removeButton.setEnabled(False)
		if self.list.rowCount() == 0:
			self.removeAllButton.setEnabled(False)
			self.convertButton.setEnabled(False)

	def toggleRemove(self):
		if self.list.selectedItems() > 0:
			self.removeButton.setEnabled(True)
		else:
			self.removeButton.setEnabled(False)

	def removeAll(self):
		self.tobeconverted = []
		self.list.clear()
		self.list.setRowCount(0)
		self.removeAllButton.setEnabled(False)
		self.convertButton.setEnabled(False)

	def convert(self):
		codec = unicode(self.formatCombo.itemData(self.formatCombo.currentIndex()).toString())
		path = self.path
		settings.setValue('lastSaveCodec',QVariant(self.formatCombo.itemText(self.formatCombo.currentIndex())))
		settings.setValue('lastSaveDir',QVariant(path))
		thread = convertThread(path,codec,self)
		self.connect(thread, SIGNAL("converted(int)"), self.converted)
		self.connect(thread, SIGNAL("finished()"), self.allConverted)
		self.connect(thread, SIGNAL("terminated()"), self.allConverted)
		self.addFile.setEnabled(False)
		self.addWeb.setEnabled(False)
		self.removeButton.setEnabled(False)
		self.removeAllButton.setEnabled(False)
		self.convertButton.setEnabled(False)
		self.pathButton.setEnabled(False)
		self.formatCombo.setEnabled(False)
		self.repaint()
		self.setCursor(Qt.WaitCursor)
		thread.start()

	def converted(self,index):
		iconWidget = QLabel()
		iconWidget.setAlignment(Qt.AlignCenter)
		iconWidget.setPixmap(app.style().standardPixmap(QStyle.SP_DialogOkButton))
		self.list.setCellWidget(index,0,iconWidget)

	def allConverted(self):
		self.addFile.setEnabled(True)
		self.addWeb.setEnabled(True)
		self.removeAllButton.setEnabled(True)
		self.pathButton.setEnabled(True)
		self.formatCombo.setEnabled(True)
		self.unsetCursor()
#		self.list.setCurrentRow(-1)

class fileOpenThread(QThread):
	def __init__(self, fname, parent = None):
		super(fileOpenThread, self).__init__(parent)
		self.fname = fname

	def run(self):
		try:
			sb = SwatchBook(unicode(self.fname))
			self.parent().tobeconverted.append([sb,False])
			row = self.parent().list.rowCount()
			self.parent().list.insertRow(row)
			self.parent().list.setItem(row,1,QTableWidgetItem(sb.info.title))
#			self.parent().list.setItem(row,2,QTableWidgetItem(str(len(sb.materials))))
			self.emit(SIGNAL("added()"))
		except FileFormatError:
			pass

class webOpenThread(QThread):
	def __init__(self, svc, id, parent = None):
		super(webOpenThread, self).__init__(parent)
		self.svc = svc
		self.id = id

	def run(self):
		sb = SwatchBook(websvc=self.svc,webid=self.id)
		self.parent().tobeconverted.append([sb,False])
		row = self.parent().list.rowCount()
		self.parent().list.insertRow(row)
		self.parent().list.setItem(row,1,QTableWidgetItem(sb.info.title))
#		self.parent().list.setItem(row,2,QTableWidgetItem(str(len(sb.materials))))
		self.emit(SIGNAL("added()"))

class convertThread(QThread):
	def __init__(self, path, codec, parent = None):
		super(convertThread, self).__init__(parent)
		self.path = path
		self.codec = codec

	def run(self):
		ext = eval('codecs.'+self.codec).ext[0]
		for sb in self.parent().tobeconverted:
			if not sb[1]:
				fname = basename = os.path.join(self.path,sb[0].info.title)
				if os.path.exists(basename+'.'+ext):
					i = 1
					while os.path.exists(fname+'.'+ext):
						fname = basename+' ('+str(i)+')'
						i += 1
				sb[0].write(self.codec,fname+'.'+ext)
				sb[1] = True
				self.emit(SIGNAL("converted(int)"), self.parent().tobeconverted.index(sb))

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setOrganizationName("Selapa")
	app.setOrganizationDomain("selapa.net")
	app.setApplicationName("SwatchBooker")
	settings = QSettings()

	translate_sb(app,settings,globals())

	form = MainWindow()
	form.show()

	app.exec_()
