class art_index:
    """
    Inizializzazione di tutte le variabili di classe
    """
    def __init__(self):
        self.reset()
    """
    Reset di tutti gli attributi di classe
    """
    def reset(self):
        self.codice=[]
        self.colore=[]
        self.tipo=[]
        self.densita=[]
        self.porosita=[]
        self.misura=[]
        self.altezza=[]

    def index_add(self,index,item):
        present = False
        for this in index:
            if this==item:
                present=True
        if not present:
            index.append(item)
            return True
        else:
            return False

    def create_index(self,mycsvfile):
        for row in mycsvfile.rows:
            self.index_add(self.codice,row[0])
            self.index_add(self.colore,row[1])
            self.index_add(self.tipo,row[2])
            self.index_add(self.densita,row[3])
            self.index_add(self.porosita,row[4])
            self.index_add(self.misura,row[5])
            self.index_add(self.altezza,row[6])

    def __str__(self):
        string=f"Istance of art_index:"
        string+=f"\ncodice={self.codice}"
        string+=f"\ncolore={self.colore}"
        string+=f"\ntipo={self.tipo}"
        string+=f"\ndensita={self.densita}"
        string+=f"\nporosita={self.porosita}"
        string+=f"\nmisura={self.misura}"
        string+=f"\naltezza={self.altezza}"
        return string
