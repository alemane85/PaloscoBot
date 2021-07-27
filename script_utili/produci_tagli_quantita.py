from MyTab import MyTab
from MyCsv import MyCsvFile
import os

infile=f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI.txt"
outfile=f"{os.path.dirname(os.path.realpath(__file__))}\data\TAGLI_QUANTITA.txt"

file= MyCsvFile()
file.load(infile)

output= MyCsvFile()
output.fields.append("CODICE")
output.fields.append("QUANTITA")
for row in file.rows:
    print(f"{row[1]}=0")
    output.rows.append([f"{row[1]}","0"])
output.saveas(outfile)
