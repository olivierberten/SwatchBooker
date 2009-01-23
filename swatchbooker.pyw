#!/usr/bin/env python
# coding: utf-8
#
#       Copyright 2008 Olivier Berten <olivier.berten@gmail.com>
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

from __future__ import division
import sys
import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from swatchbook import *

__version__ = "0.3"

current_sw = False
current_sp = False

# 0: float, 1: percentage, 2: degrees
models = {'Lab':(('L',0),('a',0),('b',0)),
		  'XYZ':(('X',0),('Y',0),('Z',0)),
		  'RGB':(('R',1),('G',1),('B',1)),
		  'RGBa':(('R',1),('G',1),('B',1),(u'α',1)),
		  'CMY':(('C',1),('M',1),('Y',1)),
		  'HSL':(('H',2),('S',1),('L',1)),
		  'HSV':(('H',2),('S',1),('V',1)),
		  'CMYK':(('C',1),('M',1),('Y',1),('K',1)),
		  'CMYKOG':(('C',1),('M',1),('Y',1),('K',1),('O',1),('G',1)),
		  'Gray':(('K',1),),
		  'YIQ':(('Y',0),('I',0),('Q',0))
		 }

class GroupWidget(QGroupBox):
	def __init__(self, parent=None):
		global current_sw
		super(GroupWidget, self).__init__(parent)
		
		self.setTitle("Group")

		nameLabel = QLabel("Name:")
		self.swName = QLineEdit()
		self.swDescription = QTextEdit()
		descriptionLabel = QLabel("Description:")
		swInfo = QGridLayout()
		swInfo.addWidget(nameLabel, 0, 0)
		swInfo.addWidget(self.swName, 0, 1)
		swInfo.addWidget(descriptionLabel, 1, 0, 1, 2)
		swInfo.addWidget(self.swDescription, 2, 0, 1, 2)
		self.setLayout(swInfo)

		if hasattr(current_sw,'info'):
			if 'name' in current_sw.info:
				self.swName.setText(current_sw.info['name'][0])
			if 'description' in current_sw.info:
				self.swDescription.setText(current_sw.info['description'][0])

		# Actions
		self.connect(self.swName,
				SIGNAL("textEdited(QString)"), self.sw_edit)
		self.connect(self.swDescription,
				SIGNAL("textChanged()"), self.sw_edit)

	def sw_edit(self):
		global current_sw
		if  self.sender() == self.swName:
			if self.swName.text() == '':
				del current_sw.info['name'][0]
			else:
				if 'name' not in current_sw.info:
					current_sw.info['name'] = {}
				current_sw.info['name'][0] = unicode(self.swName.text())
		if  self.sender() == self.swDescription:
			if self.swDescription.toPlainText() == '':
				del current_sw.info['description'][0]
			else:
				if 'description' not in current_sw.info:
					current_sw.info['description'] = {}
				current_sw.info['description'][0] = unicode(self.swDescription.toPlainText())

class ColorWidget(QGroupBox):
	def __init__(self, parent=None):
		super(ColorWidget, self).__init__(parent)
		
		self.parent = parent
		self.setTitle("Color")

		nameLabel = QLabel("Name:")
		self.swName = QLineEdit()
		descriptionLabel = QLabel("Description:")
		self.swDescription = QTextEdit()
		self.sample = QLabel()
		self.sample.setMinimumHeight(30)
		self.swSpot = QCheckBox("Spot")
		self.swValues = QTabWidget()
		self.butVal = QToolButton(self.swValues)
		self.butVal.setFixedSize(12,12)
		cornLay = QVBoxLayout()
		cornLay.setContentsMargins(20,0,0,20)
		cornLay.addWidget(self.butVal)
		cornWid = QWidget()
		cornWid.setLayout(cornLay)
		cornWid.setMinimumSize(12,12)
		self.menuVal = QMenu()
		self.menuValModl = self.menuVal.addMenu('Add')
		global models
		for model in models:
			self.menuValModl.addAction(model,self.addVal)
		self.delValAction = self.menuVal.addAction('Remove',self.delVal)
		self.delValAction.setEnabled(False)
		self.butVal.setPopupMode(QToolButton.InstantPopup)
		self.butVal.setMenu(self.menuVal)
		self.swValues.setCornerWidget(cornWid)
		swInfo = QGridLayout()
		swInfo.addWidget(nameLabel, 0, 0)
		swInfo.addWidget(self.swName, 0, 1)
		swInfo.addWidget(descriptionLabel, 1, 0, 1, 2)
		swInfo.addWidget(self.swDescription, 2, 0, 1, 2)
		swInfo.addWidget(self.sample, 3, 0, 1, 2)
		swInfo.addWidget(self.swSpot, 4, 0, 1, 2)
		swInfo.addWidget(self.swValues, 5, 0, 1, 2)
		self.setLayout(swInfo)

		if hasattr(current_sw,'info'):
			if 'name' in current_sw.info:
				self.swName.setText(current_sw.info['name'][0])
			if 'description' in current_sw.info:
				self.swDescription.setText(current_sw.info['description'][0])
		if hasattr(current_sw,'attr') and 'spot' in current_sw.attr:
			self.swSpot.setChecked(True)
		self.val = {}
		if hasattr(current_sw,'values') and len(current_sw.values) > 0:
			self.delValAction.setEnabled(True)
			r,g,b = current_sw.toRGB8()
			self.sample.setStyleSheet("QWidget { background-color: #"+hex2(r)+hex2(g)+hex2(b)+" }")
			for model in current_sw.values:
				self.add_val_tab(model,current_sw.values[model])

			self.def_current_sp()

		# Actions
		self.connect(self.swName,
				SIGNAL("textEdited(QString)"), self.sw_edit)
		self.connect(self.swDescription,
				SIGNAL("textChanged()"), self.sw_edit)
		self.connect(self.swSpot,
				SIGNAL("stateChanged(int)"), self.sw_edit)
		self.connect(self.swValues,
				SIGNAL("currentChanged(int)"), self.def_current_sp)

	def add_val_tab(self,model,values=None):
		global current_sw
		global models
		profile = False
		if isinstance(model,tuple):
			profile = model[1]
			modell = model[0]
		else:
			modell = model
		swColor = QWidget()
		grid = QGridLayout()
		width = 2
		count = 0
		if modell in models:
			for elem in models[modell]:
				val = QLineEdit()
				self.val[val] = (model,count)
				self.connect(val,
						SIGNAL("textEdited(QString)"), self.sw_valedit)
				grid.addWidget(QLabel(elem[0]+":"), count, 0)
				if elem[1] == 0:
					if values:
						val.setText(str(round(values[count],2)))
					else:
						val.setText('0')
					grid.addWidget(val, count, 1)
				elif elem[1] == 1:
					width = 3
					if values:
						val.setText(str(round(values[count]*100,2)))
					else:
						val.setText('0')
					grid.addWidget(val, count, 1)
					grid.addWidget(QLabel("%"), count, 2)
				if elem[1] == 2:
					width = 3
					if values:
						val.setText(str(round(values[count]*360,2)))
					else:
						val.setText('0')
					grid.addWidget(val, count, 1)
					grid.addWidget(QLabel(u"°"), count, 2)
				count += 1
		elif modell == 'hifi':
			for ink in values:
				grid.addWidget(QLabel("Ink "+ink+":"), count, 0)
				val = QLineEdit()
				self.val[val] = (model,count)
				self.connect(val,
						SIGNAL("textEdited(QString)"), self.sw_valedit)
				if values:
					val.setText(str(round(values[ink],2)))
				else:
					val.setText('0')
				grid.addWidget(val, count, 1)
				count += 1
		else:
			self.val[model] = {}
			for ink in values:
				val = QLineEdit()
				self.val[val] = (model,count)
				if values:
					val.setText(str(round(values[count],2)))
				else:
					val.setText('0')
				grid.addWidget(val, count, 1)
				count += 1
				
		grid.addWidget(QLabel("Profile"), count, 0, 1, width)
		profList = QComboBox()
		profList.addItems(self.getProfList(modell))
		if profile in self.parent.sb.profiles:
			profList.setCurrentIndex(self.parent.profiles[modell].index(profile)+1)
		self.connect(profList,
				SIGNAL("currentIndexChanged(int)"), self.change_profile)
		grid.addWidget(profList, count+1, 0, 1, width)
		swColor.setLayout(grid)
		
		self.swValues.addTab(swColor,modell)

	def sw_edit(self):
		global current_sw
		if self.sender() == self.swName:
			if self.swName.text() == '':
				del current_sw.info['name'][0]
				self.parent.itemList[current_sw].setToolTip('')
				self.parent.itemTree[current_sw].setText(0,'')
			else:
				if 'name' not in current_sw.info:
					current_sw.info['name'] = {}
				current_sw.info['name'][0] = unicode(self.swName.text())
				self.parent.itemList[current_sw].setToolTip(self.swName.text())
				self.parent.itemTree[current_sw].setText(0,self.swName.text())
		if self.sender() == self.swDescription:
			if self.swDescription.toPlainText() == '':
				del current_sw.info['description'][0]
			else:
				if 'description' not in current_sw.info:
					current_sw.info['description'] = {}
				current_sw.info['description'][0] = unicode(self.swDescription.toPlainText())
		if self.sender() == self.swSpot:
			if self.swSpot.isChecked():
				current_sw.attr.append('spot')
			else:
				current_sw.attr.remove('spot')
			self.set_preview()

	def set_preview(self):
		if isinstance(current_sw,Color) and len(current_sw.values) > 0:
			r,g,b = current_sw.toRGB8()
			self.sample.setStyleSheet("QWidget { background-color: #"+hex2(r)+hex2(g)+hex2(b)+" }")
			icon = self.parent.colorswatch(current_sw)
		else:
			self.sample.setStyleSheet("")
			icon = QIcon("icons/swatchbooker.svg")
		self.parent.itemTree[current_sw].setIcon(0,icon)
		self.parent.itemList[current_sw].setIcon(icon)
		

	def sw_valedit(self):
		global models
		global current_sw
		sender = self.val[self.sender()]
		if isinstance(sender[0],tuple):
			profile = sender[0][1]
			modell = sender[0][0]
		else:
			modell = sender[0]
		if modell in models:
			if models[modell][sender[1]][1] == 0:
				current_sw.values[sender[0]][sender[1]] = eval(str(self.sender().text()))
			elif models[modell][sender[1]][1] == 1:
				current_sw.values[sender[0]][sender[1]] = eval(str(self.sender().text()))/100
			elif models[modell][sender[1]][1] == 2:
				current_sw.values[sender[0]][sender[1]] = eval(str(self.sender().text()))/360
		elif modell == 'hifi':
			current_sw.values[sender[0]][sender[1]] = eval(str(self.sender().text()))/100
		else:
			current_sw.values[sender[0]][sender[1]] = eval(str(self.sender().text()))
		self.set_preview()

	def def_current_sp(self):
		global current_sp
		if self.swValues.count() > 0:
			model = str(self.swValues.tabText(self.swValues.currentIndex()))
			profindex = self.swValues.currentWidget().findChild(QComboBox).currentIndex()
			if profindex > 0:
				current_sp = (model,self.parent.profiles[model][profindex-1])
			else:
				current_sp = model
		else:
			current_sp = False

	def change_profile(self):
		global current_sw
		global current_sp
		value = current_sw.values[current_sp]
		del current_sw.values[current_sp]
		self.def_current_sp()
		current_sw.values[current_sp] = value
		fields = self.swValues.currentWidget().findChildren(QLineEdit)
		for field in fields:
			self.val[field] = (current_sp,self.val[field][1])
		self.set_preview()

	def delVal(self):
		global current_sw
		global current_sp
		value = current_sw.values[current_sp]
		del current_sw.values[current_sp]
		self.swValues.removeTab(self.swValues.currentIndex())
		self.set_preview()

	def addVal(self):
		global models
		global current_sw
		model = str(self.sender().text())
		if not hasattr(self,'val'):
			self.val = {}
		current_sw.values[model] = []
		self.add_val_tab(model)
		for elem in models[model]:
			current_sw.values[model].append(0)
		self.swValues.setCurrentIndex(self.swValues.count()-1)
		self.def_current_sp()
		self.delValAction.setEnabled(True)
		self.set_preview()
		

	def getProfList(self,model):
		profList = QStringList()
		profList << ''
		if model in self.parent.profiles:
			for prof in self.parent.profiles[model]:
				profList << self.parent.sb.profiles[prof].info['desc'][0]
		return profList

class MainWindow(QMainWindow):

	def __init__(self, file=False, parent=None):
		super(MainWindow, self).__init__(parent)
		
		self.setWindowTitle('SwatchBooker')
		self.setWindowIcon(QIcon("icons/swatchbooker.svg"))
		
		self.filename = None

		self.sbWidget = QSplitter(Qt.Horizontal)
		# sbInfo
		nameLabel = QLabel("Name:")
		self.sbName = QLineEdit()
		descriptionLabel = QLabel("Description:")
		self.sbDescription = QTextEdit()
		copyrightLabel = QLabel("Copyright:")
		self.copyright = QLineEdit()
		versionLabel = QLabel("Version:")
		self.version = QLineEdit()
		licenseLabel = QLabel("License:")
		self.sbLicense = QTextEdit()
		
		groupBoxInfo1 = QGroupBox("Information")
		sbInfo1 = QGridLayout()
		sbInfo1.addWidget(nameLabel, 0, 0)
		sbInfo1.addWidget(self.sbName, 0, 1)
		sbInfo1.addWidget(descriptionLabel, 1, 0, 1, 2)
		sbInfo1.addWidget(self.sbDescription, 2, 0, 1, 2)
		sbInfo1.addWidget(copyrightLabel, 3, 0)
		sbInfo1.addWidget(self.copyright, 3, 1)
		sbInfo1.addWidget(versionLabel, 4, 0)
		sbInfo1.addWidget(self.version, 4, 1)
		sbInfo1.addWidget(licenseLabel, 5, 0, 1, 2)
		sbInfo1.addWidget(self.sbLicense, 6, 0, 1, 2)


		self.sbProfiles = QTableWidget()
		self.sbProfiles.horizontalHeader().setStretchLastSection(True)
		self.sbProfiles.verticalHeader().hide()
		self.sbProfiles.horizontalHeader().hide()
		self.sbProfiles.setColumnCount(2)
		self.sbProfiles.setColumnHidden(1,True)
		self.sbProfiles.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.butProf = QToolButton(self)
		self.butProf.setFixedSize(12,12)
		self.menuProf = QMenu()
		self.menuProf.addAction('Add',self.addProfile)
		self.profEditAction = self.menuProf.addAction('Edit')
		self.profRemoveAction = self.menuProf.addAction('Remove',self.remProfile)
		self.butProf.setPopupMode(QToolButton.InstantPopup)
		self.butProf.setMenu(self.menuProf)
		self.profEditAction.setEnabled(False)
		self.profRemoveAction.setEnabled(False)

		groupBoxInfo2 = QGroupBox("Color profiles")
		sbInfo2 = QHBoxLayout()
		sbInfo2.addWidget(self.sbProfiles)
		sbInfo2.addWidget(self.butProf,0,Qt.AlignTop)
		

		sbInfo = QVBoxLayout()
		sbInfo.setContentsMargins(0,0,0,0)
		groupBoxInfo1.setLayout(sbInfo1)
		groupBoxInfo2.setLayout(sbInfo2)
		sbInfo.addWidget(groupBoxInfo1)
		sbInfo.addWidget(groupBoxInfo2)
		sbInfoWidget = QWidget()
		sbInfoWidget.setLayout(sbInfo)
		
		self.sbWidget.addWidget(sbInfoWidget)

		# sbTree
		self.treeWidget = QTreeWidget()
		self.treeWidget.setHeaderHidden(True)
		self.treeWidget.setItemsExpandable(True)
		self.swnbLabel = QLabel()
		self.swEditBut = QToolButton(self)
		self.swEditBut.setMaximumSize(12,12)
		self.swEditMenu = QMenu()
		self.swEditMenu.addAction('Add Color',self.swAddColor)
		self.swEditMenu.addAction('Add Gradient',self.swAddGradient)
		self.swEditMenu.addAction('Add Pattern',self.swAddPattern)
		self.swEditMenu.addAction('Add Texture',self.swAddTexture)
		self.deleteAction = self.swEditMenu.addAction('Delete',self.swDelete)
		self.swEditBut.setPopupMode(QToolButton.InstantPopup)
		self.swEditBut.setMenu(self.swEditMenu)
		self.deleteAction.setEnabled(False)
		
		groupBoxTree = QGroupBox("Tree view")
		sbTree = QGridLayout()
		sbTree.addWidget(self.treeWidget,0,0,1,2)
		sbTree.addWidget(self.swnbLabel,1,0)
		sbTree.addWidget(self.swEditBut,1,1)
		groupBoxTree.setLayout(sbTree)
		self.sbWidget.addWidget(groupBoxTree)

		# sbGrid
		self.listWidget = QListWidget()
		self.listWidget.setViewMode(QListView.IconMode)
		self.listWidget.setMovement(QListView.Static)
		colsLabel = QLabel("Columns:")
		self.cols = QSpinBox()
		self.cols.setRange(0, 64)
		rowsLabel = QLabel("Rows:")
		self.rows = QSpinBox()
		self.rows.setRange(0, 64)

		groupBoxGrid = QGroupBox("Grid view")
		sbGrid = QVBoxLayout()
		dims = QGridLayout()
		dims.addWidget(colsLabel, 0, 0)
		dims.addWidget(self.cols, 0, 1)
		dims.addWidget(rowsLabel, 1, 0)
		dims.addWidget(self.rows, 1, 1)
		dimsWidget = QWidget()
		dimsWidget.setLayout(dims)
		sbGrid.addWidget(self.listWidget)
		sbGrid.addStretch()
		sbGrid.addWidget(dimsWidget)
		groupBoxGrid.setLayout(sbGrid)
		self.sbWidget.addWidget(groupBoxGrid)

		self.setCentralWidget(self.sbWidget)
		
		fileMenu = self.menuBar().addMenu("&File")
		fileMenu.addAction("&New...", self.fileNew, QKeySequence.New)
		fileMenu.addAction("&Open...", self.fileOpen, QKeySequence.Open)
		fileMenu.addAction("&Save As...", self.fileSaveAs, QKeySequence.Save)
		self.menuBar().addAction("Settings", self.settings)
		self.menuBar().addAction("&About", self.about)
		options = QSettings()

		# Actions
		self.connect(self.sbName,
				SIGNAL("textEdited(QString)"), self.sb_edit)
		self.connect(self.sbDescription,
				SIGNAL("textChanged()"), self.sb_edit)
		self.connect(self.copyright,
				SIGNAL("textEdited(QString)"), self.sb_edit)
		self.connect(self.sbLicense,
				SIGNAL("textChanged()"), self.sb_edit)
		self.connect(self.version,
				SIGNAL("textEdited(QString)"), self.sb_edit)
		self.connect(self.cols,
				SIGNAL("valueChanged(int)"), self.sb_edit)
		self.connect(self.rows,
				SIGNAL("valueChanged(int)"), self.sb_edit)
		self.connect(self.treeWidget,
				SIGNAL("itemSelectionChanged()"), self.sw_display_tree)
		self.connect(self.listWidget,
				SIGNAL("itemSelectionChanged()"), self.sw_display_list)
		self.connect(self.sbProfiles,
				SIGNAL("itemSelectionChanged()"),self.prof_editable)

		#Initialisation
		self.sb = SwatchBook()
		if file:
			self.loadFile(file)
		else:
			self.sb_flush()

	def sw_display_tree(self):
		global current_sw
		if self.treeWidget.selectedItems():
			treeItem = self.treeWidget.selectedItems()[0]
			current_sw = item = self.treeItems[treeItem]
			if isinstance(item,Color):
				self.listWidget.setCurrentItem(self.itemList[item])
			else:
				self.listWidget.setCurrentItem(None)
			if hasattr(self,'sbSwatch'):
				self.sbSwatch.setParent(None)
			if isinstance(item,Color):
				self.sbSwatch = ColorWidget(self)
			elif isinstance(item,Group):
				self.sbSwatch = GroupWidget()
			if not isinstance(item, Spacer) and not isinstance(item, Break):
				self.sbWidget.addWidget(self.sbSwatch)
			self.deleteAction.setEnabled(True)

	def sw_display_list(self):
		global current_sw
		if self.listWidget.selectedItems():
			listItem = self.listWidget.selectedItems()[0]
			current_sw = item = self.listItems[listItem]
			self.treeWidget.setCurrentItem(self.itemTree[item])

	def sb_edit(self):
		if self.sbName.text() > '':
			if 'name' not in self.sb.info:
				self.sb.info['name'] = {}
			self.sb.info['name'][0] = unicode(self.sbName.text())
		if self.sbDescription.toPlainText() > '':
			if 'description' not in self.sb.info:
				self.sb.info['description'] = {}
			self.sb.info['description'][0] = unicode(self.sbDescription.toPlainText())
		if self.copyright.text() > '':
			if 'copyright' not in self.sb.info:
				self.sb.info['copyright'] = {}
			self.sb.info['copyright'][0] = unicode(self.copyright.text())
		if self.sbLicense.toPlainText() > '':
			if 'license' not in self.sb.info:
				self.sb.info['license'] = {}
			self.sb.info['license'][0] = unicode(self.sbLicense.toPlainText())
		if self.version.text() > '':
			self.sb.info['version'] = unicode(self.version.text())
		if self.cols.value() > 0:
			self.sb.display['columns'] = self.cols.value()
			self.listWidget.setFixedWidth(self.sb.display['columns']*17 + 20)
		elif self.cols.value() == 0:
			self.listWidget.setMinimumWidth(0)
			self.listWidget.setMaximumWidth(0xFFFFFF)
		if self.rows.value() > 0:
			self.sb.display['rows'] = self.rows.value()
			self.listWidget.setFixedHeight(self.sb.display['rows']*17 + 5)
		elif self.rows.value() == 0:
			self.listWidget.setMinimumHeight(0)
			self.listWidget.setMaximumHeight(0xFFFFFF)

	def fileNew(self):
		self.sb_flush()

	def fileOpen(self):
		dir = os.path.dirname(self.filename) \
				if self.filename is not None else "."
		import swatchbook.codecs as codecs
		filetypes = []
		for codec in codecs.reads:
			codec_exts = []
			for ext in eval('codecs.'+codec).ext:
				codec_exts.append('*.'+ext)
			codec_txt = eval('codecs.'+codec).__doc__ +' ('+" ".join(codec_exts)+')'
			filetypes.append(codec_txt)
		allexts = ["*.%s" % unicode(format).lower() \
				   for format in codecs.readexts.keys()]
		fname = self.sb.info['filename'] if 'filename' in self.sb.info else "."
		filetype = QString()
		fname = unicode(QFileDialog.getOpenFileName(self,
							"SwatchBooker - Choose file", dir,
							("All supported files (%s)" % " ".join(allexts))+";;"+(";;".join(sorted(filetypes)))))
		if fname:
			self.loadFile(fname)

	def sb_flush(self):
		self.filename = None
		self.sbName.clear()
		self.sbDescription.clear()
		self.copyright.clear()
		self.version.clear()
		self.sbLicense.clear()
		self.cols.setValue(0)
		self.cols.clear()
		self.rows.setValue(0)
		self.rows.clear()
		self.treeWidget.clear()
		self.listWidget.clear()
		self.listWidget.setGridSize(QSize(17,17))
		self.listWidget.setResizeMode(QListView.Adjust)
		self.listWidget.setMinimumSize(QSize(0,0))
		self.listWidget.setMaximumSize(QSize(0xFFFFFF,0xFFFFFF))
		self.treeItems = {}
		self.itemTree = {}
		self.listItems = {}
		self.itemList = {}
		self.profiles = {}
		self.swnb = 0
		self.swnbLabel.clear()
		self.deleteAction.setEnabled(False)
		if hasattr(self,'sbSwatch'):
			self.sbSwatch.setParent(None)
		current_sw = False
		current_sp = False

	def loadFile(self, fname=None):
		if fname is None:
			action = self.sender()
			if isinstance(action, QAction):
				fname = unicode(action.data().toString())
				if not self.okToContinue():
					return
			else:
				return
		if fname:
			self.sb_flush()
			self.sb = SwatchBook(fname)
			if 'name' in self.sb.info:
				self.sbName.setText(self.sb.info['name'][0])
			if 'description' in self.sb.info:
				self.sbDescription.setText(self.sb.info['description'][0])
			if 'copyright' in self.sb.info:
				self.copyright.setText(self.sb.info['copyright'][0])
			if 'license' in self.sb.info:
				self.sbLicense.setText(self.sb.info['license'][0])
			if 'version' in self.sb.info:
				self.version.setText(self.sb.info['version'])
			if 'columns' in self.sb.display:
				self.cols.setValue(self.sb.display['columns'])
				self.listWidget.setFixedWidth(self.sb.display['columns']*17 + 20)
			if 'rows' in self.sb.display:
				self.rows.setValue(self.sb.display['rows'])
				self.listWidget.setFixedHeight(self.sb.display['rows']*17 + 5)
			self.sbProfiles.setRowCount(len(self.sb.profiles))
			row = 0
			for prof in self.sb.profiles:
				profItemID = QTableWidgetItem(prof)
				profItemTitle = QTableWidgetItem(self.sb.profiles[prof].info['desc'][0])
				self.sbProfiles.setItem(row, 0, profItemTitle)
				self.sbProfiles.setItem(row, 1, profItemID)
				space = self.sb.profiles[prof].info['space'].strip()
				if space in self.profiles:
					self.profiles[space].append(prof)
				else:
					self.profiles[space] = [prof]
				row += 1
			self.populateTree()

	def fileSave(self,codec):
		if self.filename == None:
			self.fileSaveAs()
		else:
			#TODO: test if writable
			self.sb.write(codec,self.filename)
			self.dirty = False

	def fileSaveAs(self):
		import swatchbook.codecs as codecs
		filetypes = {}
		for codec in codecs.writes:
			codec_exts = []
			for ext in eval('codecs.'+codec).ext:
				codec_exts.append('*.'+ext)
			codec_txt = eval('codecs.'+codec).__doc__ +' ('+" ".join(codec_exts)+')'
			filetypes[codec_txt] = (codec,eval('codecs.'+codec).ext[0])
		fname = self.sb.info['filename'] if 'filename' in self.sb.info else "."
		filetype = QString()
		fname = unicode(QFileDialog.getSaveFileName(self,
						"SwatchBooker - Save file", fname,
						";;".join(filetypes.keys()),filetype))
		if fname:
			if "." not in fname:
				fname += "."+filetypes[unicode(filetype)][1]
			self.filename = fname
			self.fileSave(filetypes[unicode(filetype)][0])

	def populateTree(self):
		self.fillTree(self.sb.items)
		self.treeWidget.resizeColumnToContents(0)
		self.treeWidget.resizeColumnToContents(1)
		swnbLabelText = str(self.swnb)+' swatch'
		if self.swnb > 1:
			swnbLabelText += 'es'
		self.swnbLabel.setText(swnbLabelText)

	def fillTree(self,items,group = False):
		for item in items.values():
			if group:
				parent = group
			else:
				parent = self.treeWidget
			if isinstance(item,Group):
				treeItem = QTreeWidgetItem(parent,[QString(item.info['name'][0])])
				self.fillTree(item.items,treeItem)
			elif isinstance(item,Spacer):
				listItem = QListWidgetItem(self.listWidget)
				listItem.setIcon(QIcon())
				treeItem = QTreeWidgetItem(parent,[QString('<spacer>')])
				font = QFont()
				font.setItalic(True)
				treeItem.setFont(0,font)
				treeItem.setTextColor(0,QColor(128))
			elif isinstance(item,Break):
				treeItem = QTreeWidgetItem(parent,[QString('<break>')])
				font = QFont()
				font.setItalic(True)
				treeItem.setFont(0,font)
				treeItem.setTextColor(0,QColor(128))
			else:
				listItem = QListWidgetItem(self.listWidget)
				if isinstance(item,Color) and len(item.values) > 0:
					icon = self.colorswatch(item)
				else:
					icon = QIcon("icons/swatchbooker.svg")
				listItem.setIcon(icon)
				self.listItems[listItem] = item
				self.itemList[item] = listItem
				if 'name' in item.info:
					treeItem = QTreeWidgetItem(parent,[QString(item.info['name'][0])])
					listItem.setToolTip(item.info['name'][0])
				else:
					treeItem = QTreeWidgetItem(parent)
				treeItem.setIcon(0,icon)
			self.treeItems[treeItem] = item
			self.itemTree[item] = treeItem
			if group:
				self.treeWidget.expandItem(parent)
			if not isinstance(item, Group) and not isinstance(item, Spacer) and not isinstance(item, Break):
				self.swnb += 1

	def colorswatch(self,swatch):
		r,g,b = swatch.toRGB8()
		icon = QPixmap(16,16)
		paint = QPainter()
		paint.begin(icon)
		if 'spot' in swatch.attr:
			paint.setBrush(QColor(255,255,255))
			paint.drawRect(-1, -1, 17, 17)
			paint.setBrush(QColor(r,g,b))
			paint.drawEllipse(0, 0, 15, 15)
		else:
			paint.setBrush(QColor(r,g,b))
			paint.drawRect(0, 0, 15, 15)
		paint.end()
		return QIcon(icon)

	def about(self):
		QMessageBox.about(self, "About SwatchBooker",
                """<b>SwatchBooker</b> %s
                <p>&copy; 2008 Olivier Berten
                <p>Qt %s - PyQt %s""" % (
                __version__, QT_VERSION_STR, PYQT_VERSION_STR))

	def settings(self):
		print "Settings"

	def swDelete(self):
		global current_sw
		sw_tbd = current_sw
		if hasattr(self,'sbSwatch'):
			self.sbSwatch.setParent(None)
		tbd = self.get_parent(self.sb,sw_tbd)
		if isinstance(sw_tbd, Group):
			self.del_group_from_list(tbd[0],tbd[1])
		else:
			self.listWidget.takeItem(self.listWidget.row(self.itemList[sw_tbd]))
			del self.itemList[sw_tbd]
			self.swnb -= 1
		if self.itemTree[sw_tbd].parent() == None:
			self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(self.itemTree[sw_tbd]))
		else:
			self.itemTree[sw_tbd].parent().takeChild(self.itemTree[sw_tbd].parent().indexOfChild(self.itemTree[sw_tbd]))
		del tbd[0].items[tbd[1]]
		del self.itemTree[sw_tbd]
		swnbLabelText = str(self.swnb)+' swatch'
		if self.swnb > 1:
			swnbLabelText += 'es'
		self.swnbLabel.setText(swnbLabelText)
		current_sw = False
		self.deleteAction.setEnabled(False)
	
	def del_group_from_list(self,parent,group):
		for sw in parent.items[group].items:
			if isinstance(parent.items[group].items[sw], Group):
				self.del_group_from_list(parent.items[group],sw)
			else:
				self.listWidget.takeItem(self.listWidget.row(self.itemList[parent.items[group].items[sw]]))
				del self.itemList[parent.items[group].items[sw]]
				self.swnb -= 1
	
	def get_parent(self,parent,value):
		for item in parent.items.values():
			if value == item:
				return (parent,parent.items.keys()[parent.items.values().index(item)])
			elif isinstance(item, Group):
				if self.get_parent(item,value):
					return self.get_parent(item,value)
		return False

	def swAddColor(self):
		global current_sw
		item = Color()
		key = 'col'+str(int(time.mktime(time.gmtime())))
		item.id = key
		icon = QIcon("icons/swatchbooker.svg")
		listItem = QListWidgetItem()
		listItem.setIcon(icon)
		self.listItems[listItem] = item
		self.itemList[item] = listItem
		treeItem = QTreeWidgetItem()
		treeItem.setIcon(0,icon)
		self.treeItems[treeItem] = item
		self.itemTree[item] = treeItem
		if self.treeWidget.selectedItems():
			selItem = self.get_parent(self.sb,current_sw)
			index = selItem[0].items.values().index(current_sw)
			selItem[0].items.insert(index+1,key,item)
			selLItem = self.listWidget.selectedItems()[0]
			lIndex = self.listWidget.indexFromItem(selLItem).row()
			self.listWidget.insertItem(lIndex+1,self.itemList[item])
			selTItem = self.treeWidget.selectedItems()[0]
			if selTItem.parent() == None:
				tIndex = self.treeWidget.indexOfTopLevelItem(selTItem)
				self.treeWidget.insertTopLevelItem(tIndex+1, treeItem)
			else:
				tIndex = selTItem.parent().indexOfChild(selTItem)
				selTItem.parent().insertChild(tIndex+1,treeItem)
		else:
			self.sb.items[key] = item
			self.treeWidget.addTopLevelItem(self.itemTree[item])
			self.listWidget.addItem(self.itemList[item])
		self.treeWidget.setCurrentItem(self.itemTree[item])
		self.swnb += 1
		swnbLabelText = str(self.swnb)+' swatch'
		if self.swnb > 1:
			swnbLabelText += 'es'
		self.swnbLabel.setText(swnbLabelText)
		current_sw = item

	def swAddTexture(self):
		print 'unimplemented'

	swAddSpacer = swAddBreak = swAddGradient = swAddPattern = swAddTexture

	def prof_editable(self):
		if self.sbProfiles.isItemSelected(self.sbProfiles.currentItem()):
			self.profEditAction.setEnabled(True)
			self.profRemoveAction.setEnabled(True)

	def addProfile(self):
		fname = unicode(QFileDialog.getOpenFileName(self,
							"SwatchBooker - Choose file", ".",
							("ICC profiles (*.icc *.icm *.3cc)")))
		if fname:
			import swatchbook.icc as icc
			self.sb.profiles[fname] = icc.ICCprofile(fname)
			profItemID = QTableWidgetItem(fname)
			profItemTitle = QTableWidgetItem(self.sb.profiles[fname].info['desc'][0])
			row = self.sbProfiles.rowCount()
			self.sbProfiles.setRowCount(row+1)
			self.sbProfiles.setItem(row, 0, profItemTitle)
			self.sbProfiles.setItem(row, 1, profItemID)
			space = self.sb.profiles[fname].info['space'].strip()
			if space in self.profiles:
				self.profiles[space].append(fname)
			else:
				self.profiles[space] = [fname]

	def remProfile(self):
		profid = unicode(self.sbProfiles.item(self.sbProfiles.currentItem().row(),1).text())
		self.sbProfiles.removeRow(self.sbProfiles.currentItem().row())
		self.profiles[self.sb.profiles[profid].info['space'].strip()].remove(profid)
		del self.sb.profiles[profid]
		self.profEditAction.setEnabled(False)
		self.profRemoveAction.setEnabled(False)
		# TODO remove profile from color values

if __name__ == "__main__":
	app = QApplication(sys.argv)
	if len(sys.argv) > 1:
		form = MainWindow(sys.argv[1])
	else:
		form = MainWindow()
	form.show()
	app.exec_()
