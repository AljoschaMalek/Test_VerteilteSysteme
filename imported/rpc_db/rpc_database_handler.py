# -----------------------------------------------------------
# rpc_database_handler.py
# Diese Datei enthält die Logik für die In-Memory-Datenbank.
# Sie implementiert die vom Thrift-Interface definierten Methoden.
# -----------------------------------------------------------

# -----------------------------------------------------------
# Import der generierten Thrift-Komponenten
# -----------------------------------------------------------

import sys
sys.path.append("gen-py")  # Damit Python den generierten Thrift-Code findet

from rpc_database import DatabaseService  # Thrift-Service-Interface
from rpc_database.ttypes import Record    # Thrift-Datenstruktur (Record)

# -----------------------------------------------------------
# Die Handler-Klasse implementiert die Methoden aus .thrift
# -----------------------------------------------------------

class DatabaseHandler:
    def __init__(self):
        # Einfache In-Memory-Datenbank (dict mit ID als Schlüssel)
        self.storage = {}

    # -------------------------
    # CREATE
    # -------------------------
    def create(self, record):
        if record.id in self.storage:
            print(f"[!] WARNUNG: ID {record.id} existiert bereits. Überschreibe den Eintrag.")
        else:
            print(f"[+] Neuer Datensatz empfangen: ID={record.id}, Inhalt='{record.data}'")
        self.storage[record.id] = record
        print(f"[✓] Datensatz mit ID {record.id} gespeichert.")

    # -------------------------
    # READ
    # -------------------------
    def read(self, id):
        if id in self.storage:
            print(f"[i] Datensatz mit ID {id} gelesen.")
            return self.storage[id]
        else:
            print(f"[!] FEHLER: Datensatz mit ID {id} nicht gefunden.")
            raise Exception(f"Datensatz mit ID {id} existiert nicht.")

    # -------------------------
    # UPDATE
    # -------------------------
    def update(self, id, data):
        if id in self.storage:
            old = self.storage[id].data
            self.storage[id].data = data
            print(f"[~] Datensatz mit ID {id} aktualisiert: '{old}' → '{data}'")
        else:
            print(f"[!] FEHLER: Kein Datensatz mit ID {id} zum Aktualisieren vorhanden.")
            raise Exception(f"Datensatz mit ID {id} existiert nicht.")

    # -------------------------
    # DELETE (in .thrift: erase)
    # -------------------------
    def erase(self, id):
        if id in self.storage:
            del self.storage[id]
            print(f"[-] Datensatz mit ID {id} gelöscht.")
        else:
            print(f"[!] FEHLER: Kein Datensatz mit ID {id} zum Löschen vorhanden.")
            raise Exception(f"Datensatz mit ID {id} existiert nicht.")

    # -------------------------
    # LIST_IDS – alle gespeicherten IDs zurückgeben
    # -------------------------
    def list_ids(self):
        print(f"[i] Liste aller gespeicherten IDs angefragt.")
        return list(self.storage.keys())
