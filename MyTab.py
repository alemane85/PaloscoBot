"""
-MyTab-
    Classe personale per una gestione semplificata dizonary con values di liste
    Attributi:
        path        - indirizzo directory del file
        name        - nome del file
        fields      - campi di testata del file
        rows        - lista di righe del file
        delimiter   - delimitatore scelto per il Csv
        quotechar   - char di quotatura scelto per il Csv
        quoting     - stile di lettura/scrittura di csvfile
        escapechar  - char aggiunto fra delimiter e quotechar
        error       - classe di errore
"""
class MyTab():
    """
    Inizializzazione di tutte le variabili di classe
    """
    def __init__(self):
        self.reset()
    """
    Reset di tutti gli attributi di classe
    """
    def reset(self):
        self.dictionary={}
        self.dict_filter={}
        self.error=0

    """
    Restituisce in forma di stringa una fotografia della classe in quel momento
    utile in fase di controllo
    """
    def __str__(self):
        string=""
        for key in self.dictionary.keys():
            string+=f"\nMyTab.dictionary[{key}]={self.dictionary[key]}"
        for key in self.dict_filter.keys():
            string+=f"\nMyTab.dict_filter[{key}]={self.dict_filter[key]}"
        string+=f"\nMyTab.error={self.error}"
        return string

    """
    Crea un dizionario e dizonario-filtro sula base di fields e rows passati in argomento
    """
    def create(self,fields,rows):
        if fields and rows and self.error==0:
            """"Inizializza le key sulla base di fileds e ne assegna una lista vuota"""
            for index in fields:
                self.dictionary[index]=[]
                self.dict_filter[index]=[]
            for row in rows:
                i=0
                for element in row:
                    self.dictionary[fields[i]].append(element)
                    if not element in self.dict_filter[fields[i]]:
                        self.dict_filter[fields[i]].append(element)
                    i+=1
            """Ordina il dizionario di supporto come filtro"""
            for key in self.dict_filter.keys():
                self.dict_filter[key].sort()
            return True
        else:
            return False

    """
    Restituisce un nuovo dizionario MyTab filtrato sulla base di key e value
    """
    def filter_by(self,key,value):
        new_fields=[]
        new_rows=[]
        sel_index=[]
        this_index=0
        for k in self.dictionary.keys():
            new_fields.append(k)
        for element in self.dictionary[key]:
            if element==value:
                row=[]
                for k in self.dictionary.keys():
                    #print(self.dictionary[k][this_index])
                    row.append(self.dictionary[k][this_index])
                    sel_index.append(this_index)
                new_rows.append(row)
            this_index+=1
        new_tab=MyTab()
        new_tab.create(new_fields,new_rows)
        return new_tab
