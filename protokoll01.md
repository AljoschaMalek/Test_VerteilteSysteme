# Messprotokoll 01

Elia Kaymer - 1119064
Aljoscha Malek - 1115211
Mohammed Chehab - 752002


## Ausgangslage
### Nicht-Funktionale Tests
Der Server läuft mit dem befehl "docker-compose up server" im Docker Container.
Er lauscht an Port 8080 und wartet auf http Requests.

Der Client läuft auch in einem Docker-Container ("docker-compose run client").  
Er sendet einen HTTP-POST-Request mit ausgedachten Sensordaten (Temperatur) an den Server.
Der Client selbst misst die RTT für sein eigenes Request und die Response vom Server.

Das ausführliche Testen läuft aber über ein lokales python skript, das den Docker-Client nutzt.
Das Skript schickt zehn HTTP-POST-Anfragen (es nutzt die Funktion des Clients und auch den Docker-Client selbst) nacheinander an den Server und misst dabei jedes Mal die RTT. 
Die gemessenen Zeiten werden am Ende ausgewertet (Durchschnitt, Minimum, Maximum, Standardabweichung).
In einem zweiten Durchgang haben wir 100 Tests durchgeführt und in einem dritten Durchgang 1000. 

### Funktionale Tests
Es wurden an vielen Stellen Fehlermeldungen eingebaut, falls Funktionen nicht korrekt ausgeführt werden konnten. Außerdem wurde die Funktionalität ebenfalls durch Terminalausgaben bestätitgt. 
Beispielsweise wenn der Server gestartet ist und anfängt auf 0.0.0.0:8080 zu lauschen gibt es eine Terminalausgabe oder wenn es eingehende Verbindungen von Clients zum Server gibt. Wird eine POST-Anfrage vom Client erfolgreich verschickt gibt er die Antwort des Servers in seinem Terminal aus. Die Anfragen wurden also korrekt verschickt, verarbeitet und beantwortet. Bei GET-Anfragen ist die html Seite auch korrekt verfügbar und neu hinzugefügte Daten werden dort angezeigt. Fehlermeldungen mussten zum Glück noch nicht greifen. 

## Ergebnisse
### 10 Durchläufe
1. Durchlauf:  0.00118s  
2. Durchlauf:  0.00116s  
3. Durchlauf:  0.00124s  
4. Durchlauf:  0.00128s  
5. Durchlauf:  0.00112s  
6. Durchlauf:  0.00112s  
7. Durchlauf:  0.00150s  
8. Durchlauf:  0.00106s  
9. Durchlauf:  0.00145s  
10. Durchlauf: 0.00112s

Durchschnittliche RTT: 0.001223s
Minimale RTT:          0.00106s
Maximale RTT:          0.00150s
Standardabweichung:    0.0001476s

### 100 Durchläufe
Durchschnittliche RTT: 0.0012404s
Minimale RTT:          0.00101s
Maximale RTT:          0.00424s
Standardabweichung:    0.000336s

### 1000 Durchläufe
Durchschnittliche RTT: 0.001218s
Minimale RTT:          0.00098s
Maximale RTT:          0.00787s
Standardabweichung:    0.00028589s

## Fazit
Die RTTs sind alle sehr stabil und es gibt keine wirklich relevanten Ausreißer. 
Alle RTTs liegen im Millisekundenbereich. 


