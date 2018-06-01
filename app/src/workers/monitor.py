"""
Monitors to gather data as the game runs
"""
import os
import sys
import traceback

from PyQt5.QtCore import (
    QFile, QFileSystemWatcher, QObject, QRunnable, pyqtSlot, pyqtSignal
)

from ..utils.parser import ClientLogParser

# TODO Grab client path from user
CLIENT_PATH = "C:\\Program Files (x86)\\Grinding Gear Games\\Path of Exile"
LOG_PATH = os.path.join(CLIENT_PATH + "logs/Client.txt")


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    '''
    error = pyqtSignal()
    level_up_signal = pyqtSignal(dict)
    area_enter_signal = pyqtSignal(dict)


class ClientLogMonitor(QRunnable):
    """
    Worker thread to monitor the game client log file
    """
    def __init__(self):
        super(ClientLogMonitor, self).__init__()

        self.watcher = QFileSystemWatcher(self)
        self.parser = ClientLogParser()
        self.log_file = None

    @pyqtSlot()
    def run(self):
        """
        Runs the log monitor worker
        """
        self.log_file = QFile(LOG_PATH)

        # check if the log file exists
        if self.log_file.exists():
            # Try to open pen log file
            if self.log_file.open(QFile.ReadOnly):
                # Go to the end of the file
                self.log_file.seek(self.log_file.size())
                # Connect the read handler to file change signal
                self.watcher.addPath(LOG_PATH)
                self.watcher.fileChanged.connect(self.read)
        else:
            self.signals.error.emit()

        return

    def read(self):
        """
        Reads the latest line in the log file
        """
        if self.log_file.isOpen():
            try:
                line = self.log_file.readLine()
            except EOFError:
                exctype, val = sys.exc_info()[:2]
                self.signals.error.emit((exctype, val, traceback.format_exc()))
                return
        else:
            self.signals.error.emit("File not open")
            return

        clean_line = line.strip()

        self.parser.parse_log(clean_line)

        if self.parser.message_type is 'area_enter':
            self.signals.area_enter_signal.emit(self.parser.message_data)
        elif self.parser.message_type is 'level_up':
            self.signals.level_up_signal.emit(self.parser.message_data)
        elif self.parser.message_type is 'skill_up':
            pass

        return
