import time
import statistics
from rpc_client import send_to_rpc_db

anzahl_tests = 1000  # Anzahl der Testdurchläufe
zeiten = []         # Liste für gemessene Antwortzeiten
fehler = 0          # Fehlerzähler

print(f"Starte RPC-Test mit {anzahl_tests} Durchläufen...")

for i in range(anzahl_tests):
    try:
        start = time.time()
        send_to_rpc_db(f"testdaten {i}")
        ende = time.time()
        zeiten.append(ende - start)
    except Exception as e:
        fehler += 1
        print(f"[Fehler bei Durchlauf {i}]: {e}")

# Statistische Auswertung
if zeiten:
    print("\nTest abgeschlossen.")
    print(f"Durchläufe: {anzahl_tests} | Erfolgreich: {len(zeiten)} | Fehler: {fehler}")
    print("Durchschnitt: {:.5f}s | Min: {:.5f}s | Max: {:.5f}s | StdDev: {:.5f}s".format(
        statistics.mean(zeiten),
        min(zeiten),
        max(zeiten),
        statistics.stdev(zeiten) if len(zeiten) > 1 else 0.0
    ))
else:
    print("Keine gültigen Antwortzeiten gemessen.")
