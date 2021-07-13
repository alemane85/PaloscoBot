"""
MyCsv.py
"""

import os
import csv


"""
-MyCsvFile-
    Classe personale per una gestione semplificata dei File CSV
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
class MyCsvFile:
    """
    Inizializzazione di tutte le variabili di classe
    """
    def __init__(self):
        self.reset()
    """
    Reset di tutti gli attributi di classe
    """
    def reset(self):
        self.path=""
        self.name=""
        self.fields=[]
        self.rows=[]
        self.delimiter=","
        self.quotechar=''
        self.quoting=csv.QUOTE_NONE
        self.escapechar="$"
        self.error=0
    """
    Restituisce in forma di stringa una fotografia della classe in quel momento
    utile in fase di controllo
    """
    def __str__(self):
        string=f"Istance of MyCsvFile:"
        string+=f"\npath={self.path}"
        string+=f"\nname={self.name}"
        string+=f"\nfields={self.fields}"
        if not self.rows:
            string+=f"\nrows={self.rows}"
        else:
            i=0
            for row in self.rows:
                string+=f"\nrow[{i}]={row}"
                i+=1
        string+=f"\ndelimiter={self.delimiter}"
        string+=f"\nquotechar={self.quotechar}"
        string+=f"\nquoting={self.quoting}"
        string+=f"\nescapechar={self.escapechar}"
        string+=f"\nerror={self.error}"
        return string
    """
    Compara i fields con la prima riga del reader assicurarsi che sia il csv adatto
    """
    def IsMyCsvFile(self,reader,fields):
        try:
            """Leggi la prima riga e compara con fields"""
            first_row=next(reader)
            if first_row==fields:
                return True
            else:
                raise MyCsvError()
        except Exception as this_error:
            self.error=type(this_error).__name__
            return False
    """
    Controlla il file obj se è un Csv corretto
    """
    def IsCsvFile(self,file):
        try:
            sample=file.read(1024)
            """Check di presenza di char non stampabili"""
            #if not all([c in string.printable or c.isprintable() for c in tab]):
            #raise MyCsvError()
            """Check presenza di dialetto"""
            dialect = csv.Sniffer().sniff(sample)
            file.seek(0)
        except csv.Error as this_error:
            """Cattura l'errore csv.Error: torna falso e assegna l'errore alla variabile di classe"""
            self.error=type(this_error).__name__
            file.seek(0)
            return False
        return True
    """
    Carica il file indicato in fullpath che rispetta i fields specificati.
    Se valido e il caricamento è andato bene ritorna True
    """
    def load(self,fullpath,fields=0):
        try:
            with open(fullpath,'r',newline='') as csvfile:
                if not self.IsCsvFile(csvfile):
                    return False
                reader=csv.reader(csvfile, delimiter=self.delimiter, quotechar=self.quotechar, quoting=self.quoting)
                if fields!=0:
                    """Fai il check su fields se valorizzato"""
                    if not self.IsMyCsvFile(reader,fields):
                        return False
                """
                Arrivati qui tutti i check sono positivi quindi
                popola le variabili di classe
                """
                self.path,self.name=os.path.split(fullpath)
                csvfile.seek(0)
                self.fields=next(reader)
                for row in reader:
                    self.rows.append(row)
        except Exception as this_error:
            self.error=type(this_error).__name__
            return False
        self.error=0
        return True
    """
    Salva il file di name e path
    Se specificato con le nuove righe e testata.
    Ritorna True se il salvataggio è andato bene
    """
    def save(self):
        fullpath=os.path.join(self.path,self.name)
        return self.saveas(fullpath)

    """
    Salva il file in fullpath
    Se specificato con le nuove righe e testata.
    Ritorna True se il salvataggio è andato bene
    """
    def saveas(self,fullpath):
        self.path,self.name=os.path.split(fullpath)
        try:
            if not os.path.lexists(self.path):
                raise PathError()
                return False
            with open(fullpath,'w',newline='') as csvfile:
                    writer=csv.writer(csvfile,
                                        delimiter=self.delimiter,
                                        quotechar=self.quotechar,
                                        quoting=self.quoting,
                                        escapechar=self.escapechar)
                    writer.writerow(self.fields)
                    for row in self.rows:
                        writer.writerow(row)
        except csv.Error as this_error:
            """Cattura l'errore csv.Error: torna falso e assegna l'errore alla variabile di classe"""
            self.error=type(this_error).__name__
            return False
        except Exception as this_error:
            self.error=type(this_error).__name__
            return False
        self.error=0
        return True

"""
-MyCsvError-
    Classe personale per una gestione semplificata di Errori in MyCsv
    derivata da Exception per File non supportato
"""
class MyCsvError(Exception):
    def __init__(self,message="File non supportato!"):
        super().__init__(message)

    def __str__(self):
        return super().__str__()

"""
-PathError-
    Classe personale per una gestione semplificata di Errori in MyCsv
    derivata da Exception per path errato
"""
class PathError(Exception):
    def __init__(self,message="Percorso di salvataggio non valido"):
        super().__init__(message)

    def __str__(self):
        return super().__str__()
