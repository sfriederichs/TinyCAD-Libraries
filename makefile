PROJECT_NAME = TinyCAD-Libraries
REPO = $(PROJECT_NAME).git
USERNAME = sfriederichs
REPO_URL = git://github.com/$(USERNAME)/$(REPO)
SSH_URL = git@github.com:$(USERNAME)/$(REPO)
GIT = git
BRANCH = master
COMMITFILE = commit
GIT = git
BRANCH = master
COMMITFILE = commit
SSH_URL = git@github.com:$(USERNAME)/$(REPO)
PL_URL = "http://spreadsheets.google.com/pub?key=t9k879BSXydtZdb6YKeC40g&output=csv"
PYTHON_CMD = python
PL_DIR = ./Libraries/CSV
PL_FILE = parts_list.csv
TCLIB_DIR = ./Libraries/TCLib
MDB_SCRIPT = ./Script/plgen_mdb.py
TCLIB_SCRIPT = ./Script/plgen_tclib.py
DKEY_SCRIPT = ./Script/digikey_parser.py

libs: clean_libs update_pl
	$(PYTHON_CMD) $(TCLIB_SCRIPT)
	
add_libs:
	git add ./Libraries/TCLib/*
	
clean_incoming: FORCE
	-rm -r ./Incoming/*

update_pl:
	$(PYTHON_CMD) $(DKEY_SCRIPT)
	
repo:
	$(GIT) init
	$(GIT) remote add $(USERNAME) $(REPO_URL)
	$(GIT) remote add $(PROJECT_NAME) $(REPO_URL)
	$(GIT) pull $(REPO_URL)
	echo "Standard commit message" > commit

add:
	$(GIT) add . -v
	
push: commit 
	$(GIT) push $(SSH_URL)
	
pull:
	$(GIT) checkout $(BRANCH)
	$(GIT) pull $(REPO_URL)
	
commit: add_libs FORCE
	notepad commit
	-$(GIT) commit -a -v -F $(COMMITFILE)

clean_libs: FORCE
	rm -f $(TCLIB_DIR)/*.*
	
FORCE: