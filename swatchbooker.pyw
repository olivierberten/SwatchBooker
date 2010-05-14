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
import re
import tempfile
import gettext
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from swatchbook import *
import swatchbook.codecs as codecs
import swatchbook.websvc as websvc

__version__ = "0.7"

NUM_RE = re.compile('([0-9]+)')

availables_lang = {'de': u'Deutsch',
                   'fr': u'Français',
                   'pt_BR': u'Português do Brasil',
                   'ru': u'Русский'}

current_sp = False
breaks = []

swatchbooker_svg = (dirpath(__file__) or ".")+"/icons/swatchbooker.svg" 

# 0: float, 1: percentage, 2: degrees
models = SortedDict()
models['sRGB'] = (('R',1),('G',1),('B',1))
models['Lab'] = (('L',0),('a',0),('b',0))
models['XYZ'] = (('X',0),('Y',0),('Z',0))
models['RGB'] = (('R',1),('G',1),('B',1))
models['CMY'] = (('C',1),('M',1),('Y',1))
models['HLS'] = (('H',2),('L',1),('S',1))
models['HSV'] = (('H',2),('S',1),('V',1))
models['CMYK'] = (('C',1),('M',1),('Y',1),('K',1))
models['GRAY'] = (('K',1),)
models['YIQ'] = (('Y',0),('I',0),('Q',0))

def swupdate(id):
	form.swatches[id][0].update()
	for sw in form.swatches[id][1]:
		sw.update()
	for sw in form.swatches[id][2]:
		sw.update()

def grupdate(item):
	form.groups[item][0].update()

class MainWindow(QMainWindow):
	def __init__(self, file=False, parent=None):
		super(MainWindow, self).__init__(parent)
		
		if file:
			self.sb = SwatchBook(file)
		else:
			self.sb = SwatchBook()
			self.codec = 'sbz'

		self.setWindowTitle('SwatchBooker')
		self.setWindowIcon(QIcon(swatchbooker_svg))
		
		self.fileMenu = self.menuBar().addMenu(_("&File"))
		viewMenu = self.menuBar().addMenu(_("&View"))
		viewActionGroup = QActionGroup(self)
		self.treeViewAction = QAction(_("Tree view"),self)
		self.treeViewAction.setActionGroup(viewActionGroup)
		self.treeViewAction.setCheckable(True)
		self.connect(self.treeViewAction,SIGNAL("triggered()"),self.dispPane)
		self.gridViewAction = QAction(_("Grid view"),self)
		self.gridViewAction.setActionGroup(viewActionGroup)
		self.gridViewAction.setCheckable(True)
		self.connect(self.gridViewAction,SIGNAL("triggered()"),self.dispPane)
		self.directionMenu = QMenu(_("Grid direction"))
		directionActionGroup = QActionGroup(self)
		self.gridVertAction = QAction(_("Vertical"),self)
		self.gridVertAction.setActionGroup(directionActionGroup)
		self.gridVertAction.setCheckable(True)
		self.connect(self.gridVertAction,SIGNAL("triggered()"),self.gridEdit)
		self.gridHorizAction = QAction(_("Horizontal"),self)
		self.gridHorizAction.setActionGroup(directionActionGroup)
		self.gridHorizAction.setCheckable(True)
		self.connect(self.gridHorizAction,SIGNAL("triggered()"),self.gridEdit)
		self.availSwatchesAction = QAction(_("Available swatches"),self)
		self.availSwatchesAction.setCheckable(True)
		self.connect(self.availSwatchesAction,SIGNAL("triggered()"),self.dispPane)
		viewMenu.addAction(self.treeViewAction)
		viewMenu.addAction(self.gridViewAction)
		viewMenu.addMenu(self.directionMenu)
		self.directionMenu.addAction(self.gridVertAction)
		self.directionMenu.addAction(self.gridHorizAction)
		viewMenu.addSeparator()
		viewMenu.addAction(self.availSwatchesAction)
		self.menuBar().addAction(_("Settings"), self.settings)
		self.menuBar().addAction(_("&About"), self.about)
		self.updateFileMenu()

		if settings.contains('gridView') and settings.value('gridView').toBool():
			self.gridViewAction.setChecked(True)
			self.directionMenu.setEnabled(True)
		else:
			self.treeViewAction.setChecked(True)
			self.directionMenu.setEnabled(False)
		if settings.contains('swatchList') and not settings.value('swatchList').toBool():
			self.availSwatchesAction.setChecked(False)
		else:
			self.availSwatchesAction.setChecked(True)

		self.mainWidget = QSplitter(Qt.Horizontal)

		groupBoxInfo = QGroupBox(_("Information"))
		self.sbInfo = InfoWidget(self.sb,self)
		infoScrollArea = QScrollArea()
		infoScrollArea.setWidget(self.sbInfo)
		infoScrollArea.setWidgetResizable(True)
		infoScrollArea.setFrameShape(QFrame.NoFrame)
		sbInfoLayout = QVBoxLayout()
		sbInfoLayout.addWidget(infoScrollArea)
		groupBoxInfo.setLayout(sbInfoLayout)

		groupBoxProfiles = QGroupBox(_("Color profiles"))
		self.sbProfList = QTableWidget()
		self.sbProfList.horizontalHeader().setStretchLastSection(True)
		self.sbProfList.verticalHeader().hide()
		self.sbProfList.horizontalHeader().hide()
		self.sbProfList.setColumnCount(2)
		self.sbProfList.setColumnHidden(1,True)
		self.sbProfList.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.butProf = MenuButton(self)
		self.menuProf = QMenu()
		self.menuProf.addAction(_('Add'),self.addProfile)
		self.profRemoveAction = self.menuProf.addAction(_('Remove'),self.remProfile)
		self.butProf.setMenu(self.menuProf)
		self.profRemoveAction.setEnabled(False)

		sbProfiles = QHBoxLayout()
		sbProfiles.addWidget(self.sbProfList)
		sbProfiles.addWidget(self.butProf,0,Qt.AlignTop)
		groupBoxProfiles.setLayout(sbProfiles)

		sbLeftPane = QSplitter(Qt.Vertical)
		sbLeftPane.addWidget(groupBoxInfo)
		sbLeftPane.addWidget(groupBoxProfiles)
		
		# swList
		self.groupBoxList = QGroupBox(_("Available swatches"))

		self.swList = QListWidget()
		self.swList.setSortingEnabled(True)
		self.swnbLabel = QLabel()
		self.swLEditBut = MenuButton(self)
		self.swLEditMenu = QMenu()
		self.swLEditMenu.addAction(_('Add Color'),self.swAddColor)
		self.swDeleteAction = self.swLEditMenu.addAction(_('Delete'),self.swDelete)
		self.swLEditMenu.addAction(_('Delete unused swatches'),self.swDeleteUnused)
		self.swLEditBut.setMenu(self.swLEditMenu)
		self.swDeleteAction.setEnabled(False)
		
		sbList = QGridLayout()
		sbList.addWidget(self.swList,0,0)
		sbList.addWidget(self.swnbLabel,1,0)
		sbList.addWidget(self.swLEditBut,0,1,Qt.AlignTop)
		self.groupBoxList.setLayout(sbList)
		
		# sbTree
		self.groupBoxTree = QGroupBox(_("Tree view"))

		self.treeWidget = sbTreeWidget()
		self.swTEditBut = MenuButton(self)
		self.swTEditMenu = QMenu()
		self.swTEditMenu.addAction(_('Add Color'),self.addColor)
		self.swTEditMenu.addAction(_('Add Spacer'),self.addSpacer)
		self.swTEditMenu.addAction(_('Add Break'),self.addBreak)
		self.swTEditMenu.addAction(_('Add Group'),self.addGroup)
		self.deleteAction = self.swTEditMenu.addAction(_('Delete'),self.delete)
		self.deleteAction.setShortcut(Qt.Key_Delete)
		self.swTEditBut.setMenu(self.swTEditMenu)
		self.deleteAction.setEnabled(False)
		
		sbTree = QHBoxLayout()
		sbTree.addWidget(self.treeWidget)
		sbTree.addWidget(self.swTEditBut,0,Qt.AlignTop)
		self.groupBoxTree.setLayout(sbTree)

		# sbGrid
		self.groupBoxGrid = QGroupBox(_("Grid view"))

		self.gridWidget = sbGridWidget()
		self.colsLabel = QLabel()
		self.cols = QSpinBox()
		self.cols.setRange(0, 64)
		self.rowsLabel = QLabel()
		self.rows = QSpinBox()
		self.rows.setRange(0, 64)

		self.swGEditBut = MenuButton(self)
		self.swGEditMenu = QMenu()
		self.swGEditMenu.addAction(_('Add Color'),self.addColor)
		self.swGEditMenu.addAction(_('Add Spacer'),self.addSpacer)
		self.swGEditMenu.addAction(_('Add Break'),self.addBreak)
		self.swGEditMenu.addAction(self.deleteAction)
		self.swGEditBut.setMenu(self.swGEditMenu)

		sbGrid = QGridLayout()
		sbGrid.addWidget(self.gridWidget, 0, 0, 1, 2)
		sbGrid.setRowStretch(1,1)
		sbGrid.addWidget(self.colsLabel, 2, 0)
		sbGrid.addWidget(self.cols, 2, 1)
		sbGrid.addWidget(self.rowsLabel, 3, 0)
		sbGrid.addWidget(self.rows, 3, 1)
		sbGrid.addWidget(self.swGEditBut,0,2,Qt.AlignTop)
		self.groupBoxGrid.setLayout(sbGrid)

		if settings.contains('gridHoriz') and settings.value('gridHoriz').toBool():
			self.gridHorizAction.setChecked(True)
			self.colsLabel.setText(_("Rows:"))
			self.rowsLabel.setText(_("Columns:"))
		else:
			self.gridVertAction.setChecked(True)
			self.colsLabel.setText(_("Columns:"))
			self.rowsLabel.setText(_("Rows:"))

		self.mainWidget.addWidget(sbLeftPane)
		self.mainWidget.addWidget(self.groupBoxTree)
		self.mainWidget.addWidget(self.groupBoxGrid)
		self.mainWidget.addWidget(self.groupBoxList)

		self.setCentralWidget(self.mainWidget)

		self.connect(self.cols,
				SIGNAL("valueChanged(int)"), self.gridEdit)
		self.connect(self.rows,
				SIGNAL("valueChanged(int)"), self.gridEdit)
		self.connect(self.swList,
				SIGNAL("itemSelectionChanged()"), self.sw_display_list)
		self.connect(self.treeWidget,
				SIGNAL("itemSelectionChanged()"), self.sw_display_tree)
		self.connect(self.gridWidget,
				SIGNAL("itemSelectionChanged()"), self.sw_display_grid)
		self.connect(self.sbProfList,
				SIGNAL("itemSelectionChanged()"),self.prof_editable)

	def clear(self):
		global breaks
		breaks = []
		self.filename = False
		self.codec = False
		self.profiles = {}
		self.swatches = {}
		self.groups = {}
		self.items = {}

		self.sbInfo.clear()
		self.sbProfList.clear()
		self.sbProfList.setRowCount(0)
		self.swList.clear()
		self.rows.setValue(0)
		self.cols.setValue(0)
		self.gridWidget.clear()
		self.treeWidget.clear()
		self.deleteAction.setEnabled(False)
		if hasattr(self,'sbSwatch'):
			self.sbSwatch.setParent(None)

	def sw_display_list(self):
		if self.swList.selectedItems() and self.swList.hasFocus():
			listItem = self.swList.selectedItems()[0]
			if hasattr(self,'sbSwatch'):
				self.sbSwatch.setParent(None)
			self.sbSwatch = SwatchWidget(listItem.id,self)
			self.mainWidget.addWidget(self.sbSwatch)
			self.treeWidget.setCurrentItem(None)
			self.gridWidget.setCurrentItem(None)
			self.swDeleteAction.setEnabled(True)

	def sw_display_tree(self):
		if self.treeWidget.selectedItems():
			treeItem = self.treeWidget.selectedItems()[0]
			if treeItem and isinstance(treeItem,treeItemSwatch):
				self.gridWidget.setCurrentItem(self.items[treeItem])
				self.swList.setCurrentItem(self.swatches[treeItem.item.id][0])
			else:
				self.gridWidget.setCurrentItem(None)
				self.swList.setCurrentItem(None)
			if hasattr(self,'sbSwatch'):
				self.sbSwatch.setParent(None)
			if isinstance(treeItem,treeItemSwatch):
				self.sbSwatch = SwatchWidget(treeItem.item.id,self)
			if isinstance(treeItem,treeItemGroup):
				self.sbSwatch = GroupWidget(treeItem.item,self)
			if treeItem.__class__.__name__ not in ('treeItemSpacer','treeItemBreak','noChild'):
				self.mainWidget.addWidget(self.sbSwatch)
			if isinstance(treeItem, noChild):
				self.deleteAction.setEnabled(False)
			else:
				self.deleteAction.setEnabled(True)

	def sw_display_grid(self):
		global current_sw
		if self.gridWidget.selectedItems():
			listItem = self.gridWidget.selectedItems()[0]
			items = dict([v,k] for k,v in self.items.iteritems())
			self.treeWidget.setCurrentItem(items[listItem])
			self.swList.setCurrentItem(self.swatches[listItem.item.id][0])

	def gridEdit(self):
		if self.cols.value() > 0:
			self.sb.book.display['columns'] = self.cols.value()
		elif self.cols.value() == 0:
			self.sb.book.display['columns'] = False
		if self.rows.value() > 0:
			self.sb.book.display['rows'] = self.rows.value()
		elif self.rows.value() == 0:
			self.sb.book.display['rows'] = False
		if self.gridHorizAction.isChecked():
			settings.setValue("gridHoriz",QVariant(True))
			self.colsLabel.setText(_("Rows:"))
			self.rowsLabel.setText(_("Columns:"))
		if self.gridVertAction.isChecked():
			settings.setValue("gridHoriz",QVariant(False))
			self.colsLabel.setText(_("Columns:"))
			self.rowsLabel.setText(_("Rows:"))
		self.gridWidget.update()

	def update(self):
		self.clear()

		for swatch in self.sb.swatches:
			self.addSwatch(swatch)
		self.sbInfo.update(self.sb)
		self.updSwatchCount()
		self.fillViews(self.sb.book.items)
		self.gridWidget.update()
		for prof in self.sb.profiles:
			self.addProfileToList(prof,self.sb.profiles[prof])
		if self.sb.book.display['columns']:
			self.cols.setValue(self.sb.book.display['columns'])
		if self.sb.book.display['rows']:
			self.rows.setValue(self.sb.book.display['rows'])
	
	def updSwatchCount(self):
		self.swnbLabel.setText(n_('%s swatch','%s swatches',len(self.sb.swatches)) % len(self.sb.swatches))

	def addSwatch(self,id):
		swatch = listItemSwatch(id)
		self.swList.addItem(swatch)
		self.swatches[id] = (swatch,[],[])

	def swAddColor(self):
		id = _('New Color')
		if id in form.sb.swatches:
			i = 1
			while id in form.sb.swatches:
				id = _('New Color')+' ('+str(i)+')'
				i += 1
		swatch = Color(self.sb)
		swatch.info.identifier = id
		form.sb.swatches[id] = swatch
		self.addSwatch(id)
		self.swList.setFocus()
		self.swList.setCurrentItem(self.swatches[id][0])
		self.updSwatchCount()
		return id

	def swDelete(self):
		item = self.swList.selectedItems()[0]
		for treeItem in self.swatches[item.id][1]:
			if treeItem.parent():
				treeItem.parent().takeChild(treeItem.parent().indexOfChild(treeItem))
			else:
				self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(treeItem))
		treeItem = None
		for gridItem in self.swatches[item.id][2]:
			self.gridWidget.takeItem(self.gridWidget.row(gridItem))
		gridItem = None
		if hasattr(self,'sbSwatch'):
			self.sbSwatch.setParent(None)
		self.swList.takeItem(self.swList.row(item))
		del self.sb.swatches[item.id]
		del self.swatches[item.id]
		self.deleteAction.setEnabled(False)
		self.updSwatchCount()

	def swDeleteUnused(self):
		for swatch in self.swatches.keys():
			if len(self.swatches[swatch][1]) == 0:
				self.swList.takeItem(self.swList.row(self.swatches[swatch][0]))
				del self.sb.swatches[swatch]
				del self.swatches[swatch]

	def addColor(self):
		self.addSwatchToBook('Color')
		
	def addSwatchToBook(self,type):
		selected = self.treeWidget.selectedItems()
		id = eval('self.swAdd'+type+'()')
		item = Swatch(id)
		gridItem = gridItemSwatch(item)
		treeItem = treeItemSwatch(item)
		if selected:
			selTItem = selected[0]
			if selTItem.parent():
				parent = selTItem.parent().item
				if isinstance(selTItem,noChild):
					index = 0
				else:
					index = selTItem.parent().indexOfChild(selTItem)+1
			else:
				parent = form.sb.book
				index = self.treeWidget.indexOfTopLevelItem(selTItem)+1
			parent.items.insert(index,item)

			if selTItem.parent() == None:
				tIndex = self.treeWidget.indexOfTopLevelItem(selTItem)
				self.treeWidget.insertTopLevelItem(tIndex+1, treeItem)
			else:
				tIndex = selTItem.parent().indexOfChild(selTItem)
				selTItem.parent().insertChild(tIndex+1,treeItem)

			if isinstance(selTItem,treeItemGroup):
				selLItem = self.groups[selTItem.item][1][1]
			elif isinstance(selTItem,noChild):
				selLItem = self.groups[selTItem.parent().item][1][0]
			else:
				selLItem = self.items[selTItem]
			lIndex = self.gridWidget.indexFromItem(selLItem).row()
			self.gridWidget.insertItem(lIndex+1,gridItem)
			if isinstance(selTItem,noChild):
				selTItem.parent().takeChild(0)
		else:
			self.sb.book.items.append(item)
			self.treeWidget.addTopLevelItem(treeItem)
			self.gridWidget.addItem(gridItem)
		self.items[treeItem] = gridItem
		self.treeWidget.setCurrentItem(treeItem)
		self.gridWidget.update()

	def addBreak(self):
		self.addBreakSpacer('Break')

	def addSpacer(self):
		self.addBreakSpacer('Spacer')

	def addBreakSpacer(self,type):
		item = eval(type+'()')
		gridItem = eval('gridItem'+type+'(item)')
		treeItem = eval('treeItem'+type+'(item)')
		if self.treeWidget.selectedItems():
			selTItem = self.treeWidget.selectedItems()[0]
			if selTItem.parent():
				parent = selTItem.parent().item
				if isinstance(selTItem,noChild):
					index = 0
				else:
					index = selTItem.parent().indexOfChild(selTItem)+1
			else:
				parent = form.sb.book
				index = self.treeWidget.indexOfTopLevelItem(selTItem)+1
			parent.items.insert(index,item)

			if selTItem.parent() == None:
				tIndex = self.treeWidget.indexOfTopLevelItem(selTItem)
				self.treeWidget.insertTopLevelItem(tIndex+1, treeItem)
			else:
				tIndex = selTItem.parent().indexOfChild(selTItem)
				selTItem.parent().insertChild(tIndex+1,treeItem)

			if isinstance(selTItem,treeItemGroup):
				selLItem = self.groups[selTItem.item][1][1]
			elif isinstance(selTItem,noChild):
				selLItem = self.groups[selTItem.parent().item][1][0]
			else:
				selLItem = self.items[selTItem]
			lIndex = self.gridWidget.indexFromItem(selLItem).row()
			self.gridWidget.insertItem(lIndex+1,gridItem)
			if isinstance(selTItem,noChild):
				selTItem.parent().takeChild(0)
		else:
			self.sb.book.items.append(item)
			self.treeWidget.addTopLevelItem(treeItem)
			self.gridWidget.addItem(gridItem)
		self.items[treeItem] = gridItem
		self.treeWidget.setCurrentItem(treeItem)
		self.gridWidget.update()

	def addGroup(self):
		item = Group()
		item.info.title = _('New group')
		treeItem = treeItemGroup(item)
		gridItemIn = gridItemGroup(item)
		gridItemOut = gridItemGroup(item)
		if self.treeWidget.selectedItems():
			selTItem = self.treeWidget.selectedItems()[0]
			if selTItem.parent():
				parent = selTItem.parent().item
				if isinstance(selTItem,noChild):
					index = 0
				else:
					index = selTItem.parent().indexOfChild(selTItem)+1
			else:
				parent = form.sb.book
				index = self.treeWidget.indexOfTopLevelItem(selTItem)+1
			parent.items.insert(index,item)

			if selTItem.parent() == None:
				tIndex = self.treeWidget.indexOfTopLevelItem(selTItem)
				self.treeWidget.insertTopLevelItem(tIndex+1, treeItem)
			else:
				tIndex = selTItem.parent().indexOfChild(selTItem)
				selTItem.parent().insertChild(tIndex+1,treeItem)

			if isinstance(selTItem,treeItemGroup):
				selLItem = self.groups[selTItem.item][1][1]
			elif isinstance(selTItem,noChild):
				selLItem = self.groups[selTItem.parent().item][1][0]
			else:
				selLItem = self.items[selTItem]
			lIndex = self.gridWidget.indexFromItem(selLItem).row()
			self.gridWidget.insertItem(lIndex+1,gridItemOut)
			self.gridWidget.insertItem(lIndex+1,gridItemIn)
			if isinstance(selTItem,noChild):
				selTItem.parent().takeChild(0)
		else:
			self.sb.book.items.append(item)
			self.treeWidget.addTopLevelItem(treeItem)
		self.groups[item][1] = (gridItemIn,gridItemOut)
		self.gridWidget.addItem(gridItemIn)
		self.gridWidget.addItem(gridItemOut)
		self.items[treeItem] = None
		nochild = noChild()
		treeItem.addChild(nochild)
		self.treeWidget.expandItem(treeItem)
		self.treeWidget.setCurrentItem(treeItem)
		self.gridWidget.update()

	def delete(self):
		if self.treeWidget.selectedItems():
			selTItem = self.treeWidget.selectedItems()[0]
			if isinstance(selTItem,treeItemGroup):
				self.del_group_from_list(selTItem)
			else:
				if isinstance(selTItem,treeItemSwatch):
					self.swatches[selTItem.item.id][1].remove(selTItem)
					self.swatches[selTItem.item.id][2].remove(self.items[selTItem])
				self.gridWidget.takeItem(self.gridWidget.row(self.items[selTItem]))
			if isinstance(selTItem, treeItemBreak):
				global breaks
				breaks.remove(self.items[selTItem])
			if selTItem.parent():
				tParent = selTItem.parent()
				tParent.takeChild(tParent.indexOfChild(selTItem))
				tParent.item.items.remove(selTItem.item)
				if tParent.childCount() == 0:
					nochild = noChild()
					tParent.addChild(nochild)
			else:
				self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(selTItem))
				self.sb.book.items.remove(selTItem.item)
		if self.treeWidget.topLevelItemCount() == 0:
			self.deleteAction.setEnabled(False)

	def del_group_from_list(self,group):
		for i in range(group.childCount()):
			if isinstance(group.child(i), treeItemGroup):
				self.del_group_from_list(group.child(i))
			else:
				if isinstance(group.child(i),treeItemSwatch):
					self.swatches[group.child(i).item.id][1].remove(group.child(i))
					self.swatches[group.child(i).item.id][2].remove(self.items[group.child(i)])
				self.gridWidget.takeItem(self.gridWidget.row(self.items[group.child(i)]))

	def dispPane(self):
		if self.availSwatchesAction.isChecked():
			settings.setValue("swatchList",QVariant(True))
			self.groupBoxList.show()
		else:
			settings.setValue("swatchList",QVariant(False))
			self.groupBoxList.hide()
		if self.treeViewAction.isChecked():
			settings.setValue("gridView",QVariant(False))
			self.groupBoxTree.show()
			self.groupBoxGrid.hide()
			self.directionMenu.setEnabled(False)
		if self.gridViewAction.isChecked():
			settings.setValue("gridView",QVariant(True))
			self.groupBoxTree.hide()
			self.groupBoxGrid.show()
			self.directionMenu.setEnabled(True)

	def about(self):
		QMessageBox.about(self, _("About SwatchBooker"),
                """<b>SwatchBooker</b> %s
                <p>&copy; 2008 Olivier Berten
                <p>Qt %s - PyQt %s""" % (
                __version__, QT_VERSION_STR, PYQT_VERSION_STR))

	def settings(self):
		dialog = SettingsDlg(self)
		if dialog.exec_():
			if dialog.returnDisProf():
				settings.setValue("mntrProfile",QVariant(dialog.returnDisProf()))
			else:
				settings.remove("mntrProfile")
			if dialog.returnCMYKProf():
				settings.setValue("CMYKProfile",QVariant(dialog.returnCMYKProf()))
			else:
				settings.remove("CMYKProfile")
			settings.setValue("MaxRecentFiles",QVariant(dialog.RecFilesSpin.value()))
			if dialog.lang:
				settings.setValue("Language",dialog.lang)
			else:
				settings.remove("Language")
			self.updateFileMenu()

	def updateFileMenu(self,fname=False):
		if not settings.contains("MaxRecentFiles"):
			settings.setValue("MaxRecentFiles",QVariant(6))
		files = settings.value("recentFileList").toStringList()
		for file in files:
			if not QFile.exists(file):
				files.removeAll(file)
		
		if fname:
			files.removeAll(fname)
			files.prepend(fname)
			while files.count() > settings.value("MaxRecentFiles").toInt()[0]:
				files.removeAt(files.count()-1)

		settings.setValue("recentFileList", QVariant(files))

		numRecentFiles = min(files.count(), settings.value("MaxRecentFiles").toInt()[0])

		recentFileActs = []
		
		for h in range(settings.value("MaxRecentFiles").toInt()[0]):
			recentFileActs.append(QAction(self))
			recentFileActs[h].setVisible(False)
			self.connect(recentFileActs[h], SIGNAL("triggered()"),
						 self.openRecentFile)

		for i in range(numRecentFiles):
			text = QString("&%1 %2").arg(i+1).arg(self.strippedName(files[i]))
			recentFileActs[i].setText(text)
			recentFileActs[i].setData(QVariant(files[i]))
			recentFileActs[i].setVisible(True)
			
		for j in range(numRecentFiles, settings.value("MaxRecentFiles").toInt()[0]):
			recentFileActs[j].setVisible(False)

		self.fileMenu.clear()
		self.fileMenu.addAction(_("&New"), self.fileNew, QKeySequence.New)
		self.fileMenu.addAction(_("&Open"), self.fileOpen, QKeySequence.Open)
		self.fileMenu.addAction(_("Open from web"), self.webOpen)
		self.fileMenu.addAction(_("&Save"), self.fileSave, QKeySequence.Save)
		self.fileMenu.addAction(_("Save As..."), self.fileSaveAs)
		self.fileMenu.addSeparator()
		for k in range(settings.value("MaxRecentFiles").toInt()[0]):
			self.fileMenu.addAction(recentFileActs[k])

	def strippedName(self, fullFileName):
		return QFileInfo(fullFileName).fileName()

	def openRecentFile(self):
		action = self.sender()
		if action:
			self.loadFile(unicode(action.data().toString()))

	def fileNew(self):
		self.sb = SwatchBook()
		self.clear()
		self.codec = 'sbz'

	def webOpen(self):
		dialog = webOpenDlg(self)
		if dialog.exec_() and dialog.svc and dialog.id:
			self.clear()
			self.sb = SwatchBook(websvc=dialog.svc,webid=dialog.id)
			self.update()

	def fileOpen(self):
		dir = settings.value('lastOpenDir').toString() if settings.contains('lastOpenDir') else "."
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
		fname = unicode(QFileDialog.getOpenFileName(self,
							_("Choose file"), dir,
							(unicode(_("All supported files (%s)")) % " ".join(allexts))+";;"+(";;".join(sorted(filetypes)))+_(";;All files (*)"),filetype))
		if fname:
			settings.setValue('lastOpenCodec',QVariant(filetype))
			settings.setValue('lastOpenDir',QVariant(os.path.dirname(fname)))
			self.loadFile(fname)

	def loadFile(self, fname):
		try:
			self.clear()
			self.sb = SwatchBook(fname)
			self.updateFileMenu(fname)
			self.update()
			self.filename = fname
			if self.sb.codec in codecs.writes:
				self.codec = self.sb.codec
		except FileFormatError:
			QMessageBox.critical(self, _("Error"), _("Unsupported file"))

	def fillViews(self,items,group = False):
		for item in items:
			if group:
				parent = group
			else:
				parent = self.treeWidget
			if isinstance(item,Group):
				gridItemIn = gridItemGroup(item,self.gridWidget)
				treeItem = treeItemGroup(item,parent)
				if len(item.items) > 0:
					self.fillViews(item.items,treeItem)
				else:
					nochild = noChild()
					treeItem.addChild(nochild)
				self.items[treeItem] = None
				gridItemOut = gridItemGroup(item,self.gridWidget)
				self.groups[item][1] = (gridItemIn,gridItemOut)
			elif isinstance(item,Spacer):
				treeItem = treeItemSpacer(item,parent)
				gridItem = gridItemSpacer(item,self.gridWidget)
				self.items[treeItem] = gridItem
			elif isinstance(item,Break):
				treeItem = treeItemBreak(item,parent)
				gridItem = gridItemBreak(item,self.gridWidget)
				self.items[treeItem] = gridItem
			else:
				treeItem = treeItemSwatch(item,parent)
				gridItem = gridItemSwatch(item,self.gridWidget)
				self.items[treeItem] = gridItem
			if group:
				self.treeWidget.expandItem(parent)

	def fileSave(self):
		if self.filename and self.codec:
			self.sb.write(self.codec,self.filename)
		else:
			self.fileSaveAs()

	def fileSaveAs(self):
		filetypes = {}
		for codec in codecs.writes:
			codec_exts = []
			for ext in eval('codecs.'+codec).ext:
				codec_exts.append('*.'+ext)
			codec_txt = eval('codecs.'+codec).__doc__ +' ('+" ".join(codec_exts)+')'
			filetypes[codec_txt] = (codec,eval('codecs.'+codec).ext[0])
		dir = unicode(settings.value('lastSaveDir').toString()) if settings.contains('lastSaveDir') else "."
		f = os.path.splitext(os.path.basename(self.filename or ''))[0]
		if f == '':
			f = self.sb.info.title
		if settings.contains('lastSaveCodec'):
			filetype = settings.value('lastSaveCodec').toString()
		else:
			filetype = QString()
		fname = unicode(QFileDialog.getSaveFileName(self,
						_("Save file"), os.path.join(dir,f),
						";;".join(filetypes.keys()),filetype))
		if fname:
			if len(fname.rsplit(".",1)) == 1 or (len(fname.rsplit(".",1)) > 1 and fname.rsplit(".",1)[1] != filetypes[unicode(filetype)][1]):
				fname += "."+filetypes[unicode(filetype)][1]
			self.filename = fname
			settings.setValue('lastSaveDir',QVariant(os.path.dirname(fname)))
			settings.setValue('lastSaveCodec',QVariant(filetype))
			self.codec = filetypes[unicode(filetype)][0]
			self.fileSave()
			if self.codec in codecs.reads:
				self.updateFileMenu(fname)

	def prof_editable(self):
		if self.sbProfList.isItemSelected(self.sbProfList.currentItem()):
			self.profRemoveAction.setEnabled(True)

	def addProfile(self):
		fname = unicode(QFileDialog.getOpenFileName(self,
							_("Choose file"), ".",
							(_("ICC profiles (*.icc *.icm)"))))
		if fname:
			# the next 6 lines are a workaround for the unability of lcms to deal with unicode file names
			fi = open(fname, 'rb')
			uri = tempfile.mkstemp()[1]
			fo = open(uri,'wb')
			fo.write(fi.read())
			fi.close()
			fo.close()
			profile = icc.ICCprofile(uri)
			#TODO: check if exists
			id = os.path.basename(fname)
			self.sb.profiles[id] = profile
			self.addProfileToList(id,profile)

	def addProfileToList(self,id,profile):
			profItemID = QTableWidgetItem(id)
			profItemTitle = QTableWidgetItem(profile.info['desc'][0])
			cprt = profile.info['cprt']
			if 0 in cprt:
				profItemTitle.setToolTip(cprt[0])
			elif 'en_US' in cprt:
				profItemTitle.setToolTip(cprt['en_US'])
			row = self.sbProfList.rowCount()
			self.sbProfList.setRowCount(row+1)
			self.sbProfList.setItem(row, 0, profItemTitle)
			self.sbProfList.setItem(row, 1, profItemID)
			space = profile.info['space'].strip()
			if space in self.profiles:
				self.profiles[space].append(id)
			else:
				self.profiles[space] = [id]

	def remProfile(self):
		profid = unicode(self.sbProfList.item(self.sbProfList.currentItem().row(),1).text())
		self.sbProfList.removeRow(self.sbProfList.currentItem().row())
		self.profiles[self.sb.profiles[profid].info['space'].strip()].remove(profid)
		del self.sb.profiles[profid]
		self.profRemoveAction.setEnabled(False)
		# TODO remove profile from color values

class MenuButton(QToolButton):
	def __init__(self,parent=None):
		super(MenuButton, self).__init__(parent)
		self.setFixedSize(12,12)
		self.setArrowType(Qt.DownArrow)
		self.setStyleSheet("MenuButton::menu-indicator {image: none;}")
		self.setPopupMode(QToolButton.InstantPopup)

class InfoWidget(QWidget):
	def __init__(self,item,parent=None):
		super(InfoWidget, self).__init__(parent)
		self.item = item
		for field in Info.dc:
			if Info.dc[field][1]:
				exec('self.'+field+' = QTextEdit()')
				exec('self.connect(self.'+field+',	SIGNAL("textChanged()"), self.edit)')
			else:
				exec('self.'+field+' = QLineEdit()')
				exec('self.connect(self.'+field+',	SIGNAL("editingFinished()"), self.edit)')
			exec('self.'+field+'.setObjectName("'+field+'")')
			if Info.dc[field][0]:
				exec('self.l10n'+field.capitalize()+' = l10nButton()')
				exec('self.connect(self.l10n'+field.capitalize()+',	SIGNAL("pressed()"), self.l10n)')
		self.date = QDateTimeEdit()
#		self.license = LicenseWidget()
		self.license = QLineEdit()

		layout = QGridLayout()
		layout.setContentsMargins(0,0,0,0)
		i = 0
		if item.__class__.__name__ not in ('SwatchBook','Group'):
			layout.addWidget(QLabel(_("Identifier:")), i, 0)
			layout.addWidget(self.identifier, i, 1, 1, 2)
			i += 1
		layout.addWidget(QLabel(_("Title:")), i, 0)
		layout.addWidget(self.title, i, 1)
		layout.addWidget(self.l10nTitle, i, 2)
		i += 1
		
		layout.addWidget(QLabel(_("Description:")), i, 0, 1, 2)
		layout.addWidget(self.description, i+1, 0, 1, 2)
		layout.addWidget(self.l10nDescription, i+1, 2, Qt.AlignTop)
		i = i+2
		
		if item.__class__.__name__ in ('SwatchBook',):
			layout.addWidget(QLabel(_("Rights:")), i, 0, 1, 2)
			layout.addWidget(self.rights, i+1, 0, 1, 2)
			layout.addWidget(self.l10nRights, i+1, 2, Qt.AlignTop)
			i = i+2
		
			layout.addWidget(QLabel(_("License:")), i, 0)
			layout.addWidget(self.license, i, 1, 1, 2)
			i += 1
		
		self.setLayout(layout)
		self.update(item)

	def update(self,item):
		self.item = item
		for field in Info.dc:
			exec('self.'+field+'.setText(item.info.'+field+')')
			if Info.dc[field][0]:
				if eval('len(item.info.'+field+'_l10n) > 0'):
					exec('self.l10n'+field.capitalize()+'.set()')
				else:
					exec('self.l10n'+field.capitalize()+'.clear()')
#		self.date.setDateTime()
		self.license.setText(item.info.license)

	def clear(self):
		for field in Info.dc:
			exec('self.'+field+'.clear()')
			if Info.dc[field][0]:
				exec('self.l10n'+field.capitalize()+'.clear()')
#		self.date.clear()
		self.license.clear()

	def edit(self):
		if self.sender().objectName() == 'identifier':
			newid = unicode(self.sender().text())
			if self.item.info.identifier !=	newid:
				if newid in form.sb.swatches:
					QMessageBox.critical(self, _('Error'), _("There's already a swatch with that identifier."))
					self.sender().setText(self.item.info.identifier)
				else:
					form.sb.swatches[newid] = form.sb.swatches[self.item.info.identifier]
					del form.sb.swatches[self.item.info.identifier]
					form.swatches[newid] = form.swatches[self.item.info.identifier]
					del form.swatches[self.item.info.identifier]
					self.item.info.identifier = newid
					form.swatches[newid][0].id = newid
					for sw in form.swatches[newid][1]:
						sw.item.id = newid
		else:
			if isinstance(self.sender(),QTextEdit):
				text = self.sender().toPlainText()
			else:
				text = self.sender().text()
			exec('self.item.info.'+str(self.sender().objectName())+' = unicode(text)')
		if isinstance(self.item,Group):
			grupdate(self.item)
		elif not isinstance(self.item,SwatchBook):
			swupdate(self.item.info.identifier)
			form.swList.scrollTo(form.swList.currentIndex())

	def l10n(self):
		if not self.sender().isChecked():
			infos = {}
			for field in Info.dc:
				if Info.dc[field][0]:
					exec('infos[self.l10n'+field.capitalize()+'] = "'+field+'"')
			long = Info.dc[infos[self.sender()]][1]
			l10nPopup = l10nWidget(self.sender(),eval('self.item.info.'+infos[self.sender()]+'_l10n'),long,self)
			l10nPopup.show()

class cornerButton(QToolButton):
	def __init__(self, parent=None):
		super(cornerButton, self).__init__(parent)

class l10nButton(QToolButton):
	def __init__(self, parent=None):
		super(l10nButton, self).__init__(parent)
		self.setCheckable(True)
		self.setText('l10n')

	def set(self):
		self.setStyleSheet("l10nButton { font-size: 9px; font-weight: bold }")

	def clear(self):
		self.setStyleSheet("l10nButton { font-size: 9px; font-weight: normal }")

class l10nWidget(QWidget):
	def __init__(self, caller, info, long=False, parent=None):
		super(l10nWidget, self).__init__(parent)
		self.setWindowFlags(Qt.Popup)
		
		self.caller = caller
		self.info = info
		self.long = long
		
		list = QWidget()
		self.l10nList = QVBoxLayout()
		self.l10nList.setContentsMargins(0,0,0,0)
		list.setLayout(self.l10nList)

		addButton = QPushButton(_('Add localization'))
		scrollArea = QScrollArea()
		scrollArea.setWidget(list)
		scrollArea.setContentsMargins(0,0,0,0)
		scrollArea.setWidgetResizable(True)
		layout = QVBoxLayout()
		layout.addWidget(addButton)
		layout.addWidget(scrollArea)
		self.setLayout(layout)

		screen = QApplication.desktop().availableGeometry(caller)

		x = caller.mapToGlobal(QPoint(0,0)).x() + caller.rect().width()
		y = caller.mapToGlobal(QPoint(0,0)).y()
		sh = QSize(300,150)

		self.resize(sh)
		if y + sh.height() > screen.height():
			y = y - sh.height() + caller.rect().height()
		if x + sh.width() > screen.width():
			x = x - caller.rect().width() - sh.width()
		self.move(QPoint(x,y))

		for lang in info:
			self.l10nList.addWidget(l10nItem(lang,info[lang],self.long,parent=self))

		self.connect(addButton,
				SIGNAL("clicked()"), self.addItem)

	def addItem(self):
		self.l10nList.addWidget(l10nItem(long=self.long,parent=self))
		
	def paintEvent(self, e):
		p = QPainter(self)
		frame = QStyleOptionFrame()
		frame.rect = self.rect()
		frame.palette = self.palette()
		frame.state = QStyle.State_None
		frame.lineWidth = self.style().pixelMetric(QStyle.PM_MenuPanelWidth)
		frame.midLineWidth = 0
		self.style().drawPrimitive(QStyle.PE_FrameMenu, frame, p, self)

	def hideEvent(self, e):
		self.caller.setDown(False)
		
class l10nItem(QWidget):
	def __init__(self, lang='', text='', long=False, parent=None):
		super(l10nItem, self).__init__(parent)
		
		self.lang = lang
		self.text = text
		self.parent = parent
		
		layout = QHBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		self.langEdit = QLineEdit(lang)
		self.langEdit.setFixedWidth(50)
		if long:
			self.textEdit = QTextEdit()
		else:
			self.textEdit = QLineEdit()
		self.textEdit.setText(text)
		delLoc = QPushButton('-')
		delLoc.setFixedWidth(delLoc.sizeHint().height())
		layout.addWidget(self.langEdit,0,Qt.AlignTop)
		layout.addWidget(self.textEdit,0,Qt.AlignTop)
		layout.addWidget(delLoc,0,Qt.AlignTop)
		self.setLayout(layout)

		self.connect(self.langEdit,
				SIGNAL("editingFinished()"), self.langEdited)
		self.connect(self.textEdit,
				SIGNAL("textChanged(QString)"), self.textEdited)
		self.connect(self.textEdit,
				SIGNAL("textChanged()"), self.textEdited)
		self.connect(delLoc,
				SIGNAL("clicked()"), self.delLoc)

	def langEdited(self):
		if (unicode(self.langEdit.text()) != self.lang) and (unicode(self.langEdit.text()) not in self.parent.info) and (unicode(self.langEdit.text()) > ''):
			if self.lang > '':
				del self.parent.info[self.lang]
			self.textEdited()
			self.lang = unicode(self.langEdit.text())
			self.parent.caller.set()
		else:
			self.langEdit.setText(self.lang)

	def textEdited(self):
		if isinstance(self.textEdit,QTextEdit):
			text = self.textEdit.toPlainText()
		else:
			text = self.textEdit.text()
		self.parent.info[unicode(self.langEdit.text())] = unicode(text)

	def delLoc(self):
		if self.langEdit.text() > '':
			del self.parent.info[unicode(self.langEdit.text())]
		self.parent.l10nList.removeWidget(self)
		self.setParent(None)
		if self.parent.l10nList.count() == 0:
			self.parent.caller.clear()

class swIcon(QIcon):
	def __init__(self,id):
		super(swIcon, self).__init__()
		swatch = form.sb.swatches[id]
		pix = QPixmap(16,16)
		pix.fill(Qt.transparent)
		paint = QPainter()
		if isinstance(swatch,Color) and swatch.toRGB8():
			prof_out = str(settings.value("mntrProfile").toString()) or False
			r,g,b = swatch.toRGB8(prof_out)
			paint.begin(pix)
			paint.setBrush(QColor(r,g,b))
			if 'spot' in swatch.usage:
				paint.drawEllipse(0, 0, 15, 15)
			else:
				paint.drawRect(0, 0, 15, 15)
			paint.end()
			self.addPixmap(pix)
			paint.begin(pix)
			paint.setPen(QColor(255,255,255))
			if 'spot' in swatch.usage:
				paint.drawEllipse(0, 0, 15, 15)
			else:
				paint.drawRect(0, 0, 15, 15)
			paint.setPen(Qt.DotLine)
			if 'spot' in swatch.usage:
				paint.drawEllipse(0, 0, 15, 15)
			else:
				paint.drawRect(0, 0, 15, 15)
			paint.end()
		else:
			paint.begin(pix)
			paint.setPen(QPen(QColor(218,218,218),3.0))
			paint.drawLine(QLine(3, 3, 12, 12))
			paint.drawLine(QLine(12, 3, 3, 12))
			paint.end()
			self.addPixmap(pix)
			paint.begin(pix)
			paint.setPen(QColor(255,255,255))
			paint.drawRect(0, 0, 15, 15)
			paint.setPen(Qt.DotLine)
			paint.drawRect(0, 0, 15, 15)
			paint.end()
		self.addPixmap(pix,QIcon.Selected)

class listItemSwatch(QListWidgetItem):
	def __init__(self,id):
		super(listItemSwatch, self).__init__()
		self.id = id
		self.update()

	def update(self):
		if form.sb.swatches[self.id].info.title > '':
			text = form.sb.swatches[self.id].info.title
		else:
			text = form.sb.swatches[self.id].info.identifier
		self.setText(text)
		self.setIcon(swIcon(self.id))

	@staticmethod
	def alphanum_key(s):
		return [ int(c) if c.isdigit() else c.lower() for c in NUM_RE.split(s) ]

	def __lt__ (self, other):
		lvalue = self.alphanum_key(unicode(self.data(0).toString()))
		rvalue = self.alphanum_key(unicode(other.data(0).toString()))
		if lvalue == rvalue:
			return self.id < other.id
		else:
			return lvalue < rvalue

class gridItemSwatch(QListWidgetItem):
	def __init__(self, item, parent=None):
		super(gridItemSwatch, self).__init__(parent)
		self.item = item
		form.swatches[item.id][2].append(self)
		self.setSizeHint(QSize(17,17))
		self.update()

	def update(self):
		text = [form.sb.swatches[self.item.id].info.identifier,]
		if form.sb.swatches[self.item.id].info.title > '':
			text.append(form.sb.swatches[self.item.id].info.title)
		self.setToolTip('<br />'.join(text))
		self.setIcon(swIcon(self.item.id))

class treeItemSwatch(QTreeWidgetItem):
	def __init__(self, item, parent=None):
		super(treeItemSwatch, self).__init__(parent)
		self.item = item
		form.swatches[item.id][1].append(self)
		self.setFlags(self.flags() & ~(Qt.ItemIsDropEnabled))
		self.update()

	def update(self):
		if form.sb.swatches[self.item.id].info.title > '':
			text = form.sb.swatches[self.item.id].info.title
		else:
			text = form.sb.swatches[self.item.id].info.identifier
		self.setText(0,text)
		self.setIcon(0,swIcon(self.item.id))

class treeItemGroup(QTreeWidgetItem):
	def __init__(self, item, parent=None):
		super(treeItemGroup, self).__init__(parent)
		self.item = item
		form.groups[item] = [self,None]
		self.update()

	def update(self):
		if self.item.info.title > '':
			self.setText(0,QString(self.item.info.title))
		else:
			self.setText(0,QString())

	def childCount(self):
		if isinstance(self.child(0),noChild):
			return 0
		else:
			return QTreeWidgetItem.childCount(self)

class treeItemSpacer(QTreeWidgetItem):
	def __init__(self, item, parent=None):
		super(treeItemSpacer, self).__init__(parent)

		self.item = item
		font = QFont()
		font.setItalic(True)
		self.setText(0,QString('<spacer>'))
		self.setFont(0,font)
		self.setTextColor(0,QColor(128,128,128))
		self.setFlags(self.flags() & ~(Qt.ItemIsDropEnabled))

class gridItemSpacer(QListWidgetItem):
	def __init__(self, item, parent=None):
		super(gridItemSpacer, self).__init__(parent)

		self.item = item
		pix = QPixmap(1,1)
		pix.fill(Qt.transparent)
		self.setIcon(QIcon(pix))
		self.setSizeHint(QSize(17,17))
		self.setFlags(Qt.NoItemFlags)

class treeItemBreak(QTreeWidgetItem):
	def __init__(self, item, parent=None):
		super(treeItemBreak, self).__init__(parent)

		self.item = item
		font = QFont()
		font.setItalic(True)
		self.setText(0,QString('<break>'))
		self.setFont(0,font)
		self.setTextColor(0,QColor(128,128,128))
		self.setFlags(self.flags() & ~(Qt.ItemIsDropEnabled))

class gridItemBreak(QListWidgetItem):
	def __init__(self, item, parent=None):
		super(gridItemBreak, self).__init__(parent)

		self.item = item
		breaks.append(self)
		pix = QPixmap(1,1)
		pix.fill(Qt.transparent)
		self.setIcon(QIcon(pix))
		self.setSizeHint(QSize(0,17))
		self.setFlags(Qt.NoItemFlags)

class gridItemGroup(gridItemBreak):
	def __init__(self, item, parent=None):
		super(gridItemGroup, self).__init__(item, parent)

class noChild(QTreeWidgetItem):
	def __init__(self, parent=None):
		super(noChild, self).__init__(parent)

		font = QFont()
		font.setItalic(True)
		self.setText(0,_('empty'))
		self.setFont(0,font)
		self.setTextColor(0,QColor(128,128,128))
		self.setFlags(self.flags() & ~(Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled))

class sbTreeWidget(QTreeWidget):
	def __init__(self, parent=None):
		super(sbTreeWidget, self).__init__(parent)
		self.setHeaderHidden(True)
		self.setDragDropMode(QTreeWidget.InternalMove)
		self.setDragEnabled(True)
		self.setDropIndicatorShown(True)
		self.item = False
		self.itemParent = False

	def dropEvent(self,event):
		QTreeWidget.dropEvent(self,event)
		if self.itemParent and self.itemParent.childCount() == 0:
			self.itemParent.addChild(noChild())
		if isinstance(self.item.parent(),treeItemGroup):
			if isinstance(self.item.parent().child(0),noChild):
				self.item.parent().removeChild(self.item.parent().child(0))
			if isinstance(self.item.parent().child(self.item.parent().childCount()-1),noChild):
				self.item.parent().removeChild(self.item.parent().child(self.item.parent().childCount()-1))
		if self.itemParent:
			swParent = self.itemParent.item
		else:
			swParent = form.sb.book
		sw = swParent.items.pop(swParent.items.index(self.item.item))
		if self.item.parent():
			self.item.parent().item.items.insert(self.item.parent().indexOfChild(self.item),sw)
		else:
			form.sb.book.items.insert(form.treeWidget.indexOfTopLevelItem(self.item),sw)
		gridItems = []
		self.gridItems(self.item,gridItems)
		for gridItem in gridItems:
			form.gridWidget.takeItem(form.gridWidget.indexFromItem(gridItem).row())
		self.setCurrentItem(self.item)
		item = self.swItemAbove(self.item)
		if item:
			index = form.gridWidget.indexFromItem(form.items[item]).row()+1
		else:
			index = 0
		gridItems.reverse()
		for gridItem in gridItems:
			form.gridWidget.insertItem(index,gridItem)
		form.gridWidget.update()
		form.sw_display_tree()

	def swItemAbove(self,item):
		nitem = self.itemAbove(item)
		if isinstance(nitem,treeItemGroup):
			if nitem == item.parent() or not self.lastChild(nitem):
				nitem = self.swItemAbove(nitem)
			else:
				nitem = self.lastChild(nitem)
		elif isinstance(nitem,noChild):
			nitem = self.swItemAbove(nitem.parent())
		return nitem

	def lastChild(self,group):
		if group.childCount > 0:
			item = group.child(group.childCount()-1)
			if isinstance(item,treeItemGroup):
				item = self.lastChild(item)
			return item

	def gridItems(self,item,gridItems):
		if isinstance(item,treeItemGroup):
			for i in range(item.childCount()):
				self.gridItems(item.child(i),gridItems)
		else:
			gridItems.append(form.items[item])

	def mousePressEvent(self,event):
		QTreeWidget.mousePressEvent(self,event)
		self.item = self.itemAt(event.pos())
		if self.item:
			self.itemParent = self.item.parent()

class sbGridWidget(QListWidget):
	def __init__(self, parent=None):
		super(sbGridWidget, self).__init__(parent)
		self.setViewMode(QListView.IconMode)
		self.setMovement(QListView.Static)
		self.setResizeMode(QListView.Adjust)

	def update(self):
		if settings.contains('gridHoriz') and settings.value('gridHoriz').toBool():
			if form.sb.book.display['columns']:
				self.setFixedHeight(form.sb.book.display['columns']*17 + self.zHeight)
			else:
				self.setMinimumHeight(0)
				self.setMaximumHeight(0xFFFFFF)
			if form.sb.book.display['rows']:
				self.setFixedWidth(form.sb.book.display['rows']*17 + self.zWidth)
			else:
				self.setMinimumWidth(0)
				self.setMaximumWidth(0xFFFFFF)
			self.setFlow(QListView.TopToBottom)
			self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
			self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
			self.zWidth = 2*self.frameWidth()
			self.zHeight = 2*self.frameWidth() + self.horizontalScrollBar().size().height() + 1
			avail_height = self.size().height() - self.zHeight
			breaks2 = {}
			for item in breaks:
				breaks2[self.row(item)] = item
			for key in sorted(breaks2.iterkeys()):
				if isinstance(self.item(key),gridItemGroup) and (isinstance(self.item(key-1),gridItemBreak) or isinstance(self.item(key-1),gridItemGroup) or key == 0):
					height = 0
				elif isinstance(self.item(key-1),gridItemBreak) or key == 0:
					height = avail_height
				else:
					height = (int((avail_height-self.visualItemRect(self.item(key-1)).top())/17)-1)*17
				breaks2[key].setSizeHint(QSize(17,height))
				self.doItemsLayout()
		else:
			if form.sb.book.display['columns']:
				self.setFixedWidth(form.sb.book.display['columns']*17 + self.zWidth)
			else:
				self.setMinimumWidth(0)
				self.setMaximumWidth(0xFFFFFF)
			if form.sb.book.display['rows']:
				self.setFixedHeight(form.sb.book.display['rows']*17 + self.zHeight)
			else:
				self.setMinimumHeight(0)
				self.setMaximumHeight(0xFFFFFF)
			self.setFlow(QListView.LeftToRight)
			self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
			self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
			self.zWidth = 2*self.frameWidth() + self.verticalScrollBar().size().width() + 1
			self.zHeight = 2*self.frameWidth()
			avail_width = self.size().width() - self.zWidth
			breaks2 = {}
			for item in breaks:
				breaks2[self.row(item)] = item
			for key in sorted(breaks2.iterkeys()):
				if isinstance(self.item(key),gridItemGroup) and (isinstance(self.item(key-1),gridItemBreak) or isinstance(self.item(key-1),gridItemGroup) or key == 0):
					width = 0
				elif isinstance(self.item(key-1),gridItemBreak) or key == 0:
					width = avail_width
				else:
					if self.isLeftToRight():
						width = (int((avail_width-self.visualItemRect(self.item(key-1)).left())/17)-1)*17
					else:
						width = (int(self.visualItemRect(self.item(key-1)).right()/17)-1)*17
				breaks2[key].setSizeHint(QSize(width,17))
				self.doItemsLayout()

	def resizeEvent(self,event):
		QListWidget.resizeEvent(self,event)
		self.update()

class GroupWidget(QGroupBox):
	def __init__(self, item, parent):
		super(GroupWidget, self).__init__(parent)
		
		self.setTitle(_("Group"))
		self.swInfo = InfoWidget(item,self)
		infoScrollArea = QScrollArea()
		infoScrollArea.setWidget(self.swInfo)
		infoScrollArea.setWidgetResizable(True)
		infoScrollArea.setFrameShape(QFrame.NoFrame)
		sbInfoLayout = QVBoxLayout()
		sbInfoLayout.addWidget(infoScrollArea)
		self.setLayout(sbInfoLayout)

class SwatchWidget(QGroupBox):
	def __init__(self, id, parent):
		super(SwatchWidget, self).__init__(parent)

		self.item = form.sb.swatches[id]

		self.swInfo = InfoWidget(self.item,self)
		infoScrollArea = QScrollArea()
		infoScrollArea.setWidget(self.swInfo)
		infoScrollArea.setWidgetResizable(True)
		infoScrollArea.setFrameShape(QFrame.NoFrame)

		if isinstance(self.item, Color):
			self.setTitle(_("Color"))
			self.swatch = ColorWidget(id,self)

		self.swExtra = QTableWidget()
		self.swExtra.setColumnCount(2)
		self.swExtra.horizontalHeader().setStretchLastSection(True)
		self.swExtra.verticalHeader().hide()
		self.swExtra.setHorizontalHeaderLabels([_("Key"),_("Value")])
		self.swExtra.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.butExtra = MenuButton(self)
		self.menuExtra = QMenu()
		self.menuExtra.addAction(_('Add'),self.addExtra)
		self.extraRemoveAction = self.menuExtra.addAction(_('Remove'),self.remExtra)
		self.butExtra.setMenu(self.menuExtra)
		self.extraRemoveAction.setEnabled(False)

		groupBoxExtra = QGroupBox(_("Extra info"))
		boxExtra = QHBoxLayout()
		boxExtra.addWidget(self.swExtra)
		boxExtra.addWidget(self.butExtra,0,Qt.AlignTop)
		groupBoxExtra.setLayout(boxExtra)

		layout = QVBoxLayout()
		layout.addWidget(infoScrollArea)
		layout.addWidget(self.swatch)
		layout.addWidget(groupBoxExtra)
		self.setLayout(layout)

		self.tExtra = []
		row = 0
		for extra in self.item.extra:
			self.swExtra.insertRow(row)
			key = QTableWidgetItem(extra)
			if self.item.extra[extra]:
				val = QTableWidgetItem(self.item.extra[extra])
			else:
				val = QTableWidgetItem()
			self.swExtra.setItem(row, 0, key)
			self.swExtra.setItem(row, 1, val)
			row += 1
			self.tExtra.append([unicode(extra),unicode(self.item.extra[extra])])
			
		self.connect(self.swExtra,
				SIGNAL("cellChanged(int,int)"), self.editExtra)
		self.connect(self.swExtra,
				SIGNAL("cellClicked(int,int)"), self.extra_editable)

	def extra_editable(self):
		self.extraRemoveAction.setEnabled(True)

	def addExtra(self):
		self.swExtra.insertRow(self.swExtra.rowCount())
		if not hasattr(self,"tExtra"):
			self.tExtra = []
		self.tExtra.append([None,None])
		
	def remExtra(self):
		if self.swExtra.item(self.swExtra.currentRow(),0):
			extra = unicode(self.swExtra.item(self.swExtra.currentRow(),0).text())
			del self.item.extra[extra]
		self.swExtra.removeRow(self.swExtra.currentRow())
		self.extraRemoveAction.setEnabled(False)

	def editExtra(self):
		row,col = self.swExtra.currentRow(),self.swExtra.currentColumn()
		if col == 0:
			if self.tExtra[row][0] in self.item.extra:
				del self.item.extra[self.tExtra[row][0]]
			self.tExtra[row][0] = unicode(self.swExtra.item(row,col).text())
		else:
			self.tExtra[row][0] = unicode(self.swExtra.item(row,col).text())
			self.tExtra[row][col] = unicode(self.swExtra.item(row,col).text())
		if self.swExtra.item(row,0):
			if self.swExtra.item(row,1):
				self.item.extra[unicode(self.swExtra.item(row,0).text())] = unicode(self.swExtra.item(row,1).text())
			else:
				self.item.extra[unicode(self.swExtra.item(row,0).text())] = None

class ColorWidget(QWidget):
	def __init__(self, id, parent):
		super(ColorWidget, self).__init__(parent)

		self.item = form.sb.swatches[id]

		self.sample = QLabel()
		self.sample.setMinimumHeight(30)
		self.swSpot = QCheckBox(_("Spot"))
		self.swValues = QTabWidget()
		self.butVal = MenuButton(self.swValues)
		cornLay = QVBoxLayout()
		cornLay.setContentsMargins(20,0,0,20)
		cornLay.addWidget(self.butVal)
		cornWid = QWidget()
		cornWid.setLayout(cornLay)
		cornWid.setMinimumSize(12,12)
		self.menuVal = QMenu()
		self.menuValModl = self.menuVal.addMenu(_('Add'))
		for model in models:
			self.menuValModl.addAction(model,self.addVal)
		self.menuValModlN = self.menuValModl.addMenu('nCLR')
		for n in range(15):
			self.menuValModlN.addAction(("%X" % (n+1))+'CLR',self.addVal)
		self.delValAction = self.menuVal.addAction(_('Remove'),self.delVal)
		self.delValAction.setEnabled(False)
		self.butVal.setMenu(self.menuVal)
		self.swValues.setCornerWidget(cornWid)
		self.swValues.setMovable(True)

		layout = QVBoxLayout()
		layout.setContentsMargins(0,0,0,0)
		layout.addWidget(self.sample)
		layout.addWidget(self.swSpot)
		layout.addWidget(self.swValues)
		self.setLayout(layout)

		if 'spot' in self.item.usage:
			self.swSpot.setChecked(True)
		self.val = {}
		if len(self.item.values) > 0:
			self.delValAction.setEnabled(True)
			prof_out = str(settings.value("mntrProfile").toString()) or False
			r,g,b = self.item.toRGB8(prof_out)
			self.sample.setStyleSheet("QWidget { background-color: rgb("+str(r)+","+str(g)+","+str(b)+") }")
			for space in self.item.values:
				self.add_val_tab(space,self.item.values[space])
		self.def_current_sp()

		# Actions
		self.connect(self.swSpot,
				SIGNAL("stateChanged(int)"), self.edit)
		self.connect(self.swValues,
				SIGNAL("currentChanged(int)"), self.def_current_sp)
		self.connect(self.swValues.tabBar(),
				SIGNAL("tabMoved(int,int)"), self.tab_moved)

	def tab_moved(self,tfrom,tto):
		combo = self.swValues.widget(tfrom).findChild(QComboBox)
		if combo and combo.currentIndex() > 0:
			space = unicode(combo.itemData(combo.currentIndex()).toString())
		else:
			space = False
		key = (str(self.swValues.tabText(tfrom)),space)
		val = self.item.values.pop(key)
		self.item.values.insert(tfrom,key,val)
		self.set_preview()

	def add_val_tab(self,space,values):
		profile = space[1]
		model = space[0]
		valWidget = QWidget()
		grid = QGridLayout()
		count = 0
		if model in models:
			for elem in models[model]:
				val = QLineEdit()
				self.val[val] = (space,count)
				self.connect(val,
						SIGNAL("textEdited(QString)"), self.valedit)
				grid.addWidget(QLabel(elem[0]+":"), count, 0)
				if elem[1] == 0:
					grid.addWidget(val, count, 1)
					val.setText(str(round(values[count],2)))
				elif elem[1] == 1:
					grid.addWidget(val, count, 1)
					grid.addWidget(QLabel("%"), count, 2)
					val.setText(str(round(values[count]*100,2)))
				if elem[1] == 2:
					grid.addWidget(val, count, 1)
					grid.addWidget(QLabel(u"°"), count, 2)
					val.setText(str(round(values[count]*360,2)))
				count += 1
		else:
			self.val[space] = {}
			for ink in values:
				val = QLineEdit()
				self.val[val] = (space,count)
				grid.addWidget(val, count, 1)
				grid.addWidget(QLabel("%"), count, 2)
				val.setText(str(round(values[count]*100,2)))
				count += 1
				
		valWidget.setLayout(grid)
		valScrollArea = QScrollArea()
		valScrollArea.setWidget(valWidget)
		valScrollArea.setWidgetResizable(True)
		valScrollArea.setFrameShape(QFrame.NoFrame)
		
		spaceWidget = QWidget()
		spaceLayout = QVBoxLayout()
		spaceLayout.addWidget(valScrollArea)

		if model not in ('Lab','XYZ','sRGB'):
			spaceLayout.addWidget(QLabel(_("Profile")))
			if model in ('RGB','HSL','HSV','YIQ','CMY'):
				modellist = 'RGB'
			else:
				modellist = model
			profCombo = QComboBox()
			profCombo.addItem('')
			for prof in sorted(self.getProfList(modellist),cmp=lambda x,y: cmp(x[0].lower(), y[0].lower())):
				profCombo.addItem(prof[0],QVariant(prof[1]))
			if profile in form.sb.profiles:
				profCombo.setCurrentIndex(profCombo.findData(QVariant(profile)))
			self.connect(profCombo,
					SIGNAL("currentIndexChanged(int)"), self.change_profile)
			spaceLayout.addWidget(profCombo)
		spaceWidget.setLayout(spaceLayout)

		self.swValues.addTab(spaceWidget,model)
		self.set_preview()

	def edit(self):
		if self.sender() == self.swSpot:
			if self.swSpot.isChecked():
				self.item.usage.append('spot')
			else:
				self.item.usage.remove('spot')
			swupdate(self.item.info.identifier)

	def set_preview(self):
		prof_out = str(settings.value("mntrProfile").toString()) or False
		if self.item.toRGB8(prof_out):
			r,g,b = self.item.toRGB8(prof_out)
			self.sample.setStyleSheet("QWidget { background-color: rgb("+str(r)+","+str(g)+","+str(b)+") }")
		else:
			self.sample.setStyleSheet("")
		swupdate(self.item.info.identifier)

	def valedit(self):
		sender = self.val[self.sender()]
		model = sender[0][0]
		if model in models:
			if models[model][sender[1]][1] == 0:
				self.item.values[sender[0]][sender[1]] = eval(str(self.sender().text()))
			elif models[model][sender[1]][1] == 1:
				self.item.values[sender[0]][sender[1]] = eval(str(self.sender().text()))/100
			elif models[model][sender[1]][1] == 2:
				self.item.values[sender[0]][sender[1]] = eval(str(self.sender().text()))/360
		else:
			self.item.values[sender[0]][sender[1]] = eval(str(self.sender().text()))
		self.set_preview()

	def def_current_sp(self):
		global current_sp
		if self.swValues.count() > 0:
			model = str(self.swValues.tabText(self.swValues.currentIndex()))
			combo = self.swValues.currentWidget().findChild(QComboBox)
			if combo and combo.currentIndex() > 0:
				current_sp = (model,unicode(combo.itemData(combo.currentIndex()).toString()))
			else:
				current_sp = (model,False)
		else:
			current_sp = False

	def change_profile(self):
		global current_sp
		value = self.item.values[current_sp]
		del self.item.values[current_sp]
		self.def_current_sp()
		self.item.values[current_sp] = value
		fields = self.swValues.currentWidget().findChildren(QLineEdit)
		for field in fields:
			self.val[field] = (current_sp,self.val[field][1])
		self.set_preview()

	def delVal(self):
		global current_sp
		del self.item.values[current_sp]
		self.swValues.removeTab(self.swValues.currentIndex())
		self.set_preview()

	def addVal(self):
		model = str(self.sender().text())
		if not hasattr(self,'val'):
			self.val = {}
		self.item.values[(model,False)] = []
		if model in models:
			for elem in models[model]:
				self.item.values[(model,False)].append(0)
		elif len(model) == 4 and model[1:] == 'CLR':
			for ink in range(int(model[0],16)):
				self.item.values[(model,False)].append(0)
		self.add_val_tab((model,False),self.item.values[(model,False)])
		self.swValues.setCurrentIndex(self.swValues.count()-1)
		self.def_current_sp()
		self.delValAction.setEnabled(True)
		self.set_preview()
		
	def getProfList(self,model):
		profList = []
		if model in form.profiles:
			for prof in form.profiles[model]:
				profList.append((form.sb.profiles[prof].info['desc'][0],prof))
		return profList

class SettingsDlg(QDialog):
	def __init__(self, parent=None):
		super(SettingsDlg, self).__init__(parent)
		
		self.mntrProfile = False
		self.cmykProfile = False
		self.profiles = []
		self.listProfiles()
		
		
		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
		
		self.mntrCombo = QComboBox()
		self.cmykCombo = QComboBox()
		self.mntrCombo.addItem(_('sRGB built-in'))
		self.cmykCombo.addItem('Fogra27L')
		self.mntrCombo.insertSeparator(self.mntrCombo.count())
		self.cmykCombo.insertSeparator(self.cmykCombo.count())
		for profile in sorted(self.profiles,cmp=lambda x,y: cmp(x[0].lower(), y[0].lower())):
			if profile[2] == "mntr" and profile[3] == 'RGB ':
				self.mntrCombo.addItem(profile[0],QVariant(profile[1]))
			if profile[3] == 'CMYK':
				self.cmykCombo.addItem(profile[0],QVariant(profile[1]))
		self.mntrCombo.insertSeparator(self.mntrCombo.count())
		self.cmykCombo.insertSeparator(self.cmykCombo.count())
		if settings.contains("mntrProfile") and self.mntrCombo.findData(settings.value("mntrProfile")) < 0:
			prof = ICCprofile(settings.value("mntrProfile").toString()).info
			self.mntrCombo.addItem(prof['desc'][prof['desc'].keys()[0]],settings.value("mntrProfile"))
		if settings.contains("cmykProfile") and self.cmykCombo.findData(settings.value("cmykProfile")) < 0:
			prof = ICCprofile(settings.value("cmykProfile").toString()).info
			self.cmykCombo.addItem(prof['desc'][prof['desc'].keys()[0]],settings.value("cmykProfile"))
		self.mntrCombo.addItem(_("Other..."))
		self.cmykCombo.addItem(_("Other..."))
		
		profilesBox = QGroupBox(_("Color profiles"))
		profilesLayout = QVBoxLayout()
		profilesLayout.addWidget(QLabel(_("Monitor Profile")))
		profilesLayout.addWidget(self.mntrCombo)
		profilesLayout.addWidget(QLabel(_("Default CMYK Profile")))
		profilesLayout.addWidget(self.cmykCombo)
		profilesBox.setLayout(profilesLayout)

		self.RecFilesSpin = QSpinBox()
		self.RecFilesSpin.setRange(0, 12)

		gRecFiles = QGroupBox(_("Recent files"))
		RecFiles = QHBoxLayout()
		RecFiles.addWidget(QLabel(_("Number of files displayed:")))
		RecFiles.addWidget(self.RecFilesSpin)
		gRecFiles.setLayout(RecFiles)

		self.LangCombo = QComboBox()
		self.LangCombo.addItem(_('(default)'))
		for lang in sorted(availables_lang):
			self.LangCombo.addItem(availables_lang[lang],QVariant(lang))

		gLang = QGroupBox(_("Application language"))
		Lang = QHBoxLayout()
		Lang.addWidget(self.LangCombo)
		gLang.setLayout(Lang)

		sett = QVBoxLayout()
		sett.addWidget(profilesBox)
		sett.addWidget(gRecFiles)
		sett.addWidget(gLang)
		sett.addWidget(buttonBox)
		self.setLayout(sett)

		if settings.contains("mntrProfile"):
			self.mntrProfile = settings.value("mntrProfile").toString()
			self.mntrCombo.setCurrentIndex(self.mntrCombo.findData(self.mntrProfile))
		else:
			self.mntrCombo.setCurrentIndex(0)
		if settings.contains("CMYKProfile"):
			self.cmykProfile = settings.value("cmykProfile").toString()
			self.cmykCombo.setCurrentIndex(self.cmykCombo.findData(self.cmykProfile))
		else:
			self.cmykCombo.setCurrentIndex(0)
		self.RecFilesSpin.setValue(settings.value("MaxRecentFiles").toInt()[0])
		self.lang = False
		if settings.contains("Language"):
			self.lang = settings.value("Language")
			self.LangCombo.setCurrentIndex(self.LangCombo.findData(self.lang))

		self.connect(buttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
		self.connect(buttonBox, SIGNAL("rejected()"), self, SLOT("reject()"))
		self.connect(self.mntrCombo, SIGNAL("currentIndexChanged(int)"), self.setProfile)
		self.connect(self.cmykCombo, SIGNAL("currentIndexChanged(int)"), self.setProfile)
		self.connect(self.LangCombo, SIGNAL("currentIndexChanged(int)"), self.setLang)
		self.setWindowTitle(_("Settings"))

	def returnDisProf(self):
		if hasattr(self,'mntrProfile'):
			return self.mntrProfile

	def returnCMYKProf(self):
		if hasattr(self,'cmykProfile'):
			return self.cmykProfile

	def setRGBFile(self):
		fname = QFileDialog.getOpenFileName(self, _("Choose file"), QDir.homePath(),_("ICC profiles (*.icc *.icm)"))
		if fname:
			profile = icc.ICCprofile(fname)
			if profile.info['class'] == "mntr" and profile.info['space'] == 'RGB ':
				self.mntrCombo.setCurrentIndex(0)
				self.mntrCombo.insertItem(self.mntrCombo.count()-1,profile.info['desc'][profile.info['desc'].keys()[0]],QVariant(fname))
				self.mntrCombo.setCurrentIndex(self.mntrCombo.findData(fname))
			else:
				QMessageBox.critical(self, _('Error'), _("This isn't a RGB monitor profile"))
				if self.mntrProfile:
					self.mntrCombo.setCurrentIndex(self.mntrCombo.findData(self.mntrProfile))
				else:
					self.mntrCombo.setCurrentIndex(0)
		
	def setCMYKFile(self):
		fname = QFileDialog.getOpenFileName(self, _("Choose file"), QDir.homePath(),_("ICC profiles (*.icc *.icm)"))
		if fname:
			profile = icc.ICCprofile(fname)
			if profile.info['space'] == 'CMYK':
				self.cmykCombo.setCurrentIndex(0)
				self.cmykCombo.insertItem(self.cmykCombo.count()-1,profile.info['desc'][profile.info['desc'].keys()[0]],QVariant(fname))
				self.cmykCombo.setCurrentIndex(self.cmykCombo.findData(fname))
			else:
				QMessageBox.critical(self, _('Error'), _("This isn't a CMYK profile"))
				self.cmykCombo.setCurrentIndex(self.cmykCombo.findData(self.cmykProfile) or 0)
		
	def setLang(self,index):
		if index > 0:
			self.lang = self.sender().itemData(index)
		else:
			self.lang = False

	def setProfile(self,index):
		if self.sender() == self.mntrCombo:
			if index == self.mntrCombo.count()-1:
				self.setRGBFile()
			elif index > 0:
				self.mntrProfile = self.sender().itemData(index)
			else:
				self.mntrProfile = False

	def listProfiles(self):
		def listprof(dir):
			for s in os.listdir(dir):
				file = os.path.join(dir,s)
				if os.path.isdir(file) and s not in ('.','..'):
					listprof(file)
				else:
					if os.path.isfile(file) and os.path.splitext(os.path.basename(file))[1].lower()[1:] in ('icc','icm','3cc') and not os.path.islink(file):
						try:
							prof = ICCprofile(file).info
							self.profiles.append((prof['desc'][prof['desc'].keys()[0]],file,prof['class'],prof['space']))
						except BadICCprofile:
							pass
		if os.name == 'posix':
			profdirs = [unicode(QDir.homePath())+"/.color/icc","/usr/share/color/icc","/usr/local/share/color/icc"]
		elif os.name == 'nt':
			profdirs = ["C:\\Windows\\System\\Color","C:\\Winnt\\system32\\spool\\drivers\\color","C:\\Windows\\system32\\spool\\drivers\\color"]
		elif os.name == 'mac':
			profdirs = ["/Network/Library/ColorSync/Profiles","/System/Library/Colorsync/Profiles","/Library/ColorSync/Profiles",unicode(QDir.homePath())+"/Library/ColorSync/Profiles"]
		else:
			profdirs = []
		for profdir in profdirs:
			if os.path.exists(profdir):
				listprof(profdir)

class webOpenDlg(QDialog):
	def __init__(self, parent=None):
		super(webOpenDlg, self).__init__(parent)

		self.svc = False
		self.id = False

		self.webSvcStack = QStackedWidget()
		self.webSvcList = QListWidget(self)
		palette = self.webSvcList.palette()
		palette.setColor(QPalette.Base,Qt.transparent)
		self.webSvcList.setPalette(palette)
		self.webSvcList.setFrameShape(QFrame.NoFrame)
		self.about = QLabel()
		self.about.setWordWrap(True)
		self.about.setMargin(10)
		self.about.setFrameShape(QFrame.StyledPanel)

		self.webWidgets = {}

		for svc in websvc.list:
			current_svc = eval('websvc.'+svc+'()')
			if current_svc.type == 'list':
				webWidget = webWidgetList(svc,self)
			self.webSvcStack.addWidget(webWidget)
			self.webWidgets[svc] = (webWidget,current_svc.about)
			listItem = QListWidgetItem(websvc.list[svc],self.webSvcList)
			listItem.setData(Qt.UserRole,svc)
			icon = (dirpath(__file__) or '.')+'/swatchbook/websvc/'+svc+'.png'
			if(QFile.exists(icon)):
				listItem.setIcon(QIcon(icon))
		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
		self.webSvcList.sortItems()
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
		webl.addWidget(self.about,0,1,Qt.AlignTop)
		webl.addWidget(buttonBox,1,0,1,3)
		self.setLayout(webl)

		self.setWindowTitle(_("Open from web"))
		self.connect(self.webSvcList,
				SIGNAL("itemSelectionChanged()"), self.changeTab)
		self.connect(buttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
		self.connect(buttonBox, SIGNAL("rejected()"), self, SLOT("reject()"))

	def changeTab(self):
		self.svc = str(self.webSvcList.selectedItems()[0].data(Qt.UserRole).toString())
		self.webSvcStack.setCurrentWidget(self.webWidgets[self.svc][0])
		self.about.setText(self.webWidgets[self.svc][1])
		self.webSvcStack.currentWidget().load()
		self.webSvcList.setCurrentItem(self.webSvcList.selectedItems()[0],QItemSelectionModel.Current)

class webWidgetList(QTreeWidget):
	def __init__(self, svc, parent=None):
		super(webWidgetList, self).__init__(parent)
		self.loaded = False
		self.parent = parent
		self.svc = eval('websvc.'+svc+'()')
		self.setHeaderHidden(True)
		self.setColumnHidden(1,True)
		self.setFrameShape(QFrame.NoFrame)
		self.connect(self,
				SIGNAL("itemSelectionChanged()"), self.activate)
		self.connect(self,
				SIGNAL("itemExpanded(QTreeWidgetItem *)"), self.nextLevel)

	def activate(self):
		if self.selectedItems():
			treeItem = self.selectedItems()[0]
			self.parent.id = unicode(treeItem.text(1))

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

	if len(sys.argv) > 1:
		form = MainWindow(sys.argv[1])
	else:
		form = MainWindow()
	form.show()
	form.update()
	form.dispPane()

	app.exec_()
