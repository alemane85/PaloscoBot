from MyCsv import MyCsvFile
from MyTab import MyTab
from flask import Flask, render_template, request
import webbrowser
import os
import sys
from datetime import datetime

# SETTING DB AND LIB PATH
upper_path = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}"
mydb_path = f"{upper_path}/db"
mylib_path = f"{upper_path}/lib"

# ADD MY LIB DIR TO PYTHON PATH SYSTEM
sys.path.append(mylib_path)

# MY OWN MODULE IMPORTS

# SET CUTTING ROUTINES FILES
in_cut_file = f"{mydb_path}/TAGLI.txt"
FILE_DA_BOLLARE = f"{mydb_path}/TAGLI_DA_BOLLARE.txt"
FILE_BOLLATI = f"{mydb_path}/TAGLI_BOLLATI.txt"

# SET MIXING ROUTINES FILES
in_mix_file = f"{mydb_path}/MESCOLE.txt"
out_mix_file = f"{mydb_path}/MESCOLE_DA_BOLLARE.txt"

app = Flask(__name__)
url = "http://127.0.0.1:5000/PaloscoWeb"
webbrowser.open(url, new=2)
# Defining the home page of our site


@app.route("/PaloscoWeb")  # this sets the route to this page
def home():
    da_bollare_csv = MyCsvFile()
    da_bollare_csv.load(FILE_DA_BOLLARE)
    da_bollare_tab = da_bollare_csv.tab
    if da_bollare_tab.is_empty():
        return render_template("index.html",
                               empty=True,
                               fields=0,
                               data=0,
                               enum_rows=0,
                               sub_fields=0,
                               sub_tabs=0)
    main_tab = da_bollare_tab.make_sub_tab(
        ["QUANTITA", "CODICE", "MISURA", "ALTEZZA", "TIPO", "DENSITA", "POROSITA", "COLORE"])
    main_tab = main_tab.group_by_sum_by("CODICE", "QUANTITA")
    fields = main_tab.give_fields()
    rows = main_tab.give_rows()
    sub_tabs = []
    sub_fields = ["QUANTITA", "DATA", "ORA", "UTENTE"]
    for row in rows:
        this_tab = da_bollare_tab.filter_by("CODICE", row[1])
        this_tab = this_tab.make_sub_tab(sub_fields)
        sub_tabs.append(this_tab.give_rows())
    data = datetime.now().strftime("%d/%m/%Y")
    return render_template("index.html",
                           empty=False,
                           fields=fields,
                           data=data,
                           enum_rows=enumerate(rows),
                           sub_fields=sub_fields,
                           sub_tabs=sub_tabs)


@app.route('/crea_bolla', methods=['POST', 'GET'])
def crea_bolla():
    if request.method == 'POST':
        bolla = request.form['numero']
        data_bolla = request.form['data']
        codici = request.form.getlist('mycheck')
        da_bollare_csv = MyCsvFile()
        da_bollare_csv.load(FILE_DA_BOLLARE)
        da_bollare_tab = da_bollare_csv.tab
        all_rows = da_bollare_tab.give_rows()
        all_fields = da_bollare_tab.give_fields()
        not_included_rows = []
        included_rows = []
        for row in all_rows:
            included = False
            for codice in codici:
                if row[5] == codice:
                    included = True
                    break
            if not included:
                not_included_rows.append(row)
            else:
                included_rows.append(row)
        with open(FILE_BOLLATI, "a") as file_object:
            contatore = 0
            for row in included_rows:
                line = ""
                for element in row:
                    line += f"{element},"
                supp = f"{line}{bolla},{data_bolla}"
                supp += "\n"
                file_object.write(supp)
                contatore += 1
        with open(FILE_DA_BOLLARE, "w") as file_object:
            line = ""
            for field in all_fields:
                line += f"{field}"
                if field == all_fields[-1]:
                    line += f"\n"
                else:
                    line += f","
            print(line)
            file_object.write(line)
            if not_included_rows:
                for row in not_included_rows:
                    line = ""
                    for element in row:
                        line += f"{element}"
                        if element == row[-1]:
                            line += f"\n"
                        else:
                            line += f","
                    print(line)
                    file_object.write(line)
        main_tab = MyTab()
        main_tab.create(all_fields, included_rows)
        main_tab = main_tab.make_sub_tab(
            ["QUANTITA", "CODICE", "MISURA", "ALTEZZA", "TIPO", "DENSITA", "POROSITA", "COLORE"])
        main_tab = main_tab.group_by_sum_by("CODICE", "QUANTITA")
        fields = main_tab.give_fields()
        rows = main_tab.give_rows()
        sub_tabs = []
        sub_fields = ["QUANTITA", "DATA", "ORA", "UTENTE"]
        for row in rows:
            this_tab = da_bollare_tab.filter_by("CODICE", row[1])
            this_tab = this_tab.make_sub_tab(sub_fields)
            sub_tabs.append(this_tab.give_rows())
        return render_template("crea_bolla.html",
                               bolla=bolla,
                               data_bolla=data_bolla,
                               fields=fields,
                               enum_rows=enumerate(rows),
                               sub_fields=sub_fields,
                               sub_tabs=sub_tabs)
    else:
        return "METODO GET NON VALIDO"


if __name__ == "__main__":
    app.run()
