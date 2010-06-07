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

import gettext
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from swatchbook import *
import swatchbook.codecs as codecs
import swatchbook.websvc as websvc

__version__ = "0.7"

swatchbooker_svg = (dirpath(__file__) or ".")+"/icons/swatchbooker.svg" 

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		
		self.setWindowTitle(_('SwatchBooker Batch Convertor'))
		self.setWindowIcon(QIcon(swatchbooker_svg))

		mainWidget = QWidget()

		self.threads = 0
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
		inputLayout.addWidget(self.addFile,0,1)
		inputLayout.addWidget(self.addWeb,1,1)
		inputLayout.addWidget(self.removeButton,2,1)
		inputLayout.addWidget(self.removeAllButton,3,1)
		inputLayout.rowStretch(4)
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
			thread = fileOpenThread(flist,self)
			self.connect(thread, SIGNAL("added()"), self.updateProgressBar)
			self.connect(thread, SIGNAL("finished()"), self.toggleAdding)
			self.connect(thread, SIGNAL("terminated()"), self.toggleAdding)
			self.tobeadded += flist.count()
			self.progress.setMaximum(self.tobeadded)
			self.progress.setValue(self.added)
			self.progress.show()
			self.threads += 1
			self.convertButton.setEnabled(False)
			self.removeAllButton.setEnabled(False)
			thread.start()

	def webOpen(self):
		dialog = webOpenDlg(self)
		if dialog.exec_() and dialog.svc and dialog.ids:
			thread = webOpenThread(dialog.svc,dialog.ids,self)
			self.connect(thread, SIGNAL("added()"), self.updateProgressBar)
			self.connect(thread, SIGNAL("finished()"), self.toggleAdding)
			self.connect(thread, SIGNAL("terminated()"), self.toggleAdding)
			self.tobeadded += len(dialog.ids)
			self.progress.setMaximum(self.tobeadded)
			self.progress.setValue(self.added)
			self.progress.show()
			self.threads += 1
			self.convertButton.setEnabled(False)
			self.removeAllButton.setEnabled(False)
			thread.start()

	def toggleAdding(self):
		self.threads -= 1
		if self.threads == 0:
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
	def __init__(self, flist, parent = None):
		super(fileOpenThread, self).__init__(parent)
		self.flist = flist

	def run(self):
		for fname in self.flist:
			try:
				sb = SwatchBook(unicode(fname))
				self.parent().tobeconverted.append([sb,False])
				row = self.parent().list.rowCount()
				self.parent().list.insertRow(row)
				self.parent().list.setItem(row,1,QTableWidgetItem(sb.info.title))
				self.parent().list.setItem(row,2,QTableWidgetItem(str(len(sb.swatches))))
				self.emit(SIGNAL("added()"))
			except FileFormatError:
				pass

class webOpenThread(QThread):
	def __init__(self, svc, ids, parent = None):
		super(webOpenThread, self).__init__(parent)
		self.svc = svc
		self.ids = ids

	def run(self):
		for id in self.ids:
			sb = SwatchBook(websvc=self.svc,webid=id)
			self.parent().tobeconverted.append([sb,False])
			row = self.parent().list.rowCount()
			self.parent().list.insertRow(row)
			self.parent().list.setItem(row,1,QTableWidgetItem(sb.info.title))
			self.parent().list.setItem(row,2,QTableWidgetItem(str(len(sb.swatches))))
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

class webOpenDlg(QDialog):
	def __init__(self, parent=None):
		super(webOpenDlg, self).__init__(parent)

		self.svc = False
		self.ids = False

		self.webSvcStack = QStackedWidget()
		self.webSvcList = QListWidget(self)
		palette = self.webSvcList.palette()
		palette.setColor(QPalette.Base,Qt.transparent)
		self.webSvcList.setPalette(palette)
		self.webSvcList.setFrameShape(QFrame.NoFrame)
		aboutBox = QGroupBox(_("About"))
		self.about = QLabel()
		self.about.setWordWrap(True)
		self.about.setOpenExternalLinks(True)
		aboutBoxLayout = QVBoxLayout()
		aboutBoxLayout.addWidget(self.about)
		aboutBox.setLayout(aboutBoxLayout)

		self.webWidgets = {}

		for svc in websvc.list:
			current_svc = eval('websvc.'+svc+'()')
			if 'swatchbook' in current_svc.content:
				webWidget = webWidgetList(svc,self)
			else:
				continue
			self.webSvcStack.addWidget(webWidget)
			listItem = QListWidgetItem(websvc.list[svc],self.webSvcList)
			listItem.setData(Qt.UserRole,svc)
			icon = (dirpath(__file__) or '.')+'/swatchbook/websvc/'+svc+'.png'
			if(QFile.exists(icon)):
				listItem.setIcon(QIcon(icon))
			self.webWidgets[svc] = (webWidget,current_svc.about,listItem)
		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
		self.webSvcList.sortItems()
		if settings.contains('lastWebSvc') and str(settings.value('lastWebSvc').toString()) in self.webWidgets:
			self.webSvcList.setCurrentItem(self.webWidgets[str(settings.value('lastWebSvc').toString())][2])
		else:
			self.webSvcList.setCurrentRow(0)
		self.changeTab()

		web1 = QWidget()
		web1l = QGridLayout()
		web1l.setContentsMargins(0,0,0,0)
		web1l.setSpacing(0)
		web1l.addWidget(self.webSvcList,0,0)
		web1l.addWidget(self.webSvcStack,0,1)
		web1.setLayout(web1l)

		webl = QGridLayout()
		webl.addWidget(web1,0,0,Qt.AlignTop)
		webl.addWidget(aboutBox,0,1,Qt.AlignTop)
		webl.addWidget(buttonBox,1,0,1,3)
		self.setLayout(webl)

		self.setWindowTitle(_("Add from web"))
		self.connect(self.webSvcList,
				SIGNAL("itemSelectionChanged()"), self.changeTab)
		self.connect(buttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
		self.connect(buttonBox, SIGNAL("rejected()"), self, SLOT("reject()"))

	def changeTab(self):
		self.svc = str(self.webSvcList.selectedItems()[0].data(Qt.UserRole).toString())
		self.ids = False
		self.webSvcStack.setCurrentWidget(self.webWidgets[self.svc][0])
		self.about.setText(self.webWidgets[self.svc][1])
		self.webSvcStack.currentWidget().load()
		self.webSvcList.setCurrentItem(self.webSvcList.selectedItems()[0],QItemSelectionModel.Current)
		settings.setValue('lastWebSvc',QVariant(self.svc))

class webWidgetList(QTreeWidget):
	def __init__(self, svc, parent=None):
		super(webWidgetList, self).__init__(parent)
		self.loaded = False
		self.parent = parent
		self.svc = eval('websvc.'+svc+'()')
		self.setHeaderHidden(True)
		self.setColumnHidden(1,True)
		self.setFrameShape(QFrame.NoFrame)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.connect(self,
				SIGNAL("itemSelectionChanged()"), self.activate)
		self.connect(self,
				SIGNAL("itemExpanded(QTreeWidgetItem *)"), self.nextLevel)

	def activate(self):
		self.parent.ids = False
		if self.selectedItems():
			self.parent.ids = []
			for item in self.selectedItems():
				self.parent.ids.append(unicode(item.text(1)))

	def load(self):
		if not self.loaded:
			try:
				root = self.svc.level0()
			except IOError:
				root = []
			for item in root:
				itemtext = QStringList()
				itemtext << root[item] << item
				titem = QTreeWidgetItem(self,itemtext)
				if self.svc.nbLevels > 1:
					titem.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
					titem.setFlags(titem.flags() & ~(Qt.ItemIsSelectable))
			self.loaded = True

	def nextLevel(self,treeItem):
		if treeItem.childCount() == 0:
			level = 1
			parent = treeItem.parent()
			while parent:
				parent = parent.parent()
				level += 1
			llist = eval('self.svc.level'+str(level))(unicode(treeItem.text(1)))
			for item in llist:
				itemtext = QStringList()
				itemtext << llist[item] << item
				titem = QTreeWidgetItem(treeItem,itemtext)
				if self.svc.nbLevels > level+1:
					titem.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
					titem.setFlags(titem.flags() & ~(Qt.ItemIsSelectable))
					

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setOrganizationName("Selapa")
	app.setOrganizationDomain("selapa.net")
	app.setApplicationName("SwatchBooker")
	settings = QSettings()

	locale = settings.value("Language").toString() or QLocale.system().name()
	# translation of the app
	try:
		lang = gettext.translation('swatchbooker', 'locale', languages=[str(locale)])
		lang.install()
		def _(msgid):
			return lang.gettext(msgid).decode('utf-8')

		def n_(msgid0,msgid1,n):
			return lang.ngettext(msgid0,msgid1,n).decode('utf-8')
	except IOError:
		def _(msgid):
			return gettext.gettext(msgid).decode('utf-8')

		def n_(msgid0,msgid1,n):
			return gettext.ngettext(msgid0,msgid1,n).decode('utf-8')

	# translation of the built-in dialogs
	qtTranslator = QTranslator()
	if qtTranslator.load("qt_" + locale, QLibraryInfo.location(QLibraryInfo.TranslationsPath)):
		app.installTranslator(qtTranslator)

	form = MainWindow()
	form.show()

	app.exec_()
