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

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from swatchbook import *

__version__ = "0.2"

current_sw = False

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
		if self.swName.text() > '':
			if 'name' not in current_sw.info:
				current_sw.info['name'] = {}
			current_sw.info['name'][0] = unicode(self.swName.text())
		if self.swDescription.toPlainText() > '':
			if 'description' not in current_sw.info:
				current_sw.info['description'] = {}
			current_sw.info['description'][0] = unicode(self.swDescription.toPlainText())

class ColorWidget(QGroupBox):
	def __init__(self, profiles, parent=None):
		super(ColorWidget, self).__init__(parent)
		
		self.setTitle("Color")

		nameLabel = QLabel("Name:")
		self.swName = QLineEdit()
		descriptionLabel = QLabel("Description:")
		self.swDescription = QTextEdit()
		self.sample = QLabel()
		self.sample.setMinimumHeight(30)
		self.swSpot = QCheckBox("Spot")
		self.swValues = QTabWidget()
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
		if hasattr(current_sw,'values') and len(current_sw.values) > 0:
			r,g,b = current_sw.toRGB8()
			self.sample.setStyleSheet("QWidget { background-color: #"+hex2(r)+hex2(g)+hex2(b)+" }")
			self.val = {}
			for model in current_sw.values:
				profile = False
				values = current_sw.values[model]
				if isinstance(model,tuple):
					profile = model[1]
					modell = model[0]
				else:
					modell = model
				swColor = QWidget()
				grid = QGridLayout()
				width = 2
				count = 0
				global models
				if modell in models:
					for elem in models[modell]:
						val = QLineEdit()
						self.val[val] = (model,count)
						self.connect(val,
								SIGNAL("textEdited(QString)"), self.sw_valedit)
						grid.addWidget(QLabel(elem[0]+":"), count, 0)
						if elem[1] == 0:
							val.setText(str(round(values[count],2)))
							grid.addWidget(val, count, 1)
						elif elem[1] == 1:
							width = 3
							val.setText(str(round(values[count]*100,2)))
							grid.addWidget(val, count, 1)
							grid.addWidget(QLabel("%"), count, 2)
						if elem[1] == 2:
							width = 3
							val.setText(str(round(values[count]*360,2)))
							grid.addWidget(val, count, 1)
							grid.addWidget(QLabel(u"°"), count, 2)
						count += 1
				elif modell == 'hifi':
					for ink in values:
						grid.addWidget(QLabel("Ink "+ink+":"), count, 0)
						val = QLineEdit()
						self.val[val] = (model,count)
						val.setText(str(round(values[ink],2)))
						grid.addWidget(val, count, 1)
						count += 1
				else:
					self.val[model] = {}
					for ink in values:
						val = QLineEdit()
						self.val[val] = (model,count)
						val.setText(str(round(values[count],2)))
						grid.addWidget(val, count, 1)
						count += 1
						
				grid.addWidget(QLabel("Profile"), count, 0, 1, width)
				grid.addWidget(QComboBox(), count+1, 0, 1, width)
				swColor.setLayout(grid)
				self.swValues.addTab(swColor,modell)

		# Actions
		self.connect(self.swName,
				SIGNAL("textEdited(QString)"), self.sw_edit)
		self.connect(self.swDescription,
				SIGNAL("textChanged()"), self.sw_edit)

	def sw_edit(self):
		global current_sw
		if self.swName.text() > '':
			if 'name' not in current_sw.info:
				current_sw.info['name'] = {}
			current_sw.info['name'][0] = unicode(self.swName.text())
		if self.swDescription.toPlainText() > '':
			if 'description' not in current_sw.info:
				current_sw.info['description'] = {}
			current_sw.info['description'][0] = unicode(self.swDescription.toPlainText())

	def sw_valedit(self):
		print self.val[self.sender()]

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
		
		groupBoxInfo = QGroupBox("Information")
		sbInfo = QGridLayout()
		sbInfo.addWidget(nameLabel, 0, 0)
		sbInfo.addWidget(self.sbName, 0, 1)
		sbInfo.addWidget(descriptionLabel, 1, 0, 1, 2)
		sbInfo.addWidget(self.sbDescription, 2, 0, 1, 2)
		sbInfo.addWidget(copyrightLabel, 3, 0)
		sbInfo.addWidget(self.copyright, 3, 1)
		sbInfo.addWidget(versionLabel, 4, 0)
		sbInfo.addWidget(self.version, 4, 1)
		sbInfo.addWidget(licenseLabel, 5, 0, 1, 2)
		sbInfo.addWidget(self.sbLicense, 6, 0, 1, 2)

		groupBoxInfo.setLayout(sbInfo)
		self.sbWidget.addWidget(groupBoxInfo)

		# sbTree
		self.treeWidget = QTreeWidget()
		self.treeWidget.setHeaderHidden(True)
		self.treeWidget.setItemsExpandable(True)
		self.swnbLabel = QLabel()
		
		groupBoxTree = QGroupBox("Tree view")
		sbTree = QVBoxLayout()
		sbTree.addWidget(self.treeWidget)
		sbTree.addWidget(self.swnbLabel)
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
				self.sbSwatch = ColorWidget(self.sb.profiles)
			elif isinstance(item,Group):
				self.sbSwatch = GroupWidget()
			self.sbWidget.addWidget(self.sbSwatch)

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
		self.listWidget.setMinimumSize(QSize(0,0))
		self.listWidget.setMaximumSize(QSize(0xFFFFFF,0xFFFFFF))
		self.swnbLabel.clear()
		if hasattr(self,'sbSwatch'):
			self.sbSwatch.setParent(None)
		current_sw = False

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
		self.treeWidget.clear()
		self.listWidget.clear()
		self.listWidget.setGridSize(QSize(17,17))
		self.listWidget.setResizeMode(QListView.Adjust)
		self.treeItems = {}
		self.itemTree = {}
		self.listItems = {}
		self.itemList = {}
		self.swnb = 0
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
			elif isinstance(item,Break):
				pass
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
			if not isinstance(item, Spacer) and not isinstance(item, Break):
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

if __name__ == "__main__":
	app = QApplication(sys.argv)
	if len(sys.argv) > 1:
		form = MainWindow(sys.argv[1])
	else:
		form = MainWindow()
	form.show()
	app.exec_()
