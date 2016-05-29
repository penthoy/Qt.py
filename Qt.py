"""Map all bindings to PySide2

This module replaces itself with the most desirable binding.

Resolution order:
    - PySide2
    - PyQt5
    - PySide
    - PyQt4

Usage:
    >>> import sys
    >>> from Qt import QtWidgets
    >>> app = QtWidgets.QApplication(sys.argv)
    >>> button = QtWidgets.QPushButton("Hello World")
    >>> button.show()
    >>> app.exec_()

"""

import sys


def _pyqt5():
    import PyQt5.Qt

    # Remap
    PyQt5.QtCore.Signal = PyQt5.QtCore.pyqtSignal
    PyQt5.QtCore.Slot = PyQt5.QtCore.pyqtSlot
    PyQt5.QtCore.Property = PyQt5.QtCore.pyqtProperty

    # Add
    PyQt5.__binding__ = "PyQt5"

    return PyQt5


def _pyqt4():
    import PyQt4.Qt

    # Remap
    PyQt4.QtWidgets = PyQt4.QtGui

    PyQt4.QtCore.Signal = PyQt4.QtCore.pyqtSignal
    PyQt4.QtCore.Slot = PyQt4.QtCore.pyqtSlot
    PyQt4.QtCore.Property = PyQt4.QtCore.pyqtProperty

    # Add
    PyQt4.__binding__ = "PyQt4"

    return PyQt4


def _pyside2():
    import PySide2

    # Add
    PySide2.__binding__ = "PySide2"

    return PySide2


def _pyside():
    import PySide

    # Remap
    PySide.QtWidgets = PySide.QtGui

    PySide.QtCore.QSortFilterProxyModel = PySide.QtGui.QSortFilterProxyModel

    # Add
    PySide.__binding__ = "PySide"

    return PySide


def _init():
    # Try loading each binding in turn
    for binding in (_pyside2,
                    _pyqt5,
                    _pyside,
                    _pyqt4):
        try:
            sys.modules["Qt"] = binding()
            return
        except ImportError:
            continue

    # If not binding were found, throw this error
    raise ImportError("No Qt binding were found.")

_init()