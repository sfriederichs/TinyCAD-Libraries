PROJECT_NAME = TinyCAD-Libraries
REPO = $(PROJECT_NAME).git
USERNAME = sfriederichs
REPO_URL = git://github.com/$(USERNAME)/$(REPO)
SSH_URL = git@github.com:$(USERNAME)/$(REPO)
GIT = git
BRANCH = master
COMMITFILE = commit


PL_URL = "http://spreadsheets.google.com/pub?key=t9k879BSXydtZdb6YKeC40g&output=csv"
PYTHON_CMD = python
PL_DIR = ./Libraries/CSV
PL_FILE = parts_list.csv
MDB_SCRIPT = ./Script/plgen_mdb.py
TCLIB_SCRIPT = ./Script/plgen_tclib.py

libs: update_pl
	$(PYTHON_CMD) $(TCLIB_SCRIPT)

update_pl:
	wget $(PL_URL) -O $(PL_DIR)/$(PL_FILE)
	
repo:
	$(GIT) init
	$(GIT) remote add $(USERNAME) $(REPO_URL)
	$(GIT) pull $(REPO_URL)
	echo "Standard commit message" > commit

add:
	$(GIT) add .
	
push: commit
	$(GIT) push $(SSH_URL)
	
pull:
	$(GIT) checkout $(BRANCH)
	$(GIT) pull
commit: FORCE
	-$(GIT) commit -a -F $(COMMITFILE)

FORCE: