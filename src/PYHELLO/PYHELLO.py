# Copyright (C) 2007-2014  CEA/DEN, EDF R&D, OPEN CASCADE
#
# Copyright (C) 2003-2007  OPEN CASCADE, EADS/CCR, LIP6, CEA/DEN,
# CEDRAT, EDF R&D, LEG, PRINCIPIA R&D, BUREAU VERITAS
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

# ---
# File   : PYHELLOGUI.py
# Author : Vadim SANDLER, Open CASCADE S.A.S. (vadim.sandler@opencascade.com)
# ---
#
import PYHELLO_ORB__POA
import SALOME_ComponentPy
import SALOME_DriverPy
import SALOMEDS
from SALOME_DataContainerPy import *

from PYHELLO_utils import *

class PYHELLO(PYHELLO_ORB__POA.PYHELLO_Gen,
              SALOME_ComponentPy.SALOME_ComponentPy_i,
              SALOME_DriverPy.SALOME_DriverPy_i):
    """
    Construct an instance of PYHELLO module engine.
    The class PYHELLO implements CORBA interface PYHELLO_Gen (see PYHELLO_Gen.idl).
    It is inherited from the classes SALOME_ComponentPy_i (implementation of
    Engines::EngineComponent CORBA interface - SALOME component) and SALOME_DriverPy_i
    (implementation of SALOMEDS::Driver CORBA interface - SALOME module's engine).
    """
    def __init__ ( self, orb, poa, contID, containerName, instanceName, 
                   interfaceName ):
        SALOME_ComponentPy.SALOME_ComponentPy_i.__init__(self, orb, poa,
                    contID, containerName, instanceName, interfaceName, 0)
        SALOME_DriverPy.SALOME_DriverPy_i.__init__(self, interfaceName)
        #
        self._naming_service = SALOME_ComponentPy.SALOME_NamingServicePy_i( self._orb )
        #
        pass

    """
    Get version information.
    """
    def getVersion( self ):
        import salome_version
        return salome_version.getVersion("PYHELLO", True)

    """
    Generate hello banner.
    """
    def makeBanner( self, name ):
        banner = "Hello %s!" % name
        return banner

    """
    Create object.
    """
    def createObject( self, study, name ):
        self._createdNew = True # used for getModifiedData method
        builder = study.NewBuilder()
        father  = findOrCreateComponent( study )
        object  = builder.NewObject( father )
        attr    = builder.FindOrCreateAttribute( object, "AttributeName" )
        attr.SetValue( name )
        attr    = builder.FindOrCreateAttribute( object, "AttributeLocalID" )
        attr.SetValue( objectID() )
        pass

    """
    Dump module data to the Python script.
    """
    def DumpPython( self, study, isPublished, isMultiFile ):
        abuffer = []
        names = []
        father = study.FindComponent( moduleName() )
        if father:
            iter = study.NewChildIterator( father )
            while iter.More():
                name = iter.Value().GetName()
                if name: names.append( name )
                iter.Next()
                pass
            pass
        if names:
            abuffer += [ "from salome import lcc" ]
            abuffer += [ "import PYHELLO_ORB" ]
            abuffer += [ "" ]
            abuffer += [ "pyhello = lcc.FindOrLoadComponent( 'FactoryServerPy', '%s' )" % moduleName() ]
            abuffer += [ "" ]
            abuffer += [ "pyhello.createObject( theStudy, '%s' )" % name for name in names ]
            abuffer += [ "" ]
            pass
        if isMultiFile:
            abuffer       = [ "  " + s for s in abuffer ]
            abuffer[0:0]  = [ "def RebuildData( theStudy ):" ]
            abuffer      += [ "  pass" ]
        abuffer += [ "\0" ]
        return ("\n".join( abuffer ), 1)

    """
    Import file to restore module data
    """
    def importData(self, studyId, dataContainer, options):
      # get study by Id
      obj = self._naming_service.Resolve("myStudyManager")
      myStudyManager = obj._narrow(SALOMEDS.StudyManager)
      study = myStudyManager.GetStudyByID(studyId)
      # create all objects from the imported stream
      stream = dataContainer.get()
      for objname in stream.split("\n"):
        if len(objname) != 0:
          self.createObject(study, objname)
      self._createdNew = False # to store the modification of the study information later
      return ["objects"] # identifier what is in this file

    def getModifiedData(self, studyId):
      if self._createdNew:
        # get study by Id
        obj = self._naming_service.Resolve("myStudyManager")
        myStudyManager = obj._narrow(SALOMEDS.StudyManager)
        study = myStudyManager.GetStudyByID(studyId)
        # iterate all objects to get their names and store this information in stream
        stream=""
        father = study.FindComponent( moduleName() )
        if father:
            iter = study.NewChildIterator( father )
            while iter.More():
                name = iter.Value().GetName()
                stream += name + "\n"
                iter.Next()
        # store stream to the temporary file to send it in DataContainer
        dataContainer = SALOME_DataContainerPy_i(stream, "", "objects", False, True)
        aVar = dataContainer._this()
        return [aVar]
      return []
