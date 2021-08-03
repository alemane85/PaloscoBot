import os
import art
from datetime import datetime
from MyRoutine import MyRoutine
from MyRoutine import MyCutRoutine
from colorama import Fore,init,Style
from MyTab import MyTab
from MyCsv import MyCsvFile
import webbrowser
import glob

garbage = glob.glob(f"{os.path.dirname(os.path.realpath(__file__))}/data/html/temp/*.html")
for trash in garbage:
    os.remove(trash)

in_csv=MyCsvFile()
in_fields="DATA,ORA,UTENTE,QUANTITA,PRODOTTO,CODICE,COLORE,TIPO,DENSITA,POROSITA,MISURA,ALTEZZA\n"
in_file_path=f"{os.path.dirname(os.path.realpath(__file__))}\data\db\TAGLI_DA_BOLLARE.txt"
html_base=f"{os.path.dirname(os.path.realpath(__file__))}/data/html/base.txt"
header="TAGLI DA BOLLARE"
in_csv.load(in_file_path)
out_file_path=f"{os.path.dirname(os.path.realpath(__file__))}\data\db\TAGLI_BOLLATI.txt"
this_tab=in_csv.tab.make_sub_tab(["QUANTITA","CODICE","MISURA","TIPO","ALTEZZA","DENSITA","POROSITA","COLORE"])
this_tab=this_tab.group_by_sum_by("CODICE","QUANTITA")
tab_html=this_tab.to_html(
                            table_class="table table-sm table-hover table-striped text-center table-responsive",
                            table_style="font-size: 14px",
                            thead_class="table-light",
                            bold_key="QUANTITA"
                            )

with open(html_base, "r") as file_object:
    basefile=file_object.read()
base=basefile.split("$")
htmlfile=base[0]
htmlfile+=f"""<div class="container">
    <header class="d-flex flex-wrap py-3 mb-4 border-bottom">
      <h3 class="d-flex mb-3 mb-md-0 me-md-auto text-dark text-decoration-none">
        {header}
      </h3>
  </div>
  <div class="container">"""
htmlfile+=tab_html
htmlfile+="</div>"
htmlfile+=base[1]

time = datetime.now().strftime("%d%m%Y_%H%M%S")
html_name=f"{os.path.dirname(os.path.realpath(__file__))}/data/html/temp/{time}_bolla.html"
with open(html_name, "w") as file_object:
    file_object.write(htmlfile)
url = f"file://{html_name}"
webbrowser.open(url,new=2)
bolla=input("\n\nNUMERO DI BOLLA DA ASSEGNARE AI TAGLI: ")
conf=input("\n\nCONFERMA NUMERO DI BOLLA {bolla} DA ASSEGNARE AI TAGLI: ")
if conf==bolla:
    print(f"\nTRASFERIMENTO TAGLI NELLA BOLLA N. {bolla} IN CORSO ...\n")
    with open(out_file_path, "a") as file_object:
        contatore=0
        for row in in_csv.rows:
            line = "".join(f"{element}," for element in row)
            supp=f"{line}{bolla}"
            print(supp)
            supp+="\n"
            file_object.write(supp)
            contatore+=1
    print(f"\nTRASFERIMENTO DI N. {contatore} TAGLI NELLA BOLLA N. {bolla} COMPLETATO")
    print(f"\nRIMOZIONE DI N. {contatore} TAGLI DAL FILE DEI TAGLI DA BOLLARE IN CORSO ...")
    with open(in_file_path, "w") as file_object:
        file_object.write(in_fields)
    print(f"\nRIMOZIONE COMPLETATA!")
else:
    print(f"\nNUMERI INSERITI NON CORRISPONDENTI")
