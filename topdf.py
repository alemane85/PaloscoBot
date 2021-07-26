import os
import art
from datetime import datetime
from MyRoutine import MyRoutine
from MyRoutine import MyCutRoutine
from colorama import Fore,init,Style
from MyTab import MyTab
from MyCsv import MyCsvFile
import webbrowser

in_csv=MyCsvFile()
in_csv.load(f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI_DA_BOLLARE2.txt")
out_file_path=f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI_BOLLATI.txt"
new_tab_rows=[]
for code in in_csv.tab.dict_filter["CODICE"]:
    #print(code)
    supp_tab=(in_csv.tab.filter_by("CODICE",code))
    total=0
    for num in supp_tab.dictionary["QUANTITA"]:
        total+=int(num)
    row=[
        total,code,
        supp_tab.dict_filter["MISURA"][0],
        supp_tab.dict_filter["ALTEZZA"][0],
        supp_tab.dict_filter["DENSITA"][0],
        supp_tab.dict_filter["POROSITA"][0],
        supp_tab.dict_filter["COLORE"][0]
        ]
    new_tab_rows.append(row)
tab_fields=f"""
<thead class="table-light">
    <tr>
      <th scope="col" class="col-md-1">QUANTITA</th>
      <th scope="col" class="col-md-1">CODICE</th>
      <th scope="col" class="col-md-1">MISURA</th>
      <th scope="col" class="col-md-1">ALTEZZA</th>
      <th scope="col" class="col-md-1">DENSITA</th>
      <th scope="col" class="col-md-1">POROSITA</th>
      <th scope="col" class="col-md-1">COLORE</th>
      <th scope="col" class="col-md-5"></th>
    </tr>
</thead>
      """
tab_rows=""
for row in new_tab_rows:
    tab_rows+=f"""
    <tr>
        <th scope="row">{row[0]}</th>
        <td>{row[1]}</td>
        <td>{row[2]}</td>
        <td>{row[3]}</td>
        <td>{row[4]}</td>
        <td>{row[5]}</td>
        <td>{row[6]}</td>
        <td></td>
    </tr>"""
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
        <table class="table table-sm table-hover table-striped text-center table-responsive" style="font-size: 14px">
            {tab_fields}
            <tbody>
                {tab_rows}
            </tbody>
        </table>
    </div>
    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
  </body>
</html>"""
html_name=f"{os.path.dirname(os.path.realpath(__file__))}\prova.html"
with open(html_name, "w") as file_object:
    file_object.write(htmlfile)
url = f"file://{html_name}"
webbrowser.open(url,new=2)
bolla=input("\n\nNUMERO DI BOLLA DA ASSEGNARE AI TAGLI: ")
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
