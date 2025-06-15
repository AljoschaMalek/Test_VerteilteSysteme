# Basisimage mit Python 3.11
FROM python:3.11-slim

# Arbeitsverzeichnis im Container setzen
WORKDIR /app

# Thrift-Compiler installieren (für Apache Thrift)
RUN apt-get update && apt-get install -y thrift-compiler

# Python-Abhängigkeiten installieren
RUN pip install thrift

# Projektdateien in den Container kopieren
COPY . .

# Thrift-Server starten
CMD ["python", "-u", "rpc_database_server.py"]