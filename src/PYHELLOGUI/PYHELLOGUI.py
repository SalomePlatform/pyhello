#  Copyright (C) 2005  CEA/DEN, EDF R&D
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#
from qt import *
import traceback

from omniORB import CORBA
from SALOME_NamingServicePy import *
from LifeCycleCORBA import *
import SALOMEDS
import SALOMEDS_Attributes_idl

################################################
# module name
__MODULE_NAME__ = "PYHELLO"
__MODULE_ID__   = 1000
__OBJECT_ID__   = 1010
################################################

# Get SALOME PyQt interface
import SalomePyQt
sgPyQt=SalomePyQt.SalomePyQt()

# Get SALOME Swig interface
import libSALOME_Swig
sg = libSALOME_Swig.SALOMEGUI_Swig()

################################################

# init ORB
orb = CORBA.ORB_init( [''], CORBA.ORB_ID )

# create naming service instance
naming_service = SALOME_NamingServicePy_i( orb )

# create life cycle CORBA instance
lcc = LifeCycleCORBA( orb )

# get study manager
obj = naming_service.Resolve( '/myStudyManager' )
studyManager = obj._narrow( SALOMEDS.StudyManager )

################################################
# Internal methods

# --- get PYHELLO engine ---
def _getEngine():
    import PYHELLO_ORB
    engine = lcc.FindOrLoadComponent( "FactoryServerPy", __MODULE_NAME__ )
    return engine

# --- get active study ---
def _getStudy():
    studyId = sgPyQt.getStudyId()
    study = studyManager.GetStudyByID( studyId )
    return study
    
# --- returns 1 if object has children ---
def _hasChildren( sobj ):
    if sobj:
        study = _getStudy()
        iter  = study.NewChildIterator( sobj )
        while iter.More():
            name = iter.Value().GetName()
            if name:
                return 1
            iter.Next()
    return 0

# --- finds or creates component object ---
def _findOrCreateComponent():
    study = _getStudy()
    father = study.FindComponent( __MODULE_NAME__ )
    if father is None:
        builder = study.NewBuilder()
        father = builder.NewComponent( __MODULE_NAME__ )
        attr = builder.FindOrCreateAttribute( father, "AttributeName" )
        attr.SetValue( __MODULE_NAME__ )
        attr = builder.FindOrCreateAttribute( father, "AttributeLocalID" )
        attr.SetValue( __MODULE_ID__ )
        try:
            ### The following line is commented because it causes crashes ! ###
            ### builder.DefineComponentInstance( father, _getEngine() )
            pass
        except:
            pass
    return father
    
################################################
# Callback functions

# set workspace (obsolete method, not used)
def setWorkSpace( pyws ):
    print "PYHELLOGUI::setWorkSpace : ", pyws
    pass

# called when module is activated
def setSettings():
    print "PYHELLOGUI::setSettings"
    pass

# called when active study is changed
def activeStudyChanged( studyID ):
    print "PYHELLOGUI::activeStudyChanged: study ID =", studyID
    pass

# define popup menu
def definePopup( context, object, parent ):
    object = ""
    parent = ""

    study = _getStudy()
    if sg.SelectedCount() == 1:
        entry = sg.getSelected( 0 )
        if entry != '':
            sobj = study.FindObjectID( entry )
            if sobj is not None:
                test, anAttr = sobj.FindAttribute( "AttributeLocalID" )
                if test :
                    id = anAttr._narrow( SALOMEDS.AttributeLocalID ).Value()
                    if ( id >= 0 ):
                        object = str( id )
    print "PYHELLOGUI::definePopup :", context, object, parent
    return context, object, parent

# customize popup menu
def customPopup( popup, context, object, parent ):
    print "PYHELLOGUI::customPopup :", context, object, parent
    try:
        id = int( object )
        if id == __MODULE_ID__:
            study = _getStudy()
            if sg.SelectedCount() == 1:
                entry = sg.getSelected( 0 )
                if entry != '':
                    sobj = study.FindObjectID( entry )
                    if sobj and not _hasChildren( sobj ):
                        popup.removeItem( 951 ) # remove 'Delete All' command
    except:
        pass
    pass

# process GUI action
def OnGUIEvent(commandID) :
    print "PYHELLOGUI::OnGUIEvent : commandID =",commandID
    if dict_command.has_key( commandID ):
        try:
            dict_command[commandID]()
        except:
            traceback.print_exc()
    else:
       print "The command is not implemented: ",commandID

################################################
# GUI actions implementation

# ----------------------- #
# Sample dialog box
# ----------------------- #
class MyDialog( QDialog ):
    # constructor
    def __init__( self, parent = None, modal = 0):
        QDialog.__init__( self, parent, "MyDialog", modal )
        self.setCaption( "HELLO!" )
        vb = QVBoxLayout( self, 8 )
        vb.setAutoAdd( 1 )
        hb0 = QHBox( self )
        label = QLabel( "Prenom: ", hb0 )
        self.entry = QLineEdit( hb0 )
        self.entry.setMinimumWidth( 200 )
        
        hb1 = QHBox( self )
        bOk = QPushButton( "&OK", hb1 )
        self.connect( bOk, SIGNAL( 'clicked()' ), self, SLOT( 'accept()' ) )
        dummy = QWidget( hb1 )
        bCancel = QPushButton( "&Cancel", hb1 )
        self.connect( bCancel, SIGNAL( 'clicked()' ), self, SLOT( 'close()' ) )
        hb1.setStretchFactor( dummy, 10 )
        pass
    
    # OK button slot
    def accept( self ):
        name = str( self.entry.text() )
        if name != "":
            banner = _getEngine().makeBanner( name )
            QMessageBox.information( self, 'Info', banner )
            self.close()
        else:
            QMessageBox.warning( self, 'Error!', 'Please, enter the name!' )
        pass

# ----------------------- #
def ShowHELLO():
    # create dialog box
    d = MyDialog( sgPyQt.getDesktop(), 1 )
    # show dialog box
    d.exec_loop()

__id__ = 0

# ----------------------- #
def CreateObject():
    global __id__
    study   = _getStudy()
    builder = study.NewBuilder()
    father  = _findOrCreateComponent()
    object  = builder.NewObject( father )
    attr    = builder.FindOrCreateAttribute( object, "AttributeName" )
    __id__  = __id__ + 1
    attr.SetValue( "Object " +  str( __id__ ) )
    attr    = builder.FindOrCreateAttribute( object, "AttributeLocalID" )
    attr.SetValue( __OBJECT_ID__ )
    sgPyQt.updateObjBrowser()
    pass

# ----------------------- #
def DeleteAll():
    study = _getStudy()
    father = study.FindComponent( __MODULE_NAME__ )
    if father:
        iter = study.NewChildIterator( father )
        builder = study.NewBuilder()
        while iter.More():
            sobj = iter.Value()
            iter.Next()
            builder.RemoveObjectWithChildren( sobj )
        sgPyQt.updateObjBrowser()
    pass

# ----------------------- #
def ShowMe():
    study = _getStudy()
    entry = sg.getSelected( 0 )
    if entry != '':
        sobj = study.FindObjectID( entry )
        if ( sobj ):
            test, attr = sobj.FindAttribute( "AttributeName" )
            if test:
                QMessageBox.information( sgPyQt.getDesktop(), 'Info', "My name is '%s'" % attr.Value() )
                
    pass

# ----------------------- #
def Delete():
    study = _getStudy()
    entry = sg.getSelected( 0 )
    if entry != '':
        sobj = study.FindObjectID( entry )
        if ( sobj ):
            builder = study.NewBuilder()
            builder.RemoveObject( sobj )
            sgPyQt.updateObjBrowser()
    pass

# ----------------------- #
dict_command = {
    941 : ShowHELLO,
    942 : CreateObject,
    951 : DeleteAll,
    952 : ShowMe,
    953 : Delete,
    }
