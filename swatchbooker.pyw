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

__version__ = "0.1"

sb_theme = "tango" # echo
current_sw = False

class GroupWidget(QGroupBox):
	def __init__(self, item, parent=None):
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

		if hasattr(item,'info'):
			if 'name' in item.info:
				self.swName.setText(item.info['name'][0])
			if 'description' in item.info:
				self.swDescription.setText(item.info['description'][0])

class ColorWidget(QGroupBox):
	def __init__(self, item, parent=None):
		super(ColorWidget, self).__init__(parent)
		
		self.setTitle("Color")

		nameLabel = QLabel("Name:")
		self.swName = QLineEdit()
		self.swDescription = QTextEdit()
		descriptionLabel = QLabel("Description:")
		self.swSpot = QCheckBox("Spot")
		self.swValues = QTabWidget()
		swInfo = QGridLayout()
		swInfo.addWidget(nameLabel, 0, 0)
		swInfo.addWidget(self.swName, 0, 1)
		swInfo.addWidget(descriptionLabel, 1, 0, 1, 2)
		swInfo.addWidget(self.swDescription, 2, 0, 1, 2)
		swInfo.addWidget(self.swSpot, 3, 0, 1, 2)
		swInfo.addWidget(self.swValues, 4, 0, 1, 2)
		self.setLayout(swInfo)

		if hasattr(item,'info'):
			if 'name' in item.info:
				self.swName.setText(item.info['name'][0])
			if 'description' in item.info:
				self.swDescription.setText(item.info['description'][0])
		if hasattr(item,'attr') and 'spot' in item.attr:
			self.swSpot.setChecked(True)
		if hasattr(item,'values') and item.values:
			for model in item.values:
				values = item.values[model]
				swColor = QWidget()
				if model == 'Lab':
					LLabel = QLabel("L:")
					L = QLineEdit()
					aLabel = QLabel("a:")
					a = QLineEdit()
					bLabel = QLabel("b:")
					b = QLineEdit()
					L.setText(str(round(values[0],2)))
					a.setText(str(round(values[1],2)))
					b.setText(str(round(values[2],2)))
					grid = QGridLayout()
					grid.addWidget(LLabel, 0, 0)
					grid.addWidget(L, 0, 1)
					grid.addWidget(aLabel, 1, 0)
					grid.addWidget(a, 1, 1)
					grid.addWidget(bLabel, 2, 0)
					grid.addWidget(b, 2, 1)
				elif model == 'XYZ':
					X = QLineEdit()
					Y = QLineEdit()
					Z = QLineEdit()
					X.setText(str(round(values[0],2)))
					Y.setText(str(round(values[1],2)))
					Z.setText(str(round(values[2],2)))
					grid = QGridLayout()
					grid.addWidget(QLabel("X:"), 0, 0)
					grid.addWidget(X, 0, 1)
					grid.addWidget(QLabel("Y:"), 1, 0)
					grid.addWidget(Y, 1, 1)
					grid.addWidget(QLabel("Z:"), 2, 0)
					grid.addWidget(Z, 2, 1)
				elif model == 'RGB':
					RLabel = QLabel("R:")
					R = QLineEdit()
					GLabel = QLabel("G:")
					G = QLineEdit()
					BLabel = QLabel("B:")
					B = QLineEdit()
					R.setText(str(round(values[0]*100,2)))
					G.setText(str(round(values[1]*100,2)))
					B.setText(str(round(values[2]*100,2)))
					grid = QGridLayout()
					grid.addWidget(RLabel, 0, 0)
					grid.addWidget(R, 0, 1)
					grid.addWidget(QLabel("%"), 0, 2)
					grid.addWidget(GLabel, 1, 0)
					grid.addWidget(G, 1, 1)
					grid.addWidget(QLabel("%"), 1, 2)
					grid.addWidget(BLabel, 2, 0)
					grid.addWidget(B, 2, 1)
					grid.addWidget(QLabel("%"), 2, 2)
				elif model == 'RGBa':
					R = QLineEdit()
					G = QLineEdit()
					B = QLineEdit()
					a = QLineEdit()
					R.setText(str(round(values[0]*100,2)))
					G.setText(str(round(values[1]*100,2)))
					B.setText(str(round(values[2]*100,2)))
					a.setText(str(round(values[3]*100,2)))
					grid = QGridLayout()
					grid.addWidget(QLabel("R:"), 0, 0)
					grid.addWidget(R, 0, 1)
					grid.addWidget(QLabel("%"), 0, 2)
					grid.addWidget(QLabel("G:"), 1, 0)
					grid.addWidget(G, 1, 1)
					grid.addWidget(QLabel("%"), 1, 2)
					grid.addWidget(QLabel("B:"), 2, 0)
					grid.addWidget(B, 2, 1)
					grid.addWidget(QLabel("%"), 2, 2)
					grid.addWidget(QLabel(u"α:"), 3, 0)
					grid.addWidget(a, 3, 1)
					grid.addWidget(QLabel("%"), 3, 2)
				elif model == 'HSL':
					H = QLineEdit()
					S = QLineEdit()
					L = QLineEdit()
					H.setText(str(round(values[0]*360,2)))
					S.setText(str(round(values[1]*100,2)))
					L.setText(str(round(values[2]*100,2)))
					grid = QGridLayout()
					grid.addWidget(QLabel("H:"), 0, 0)
					grid.addWidget(H, 0, 1)
					grid.addWidget(QLabel(u"°"), 0, 2)
					grid.addWidget(QLabel("S:"), 1, 0)
					grid.addWidget(S, 1, 1)
					grid.addWidget(QLabel("%"), 1, 2)
					grid.addWidget(QLabel("L:"), 2, 0)
					grid.addWidget(L, 2, 1)
					grid.addWidget(QLabel("%"), 2, 2)
				elif model == 'HSV':
					H = QLineEdit()
					S = QLineEdit()
					V = QLineEdit()
					H.setText(str(round(values[0]*360,2)))
					S.setText(str(round(values[1]*100,2)))
					V.setText(str(round(values[2]*100,2)))
					grid = QGridLayout()
					grid.addWidget(QLabel("H:"), 0, 0)
					grid.addWidget(H, 0, 1)
					grid.addWidget(QLabel(u"°"), 0, 2)
					grid.addWidget(QLabel("S:"), 1, 0)
					grid.addWidget(S, 1, 1)
					grid.addWidget(QLabel("%"), 1, 2)
					grid.addWidget(QLabel("V:"), 2, 0)
					grid.addWidget(V, 2, 1)
					grid.addWidget(QLabel("%"), 2, 2)
				elif model == 'CMYK':
					C = QLineEdit()
					M = QLineEdit()
					Y = QLineEdit()
					K = QLineEdit()
					C.setText(str(round(values[0]*100,2)))
					M.setText(str(round(values[1]*100,2)))
					Y.setText(str(round(values[2]*100,2)))
					K.setText(str(round(values[3]*100,2)))
					grid = QGridLayout()
					grid.addWidget(QLabel("C:"), 0, 0)
					grid.addWidget(C, 0, 1)
					grid.addWidget(QLabel("%"), 0, 2)
					grid.addWidget(QLabel("M:"), 1, 0)
					grid.addWidget(M, 1, 1)
					grid.addWidget(QLabel("%"), 1, 2)
					grid.addWidget(QLabel("Y:"), 2, 0)
					grid.addWidget(Y, 2, 1)
					grid.addWidget(QLabel("%"), 2, 2)
					grid.addWidget(QLabel("K:"), 3, 0)
					grid.addWidget(K, 3, 1)
					grid.addWidget(QLabel("%"), 3, 2)
				elif model == 'Gray':
					K = QLineEdit()
					K.setText(str(round(values[0]*100,2)))
					grid = QGridLayout()
					grid.addWidget(QLabel("K:"), 0, 0)
					grid.addWidget(K, 0, 1)
					grid.addWidget(QLabel("%"), 0, 2)
				swColor.setLayout(grid)
				self.swValues.addTab(swColor,model)


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
		
		# Menu
		fileNewAction = self.createAction("&New...", self.fileNew,
				QKeySequence.New, "document-new", "Create an swatchbook")
		fileOpenAction = self.createAction("&Open...", self.fileOpen,
				QKeySequence.Open, "document-open",
				"Open an existing swatchbook")
		fileSaveAsAction = self.createAction("Save &As...",
				self.fileSaveAs, icon="document-save-as",
				tip="Save the swatchbook using a new name/format")

		fileToolbar = self.addToolBar("File")
		fileToolbar.setObjectName("FileToolBar")
		self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
									  fileSaveAsAction))
		settings = QSettings()

		# Actions
		self.connect(self.sbName,
				SIGNAL("textEdited(QString)"), self.sb_edit)
		self.connect(self.sbDescription,
				SIGNAL("textChanged()"), self.sb_edit)
		self.connect(self.copyright,
				SIGNAL("textEdited(QString)"), self.sb_edit)
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
				self.sbSwatch = ColorWidget(current_sw)
			elif isinstance(item,Group):
				self.sbSwatch = GroupWidget(current_sw)
			self.sbWidget.addWidget(self.sbSwatch)

	def sw_display_list(self):
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
		if self.version.text() > '':
			self.sb.info['version'] = unicode(self.version.text())
		if self.cols.value() > 0:
			self.sb.display['columns'] = self.cols.value()
			self.listWidget.setFixedWidth(self.sb.display['columns']*17 + 20)
		if self.rows.value() > 0:
			self.sb.display['rows'] = self.rows.value()
			self.listWidget.setFixedHeight(self.sb.display['rows']*17 + 5)

	def createAction(self, text, slot=None, shortcut=None, icon=None,
					 tip=None, checkable=False, signal="triggered()"):
		action = QAction(text, self)
		if icon is not None:
			action.setIcon(QIcon("icons/"+sb_theme+"/%s.svg" % icon))
		if shortcut is not None:
			action.setShortcut(shortcut)
		if tip is not None:
			action.setToolTip(tip)
			action.setStatusTip(tip)
		if slot is not None:
			self.connect(action, SIGNAL(signal), slot)
		if checkable:
			action.setCheckable(True)
		return action


	def addActions(self, target, actions):
		for action in actions:
			if action is None:
				target.addSeparator()
			else:
				target.addAction(action)


	def fileNew(self):
		if not self.okToContinue():
			return
		self.sb_flush()

	def fileOpen(self):
		dir = os.path.dirname(self.filename) \
				if self.filename is not None else "."
		import swatchbook.codecs as codecs
		filetypes = {}
		for codec in codecs.reads:
			filetypes[eval('codecs.'+codec).__doc__ +' (*.'+eval('codecs.'+codec).ext+')'] = (codec,eval('codecs.'+codec).ext)
		allexts = ["*.%s" % unicode(format).lower() \
				   for format in codecs.exts.keys()]
		fname = self.sb.info['filename'] if 'filename' in self.sb.info else "."
		filetype = QString()
		fname = unicode(QFileDialog.getOpenFileName(self,
							"SwatchBooker - Choose file", dir,
							("All supported files (%s)" % " ".join(allexts))+";;"+(";;".join(sorted(filetypes.keys())))))
		if fname:
			self.loadFile(fname)

	def sb_flush(self):
		self.sbName.clear()
		self.sbDescription.clear()
		self.copyright.clear()
		self.version.clear()
		self.cols.setValue(0)
		self.cols.clear()
		self.rows.setValue(0)
		self.rows.clear()
		self.treeWidget.clear()
		self.listWidget.clear()
		self.listWidget.setMinimumSize(QSize(0,0))
		self.listWidget.setMaximumSize(QSize(16777215, 16777215))
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
			filetypes[eval('codecs.'+codec).__doc__ +' (*.'+eval('codecs.'+codec).ext+')'] = (codec,eval('codecs.'+codec).ext)
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
		for item in items:
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
			else:
				listItem = QListWidgetItem(self.listWidget)
				icon = self.colorswatch(item)
				listItem.setIcon(icon)
				self.listItems[listItem] = item
				self.itemList[item] = listItem
				if 'name' in item.info:
					treeItem = QTreeWidgetItem(parent,[QString(item.info['name'][0])])
					listItem.setToolTip(item.info['name'][0])
				else:
					treeItem = QTreeWidgetItem(parent)
				if len(item.values) > 0:
					treeItem.setIcon(0,self.colorswatch(item))
			if not isinstance(item, Spacer):
				self.treeItems[treeItem] = item
				self.itemTree[item] = treeItem
			if group:
				self.treeWidget.expandItem(parent)
			if not isinstance(item, Group) and not isinstance(item, Spacer):
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


if __name__ == "__main__":
	app = QApplication(sys.argv)
	if len(sys.argv) > 1:
		form = MainWindow(sys.argv[1])
	else:
		form = MainWindow()
	form.show()
	app.exec_()
