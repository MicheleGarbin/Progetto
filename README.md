# L'evoluzione del gioco del basket

Lo scopo di questo progetto è presentare come si è evoluto il gioco del basket 
nel corso del tempo. Al suo interno l'utente ha la possibilità di selezionare
tra 4 pagine:
1. La prima pagina descrive i passaggi chiave che hanno portato al modo di 
   giocare odierno, partendo dal 1979-80 (introduzione della linea da 3) ad oggi.
   Vengono individuati quei giocatori, allenatori e dirigenti che più di tutti 
   hanno modificato per sempre l'approccio al gioco; le affermazioni sono ben
   supportate dai dati.
2. La seconda pagina contiene un'analisi con le componenti principali, un 
   adattamento di un modello logit binomiale e la spiegazione del paradosso di 
   Simpson. Tutto ciò è puramente statistico, ma allo stesso tempo interessante
   per le conclusioni a cui si giunge.
3. La terza pagina è un piccolo database dei giocatori. Selezionando vari 
   parametri si possono trovare le informazioni cercate. In base al volume 
   di tiri considerato, viene prodotto poi:
   - per un volume di tiri basso (inferiore a 5 tiri per zona di tiro)
     viene prodotta una heatmap, ovvero una mappa del campo che evidenzia
     o meno le zone in cui il giocatore ha preso quei tiri;
   - per un volume di tiri elevato viene mostrata la metà campo con 100 esagoni
     centrati nelle zone di tiro, grandi quanto il volume specifico 
     di tiri effettuati in tale zona e colorati secondo la differenza tra 
     percentuale di realizzazione del giocatore e percentuale di 
     realizzazione della lega.
   
   In una zona specifica, con meno di 5 tiri a disposizione, non ha molto senso
   analizzare la percentuale di realizzazione: per effetto del caso, un giocatore
   che tira con il 40 % potrebbe registrare 3 tiri segnati su 4, dando un 
   impressione sbagliata della sua efficienza realizzativa.
4. La quarta pagina fornisce le informazioni principali sulle 30 attuali 
   franchigie NBA. Vi è inoltre una sezione apposita per tracciare il rendimento   
   di ciascuna squadra nelle varie stagioni e confrontare i valori registrati
   per le metriche principali tra squadre diverse.

Le prime due pagine sono delle vere e proprie analisi, mentre le ultime due
vogliono mimare dei piccoli database. Così facendo, l'utente può ottenere tutte le
informazioni che desidera, sia per farsi un'idea generale sul mondo dell'nba ma anche 
per verificare quanto viene affermato nelle prime due pagine.

Nulla di tutto ciò sarebbe stato possibile senza l'NBA API ([documentazione ufficiale](https://github.com/swar/nba_api/tree/master/docs/nba_api)). Questa API permette di ottenere
i dati richiesti direttamente dal sito ufficiale dell'NBA. Nell'esecuzione del 
programma, quando vi è un eccesso di chiamate in un breve intervallo di 
tempo l'API smette di restituire i risultati e dà errore. Questo succede 
abbastanza spesso; serve aspettare qualche minuto e riaggiornare la pagina.

Per evitare le troppe chiamate all'API, i dati necessari al funzionamento
delle prime due pagine si trovano nei file presenti nella cartella data.
Le procedure per ottenere tali dati sono riportate nel codice dentro a dei
blocchi indentati sotto a "if False:" (in questo modo tale blocco non viene
eseguito). Ho agito in questa maniera poichè Streamlit scrive sull'applicazione
qualsiasi blocco compreso tra due triple virgolette; l'unica altra possibile 
soluzione è quella di aggiungere "#" all'inizio di ogni riga.

Le altre due pagine non mostrano sempre gli stessi dati/grafici, per cui 
per funzionare si basano esclusivamente sulle chiamate all'API.
Purtroppo alcune statistiche non sono disponibili perchè la lega nel passato
non raccoglieva tanti dati quanto oggi.

Oltre all'API, altri strumenti mi sono stati molto utili:
- [documentazione MPL Court](https://github.com/mlsedigital/mplbasketball/blob/main/README.md):
  libreria grafica per python che permette di disegnare punti su campi da basket
- [Chat GPT](https://chatgpt.com/): questo Large Language Model non ha bisogno di
  presentazioni. Mi ha evitato la lettura di lunghe documentazioni quando mi 
  serviva introdurre moduli/librerie a me non note. In generale risolve la 
  maggior parte dei problemi

Dati e informazioni varie sono stati presi da:
- [NBA court matplotlib](http://savvastjortjoglou.com/nba-shot-sharts.html): 
  spiega come disegnare una metà campo da basket tramite gli 
  strumenti di matplotlib
- [Thinking Basketball - YT Channel](https://www.youtube.com/@ThinkingBasketball):
  Thinking Basketball si distingue per la sua capacità di esaminare il gioco da una 
  prospettiva più intellettuale e dettagliata, spesso andando oltre le statistiche 
  tradizionali per analizzare aspetti come la lettura del gioco, l’intelligenza 
  cestistica e l’impatto complessivo di un giocatore su una partita. Il canale offre
  anche contenuti su leggende del basket, confronti tra giocatori storici e attuali, 
  e riflessioni sullo sviluppo e l’evoluzione del gioco nel corso degli anni
- Basketball on paper - Dean Oliver (2004): questo libro è stato uno dei primi testi 
  a promuovere decisioni e analisi data-driven nel mondo del basket


































