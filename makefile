USERNAME = sfriederichs
URL = git://github.com/sfriederichs/TinyCAD-Libraries.git
REPOSITORY = TinyCAD-Libraries.git

GIT = git
BRANCH = master
COMMITFILE = commit
SSH_URL = git@github.com:$(USERNAME)/$(REPOSITORY)

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
	$(GIT) remote add $(USERNAME) $(URL)
	$(GIT) fetch $(USERNAME)
	echo "Standard commit message" > commit

add:
	$(GIT) add .
pull:
	$(GIT) checkout $(BRANCH)
	$(GIT) pull $(URL)
commit:
	$(GIT) commit -a -F $(COMMITFILE)
	
push: commit
=======
pull:
	$(GIT) checkout $(BRANCH)
	$(GIT) pull
commit:
	$(GIT) commit -a -F $(COMMITFILE)
	
push:
>>>>>>> 307dd7f6d32863e0abb0142d88f8e2b524ed1ac4
	$(GIT) push $(SSH_URL)