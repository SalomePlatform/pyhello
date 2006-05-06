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
#  See http://www.salome-platform.org/
#
import PYHELLO_ORB__POA
import SALOME_ComponentPy
import SALOME_DriverPy

class PYHELLO(PYHELLO_ORB__POA.PYHELLO_Gen,
              SALOME_ComponentPy.SALOME_ComponentPy_i,
              SALOME_DriverPy.SALOME_DriverPy_i):
    """
        Pour etre un composant SALOME cette classe Python
        doit avoir le nom du composant et heriter de la
        classe PYHELLO_Gen issue de la compilation de l'idl
        par omniidl et de la classe SALOME_ComponentPy_i
        qui porte les services generaux d'un composant SALOME
    """
    def __init__ ( self, orb, poa, contID, containerName, instanceName, 
                   interfaceName ):
        print "PYHELLO.__init__: ", containerName, ';', instanceName
        SALOME_ComponentPy.SALOME_ComponentPy_i.__init__(self, orb, poa,
                    contID, containerName, instanceName, interfaceName, 0)
        SALOME_DriverPy.SALOME_DriverPy_i.__init__(self, interfaceName)
        # On stocke dans l'attribut _naming_service, une reference sur
        # le Naming Service CORBA
        self._naming_service = SALOME_ComponentPy.SALOME_NamingServicePy_i( self._orb )

    def makeBanner( self, name ):
        banner = "Hello %s!" % name
        return banner
