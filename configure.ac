#
#  PLEASE DO NOT MODIFY configure.in FILE
#
#  ALL CHANGES WILL BE DISCARDED BY THE NEXT
#  build_configure COMMAND
#
#  CHANGES MUST BE MADE IN configure.in.base FILE
#
#
# Author : Marc Tajchman (CEA)
# Date : 28/06/2001
# Modified by : Patrick GOLDBRONN (CEA)
# Modified by : Marc Tajchman (CEA)
#
# Created from configure.in.base
#

AC_INIT([Salome2 Project PYHELLO module], [5.0.0], [webmaster.salome@opencascade.com], [salome])
AC_CONFIG_AUX_DIR(salome_adm/unix/config_files)
AC_CANONICAL_HOST
AC_CANONICAL_TARGET
AM_INIT_AUTOMAKE

XVERSION=`echo $VERSION | awk -F. '{printf("0x%02x%02x%02x",$1,$2,$3)}'`
AC_SUBST(XVERSION)

# set up MODULE_NAME variable for dynamic construction of directories (resources, etc.)
MODULE_NAME=pyhello
AC_SUBST(MODULE_NAME)

dnl
dnl Initialize source and build root directories
dnl

ROOT_BUILDDIR=`pwd`
ROOT_SRCDIR=`echo $0 | sed -e "s,[[^/]]*$,,;s,/$,,;s,^$,.,"`
cd $ROOT_SRCDIR
ROOT_SRCDIR=`pwd`
cd $ROOT_BUILDDIR

AC_SUBST(ROOT_SRCDIR)
AC_SUBST(ROOT_BUILDDIR)

echo
echo Source root directory : $ROOT_SRCDIR
echo Build  root directory : $ROOT_BUILDDIR
echo
echo

AC_CHECK_PROG(SHELL,sh)
AC_SUBST(SHELL)

if test -z "$AR"; then
   AC_CHECK_PROGS(AR,ar xar,:,$PATH)
fi
AC_SUBST(AR)

dnl Export the AR macro so that it will be placed in the libtool file
dnl correctly.
export AR

echo
echo ---------------------------------------------
echo testing make
echo ---------------------------------------------
echo

AC_PROG_MAKE_SET
AC_PROG_INSTALL
dnl 
dnl libtool macro check for CC, LD, NM, LN_S, RANLIB, STRIP + for shared libraries

AC_ENABLE_DEBUG(yes)
AC_DISABLE_PRODUCTION

echo ---------------------------------------------
echo testing libtool
echo ---------------------------------------------

dnl first, we set static to no!
dnl if we want it, use --enable-static
AC_ENABLE_STATIC(no)

AC_LIBTOOL_DLOPEN
AC_PROG_LIBTOOL

dnl Fix up the INSTALL macro if it s a relative path. We want the
dnl full-path to the binary instead.
case "$INSTALL" in
   *install-sh*)
      INSTALL='\${KERNEL_ROOT_DIR}'/salome_adm/unix/config_files/install-sh
      ;;
esac

echo
echo ---------------------------------------------
echo testing python
echo ---------------------------------------------
echo

CHECK_PYTHON

AM_PATH_PYTHON(2.3)

echo
echo ---------------------------------------------
echo testing omniORB
echo ---------------------------------------------
echo

CHECK_OMNIORB

echo
echo ---------------------------------------------
echo default ORB : omniORB
echo ---------------------------------------------
echo

DEFAULT_ORB=omniORB
CHECK_CORBA

AC_SUBST_FILE(CORBA)
corba=make_$ORB
CORBA=adm_local/unix/$corba

echo
echo ---------------------------------------------
echo testing QT
echo ---------------------------------------------
echo

CHECK_QT

echo
echo ---------------------------------------------
echo Testing Kernel
echo ---------------------------------------------
echo

CHECK_KERNEL

echo
echo ---------------------------------------------
echo Testing GUI
echo ---------------------------------------------
echo

CHECK_SALOME_GUI

echo
echo ---------------------------------------------
echo Testing full GUI
echo ---------------------------------------------
echo

CHECK_CORBA_IN_GUI
if test "x${CORBA_IN_GUI}" != "xyes"; then
  echo "failed : For configure PYHELLO1 module necessary full GUI !"
  exit
fi



echo
echo ---------------------------------------------
echo Summary
echo ---------------------------------------------
echo

echo Configure
variables="python_ok omniORB_ok qt_ok Kernel_ok"

for var in $variables
do
   printf "   %10s : " `echo \$var | sed -e "s,_ok,,"`
   eval echo \$$var
done

echo
echo "Default ORB   : $DEFAULT_ORB"
echo

dnl We don t need to say when we re entering directories if we re using
dnl GNU make becuase make does it for us.
if test "X$GMAKE" = "Xyes"; then
   AC_SUBST(SETX) SETX=":"
else
   AC_SUBST(SETX) SETX="set -x"
fi
echo
echo ---------------------------------------------
echo generating Makefiles and configure files
echo ---------------------------------------------
echo

AC_OUTPUT_COMMANDS([ \
      chmod +x ./bin/*; \
])

# This list is initiated using autoscan and must be updated manually
# when adding a new file <filename>.in to manage. When you execute
# autoscan, the Makefile list is generated in the output file configure.scan.
# This could be helpfull to update de configuration.
AC_OUTPUT([ \
  ./salome_adm/unix/SALOMEconfig.h \
  ./adm_local/Makefile \
  ./adm_local/unix/Makefile \
  ./adm_local/unix/config_files/Makefile \
  ./bin/VERSION \
  ./bin/runAppli \
  ./bin/Makefile \
  ./src/Makefile \
  ./src/PYHELLO/Makefile \
  ./src/PYHELLOGUI/Makefile \
  ./resources/Makefile \
  ./resources/PYHELLOCatalog.xml \
  ./idl/Makefile \
  Makefile \
])
