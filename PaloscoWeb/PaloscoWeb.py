from flask import Flask,render_template
import webbrowser
import os
import sys

# SETTING DB AND LIB PATH
upper_path=f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}"
mydb_path=f"{upper_path}/db"
mylib_path=f"{upper_path}/lib"

# ADD MY LIB DIR TO PYTHON PATH SYSTEM
sys.path.append(mylib_path)

# MY OWN MODULE IMPORTS
from MyTab import MyTab
from MyCsv import MyCsvFile

# SET CUTTING ROUTINES FILES
in_cut_file=f"{mydb_path}/TAGLI.txt"
FILE_DA_BOLLARE=f"{mydb_path}/TAGLI_DA_BOLLARE.txt"
FILE_BOLLATI=f"{mydb_path}/TAGLI_DA_BOLLARE.txt"

# SET MIXING ROUTINES FILES
in_mix_file=f"{mydb_path}/MESCOLE.txt"
out_mix_file=f"{mydb_path}/MESCOLE_DA_BOLLARE.txt"

app = Flask(__name__)
url="http://127.0.0.1:5000/PaloscoWeb"
webbrowser.open(url,new=2)
# Defining the home page of our site
@app.route("/PaloscoWeb")  # this sets the route to this page
def home():
	da_bollare_csv=MyCsvFile()
	da_bollare_csv.load(FILE_DA_BOLLARE)
	da_bollare_tab=da_bollare_csv.tab
	main_tab=da_bollare_tab.make_sub_tab(["QUANTITA","CODICE","MISURA","ALTEZZA","TIPO","DENSITA","POROSITA","COLORE"])
	main_tab=main_tab.group_by_sum_by("CODICE","QUANTITA")
	fields=main_tab.give_fields()
	rows=main_tab.give_rows()
	sub_tabs=[]
	sub_fields=["QUANTITA","DATA","ORA","UTENTE"]
	for row in rows:
		this_tab=da_bollare_tab.filter_by("CODICE",row[1])
		this_tab=this_tab.make_sub_tab(sub_fields)
		sub_tabs.append(this_tab.give_rows())
	return render_template("index.html",
							fields=fields,
							enum_rows=enumerate(rows),
							sub_fields=sub_fields,
							sub_tabs=sub_tabs)

if __name__ == "__main__":
    app.run()
