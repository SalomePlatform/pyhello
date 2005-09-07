#!/usr/bin/env python

def test(clt):
   """
        Test function that creates an instance of PYHELLO component
        usage : pyhello=test(clt)
   """
   # create an LifeCycleCORBA instance
   import LifeCycleCORBA 
   lcc = LifeCycleCORBA.LifeCycleCORBA(clt.orb)
   import PYHELLO_ORB
   pyhello = lcc.FindOrLoadComponent("FactoryServerPy", "PYHELLO")
   return pyhello

#

if __name__ == "__main__":
   import user
   from runSalome import *
   clt,args = main()
   
   #
   #  Impression arborescence Naming Service
   #
   
   if clt != None:
     print
     print " --- registered objects tree in Naming Service ---"
     clt.showNS()
     session=clt.waitNS("/Kernel/Session")
     catalog=clt.waitNS("/Kernel/ModulCatalog")
     import socket
     container =  clt.waitNS("/Containers/" + socket.gethostname().split('.')[0] + "/FactoryServerPy")
