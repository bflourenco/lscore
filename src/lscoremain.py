import gettext
import sys
import os

gettext.bindtextdomain('lscore', 'lscore/locales')
gettext.textdomain('lscore')
lscore_dir = os.getcwd
if lscore_dir not in sys.path:
	sys.path.append(lscore_dir)
from lscore.gui.mainwindow import MainWindow

MainWindow()
