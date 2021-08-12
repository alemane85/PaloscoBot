import base64
import os
import io
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import pandas as pd
from am_db import dbinterface as dbi

if __name__ == "__main__":
    password = "password"
    miodb = dbi("prova_enc.txt", password, salt_file="key.key")
    data = miodb.read()
    # file=decrypt("prova_enc.txt",password).decode("utf-8")
    #data = io.StringIO(file)
    df = pd.read_csv(data, sep=",")
    # more options can be specified also
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        for key in df["CODICE"].unique():
            total = df[df["CODICE"] == key]["QUANTITA"].sum()
            print(f"codice={key} totale={total}")
    # more options can be specified also
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)
    dataout = df.to_csv(index=False)
    # new_line="\n31/07/2021,10:23:21,Alemane85,3,TAGLIO,MERDA,ARANCIO,LASTRA,300,F,1340X880,H20,100,05/08/2021"
    # miodb.append(new_line)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
