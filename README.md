# BeatToBeat — Music Streaming Service

**Studente:** Elia Moracci
**Tipo di progetto:** Full-Stack Web Application (Music Streaming Service)
**Framework:** Django 5.x — Django Template Language, HTML/CSS scritti a mano (nessun framework CSS)
**Database:** SQLite in locale (incluso nella repo), PostgreSQL in produzione
**Link deploy:** _(da inserire dopo il deploy su Railway)_

---

## Descrizione

BeatToBeat è un servizio di music streaming realizzato con Django, secondo
l'architettura monolitica Model-View-Template. L'applicazione modella un catalogo
musicale con generi, brani e playlist, e implementa un sistema di ruoli con permessi
applicati nel codice (non solo descritti) e riflessi nell'interfaccia.

Questa è l'**ossatura** del progetto (Fase 1): scaffolding, modelli, autenticazione,
CRUD con permessi, template e dati demo. Le funzionalità aggiuntive (ruolo Moderator,
file audio e player, like, commenti, amicizie, profili, ecc.) vengono aggiunte nella
fase successiva.

## Funzionalità per ruolo

### Ospite (non autenticato)
- Registrazione (ogni nuovo account nasce come **Listener**) e login/logout.

### Listener (utente standard)
- Sfoglia il catalogo, con **ricerca** per titolo/artista e **filtro per genere**.
- Consulta la pagina di dettaglio di ogni brano.
- Crea e gestisce le proprie **playlist** (CRUD completo riservato all'owner) e vi
  aggiunge/rimuove brani.

### Curator
- Tutti i permessi del Listener, più il **CRUD completo su brani e generi** del
  catalogo (creazione, modifica, eliminazione dall'interfaccia).

### Administrator (superuser)
- Accesso al pannello di amministrazione Django (`/admin/`) per gestire ogni entità.

## Modello dati

- `CustomUser` (estende `AbstractUser`) con campo `role` (Listener/Curator) allineato
  ai gruppi Django omonimi.
- `Genre`, `Song` (FK a `Genre` e all'utente che l'ha aggiunta), `Playlist`
  (FK owner + M2M con `Song`) → relazioni **ForeignKey** e **ManyToMany**.

## Installazione locale

**Requisiti:** Python 3.11+

```bash
# 1. Clona il repository
git clone <url-del-repo>
cd BeatToBeat

# 2. Crea e attiva l'ambiente virtuale
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Installa le dipendenze
pip install -r requirements.txt

# 4. Applica le migrazioni (il db.sqlite3 incluso è già popolato)
python manage.py migrate

# 5. Avvia il server di sviluppo
python manage.py runserver
```

L'applicazione è raggiungibile su `http://127.0.0.1:8000`.

### Database e dati demo

Il file **`db.sqlite3`** è incluso nella repository e contiene già i dati demo
(account, generi, brani, playlist). Per rigenerarli da zero:

```bash
python seed_data.py
```

## Account demo

| Username | Password | Ruolo |
|---|---|---|
| `admin_demo` | `admin12345` | Administrator (superuser) |
| `curator_demo` | `curator12345` | Curator |
| `listener_demo` | `listener12345` | Listener |
| `alice` / `bob` | `password123` | Listener |

## Scenario di test (browser)

1. **Login** come `listener_demo` (`listener12345`).
2. Vai al **Catalogo**: prova la ricerca e il filtro per genere.
3. Apri un brano e aggiungilo a una playlist; vai in **Playlist**, crea una nuova
   playlist e aggiungi/rimuovi brani.
4. **Azione vietata**: da Listener, visita manualmente `/music/songs/add/` →
   ottieni un **403 Forbidden** (i Listener non possono modificare il catalogo).
5. **Login** come `curator_demo` (`curator12345`): ora nel catalogo compaiono i
   pulsanti **+ Aggiungi brano** e **Gestisci generi**; crea/modifica/elimina un brano.
6. **Login** come `admin_demo` (`admin12345`) e apri il **pannello Admin**.

## Deploy (Railway)

In produzione il progetto usa PostgreSQL se la variabile d'ambiente `DATABASE_URL`
è presente, altrimenti resta su SQLite. Variabili d'ambiente previste: `SECRET_KEY`,
`DEBUG`, `DATABASE_URL`, `RAILWAY_PUBLIC_DOMAIN`. I file statici sono serviti da
WhiteNoise. Configurazione già predisposta in `Procfile`, `runtime.txt` e
`requirements.txt`.
