# ---------------------------------------------------------------
# rpc_client.py
# Diese Datei stellt Funktionen bereit, mit denen Daten
# vom HTTP-Server per RPC an die In-Memory-Datenbank gesendet
# oder gelesen werden können.
# ---------------------------------------------------------------

# -----------------------------------------
# 1. Import von Systempfaden und Thrift-Code
# -----------------------------------------

import sys
sys.path.append("gen-py")  # Fügt den Pfad hinzu, in dem die generierten Thrift-Dateien liegen

# -----------------------------------------
# 2. Import der benötigten Thrift-Komponenten
# -----------------------------------------

from thrift import Thrift
from thrift.transport import TSocket             # Für die TCP/IP-Kommunikation
from thrift.transport import TTransport         # Für Buffered Transport
from thrift.protocol import TBinaryProtocol     # Für binäres Datenprotokoll

# -----------------------------------------
# 3. Import des generierten Thrift-Interfaces
# -----------------------------------------

from rpc_database import DatabaseService        # Import des Service-Interfaces
from rpc_database.ttypes import Record          # Import der Datenstruktur "Record"

# -----------------------------------------
# 4. Hilfsfunktion: Verbindung aufbauen
# -----------------------------------------

def get_client():
    """
    Stellt eine RPC-Verbindung zur Datenbank her und gibt Client + Transport zurück.
    """
    # Verbindung zur RPC-Datenbank auf Port 9090 des Hostnamens 'rpc_db' herstellen
    transport = TSocket.TSocket('rpc_db', 9090)
    
    # Transport mit Buffering für effiziente Übertragung
    transport = TTransport.TBufferedTransport(transport)
    
    # Binäres Protokoll für effiziente Kommunikation wählen
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    
    # Client-Objekt erzeugen
    client = DatabaseService.Client(protocol)
    
    # Verbindung öffnen
    transport.open()
    
    return client, transport

# -----------------------------------------
# 5. Funktion: Datensatz senden (CREATE)
# -----------------------------------------

def send_to_rpc_db(data_string):
    """
    Sendet einen Datensatz per RPC an die In-Memory-Datenbank.
    """
    try:
        client, transport = get_client()

        import time
        # Erzeugt eine eindeutige ID basierend auf dem aktuellen Zeitstempel
        record_id = int(time.time() * 1000)
        
        # Erstellt einen neuen Datensatz mit ID und Dateninhalt
        record = Record(id=record_id, data=data_string)

        # Sendet den Datensatz an die Datenbank
        client.create(record)

        print(f"[RPC] Datensatz erfolgreich an RPC-Datenbank gesendet (ID: {record_id})")
        transport.close()

    except Thrift.TException as e:
        print(f"[RPC-Fehler] {e}")

# -----------------------------------------
# 6. Funktion: Alle Datensätze abrufen (READ ALL)
# -----------------------------------------

def get_all_records():
    """
    Holt alle gespeicherten Datensätze per RPC von der In-Memory-Datenbank.
    :return: Liste von Record-Objekten
    """
    records = []
    try:
        client, transport = get_client()

        # Holt alle IDs aus der Datenbank
        ids = client.list_ids()

        # Holt jeden Datensatz einzeln anhand der ID
        for id in ids:
            try:
                record = client.read(id)
                records.append(record)
            except:
                pass  # Fehlerhafte oder gelöschte Einträge werden ignoriert

        transport.close()
    except Thrift.TException as e:
        print(f"[RPC-Fehler] {e}")
    return records

# -----------------------------------------
# 7. Funktion: Datensatz aktualisieren (UPDATE)
# -----------------------------------------

def update_record(id, new_data):
    """
    Aktualisiert einen vorhandenen Datensatz mit neuer Information.
    :param id: ID des zu aktualisierenden Datensatzes
    :param new_data: Neuer Inhalt des Datensatzes
    """
    try:
        client, transport = get_client()
        client.update(id, new_data)
        print(f"[RPC] Datensatz mit ID {id} erfolgreich aktualisiert.")
        transport.close()
    except Thrift.TException as e:
        print(f"[RPC-Fehler] {e}")

# -----------------------------------------
# 8. Funktion: Datensatz löschen (DELETE)
# -----------------------------------------

def delete_record(id):
    """
    Löscht einen vorhandenen Datensatz anhand seiner ID.
    :param id: ID des zu löschenden Datensatzes
    """
    try:
        client, transport = get_client()
        client.erase(id)
        print(f"[RPC] Datensatz mit ID {id} erfolgreich gelöscht.")
        transport.close()
    except Thrift.TException as e:
        print(f"[RPC-Fehler] {e}")
