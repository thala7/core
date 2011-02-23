from PyQt4 import QtCore, QtGui
from item import *

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, node, widget, parent=None):
        super(TreeModel, self).__init__(parent)

        self.widget = widget
        self.stack = QtGui.QStackedLayout(widget)
        self.rootItem = NullItem(self, name="Name", var=None, value="Value", type="Type")
        self.read(node)

    def clicked(self, item):
        self.stack.setCurrentWidget(item.widget)
        item.widget.show()

    def layoutChange(self):
        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()

    def dataChange(self, index):
        self.dataChanged.emit(index, index)

    def treeChange(self):
        self.modelReset.emit()

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def setData(self, index, value, role):
      if not index.isValid():
        return False
      #elif role != QtCore.Qt.DisplayRole:
      #  print "setData elif" 
      #  return False
      else:
        item = index.internalPointer()
        item.setData(value)
        return True

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        if index.column() == 1:
          return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        else:
          return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            i = self.createIndex(row, column, childItem)
            childItem.index = i
            return i
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        i = self.createIndex(parentItem.row(), 0, parentItem)
        parentItem.inxed = i
        return i

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()
      
    def hasChildren(self, index):
        item = index.internalPointer()
        if not hasattr(item, "childCount"):
            return True
        return item.childCount() > 0
      
    def read(self, node):
      def readItem(node, parent):
        name = node.getAttribute("name")
        var = node.getAttribute("var")
        type = node.getAttribute("type")
        range = node.getAttribute("range")
        default = node.getAttribute("default")
        value = node.getAttribute("value")
        if not value or value == "":
          value = default
        hint = node.getAttribute("hint")
        if type == "int":
            item = IntegerItem(self, name, var, value, type, range, default, hint, parent)
        elif type == "bool":
            item = BooleanItem(self, name, var, value, type, range, default, hint, parent)
        else:
            item = NullItem(self, name, var, value, type, range, default, hint, parent)

        for cnode in node.childNodes:
          if cnode.nodeName == "option":
            citem = readItem(cnode, item)
        parent.appendChild(item)
        self.stack.addWidget(item.widget)
        return item
        
      item = readItem(node, self.rootItem)
    
    def save(self):
      # We don't want to save the rootItem
      return self.rootItem.save()

    def load(self, data):
      # We have to think about the rootItem "Name":
      self.rootItem.load({"Name":data})
 