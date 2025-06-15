# Messprotokoll 01

Elia Kaymer - 1119064
Aljoscha Malek - 1115211
Mohammed Chehab - 752002

## RTT Tests von Aufgabe 3.2
Bei diesen Tests haben wir wie zuvor bei Aufgabe 3.2 die Zeiten gemessen, die von der Versendung der von HTTP-Post vom IoT-Gateway bis zur Antwort des Servers vergehen.
Dieses mal speichert der Server die Daten aber nicht lokal, sondern in der rpc_database.

### Bei 100 Durchläufen
Durchschnittliche RTT: 0.00286s
Minimale RTT:          0.00206s
Maximale RTT:          0.00976s
Standardabweichung:    0.00110s

Wenn wir das mit dem Tests mit 100 Durchläufen von Protokoll01 vergleichen fällt auf, dass sich die Kommunikationsdauer mehr als verdoppelt hat.

| Metrik              | Ohne RPC (3.2) | Mit RPC (3.3) | Veränderung    |
|---------------------|----------------|---------------|----------------|
| Durchschnitt RTT    | 0.001240 s     | 0.002858 s    | 🔺 +130%       |
| Minimale RTT        | 0.00101 s      | 0.00206 s     | 🔺 +104%       |
| Maximale RTT        | 0.00424 s      | 0.00976 s     | 🔺 +130%       |
| Standardabweichung  | 0.000336 s     | 0.001100 s    | 🔺 +227%       |

### Bei 1000 Durchläufen
Durchschnittliche RTT: 0.00269591s
Minimale RTT:          0.00193s
Maximale RTT:          0.01272s
Standardabweichung:    0.0008187763837988164s

Auch hier gab es bei fast allen Metriken eine Verdopplung der gemessenen Kommunikationsdauer


| Metrik              | Ohne RPC (3.2) | Mit RPC (3.3) | Veränderung    |
|---------------------|----------------|---------------|----------------|
| Durchschnitt RTT    | 0.001218 s     | 0.002696 s    | 🔺 +121%       |
| Minimale RTT        | 0.00098 s      | 0.00193 s     | 🔺 +97%        |
| Maximale RTT        | 0.00787 s      | 0.01272 s     | 🔺 +61%        |
| Standardabweichung  | 0.00028589 s   | 0.00081878 s  | 🔺 +186%       |


## RPC Tests
Bei diesen Tests haben wir ausschließlich die Response Time zwischen dem RPC_Clent und dem RPC_Server (RPC_Database) gemessen.


### Bei 100 Durchläufen
Durchschnittliche Response Time: 0.00211 s  
Minimale Response Time:          0.00073 s  
Maximale Response Time:          0.00438 s  
Standardabweichung:              0.00105 s


### Bei 1000 Durchläufen
Durchschnittliche Response Time: 0.00210 s  
Minimale Response Time:          0.00085 s  
Maximale Response Time:          0.00934 s  
Standardabweichung:              0.00099 s

Eine große Differenz zu den 100 Durchläufen gibt es nicht, das zeigt die durchscnittliche Response Time. 
Der reine RPC-Test zeigt im Vergleich mit dem HTTP + RPC Test, dass ein Großteil der Latenz, wohl an den RPC-Komponenten liegt.