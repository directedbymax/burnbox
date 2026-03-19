import sys
import os
from datetime import datetime, timedelta

from PySide6 import QtTest


# Force tests to look for resources in the source code tree
sys.burnbox_dev_mode = True

# Let BurnBox know the tests are running, to avoid colliding with settings files
sys.burnbox_test_mode = True


@staticmethod
def qWait(t, qtapp):
    end = datetime.now() + timedelta(milliseconds=t)
    while datetime.now() < end:
        qtapp.processEvents()


# Monkeypatch qWait, although PySide6 has it
# https://stackoverflow.com/questions/17960159/qwait-analogue-in-pyside
QtTest.QTest.qWait = qWait

# Allow importing burnbox_cli from the source tree
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "cli",
    ),
)

# Create common and qtapp singletons
from burnbox_cli.common import Common
from burnbox import Application

common = Common(verbose=True)
qtapp = Application(common)

# Attach them to sys, so GuiBaseTest can retrieve them
sys.burnbox_common = common
sys.burnbox_qtapp = qtapp
