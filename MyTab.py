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
    """
    Restituisce il numero di righe della tabella
    """
    def rows_number(self):
        lastkey=list(self.dictionary.keys())[-1]
        return len(self.dictionary[lastkey])
    """
    Restituisce un nuovo MyTab raggruppato per groupkey e con i valori di sumkey sommati
    per ogni valore di groupkey
    """
    def group_by_sum_by(self,groupkey,sumkey):
        new_rows=[]
        new_fields=[]
        for value in self.dict_filter[groupkey]:
            supp_tab=self.filter_by(groupkey,value)
            total=0
            for num in supp_tab.dictionary[sumkey]:
                total+=int(num)
            row=[]
            for key in supp_tab.dict_filter.keys():
                if not key==sumkey:
                    row.append(supp_tab.dict_filter[key][0])
                else:
                    row.append(total)
            new_rows.append(row)
        for key in self.dict_filter.keys():
            new_fields.append(key)
        new_tab=MyTab()
        new_tab.create(new_fields,new_rows)
        return new_tab

    """
    Restituisce una lista di righe della tabella
    """
    def give_rows(self):
        new_rows=[]
        for i in range(self.rows_number()):
            row=[]
            for key in self.dictionary.keys():
                row.append(self.dictionary[key][i])
            new_rows.append(row)
        return new_rows
    """
    Restituisce una lista delle chiavi del dizionario
    """
    def give_fields(self):
        return self.dictionary.keys():
    """
    Restituisce un nuovo MyTab con contenuti selezionati e ordinati sulla base della lista di chiavi
    """
    def make_sub_tab(self,keys):
        new_dictionary={}
        for key in keys:
            for oldkey in self.dictionary.keys():
                if oldkey==key:
                    new_dictionary[key]=self.dictionary[key]
        new_tab=MyTab()
        new_tab.create_from(new_dictionary)
        return new_tab
    """
    Crea un dizionario e dizonario-filtro sula base del dizionario passato in argomento
    """
    def create_from(self,old_dictionary):
        self.dictionary=old_dictionary
        for key in self.dictionary.keys():
            self.dict_filter[key]=[]
            for element in self.dictionary[key]:
                    if not element in self.dict_filter[key]:
                        self.dict_filter[key].append(element)
            for key in self.dict_filter.keys():
                self.dict_filter[key].sort()
