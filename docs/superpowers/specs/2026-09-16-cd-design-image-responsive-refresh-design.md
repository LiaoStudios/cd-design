# CD Design — aggiornamento immagini e comportamento responsive

## Obiettivo

Migliorare la presentazione fotografica del sito CD Design senza cambiarne l'identità generale. L'intervento deve rendere la hero della home più leggibile e meno coperta dai testi su mobile, correggere le fotografie non pertinenti nelle pagine prodotto, uniformare le immagini introduttive e permettere l'ingrandimento accessibile delle fotografie.

## Ambito

L'intervento riguarda:

- `index.html`;
- tutte le nove pagine di categoria prodotto;
- nuove risorse condivise per la lightbox;
- una selezione di immagini provenienti da `/Users/feng/Desktop/ cd design immagini/` e dal sito ufficiale Bettio.

Non sono previste modifiche ai contenuti legali, al modulo di contatto o alla struttura delle collezioni prodotto, salvo la rimozione della card errata indicata nella pagina degli infissi in legno.

## Home page

### Hero desktop

- Conservare la fotografia come sfondo della hero.
- Ridurre la sensazione di zoom mediante un'inquadratura e un posizionamento più ampi, scegliendo il ritaglio più adatto alla fotografia disponibile senza deformarla.
- Sostituire la dominante blu con una sfumatura neutra antracite, abbastanza scura soltanto nell'area del testo.
- Mantenere contrasto sufficiente per titolo, paragrafo e pulsanti.
- Limitare la larghezza del testo e alleggerire la quantità di superficie coperta.

### Hero mobile

- Dare priorità visiva alla fotografia.
- Ridurre dimensioni e ingombro di titolo, descrizione e pulsanti.
- Separare visivamente il blocco testuale dall'area principale della fotografia, evitando che il testo copra quasi tutto lo scatto.
- Mantenere i controlli principali facilmente raggiungibili e con target tattili di almeno 44 px.

### Navigazione home

- In cima alla pagina, la barra deve essere trasparente e sovrapposta alla hero.
- Dopo un breve scroll, deve diventare bianca, con bordo o ombra leggera.
- Logo, icona menu e relativi contrasti devono adattarsi ai due stati.
- La transizione deve essere breve e rispettare `prefers-reduced-motion`.

## Immagini introduttive delle categorie

- Sostituire l'attuale formato panoramico molto allungato con un riquadro più naturale, indicativamente 4:3 o 3:2 in base alla fotografia.
- Non deformare mai le immagini.
- Usare `object-fit` e un punto focale specifico per ciascuna fotografia.
- Fornire dimensioni esplicite o `aspect-ratio` per evitare spostamenti di layout.

## Correzioni per categoria

### Infissi in legno

- Sostituire la fotografia introduttiva con uno scatto che mostri chiaramente un serramento in legno o legno-alluminio.
- Eliminare la prima card "Finestra con scuri in legno", perché la fotografia attuale non mostra il prodotto descritto.
- Verificare e, se necessario, correggere titoli e testi alternativi delle card restanti.

### Porte blindate

- Sostituire l'immagine introduttiva ravvicinata con una fotografia che mostri la porta completa.
- Preferire uno scatto reale dell'archivio CD Design rispetto a un'immagine tecnica o a un collage.
- Inquadrare la porta senza ritagliarne i bordi principali.

### Zanzariere

- Sostituire l'immagine introduttiva con una fotografia ufficiale Bettio di tipo ambientato o promozionale, proveniente dal sito `bettio.it`.
- Conservare localmente una copia ottimizzata dell'immagine, così il sito non dipende da un collegamento esterno.
- Attribuire il contenuto a Bettio nel testo alternativo o in una breve didascalia, dove opportuno.

### Persiane e scuri in alluminio

- Rimuovere dalle card le fotografie chiaramente non pertinenti o descritte come legno.
- Utilizzare scatti che mostrino persiane lamellari e scuri in alluminio, comprese eventuali finiture effetto legno solo quando il materiale è verificabile.
- Correggere titoli e descrizioni affinché distinguano correttamente:
  - persiana: chiusura a lamelle che filtra luce e aria;
  - scuro: pannello pieno con maggiore capacità oscurante.

### Porte interne

- Sostituire la fotografia introduttiva con un'immagine ambientata che mostri chiaramente una porta interna.
- Conservare le collezioni e le card prodotto esistenti, salvo fotografie palesemente non pertinenti individuate durante la verifica finale.

## Lightbox condivisa

La lightbox verrà applicata alle fotografie introduttive e alle immagini delle card di tutte le pagine prodotto.

Comportamento richiesto:

- apertura tramite clic o tastiera;
- fotografia ingrandita entro il viewport, senza deformazioni;
- pulsante X visibile con nome accessibile;
- chiusura tramite X, tasto `Escape` o clic sullo sfondo;
- blocco dello scorrimento della pagina durante l'apertura;
- trasferimento del focus nella finestra e ripristino sul controllo originario alla chiusura;
- contrasto elevato e target tattili di almeno 44 px;
- nessuna apertura accidentale quando l'immagine non è disponibile.

L'implementazione sarà condivisa tra le pagine tramite risorse dedicate, evitando nove copie divergenti dello stesso codice.

## Gestione delle immagini

- Le fotografie selezionate dalla cartella sorgente devono essere copiate nella cartella `images/` del progetto con nomi descrittivi.
- Le immagini devono essere orientate correttamente, ridimensionate a una risoluzione adatta al web e compresse senza perdita visiva rilevante.
- Quando conveniente, creare versioni WebP mantenendo un fallback JPEG.
- Non fare riferimento diretto a percorsi esterni al progetto.
- Evitare immagini che possano descrivere un prodotto diverso da quello effettivamente mostrato.

## Accessibilità e prestazioni

- Testi alternativi specifici e veritieri.
- Focus visibile su immagini cliccabili e pulsanti della lightbox.
- Corpo del testo mobile non inferiore a 16 px.
- Caricamento prioritario solo per hero e immagini introduttive; `loading="lazy"` per le card.
- Nessun overflow orizzontale a 320 px.
- Rispetto di `prefers-reduced-motion` per transizioni e animazioni.

## Verifica

La consegna verrà verificata almeno nei seguenti scenari:

- home a 1440 × 900 e 1024 × 768;
- home a 390 × 844 e 320 × 568;
- stato della barra prima e dopo lo scroll;
- ogni pagina categoria a larghezza desktop e mobile;
- apertura e chiusura lightbox con mouse, touch simulato e tastiera;
- controllo dei percorsi di tutte le immagini;
- controllo della console del browser;
- controllo che nessuna modifica estranea già presente nel repository venga sovrascritta.

## Criteri di accettazione

Il lavoro è completo quando:

1. la hero della home mostra più fotografia e meno dominante blu;
2. su mobile il testo non copre la maggior parte dell'immagine;
3. la barra home è trasparente in cima e bianca dopo lo scroll;
4. le fotografie contestate sono state sostituite o eliminate;
5. le introduzioni di categoria non risultano eccessivamente panoramiche;
6. tutte le fotografie prodotto pertinenti sono ingrandibili con una lightbox accessibile;
7. le pagine non presentano immagini mancanti, errori JavaScript o overflow orizzontale.
