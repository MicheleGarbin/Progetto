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



























