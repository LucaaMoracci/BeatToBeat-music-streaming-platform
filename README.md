# BeatToBeat — Music Streaming Service

**Studente:** Luca Moracci
**Tipo di progetto:** Full-Stack Web Application — Music Streaming Service
**Framework:** Django 5.x (Django Template Language, HTML/CSS scritti a mano — nessun framework CSS — e JavaScript vanilla)
**Database:** SQLite in locale (incluso nella repo), PostgreSQL in produzione
**Link di deploy:** 

---

## Descrizione

BeatToBeat è un servizio di music streaming sviluppato con Django secondo l'architettura
monolitica **Model-View-Template**. L'applicazione modella un catalogo musicale (generi,
brani, playlist) e implementa un sistema di **ruoli con permessi applicati nel codice** e
riflessi nell'interfaccia, non solo descritti.

Oltre alle normali operazioni CRUD, il progetto include: riproduzione audio con un player
fisso in fondo alla pagina, **rilevamento automatico della durata** dei brani dal file
audio caricato (lato browser, in JavaScript), like e commenti asincroni, **playlist
collaborative con sistema di inviti da accettare**, **cronologia degli ascolti** con pagine
dedicate paginate, e una **moderazione dei commenti con report motivato**. Il livello dati
modella diverse relazioni (ForeignKey e Many-to-Many) per supportare playlist, collaboratori,
follower, like e cronologia. L'obiettivo è realizzare un'applicazione web interattiva che
riproduca i pattern architetturali di una piattaforma di streaming, interamente nell'ecosistema
Django.

---

## Funzionalità per ruolo

L'applicazione usa un **modello utente personalizzato** (`AbstractUser`) con avatar a scelta:
un'**immagine caricata** dall'utente oppure, in mancanza, un avatar generato dall'iniziale
(colore deterministico per utente). Il controllo degli accessi è basato sui ruoli.

### Ospite (utente non autenticato)
- **Autenticazione**: login e logout nativi di Django.
- **Registrazione**: chiunque può creare un account dal browser. Per sicurezza ogni nuovo
  account nasce con il ruolo base **Listener**.

### Listener (utente standard)
- **Catalogo**: sfoglia i brani con **ricerca** per titolo/artista, **filtro per genere** e
  filtro **"Con audio"**.
- **Riproduzione**: player fisso in fondo alla pagina per i brani dotati di file audio, con
  play/pausa, barra di avanzamento e conteggio ascolti aggiornato in tempo reale. La
  riproduzione **riprende dalla stessa posizione anche cambiando pagina** (lo stato è salvato
  in `sessionStorage` e ripristinato al caricamento).
- **Playlist**: crea e gestisce le proprie playlist (CRUD riservato all'owner), con visibilità
  **privata / pubblica / editoriale**; aggiunge e rimuove brani.
- **Playlist collaborative**: l'owner può **invitare** altri utenti; l'invito diventa attivo
  **solo dopo l'accettazione** dell'invitato, che può quindi aggiungere/rimuovere brani.
- **Salvataggi**: segue e salva nella propria libreria le playlist pubbliche o editoriali di
  altri utenti.
- **Interazioni**: mette like ai brani (in modo asincrono) e commenta; può mettere like ai
  commenti.
- **Profilo**: visualizza e modifica il proprio profilo (**immagine profilo** caricabile con
  fallback all'avatar-iniziale, bio, data di nascita, genere preferito). Consulta i profili
  pubblici degli altri utenti (ruolo, commenti recenti, playlist pubbliche).
- **Cronologia ascolti**: sezione "Ascoltati di recente" in home e "Cronologia ascolti" nel
  profilo, con **pagine dedicate paginate** (cronologia completa e brani piaciuti).
- **Suggerimenti**: la home propone i brani del **genere preferito** dell'utente, le novità e
  i più piaciuti.

### Curator
- Tutti i permessi del Listener, più il **CRUD completo su brani e generi** dall'interfaccia.
- **Storia del brano**: può aggiungere un breve racconto mostrato nella pagina del brano.
- **Caricamento audio con durata automatica**: caricando un file audio, uno script JavaScript
  ne legge i metadati e **compila automaticamente la durata**, senza inserimento manuale.
- **Playlist editoriali**: può creare playlist editoriali in evidenza per tutti gli utenti.

### Moderator
- **Moderazione dei commenti**: può rimuovere qualsiasi commento. La rimozione passa da una
  **schermata di report** in cui indica la **motivazione**; ogni intervento viene registrato.
- **Registro di moderazione**: pagina con lo storico dei commenti rimossi e delle relative
  motivazioni.

### Administrator (superuser)
- **Pannello di amministrazione** Django (`/admin/`) per gestire nativamente tutte le tabelle e
  le relazioni del database.
- Possiede anche i permessi di Curator e Moderator; può assegnare o revocare i ruoli e
  intervenire su ogni entità aggirando le restrizioni del frontend.

---

## Note tecniche

- **Ruoli e permessi**: applicati nelle view tramite `LoginRequiredMixin`, un mixin
  personalizzato `CuratorOnlyMixin` (che restituisce **403** agli autenticati senza permesso e
  reindirizza al login gli anonimi) e controlli espliciti per il moderatore.
- **Class-based view**: il progetto usa ampiamente le generic CBV (`ListView`, `DetailView`,
  `CreateView`, `UpdateView`, `DeleteView`, `TemplateView`), con paginazione (`paginate_by`).
- **Validazione input**: tramite `ModelForm`, con messaggi di errore chiari.
- **Frontend**: HTML + CSS scritti a mano (tema scuro in stile piattaforma di streaming),
  senza Bootstrap; interazioni con JavaScript vanilla (like, player, durata automatica).
- **File audio**: l'app accetta `mp3`, `wav`, `ogg`, `m4a`. La demo include **due tracce audio
  generate** (`.wav`, royalty-free) collegate a due brani, con **durata coincidente con il
  file** per dimostrare il rilevamento automatico; le altre durate sono valori demo
  rappresentativi. Il rilevamento della durata avviene lato browser al momento del caricamento,
  quindi è indipendente dal formato.
- **Produzione**: file statici serviti da WhiteNoise; database PostgreSQL configurato via
  variabile d'ambiente `DATABASE_URL` (con `dj-database-url`); server WSGI `gunicorn`.

---

## Installazione in locale

**Requisiti:** Python 3.10+

**1. Clona la repository**
```bash
git clone https://github.com/LucaaMoracci/BeatToBeat-music-streaming-platform.git
cd BeatToBeat-music-streaming-platform
```

**2. Crea e attiva l'ambiente virtuale**

Su Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```
Su macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Installa le dipendenze**
```bash
pip install -r requirements.txt
```

**4. Applica le migrazioni** (non strettamente necessario: `db.sqlite3` è già popolato)
```bash
python manage.py migrate
```

**5. Avvia il server di sviluppo**
```bash
python manage.py runserver
```
L'applicazione sarà raggiungibile su `http://127.0.0.1:8000`.

> **Nota sul database (`db.sqlite3`)**: la repository include un file `db.sqlite3` già popolato
> con dati demo (utenti, brani, playlist, commenti, cronologia). Per ricreare il database da zero
> con gli stessi dati di test è sufficiente eseguire `python seed_data.py` dopo le migrazioni.
> Il progetto è **ricostruibile da un database vuoto** (migrate + seed).

---

## Account demo pre-caricati

Il database `db.sqlite3` include i seguenti account pronti per il test:

| Username | Password | Ruolo | Note |
|---|---|---|---|
| `admin_demo` | `admin12345` | Amministratore | `is_superuser=True`, accesso completo al pannello admin |
| `curator_demo` | `curator12345` | Curator | Aggiunge/modifica/elimina brani e generi, carica audio |
| `moderator_demo` | `moderator12345` | Moderator | Rimuove i commenti tramite report motivato |
| `listener_demo` | `listener12345` | Listener | Utente standard (playlist, like, cronologia) |
| `alice` | `password123` | Listener | Account secondario (collaboratore di playlist, commenti) |
| `bob` | `password123` | Listener | Account secondario (collaboratore di playlist, commenti) |

> Gli account `listener_demo`, `curator_demo` e `alice` hanno un'**immagine profilo demo** già
> impostata; gli altri usano l'avatar con l'iniziale. Puoi caricare la tua immagine da
> **Profilo → Modifica profilo**.

---

## Scenario di test (workflow da browser)

Breve scenario per verificare i flussi principali, i ruoli e i permessi (non tutte le
funzionalità sono coperte da questi test).

### 1. Listener — riproduzione, like e commenti
1. Accedi come **`listener_demo`** (password `listener12345`).
2. Vai nel **Catalogo**: prova la **ricerca**, il **filtro per genere** e il filtro **"Con
   audio"**.
3. Apri **"Bohemian Rhapsody"** (ha audio reale) e premi **▶ Riproduci**: parte il player in
   fondo alla pagina e il contatore ascolti si aggiorna.
4. Metti **like** al brano, scrivi un **commento** e metti like a un commento esistente.
5. Torna in **Home** e nella sezione **"Ascoltati di recente"** ritrovi il brano appena
   riprodotto; nel **Profilo** trovi la **Cronologia ascolti** (con link alla pagina completa).

### 2. Curator — gestione del catalogo e durata automatica
1. Accedi come **`curator_demo`** (password `curator12345`).
2. Nel Catalogo compaiono i pulsanti **"+ Aggiungi brano"** e **"Generi"**.
3. Crea un nuovo **genere**, poi **"+ Aggiungi brano"**: inserisci titolo e artista, scegli il
   genere e **carica un file audio** → il campo durata **si compila da solo**. Salva.
4. Vai in **Playlist**, crea una playlist con visibilità **editoriale** e aggiungici il brano.
5. **Test permessi**: esci, accedi come `listener_demo` e prova a visitare a mano
   `/music/songs/add/` → ottieni un **403 Forbidden**, perché i Listener non hanno accesso al
   CRUD del catalogo.

### 3. Moderator — rimozione commenti con report
1. Accedi come **`moderator_demo`** (password `moderator12345`) e apri un brano con commenti.
2. Accanto a un commento compare **"Elimina"**: cliccandolo si apre una **schermata di report**
   in cui inserisci la **motivazione**.
3. Conferma: il commento viene rimosso e registrato. Apri **Moderazione** dalla sidebar per
   vedere lo **storico dei report**.

### 4. Playlist collaborative — invito da accettare
1. Come **`listener_demo`**, apri la playlist **"Il mio mix"**: nel pannello **Collaboratori**
   invita un utente per username (compare come *"in attesa"*).
2. Accedi come l'utente invitato (es. `alice` / `password123`): in **Playlist** trovi la sezione
   **"Inviti a collaborare"** con **Accetta / Rifiuta**. Dopo l'accettazione puoi aggiungere e
   rimuovere brani dalla playlist condivisa.

### 5. Suggerimenti per genere
1. Come `listener_demo`, vai in **Profilo → Modifica profilo** e imposta un **genere preferito**.
2. In **Home** la sezione **"Per il tuo genere"** propone i brani di quel genere.

### 6. Administrator — pannello di amministrazione
1. Accedi come **`admin_demo`** (password `admin12345`) e apri il **pannello admin** (`/admin/`).
2. Puoi ispezionare e modificare ogni entità. Ad esempio, dalla sezione utenti seleziona `bob`
   (Listener) e cambia il suo **ruolo** in `curator`, salva.
3. Esci, accedi come `bob` (`password123`) e verifica che ora abbia i permessi da Curator sul
   catalogo.

---

## Uso dell'intelligenza artificiale

Durante lo sviluppo sono stati utilizzati assistenti AI come supporto (stesura della documentazione, generazione dei dati demo e suggerimenti di refactoring).

