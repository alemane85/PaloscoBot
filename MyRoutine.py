from MyTab import MyTab
from MyCsv import MyCsvFile
from datetime import datetime

class MyRoutine():
    """
    Inizializzazione di tutte le variabili di classe
    """
    def __init__(self,username,source_file,output_file):
        self.username=username
        self.verbose=True
        self.reset()
        self.output_file=output_file
        self.source_file=source_file
        file=MyCsvFile()
        file.load(source_file)
        self.source_tab=file.tab

    """
    Reset di tutti gli attributi di classe
    """
    def reset(self):
        self.selection={}
        self.filtered_tab=0
        self.error=0
        if self.verbose:
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"{time} | User: {self.username} -> Sessione resettata")
    """
    Restituisce in forma di stringa una fotografia della classe in quel momento
    utile in fase di controllo
    """
    def __str__(self):
        string=f"MyRoutine.username={self.username}\n"
        for key in self.selection.keys():
            string+=f"MyRoutine.selection[{key}]={self.selection[key]}\n"
        string+=f"MyRoutine.filtered_tab=\n{self.filtered_tab}\n"
        string+=f"MyRoutine.source_tab=\n{self.source_tab}\n"
        string+=f"MyRoutine.source_file={self.source_file}\n"
        string+=f"MyRoutine.output_file_file={self.output_file}\n"
        string+=f"MyRoutine.error={self.error}"
        return string

class MyCutRoutine(MyRoutine):
    def handle_call(self,call,bot):
        if self.verbose:
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"{time} | User: {self.username} -> calldata = [{call.data}]")
        print("SONO CUT ROUTINE!")
