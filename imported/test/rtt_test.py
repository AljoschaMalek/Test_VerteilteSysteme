import statistics   # zum Berechnen von Min, Max und Standardabweichung
import subprocess   # Zum Ausführen von Terminalbefehlen (Docker-Client)
import re           # Zum Herausfiltern der RTT-Werte aus der Textausgabe (Regex)

rtts = []       # Liste zum Speichern der RTTs
anzahl_tests = 1000   # Anzahl der Wiederholungen festlegen

print(f"Starte Test mit {anzahl_tests} Durchläufen ...")   # Hinweis zu Beginn

for i in range(anzahl_tests):     # Wiederholen des Ganzen n-mal
    # Starte den Client-Container und sammle die Ausgabe (nur stdout)
    result = subprocess.run(
        ["docker-compose", "run", "--rm", "client"],   # "--rm" löscht den Container nach dem Lauf
        stdout=subprocess.PIPE,                        # Terminalausgabe speichern
        stderr=subprocess.DEVNULL,                     # unterdrückt Warnmeldungen von docker-compose 
        text=True                                      # gib die Ausgabe als String zurück
    )

    output = result.stdout     # Speichern der Ausgabe

    # Suche nach einer Zeile wie: "RTT: 0.00123 Sekunden"
    match = re.search(r"RTT: ([\d.]+) Sekunden", output)    # Zahl wird durch ([\d.]+) speichert Zahl nochmal extra in Gruppe 1
    if match:
        rtt = float(match.group(1))                      # RTT-Wert aus Gruppe 1 extrahieren und in float umwandeln 
        rtts.append(rtt)                                 # Wert zur Liste hinzufügen

# Durchschnittliche RTT und statistische Werte ausgeben
if rtts:        # "wenn die Liste nicht leer ist"
    print("\nTest abgeschlossen.\n")
    print("Anzahl gültiger RTT-Werte:", len(rtts))    # Wie viele Werte wurden überhaupt erfolgreich gemessen
    print("Durchschnitt RTT:", statistics.mean(rtts))            # Durchschnittliche RTT ausgeben
    print("Min:", min(rtts), "Max:", max(rtts), "StdDev:", statistics.stdev(rtts))  # Min, Max und Standardabweichung ausgeben
else:
    print("Keine RTT-Werte gefunden.")   # Fehlermeldung

