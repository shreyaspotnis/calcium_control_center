from PyQt4 import QtGui, QtCore, uic
from pyqtgraph.dockarea import DockArea, Dock
import os
# from widgets.BlankWidget import BlankWidget
from streamviewer.widgets.StreamViewer import StreamViewer


class MainWindow(QtGui.QMainWindow):
    """The only window of the application."""

    def __init__(self, settings):
        super(MainWindow, self).__init__()
        self.settings = settings

        self.setupUi()

        self.dock_area = DockArea()
        self.setCentralWidget(self.dock_area)

        self.createDocks()

        self.loadSettings()

    def setupUi(self):
        pass

    def createDocks(self):
        self.wa1000_widget = StreamViewer(self.settings, 'wa1000-calcium', self)
        self.wa1000_widget_dock = Dock('wa1000-calcium',
                                   widget=self.wa1000_widget)
        self.dock_area.addDock(self.wa1000_widget_dock)

        self.temp3_widget = StreamViewer(self.settings, 'cavity_v3_temp', self)
        self.temp3_widget_dock = Dock('cavity_v3_temp',
                                   widget=self.temp3_widget)
        self.dock_area.addDock(self.temp3_widget_dock)

        self.peak_tracker_widget = StreamViewer(self.settings, 'peak_tracker',
                                                self)
        self.peak_tracker_dock = Dock('peak_tracker',
                                       widget=self.peak_tracker_widget)
        self.dock_area.addDock(self.peak_tracker_dock)




    def loadSettings(self):
        """Load window state from self.settings"""

        self.settings.beginGroup('mainwindow')
        geometry = self.settings.value('geometry').toByteArray()
        state = self.settings.value('windowstate').toByteArray()
        dock_string = str(self.settings.value('dockstate').toString())
        if dock_string is not "":
            dock_state = eval(dock_string)
            self.dock_area.restoreState(dock_state)
        self.settings.endGroup()

        self.restoreGeometry(geometry)
        self.restoreState(state)

    def saveSettings(self):
        """Save window state to self.settings."""
        self.settings.beginGroup('mainwindow')
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('windowstate', self.saveState())
        dock_state = self.dock_area.saveState()
        # dock_state returned here is a python dictionary. Coundn't find a good
        # way to save dicts in QSettings, hence just using representation
        # of it.
        self.settings.setValue('dockstate', repr(dock_state))
        self.settings.endGroup()

    def closeEvent(self, event):
        self.wa1000_widget.saveSettings()
        self.temp3_widget.saveSettings()
        self.peak_tracker_widget.saveSettings()
        self.saveSettings()
