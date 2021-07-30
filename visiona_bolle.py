import os
import art
from datetime import datetime
from MyRoutine import MyRoutine
from MyRoutine import MyCutRoutine
from colorama import Fore,init,Style
from MyTab import MyTab
from MyCsv import MyCsvFile
import webbrowser
import time
import glob

garbage = glob.glob(f"{os.path.dirname(os.path.realpath(__file__))}/data/html/temp/*.html")
for trash in garbage:
    os.remove(trash)

in_csv=MyCsvFile()
in_file_path=f"{os.path.dirname(os.path.realpath(__file__))}\data\db\TAGLI_BOLLATI.txt"
in_csv.load(in_file_path)
my_time = datetime.now().strftime("%d%m%Y_%H%M%S")
html_name=f"{os.path.dirname(os.path.realpath(__file__))}/data/html/temp/{my_time}_visual.html"
html_base=f"{os.path.dirname(os.path.realpath(__file__))}/data/html/base.txt"

print(f"\nSELEZIONA IL NUMERO DEL FILTRO DA UTILIZZARE:\n")
print(f"\n1. BOLLA\n")
print(f"\n2. DATA\n")
input_choice=input("\n\nSELEZIONE : ")
table__html_list=[]
if input_choice=="1":
    filters=in_csv.tab.dict_filter["BOLLA"]
    header="ELENCO BOLLE"
    title="BOLLA N."
    key="BOLLA"
    no_key="DATA"
if input_choice=="2":
    filters=in_csv.tab.dict_filter["DATA"]
    header="ELENCO PER DATA"
    title="DATA: "
    key="DATA"
    no_key="BOLLA"
index=0
for element in filters:
    supp_tab=in_csv.tab.filter_by(key,element)
    this_tab=supp_tab.make_sub_tab([no_key,"UTENTE","QUANTITA","CODICE",
                                    "MISURA","TIPO","ALTEZZA","DENSITA",
                                    "POROSITA","COLORE"])
    tab_html=this_tab.to_html(
            table_class="table table-sm table-hover table-striped text-center table-responsive",
            table_style="font-size: 14px",
            thead_class="table-light",
            bold_key=input_choice
                            )
    card_html=f"""
    <div class="card">
    <div class="card-header" id="heading{index}">
        <h5 class="mb-0">
            <button class="btn btn-link" data-toggle="collapse" data-target="#collapse{index}" aria-expanded="true" aria-controls="collapse{index}">
            {title}{element}
            </button>
        </h5>
    </div>
    <div id="collapse{index}" class="collapse" aria-labelledby="heading{index}" data-parent="#accordion">
        <div class="card-body">
            {tab_html}
        </div>
    </div>
    </div>"""
    index+=1
    table__html_list.append(card_html)

with open(html_base, "r") as file_object:
    basefile=file_object.read()
base=basefile.split("$")
htmlfile=base[0]
htmlfile+=f"""<div class="container">
    <header class="d-flex flex-wrap justify-content-center py-3 mb-4 border-bottom">
      <h3 class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
        <svg class="bi me-2" width="40" height="32"><use xlink:href="#bootstrap"></use></svg>
        <span class="fs-4">{header}</span>
      </h3>
  </div>"""
htmlfile+=f"""\n<div class="container" style="line-height: 0.8" id="accordion">"""
for tab in table__html_list:
    htmlfile+=tab
htmlfile+=f"""\n</div>"""
htmlfile+=base[1]
with open(html_name, "w") as file_object:
    file_object.write(htmlfile)
url = f"file://{html_name}"
webbrowser.open(url,new=2)
time.sleep(3)
