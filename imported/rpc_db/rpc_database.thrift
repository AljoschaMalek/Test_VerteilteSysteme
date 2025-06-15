// Dieses "namespace" sorgt dafür, dass die generierten Python-Dateien
// in einem sauberen Python-Modul namens `rpc_database` landen.
namespace py rpc_database

// ---------------------------------------------
// Strukturdefinition für einen Datensatz
// ---------------------------------------------
struct Record {
  1: i64 id,        // Eindeutige ID des Eintrags (z. B. vom Client generiert)
  2: string data    // Beliebige Nutzdaten, z. B. "temperature=22.5"
}

// ---------------------------------------------
// RPC-Service mit vollständigem CRUD-Interface
// ---------------------------------------------
service DatabaseService {

  // Speichert einen neuen Datensatz in der Datenbank
  void create(1: Record record),

  // Gibt einen vorhandenen Datensatz anhand seiner ID zurück
  Record read(1: i64 id),

  // Aktualisiert den Datensatz mit neuer Information
  void update(1: i64 id, 2: string data),

  // Löscht einen Datensatz anhand seiner ID
  void erase(1: i64 id),
  
  // Gibt eine Liste aller gespeicherten IDs zurück
  list<i64> list_ids()
}

