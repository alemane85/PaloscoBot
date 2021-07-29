import os
import art
from datetime import datetime
from MyRoutine import MyRoutine
from MyRoutine import MyCutRoutine
from colorama import Fore,init,Style
from MyTab import MyTab
from MyCsv import MyCsvFile
import webbrowser
import atexit
import time

def exit_handler():
    if os.path.exists(html_name):
        os.remove(html_name)

atexit.register(exit_handler)
in_csv=MyCsvFile()
in_file_path=f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI_BOLLATI.txt"
in_csv.load(in_file_path)
my_time = datetime.now().strftime("%d%m%Y_%H%M%S")
html_name=f"{os.path.dirname(os.path.realpath(__file__))}/tagli_da_bollare_html/{my_time}_visual.html"

print(f"\nSELEZIONA IL NUMERO DEL FILTRO DA UTILIZZARE:\n")
print(f"\n1. BOLLA\n")
print(f"\n2. DATA\n")
choice_dict={"BOLLA":"1","DATA":"2"}
input_choice=input("\n\nSELEZIONE : ")
table__html_list=[]
if input_choice==choice_dict["BOLLA"]:
    for bolla in in_csv.tab.dict_filter["BOLLA"]:
        supp_tab=in_csv.tab.filter_by("BOLLA",bolla)
        this_tab=supp_tab.make_sub_tab(["DATA","UTENTE","QUANTITA","CODICE","MISURA","TIPO","ALTEZZA","DENSITA","POROSITA","COLORE"])
        tab_html=this_tab.to_html(
                                    table_class="table table-sm table-hover table-striped text-center table-responsive",
                                    table_style="font-size: 14px",
                                    thead_class="table-light",
                                    bold_key="QUANTITA"
                                    )
        h1_html=f"<h1>BOLLA N.{bolla}</h1>"
        table__html_list.append(f"{h1_html}\n{tab_html}")
if input_choice==choice_dict["DATA"]:
    for data in in_csv.tab.dict_filter["DATA"]:
        supp_tab=in_csv.tab.filter_by("DATA",data)
        this_tab=supp_tab.make_sub_tab(["BOLLA","UTENTE","QUANTITA","CODICE","MISURA","TIPO","ALTEZZA","DENSITA","POROSITA","COLORE"])
        tab_html=this_tab.to_html(
                                    table_class="table table-sm table-hover table-striped text-center table-responsive",
                                    table_style="font-size: 14px",
                                    thead_class="table-light",
                                    bold_key="QUANTITA"
                                    )
        h1_html=f"<h1>DATA: {data}</h1>"
        table__html_list.append(f"{h1_html}\n{tab_html}")
htmlfile=f"""<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>VISUALIZZA TAGLI BOLLATI</title>
  </head>
  <body>
    <div class="container" style="line-height: 0.8">"""
for tab in table__html_list:
    htmlfile+=tab
htmlfile+="""
    </div>
    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
  </body>
</html>"""
with open(html_name, "w") as file_object:
    file_object.write(htmlfile)
url = f"file://{html_name}"
webbrowser.open(url,new=2)
time.sleep(3)
