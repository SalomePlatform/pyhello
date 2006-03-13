#  Check availability of PYHELLO binary distribution
#
#  Author : Marc Tajchman (CEA, 2002)
#------------------------------------------------------------

AC_DEFUN([CHECK_PYHELLO],[

AC_CHECKING(for PyHello)

PyHello_ok=no

AC_ARG_WITH(pyHello,
	    --with-py-hello=DIR root directory path of PYHELLO installation,
	    PYHELLO_DIR="$withval",PYHELLO_DIR="")

if test "x$PYHELLO_DIR" = "x" ; then

# no --with-py-hello option used

  if test "x$PYHELLO_ROOT_DIR" != "x" ; then

    # PYHELLO_ROOT_DIR environment variable defined
    PYHELLO_DIR=$PYHELLO_ROOT_DIR

  else

    # search PyHello binaries in PATH variable
    AC_PATH_PROG(TEMP, PYHELLOGUI.py)
    if test "x$TEMP" != "x" ; then
      PYHELLO_BIN_DIR=`dirname $TEMP`
      PYHELLO_DIR=`dirname $PYHELLO_BIN_DIR`
    fi

  fi
#
fi

if test -f ${PYHELLO_DIR}/bin/salome/PYHELLOGUI.py  ; then
  PyHello_ok=yes
  AC_MSG_RESULT(Using PYHELLO distribution in ${PYHELLO_DIR})

  if test "x$PYHELLO_ROOT_DIR" == "x" ; then
    PYHELLO_ROOT_DIR=${PYHELLO_DIR}
  fi
  AC_SUBST(PYHELLO_ROOT_DIR)
else
  AC_MSG_WARN("Cannot find compiled PYHELLO distribution")
fi
  
AC_MSG_RESULT(for PYHELLO: $PyHello_ok)
 
])dnl
 
