#hello:#
#	echo "hello World"
#	apt-get update
#
TOP:=$(CURDIR)
ifneq (1,$(words $(TOP)))
TOP:=.
endif

include $(TOP)/configure/CONFIG
include $(TOP)/configure/RULES
