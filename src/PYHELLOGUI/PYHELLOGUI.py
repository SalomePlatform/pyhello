import qt
from qt import *
import traceback

# Global variable to store Salome Workspace
WORKSPACE=None

import SalomePyQt
# Communication with Salome : desktop, signal and slots
sgPyQt=SalomePyQt.SalomePyQt()
desktop=sgPyQt.getDesktop()

# LifeCycle and component PYHELLO
import salome
lifecycle = salome.lcc
import PYHELLO_ORB
pyhello=lifecycle.FindOrLoadComponent("FactoryServerPy", "PYHELLO")

def setWorkSpace(pyws):
    global WORKSPACE
    print "setWorkSpace: ",pyws
    WORKSPACE=pyws

def OnGUIEvent(commandID) :
    print "PYHELLOGUI::OnGUIEvent::commandID,WORKSPACE= ",commandID,WORKSPACE
    if dict_command.has_key(commandID):
       try:
          r=dict_command[commandID](WORKSPACE)
          print r
       except:
          traceback.print_exc()
    else:
       print "Pas de commande associée a : ",commandID

def setSettings():
    print "setSettings"

def activeStudyChanged(ID):
    print "activeStudyChanged: ",ID

def definePopup(theContext, theObject, theParent):
    print "PYHELLOGUI --- definePopup: ",theContext,theObject,theParent

def customPopup(popup, theContext, theObject, theParent):
    print "PYHELLOGUI --- customPopup: ",theContext,theObject,theParent

class MyDialog(qt.QDialog):
      def __init__(self,parent=None, name=None, modal=0, flags=0):
          qt.QDialog.__init__(self,parent, name, modal, flags)
          self.vb = qt.QVBoxLayout(self, 8)
          self.vb.setAutoAdd(1)
          self.hb0 = qt.QHBox(self)
          label=QLabel("Prenom",self.hb0)
          self.entry=QLineEdit( self.hb0)

          self.hb = qt.QHBox(self)
          c = qt.QPushButton("OK", self.hb)
          self.connect(c, qt.SIGNAL('clicked()'), self, SLOT('accept()'))
          d = qt.QPushButton("CANCEL", self.hb)
          self.connect(d, qt.SIGNAL('clicked()'), self, SLOT('reject()'))

def ExecPYHELLO(ws):
    # Modal dialog, parent desktop
    w=MyDialog(desktop,"Name",1)
    # Wait answer
    r=w.exec_loop()
    if r == QDialog.Accepted:
       name=str(w.entry.text())
       banner=pyhello.makeBanner(name)
       QMessageBox.about(desktop,'Salome Example',banner)
    else:
       print "CANCEL"

dict_command={
               941:ExecPYHELLO,
             }
