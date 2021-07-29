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

def exit_handler():
    if os.path.exists(html_name):
        os.remove(html_name)

atexit.register(exit_handler)
in_csv=MyCsvFile()
in_fields="DATA,ORA,UTENTE,QUANTITA,PRODOTTO,CODICE,COLORE,TIPO,DENSITA,POROSITA,MISURA,ALTEZZA\n"
in_file_path=f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI_DA_BOLLARE.txt"
in_csv.load(in_file_path)
out_file_path=f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI_BOLLATI.txt"
this_tab=in_csv.tab.make_sub_tab(["QUANTITA","CODICE","MISURA","TIPO","ALTEZZA","DENSITA","POROSITA","COLORE"])
this_tab=this_tab.group_by_sum_by("CODICE","QUANTITA")
tab_html=this_tab.to_html(
                            table_class="table table-sm table-hover table-striped text-center table-responsive",
                            table_style="font-size: 14px",
                            thead_class="table-light",
                            bold_key="QUANTITA"
                            )
htmlfile=f"""<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>TAGLI DA BOLLARE</title>
  </head>
  <body>
    <div class="container" style="line-height: 0.8">
        {tab_html}
    </div>
    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
  </body>
</html>"""

time = datetime.now().strftime("%d%m%Y_%H%M%S")
html_name=f"{os.path.dirname(os.path.realpath(__file__))}/tagli_da_bollare_html/{time}_bolla.html"
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
            line=""
            for element in row:
                    line+=f"{element},"
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
