import socket  # Modul für die Netzwerkkommunikation
from threading import Thread  # Modul für Multithreading, um mehrere Clients gleichzeitig zu bedienen

# ----------------------------------------------------
# NEU für Aufgabe 3.3 (RPC): Import aus rpc_client.py
# Import funktioniert auch im Docker-Container
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Fügt ./server dem Python-Pfad hinzu
from rpc_client import send_to_rpc_db, get_all_records  # RPC-Funktionen importieren
# ----------------------------------------------------

# Server-Konfiguration
HOST = '0.0.0.0'  # Der Server lauscht auf allen verfügbaren Netzwerkadressen
PORT = 8080       # Der Server lauscht auf Port 8080

# ALT: Für Aufgabe 3.2 – lokale Liste zum Speichern von empfangenen Daten
# data_store = []

# Funktion zur Verarbeitung eines einzelnen Clients
def handle_client(conn, addr):
    print(f"[+] Neue Verbindung: {addr}")  # Log-Ausgabe bei neuer Verbindung
    data = b""  # Variable zum Speichern der empfangenen Daten
    while True:
        chunk = conn.recv(1024)  # Empfang von Daten in 1024-Byte-Blöcken
        if not chunk:
            break
        data += chunk
        if b"\r\n\r\n" in data:
            break

    # Verarbeitung der empfangenen Anfrage
    request = data.decode()
    headers, _, body = request.partition('\r\n\r\n')
    method = headers.split(' ')[0]
    path = headers.split(' ')[1]

    # --------------------------------------
    # POST-Anfrage: Neue Daten empfangen
    # --------------------------------------
    if method == "POST" and path == "/":
        # --------------------------------------
        # ALT: Für Aufgabe 3.2 – lokal speichern:
        # data_store.append(body)
        # --------------------------------------

        # --------------------------------------
        # NEU: Für Aufgabe 3.3 – per RPC speichern:
        send_to_rpc_db(body)
        # --------------------------------------

        response = "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK"

    # --------------------------------------
    # GET-Anfrage: Daten im Browser anzeigen
    # --------------------------------------
    elif method == "GET" and path == "/":
        # --------------------------------------
        # ALT: Daten aus lokaler Liste anzeigen
        # html = "<html><body><h1>Empfangene Daten</h1><pre>{}</pre></body></html>".format("\n".join(data_store))
        # response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(html)}\r\n\r\n{html}"
        # --------------------------------------

        # --------------------------------------
        # NEU: Für Aufgabe 3.3 – Daten per RPC abrufen:
        records = get_all_records()
        html_entries = "\n".join(f"{r.id}: {r.data}" for r in records)
        html = f"<html><body><h1>Empfangene Daten (via RPC)</h1><pre>{html_entries}</pre></body></html>"
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(html)}\r\n\r\n{html}"
        # --------------------------------------

    elif method not in ["GET", "POST"]:
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
    else:
        response = "HTTP/1.1 404 Not Found\r\nContent-Length: 13\r\n\r\n404 Not Found"

    conn.sendall(response.encode())
    conn.close()

# Hauptprogramm: Startet den Server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[i] Server lauscht auf {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        Thread(target=handle_client, args=(conn, addr)).start()
