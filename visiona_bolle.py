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
in_file_path=f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI_BOLLATI.txt"
in_csv.load(in_file_path)

print(f"\nSELEZIONA IL NUMERO DEL FILTRO DA UTILIZZARE:\n")
print(f"\n1. BOLLA\n")
print(f"\n2. DATA\n")
choice_dict={"BOLLA":"1","DATA":"2"}
input_choice=input("\n\nSELEZIONE : ")

if input_choice==choice_dict["BOLLA"]:
    for bolla in in_csv.tab.dict_filter["BOLLA"]:
        supp_tab=in_csv.tab.filter_by("BOLLA",bolla)
        print(supp_tab)
if input_choice==choice_dict["DATA"]:
    for bolla in in_csv.tab.dict_filter["DATA"]:
        supp_tab=in_csv.tab.filter_by("DATA",bolla)
        print(supp_tab)
