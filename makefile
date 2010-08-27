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
	