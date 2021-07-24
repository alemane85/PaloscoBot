import os
import art
from datetime import datetime
from MyRoutine import MyRoutine
from MyRoutine import MyCutRoutine
from colorama import Fore,init,Style
from MyTab import MyTab
from MyCsv import MyCsvFile
import pdfkit

input=MyCsvFile()
input.load(f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI_DA_BOLLARE2.txt")
output=MyCsvFile()
new_tab_rows=[]
for code in input.tab.dict_filter["CODICE"]:
    #print(code)
    supp_tab=(input.tab.filter_by("CODICE",code))
    total=0
    for num in supp_tab.dictionary["QUANTITA"]:
        total+=int(num)
    row=[
        total,code,
        supp_tab.dict_filter["DENSITA"][0],
        supp_tab.dict_filter["POROSITA"][0],
        supp_tab.dict_filter["COLORE"][0],
        supp_tab.dict_filter["MISURA"][0],
        supp_tab.dict_filter["ALTEZZA"][0]
        ]
    new_tab_rows.append(row)
for row in new_tab_rows:
    print(row)

config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
pdfkit.from_string(str(new_tab_rows), f"{os.path.dirname(os.path.realpath(__file__))}\prova.pdf", configuration=config)
