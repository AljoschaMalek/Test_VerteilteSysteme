# --------------------------------------------------
# rpc_database_server.py
# Thrift-RPC-Server für die In-Memory-Datenbank
# Startet den Server, der CRUD-Anfragen über RPC entgegennimmt
# --------------------------------------------------

# -----------------------------
# 1. Import generierter Thrift-Code
# -----------------------------

# Damit Python den generierten Code aus dem Ordner gen-py findet,
# erweitern wir den Suchpfad (sys.path).
# Das ist notwendig, weil der Thrift-Compiler den Code dort abgelegt hat.
import sys
sys.path.append("gen-py")  # relativer Pfad zum generierten Thrift-Code

# -----------------------------
# 2. Import Thrift-Bibliothek
# -----------------------------

# Diese Module werden für den Netzwerk-Transport, das Protokoll
# und den Serverbetrieb benötigt.
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

# -----------------------------
# 3. Import der Logik
# -----------------------------

# Import der Handler-Klasse
# implementiert die Methoden: create, read, update, erase
from rpc_database_handler import DatabaseHandler

# -----------------------------
# 4. Import der generierten Service-Schnittstelle
# -----------------------------

# Diese Datei wurde vom Thrift-Compiler auf Basis deiner .thrift-Datei erstellt.
# Sie enthält das Interface "DatabaseService", das der Server bedienen muss.
from rpc_database import DatabaseService

# -----------------------------
# 5. Initialisiere die Logik
# -----------------------------

# NEU: Deutliche Startmeldung für das Terminal
print("[i] Starte RPC-Datenbankserver...")  # ← Sichtbare Bestätigung

# Erzeuge eine Instanz deiner Handler-Klasse, also der Datenbank
handler = DatabaseHandler()

# Binde den Handler an das Thrift-Service-Interface (DatabaseService)
# Der Processor ist die Brücke zwischen "außen" (RPC-Anfrage) und "innen" (dein Python-Code)
processor = DatabaseService.Processor(handler)

# -----------------------------
# 6. Server-Transport konfigurieren
# -----------------------------

# Erzeuge einen TCP-Server-Socket, der auf Port 9090 lauscht.
# 0.0.0.0 bedeutet: Der Server akzeptiert Verbindungen von überall.
transport = TSocket.TServerSocket(host='0.0.0.0', port=9090)

# Konfiguriere den Transport-Puffer (wie die Daten intern übertragen werden)
tfactory = TTransport.TBufferedTransportFactory()

# Konfiguriere das Datenformat: Thrift nutzt standardmäßig ein binäres Format
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

# -----------------------------
# 7. Starte den Thrift-Server
# -----------------------------

# Der TSimpleServer verarbeitet Anfragen nacheinander (ein Thread)
# Du kannst später auch TThreadPoolServer verwenden, wenn du parallele Anfragen brauchst.
server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

# Statusmeldung – hilfreich beim Debuggen in Docker oder lokal
print("[✓] RPC-Datenbankserver läuft auf Port 9090 ...")

# Jetzt wird der Server gestartet und bleibt an dieser Stelle blockiert,
# bis er manuell beendet wird (z. B. mit STRG+C oder Docker-Stop)
server.serve()

# Diese Zeile wird erst erreicht, wenn der Server stoppt
print("[x] Server wurde beendet.")
