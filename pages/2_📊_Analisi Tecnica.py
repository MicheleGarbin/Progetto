import streamlit as st
import pandas as pd
from nba_api.stats.endpoints import PlayerDashboardByShootingSplits, CommonPlayerInfo
from nba_api.stats.endpoints import LeagueDashTeamStats
from nba_api.stats.static import players
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


# Costruisco una funzione che restituisce i player ID di una lista di giocatore cercato
def get_player_id(player_list):
    # Inizializzo una lista vuota in cui mi salvo tutti gli ID
    player_id_list = []
    # Recupero tutti i giocatori NBA di sempre
    all_players = players.get_players()
    for player_name in player_list:
        # Cerca il giocatore per nome
        matching_players = [player for player in all_players if player_name.lower() == player['full_name'].lower()]
        if matching_players: 
            player_id_list.append(matching_players[0]["id"]) 
        else:
            player_id_list.append(None) 
    return player_id_list


# Questa funzione mostra l'analisi della PCA per il confronto dei top player 
# di due stagioni distinte
def pca_analysis():
    st.title("Analisi delle componenti principali")
    
    st.write("")
    
    st.markdown("""
                La PCA (Analisi delle Componenti Principali) è una tecnica 
                statistica utilizzata per ridurre la dimensionalità di un 
                dataset, preservandone al contempo la maggior parte della varianza,
                e quindi dell'informazione.\n\nIn questo caso, per le stagioni 
                2003-04 e 2023-24, sono stati presi i dati sui tiri da 6 diverse zone 
                di tiro: Restricted Area, nel pitturato ma non Restricted Area, 
                mid-range, triple dall'angolo sinistro, triple dall'angolo destro, 
                triple non dall'angolo. Per ogni zona si conoscono i tiri segnati, 
                i tiri tentati e la percentuale di tiri assistiti.\n\nI dataframe di 
                riferimento hanno 19 colonne (6 zone di tiro per 3 metriche 
                registrate più una colonna che indica la posizione del giocatore); 
                nelle righe troviamo una quindicina di giocatori tra i più impattanti 
                e influenti di ciascuna stagione.\n\nI grafici sottostanti rappresentano 
                i punteggi delle prime due componenti principali; sopra ciascun punto 
                è indicato il ruolo del giocatore.""")
    seasons = ["2003-04", "2023-24"]  # Modifica con la stagione desiderata

    # Siccome l'nba_api ha dei limiti per le troppe richieste, cerco di 
    # utilizzarla il meno possibile: scelgo manualmente i giocatori da analizzare,
    # cercando di prendere i più vincenti, popolari e impattanti
    player_list_1 = [
        "Shaquille O'Neal", "Kobe Bryant", "Kevin Garnett", "Tim Duncan",
        "Amar'e Stoudemire", "Paul Pierce", "Ben Wallace", "Chauncey Billups",
        "Yao Ming", "Rasheed Wallace", "Vince Carter", "Steve Nash",
        "Dirk Nowitzki", "Jason Kidd", "Allen Iverson", "Amar'e Stoudemire"
    ]
    player_list_2 = [
        "Nikola Jokic", "Giannis Antetokounmpo", "Luka Doncic", "Stephen Curry",
        "LeBron James", "Kevin Durant", "Joel Embiid", "Jayson Tatum",
        "Anthony Davis", "Jimmy Butler", "Devin Booker", "Damian Lillard",
        "Tyrese Haliburton", "Shai Gilgeous-Alexander", "Jaren Jackson Jr.",
        "De'Aaron Fox", "Bam Adebayo"
    ]
    
    # Dati i nomi dei giocatori, ricavo i relativi ID; avendo già i dati necessari
    # evito di utilizzare la funzione get_player_id per non fare una chiamata
    # inutile all'nba_api
    # player_id_list_1 = get_player_id(player_list_1)
    # player_id_list_2 = get_player_id(player_list_2)
    
    # Per non ripetere questa operazione ogni volta e avere un sovraccarico 
    # di richieste per l'API, riporto in seguito le istruzioni con cui ho 
    # ottenuto i file presenti nella cartella data
    if False:
        # Inizializzo il dataframe vuoto che conterrà tutte le informazioni riguardo
        # la rispettiva stagione
        df_season_1 = pd.DataFrame()
        
        # Mi salvo i dati dei giocatori relativi alla stagione 2023-2024
        for player_id in player_id_list_1:
            # Chiamata API per ottenere le statistiche di tiro
            shooting_stats = PlayerDashboardByShootingSplits(
                player_id = player_id,
                season = seasons[0]
            ).shot_area_player_dashboard.get_data_frame()
            
            # Elimino le colonne che non mi interessano
            shooting_stats = shooting_stats.drop(columns=["GROUP_SET", "BLKA"] + [col for col in shooting_stats.columns if "RANK" in col])
            # Elimino i tiri dal backcourt poichè non significativi
            shooting_stats = shooting_stats[shooting_stats["GROUP_VALUE"] != "Backcourt"]
            # Elimino le colonne relative alla percentuale di realizzazione, poichè sono 
            # il risultato di una combinazione lineare di altre colonne; la loro rimozione
            # aiuta ad evitare collinearità
            shooting_stats = shooting_stats.drop(columns = ["FG_PCT", "FG3_PCT", "EFG_PCT"])
            # Per lo stesso motivo visto sopra, elimino la percentuale di tiri non assistiti, 
            # poichè complementare della percentuale di tiri assistiti
            shooting_stats = shooting_stats.drop(columns = shooting_stats.filter(like = 'UAST').columns)
            # Elimino le colonne ridondanti
            shooting_stats = shooting_stats.drop(columns = ["FG3M", "FG3A", "PCT_AST_FGM"])
            # Evito la ridondanza unendo le due colonne in una nuova colonna, senza i valori zero
            shooting_stats['PCT_AST_FGM'] = shooting_stats[['PCT_AST_2PM', 'PCT_AST_3PM']].max(axis = 1)
            shooting_stats = shooting_stats.drop(columns = ['PCT_AST_2PM', 'PCT_AST_3PM'])
            # Trasformo il dataframe 6 x 4 in un dataframe 1 x 24; questo mi è utile perchè
            # mi permette di avere un record per ciascun giocatore 
            columns = [f"{group}-{stat}" for group in shooting_stats['GROUP_VALUE'] for stat in ['FGM', 'FGA', 'PCT_AST_FGM']]
            values = shooting_stats[['FGM', 'FGA', 'PCT_AST_FGM']].values.flatten()
            shooting_stats = pd.DataFrame([values], columns = columns)
            
            # Mi ricavo il ruolo di ciascun giocatore
            player_position = CommonPlayerInfo(
                player_id = player_id
                ).common_player_info.get_data_frame()["POSITION"].values
            
            # Unisco i dati sul tiro e sulla posizione di ciascun giocatore in un unico record
            shooting_stats.insert(0, "POSITION", player_position)
            # Aggiungo i dati ottenuti sul nuovo giocatore a quelli complessivi della stagione
            df_season_1 = pd.concat([df_season_1, shooting_stats])
        
        df_season_1.to_csv('data/df_season_1.txt', sep = '\t', index = False)
    
    # Eseguo gli stessi passaggi fatti sopra anche per l'altra stagione
    if False:
        # Inizializzo il dataframe vuoto che conterrà tutte le informazioni riguardo
        # la rispettiva stagione
        df_season_2 = pd.DataFrame()
        
        # Mi salvo i dati dei giocatori relativi alla stagione 2023-2024
        for player_id in player_id_list_2:
            # Chiamata API per ottenere le statistiche di tiro
            shooting_stats = PlayerDashboardByShootingSplits(
                player_id = player_id,
                season = seasons[1]
            ).shot_area_player_dashboard.get_data_frame()
            
            # Elimino le colonne che non mi interessano
            shooting_stats = shooting_stats.drop(columns=["GROUP_SET", "BLKA"] + [col for col in shooting_stats.columns if "RANK" in col])
            # Elimino i tiri dal backcourt poichè non significativi
            shooting_stats = shooting_stats[shooting_stats["GROUP_VALUE"] != "Backcourt"]
            # Elimino le colonne relative alla percentuale di realizzazione, poichè sono 
            # il risultato di una combinazione lineare di altre colonne; la loro rimozione
            # aiuta ad evitare collinearità
            shooting_stats = shooting_stats.drop(columns = ["FG_PCT", "FG3_PCT", "EFG_PCT"])
            # Per lo stesso motivo visto sopra, elimino la percentuale di tiri non assistiti, 
            # poichè complementare della percentuale di tiri assistiti
            shooting_stats = shooting_stats.drop(columns = shooting_stats.filter(like = 'UAST').columns)
            # Elimino le colonne ridondanti
            shooting_stats = shooting_stats.drop(columns = ["FG3M", "FG3A", "PCT_AST_FGM"])
            # Evito la ridondanza unendo le due colonne in una nuova colonna, senza i valori zero
            shooting_stats['PCT_AST_FGM'] = shooting_stats[['PCT_AST_2PM', 'PCT_AST_3PM']].max(axis = 1)
            shooting_stats = shooting_stats.drop(columns = ['PCT_AST_2PM', 'PCT_AST_3PM'])
            # Trasformo il dataframe 6 x 4 in un dataframe 1 x 24; questo mi è utile perchè
            # mi permette di avere un record per ciascun giocatore 
            columns = [f"{group}-{stat}" for group in shooting_stats['GROUP_VALUE'] for stat in ['FGM', 'FGA', 'PCT_AST_FGM']]
            values = shooting_stats[['FGM', 'FGA', 'PCT_AST_FGM']].values.flatten()
            shooting_stats = pd.DataFrame([values], columns = columns)
            
            # Mi ricavo il ruolo di ciascun giocatore
            player_position = CommonPlayerInfo(
                player_id = player_id
                ).common_player_info.get_data_frame()["POSITION"].values
            
            # Unisco i dati sul tiro e sulla posizione di ciascun giocatore in un unico record
            shooting_stats.insert(0, "POSITION", player_position)
            # Aggiungo i dati ottenuti sul nuovo giocatore a quelli complessivi della stagione
            df_season_2 = pd.concat([df_season_2, shooting_stats])
        
        df_season_2.to_csv('data/df_season_2.txt', sep = '\t', index = False)    
        
    # Carico i dati dai file della cartella data
    df_season_1 = pd.read_csv("data/df_season_1.txt", delimiter="\t")
    df_season_2 = pd.read_csv("data/df_season_2.txt", delimiter="\t")
    
    # Standardizzo i dati numerici poichè ho sia volumi di tiri 
    # importanti che percentuali di realizzazione
    scaler = StandardScaler()
    df_season_1_data = scaler.fit_transform(df_season_1.iloc[:, 1:])
    df_season_2_data = scaler.fit_transform(df_season_2.iloc[:, 1:])
    
    # Applico la PCA
    pca_season_1 = PCA()
    df_season_1_pca = pca_season_1.fit_transform(df_season_1_data)
    pca_season_2 = PCA()
    df_season_2_pca = pca_season_2.fit_transform(df_season_2_data)
    # Per capire quante PC tenere guardo la devianza spiegata
    # np.cumsum(pca_season_1.explained_variance_ratio_) 
    # np.cumsum(pca_season_2.explained_variance_ratio_)
    # Nel primo caso le prime due PC spiegano il 70% della variabilità totale ;
    # nel secondo caso, per arrivare alla stessa percentuale ne servono 3.
    # Mi salvo gli score delle PC che mi interessano rendendoli valori 
    # di un dataframe
    df_season_1_pca = pd.DataFrame(df_season_1_pca[:, :2], columns = ["PC1", "PC2"])
    df_season_2_pca = pd.DataFrame(df_season_2_pca[:, :3], columns = ["PC1", "PC2", "PC3"])
    # Combino i ruoli dei giocatori con i punteggi dell PC
    df_season_1_pca.insert(0, "POSITION", df_season_1["POSITION"])
    df_season_2_pca.insert(0, "POSITION", df_season_2["POSITION"])
    
    # Disegniamo i biplot per le due stagioni considerate
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize = (8, 6))
        ax.scatter(df_season_1_pca['PC1'], df_season_1_pca['PC2'], color = 'blue')
        for i, label in enumerate(df_season_1_pca["POSITION"]):
            ax.annotate(label, (df_season_1_pca['PC1'][i], df_season_1_pca['PC2'][i]),
                        textcoords = "offset points", xytext = (0, 5), ha = 'center', fontsize = 9)
        ax.set_xlabel('Componente principale 1 (PC1)')
        ax.set_ylabel('Componente principale 2 (PC2)')
        ax.set_title('Stagione 2003-2004')
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots(figsize = (8, 6))
        ax.scatter(df_season_2_pca['PC1'], df_season_2_pca['PC2'], color = 'blue')
        for i, label in enumerate(df_season_2_pca['POSITION']):
            ax.annotate(label, (df_season_2_pca['PC1'][i], df_season_2_pca['PC2'][i]),
                        textcoords = "offset points", xytext = (0, 5), ha = 'center', fontsize = 9)
        ax.set_xlabel('Componente principale 1 (PC1)')
        ax.set_ylabel('Componente principale 2 (PC2)')
        ax.set_title('Stagione 2023-2024')
        st.pyplot(fig)    
    st.markdown("""
                Coloro che riportano punteggi distanti 
                dagli altri sono Kevin Garnett e Giannis Antetokounmpo. 
                Essi hanno rivoluzionato il ruolo di ala grande ridefinendolo 
                come una posizione versatile e dinamica, capace di eccellere su 
                entrambi i lati del campo. Hanno combinato fisicità, atletismo 
                e intelligenza cestistica, distinguendosi come difensori dominanti 
                e playmaker non convenzionali, rompendo l'idea di 
                un’ala grande confinata nel pitturato.  
                """)
    # Mi ricavo la matrice dei loadings per le rispettive PC; converto la 
    # matrice dei loadings (che è un np.array) in un dataframe Pandas per 
    # rinominare le colonne per un'immediata visualizzazione su streamlit
    st.markdown("""
                Di seguito sono riportate le matrici dei loadings, ovvero 
                le matrici dei pesi associati a ciascuna variabile nella 
                costruzione delle componenti principali:
                """)
    
    st.write("")
    
    loadings_season_1 = pd.DataFrame(pca_season_1.components_[:2], 
                                     columns = df_season_1.columns[1:])
    loadings_season_2 = pd.DataFrame(pca_season_2.components_[:2], 
                                     columns = df_season_2.columns[1:])
    st.write(loadings_season_1)
    st.markdown("""
                - la PC1 riguarda soprattutto i tiri dal pitturato e i tiri da 3 punti
                - la PC2 dà importanza ai tiri dal midrange e ai tiri assistiti dalla RA
                
                In quel periodo i lunghi non si prendevano molti tiri da tre; ad esempio, 
                Yao Ming, Shaq e Ben Wallace (3 giocatori indotti nella HOF) hanno segnato 
                in totale 8 tiri da 3 punti in tutta la loro carriera. Per questo motivo le
                guardie hanno un punteggio più alto per la prima PC. Inoltre i pesi per
                le metriche sul pitturato sono negativi, per cui i lunghi, che 
                utilizzavano molto di più quei tipi di tiro, hanno un punteggio 
                più basso.
                """)
    
    st.write("")
    
    st.write(loadings_season_2)
    st.markdown("""
                - l'interpretazione della PC1 è molto simile al caso sopra
                - la PC2 riguarda i tiri assistiti
                
                Le due guardie con il punteggio per la PC2 più alto sono 
                Steph Curry e De'Aaron Fox, due playmaker capaci di crearsi
                tiri dal palleggio, ma parte di squadre che giocano un basket molto simile,
                fatto di movimento continuo che genera buoni tiri assistiti.
                Non è un caso che, nonostante siano i portatori di palla primari, 
                registrino un numero di assist relativamente basso e siano dei veri e propri 
                scorer. 
                """)
    st.markdown("---")
    st.markdown("""
                ### Considerazioni finali e possibili ampliamenti:
                - per i limiti di utilizzo dell'API si sono potuti prendere in 
                  considerazione solamente 15 giocatori per stagione; in questo caso
                  sono stati scelti i giocatori più impattanti per considerare un 
                  volume di tiri maggiore. E' il caso di considerare anche i role
                  player e i panchinari per avere una visione più generale
                  
                - se i dati degli anni '80-'90 fossero disponibili sarebbe interessante
                  un confronto con le stagioni più recenti, magari per evidenziare il distacco
                  ancora più netto tra le due filosofie di basket
                  
                - utilizzando delle statistiche avanzate non facilmente accessibili,
                  si può utilizzare il metodo delle k-medie o un metodo gerarchico per 
                  individuare dei gruppi tra i dati. Ad esempio, considerando i post-up 
                  (quando un giocatore si posiziona in post basso), gli isolamenti, il
                  numero di possessi e la shot - selection, si può mostrare
                  come l'evoluzione del gioco abbia reso i ruoli tradizionali meno rigidi.
                  L'idea è che attribuendo dei punteggi (tramite le PCA ad esempio), i giocatori
                  di 20 anni fa siano facilmente raggruppabili in quei cluster che corrispondono
                  quasi esattamente al loro ruolo effettivo; se si fa lo stesso sui giocatori odierni
                  risulta molto difficile assegnare un ruolo a un giocatore, poichè al giorno d'oggi
                  a ogni giocatore viene richiesto di saper fare tante cose diverse, e non 
                  si riesce quasi mai ad associarlo a una sola delle 5 posizioni originali
                  """)
    
    
# Questa funzione spiega il paradosso di simpson, utile da conoscere quando 
# si confrontano dati con più variabili di classificazione
def simpson_paradox():
    st.title("Il paradosso di Simpson")
    
    st.markdown("""
                Il paradosso di Simpson è un fenomeno statistico in cui 
                una tendenza che appare in diversi gruppi di dati può essere
                invertita quando i gruppi sono combinati insieme. In altre 
                parole, quando i dati vengono aggregati, la relazione tra 
                due variabili può apparire in modo opposto rispetto a quando 
                sono separati in sottogruppi.
                
                Prendiamo ad esempio due variabili quantitative X e Y e una
                variabile categoriale C con modalità c1 e c2
                """)
    st.image("charts/simpson_paradox.jpg")
    st.markdown("""
                Si nota che la tendenza entro i gruppi viene ribaltata quando 
                si aggregano i dati. 
                
                Consideriamo ora un dataframe in cui le colonne rappresentano due 
                giocatori e le righe rappresentano due stagioni. I valori entro 
                le celle rappresentano la percentuale di tiri segnati:
                """)
    freq_abs = pd.DataFrame({"Giocatore 1": ["7 / 20", "50 / 200"],
                       "Giocatore 2": ["15 / 50", "14 / 60"]})
    st.table(freq_abs)
    st.markdown("""
                Calcoliamo le frequenze relative osservate:
                """)
    freq_obs = pd.DataFrame({"Giocatore 1": ["35%", "25%"],
                       "Giocatore 2": ["30%", "23.33%"]})
    st.table(freq_obs)
    st.markdown("""
                In ciascuna delle due stagioni il giocatore 1 ha ottenuto
                una miglior percentuale al tiro del giocatore 2.
                Cosa succede però se aggreghiamo i dati?
                
                - Giocatore 1: (7 + 50) / (20 + 200) = 57 / 220 (25.9%)
                - Giocatore 2: (15 + 14) / (50 + 60) = 29 / 110 (26.4%)
                
                Il giocatore 2 risulta migliore del giocatore 1!
                Il giocatore 1 ha sì delle percentuali migliori nelle singole 
                stagioni ma i singoli denominatori sono molto diversi (20 e 200).
                Quando aggreghiamo i dati, prevale l'effetto della seconda
                stagione rispetto alla prima, proprio perchè il numero di 
                tiri tentati è molto più alto: tra le due percentuali. Per
                il giocatore 2 invece la percentuale marginale si trova quasi
                a metà tra quelle delle stagioni singole: non a caso, i singoli
                denominatori sono molto simili (50 e 60).
                
                Bisogna ammettere che questo è un esempio molto semplice
                costruito a tavolino. Non è detto che ciò accada sempre. 
                Rimane comunque necessario verificare le conclusioni per dati aggregati 
                guardando le frequenze condizionate per evitare di giungere a 
                conclusioni errate. Come colonne potremmo avere squadre oltre 
                ai giocatori; righe plausibili sono zone di tiro, quarti della 
                partita, momenti della stagione, serie di playoff e così via. La 
                disparità potrebbe derivare da un confronto di due stagioni
                in cui un giocatore con un minutaggio diverso, con 
                un infortunio subito o con un ruolo diverso.
                """)
    
    st.markdown("---")
    
    covid_simpson_paradox_link = "https://www.youtube.com/watch?v=t-Ci3FosqZs"
    
    st.markdown("""
                Gli studi osservazionali retrospettivi sono un tipo di ricerca 
                in cui i ricercatori analizzano dati raccolti in passato per 
                esaminare relazioni tra eventi o variabili. In questi studi, 
                non si interviene attivamente sulla popolazione di interesse, 
                ma si osservano eventi già accaduti, utilizzando informazioni 
                disponibili da registri, cartelle cliniche, o altre fonti 
                storiche. Quest'applicazione web descrive e permette di 
                fare proprio questo
                
                In questi studi, il paradosso di Simpson è un esempio chiave 
                di come le analisi statistiche superficiali possano portare a 
                risultati errati.
                """)
                
    st.write(f"Un approfondimento interessante riguardo a ciò si trova al \
              seguente link: \
              [Simpson e il Covid]({covid_simpson_paradox_link})")
    


# Questa funzione costruisce due modelli logistici basati in cui 
# le esplicative sono i four factors e i tiri da tre mentre la
# risposta sono le vittorie in regular season. I dati di riferimento
# sono della scorsa stagione
def win_analysis():
    st.title("Come vincere nel basket moderno")
    
    st.markdown("""
                Nel basket, il successo di una squadra può essere analizzato 
                attraverso vari aspetti del gioco, ma pochi strumenti si sono 
                dimostrati tanto efficaci quanto i Four Factors, introdotti 
                dall’analista-statistico Dean Oliver. Considerato uno dei padri 
                della moderna analisi statistica nel basket, Oliver ha rivoluzionato 
                il modo di valutare le performance delle squadre con il suo 
                approccio quantitativo. Nel suo libro Basketball on Paper (2004), 
                Oliver ha individuato quattro elementi chiave che influenzano in modo 
                determinante l’esito delle partite.

                I Four Factors sono metriche che sintetizzano le componenti 
                fondamentali del gioco: la capacità di segnare con efficienza 
                (eFG%), la protezione del pallone per evitare palle perse (TOV%),
                il controllo dei rimbalzi offensivi per ottenere seconde opportunità 
                (ORB%) e la capacità di conquistare punti facili dalla lunetta (FTR).

                In questo contesto, i Four Factors possono essere utilizzati come 
                predittori in un modello di regressione logistica per spiegare 
                e predire il successo nel basket. Verifichiamo l'adattamento 
                sui dati della stagione appena conclusa
                """)

    # Di seguito riporto la procedura per ottenere i dati desiderati. 
    # Salvo tali dati in un file per evitare di riutilizzare l'API
    if False:
        team_stats = LeagueDashTeamStats(season = "2023-24").league_dash_team_stats.get_data_frame()
        # Numero di tiri da tre tentati e segnati a partita
        team_stats["FG3M/GP"] = team_stats["FG3M"] / 82
        team_stats["FG3A/GP"] = team_stats["FG3A"] / 82
        # Percentuale effettiva dal campo (media ponderata che dà più valore
        # al tiro da tre punti in quanto, se segnato, genera più punti
        # di un tiro da due)
        team_stats["eFG%"] = (team_stats["FGM"] + 0.5 * team_stats["FG3M"]) / team_stats["FGA"]
        # Percentuale di palle perse: viene calcolata come numero di palle perse
        # su 100 possessi. Il numero di possessi viene stimato tramite una 
        # formula introdotta dallo stesso Dean Oliver
        team_stats["Possessions/GP"] = (team_stats["FGA"] + 0.44 * team_stats["FTA"] + team_stats["TOV"]) / 82
        team_stats["TOV%"] = team_stats["TOV"] / (team_stats["Possessions/GP"] * 82)
        # Percentuale di rimbalzi offensivi: numero di rimbalzi offensivi
        # diviso totale di rimbalzi, ovvero somma di rimbalzi offensivi 
        # e rimbalzi difensivi
        team_stats["ORB%"] = team_stats["OREB"] / (team_stats["OREB"] + team_stats["DREB"])
        # Numero di tiri liberi tentati / numero di tiri dal campo tentati. 
        # I tiri liberi avvengono da una posizione fissa e a gioco
        # fermo, per cui non vengono conteggiati come tiri dal campo,
        # i quali avvengono durante i 24 secondi di un'azione e
        # da posizioni variabili.
        team_stats["FTR"] = team_stats["FTA"] / team_stats["FGA"]
        # Considero solamente i dati che mi interessano: oltre ai
        # four factors appena calcolati considero anche i tiri da 3 
        # che mi serviranno per testare un ampliamento del modello
        team_stats = team_stats[["W", "L", "FG3M/GP", "FG3A/GP", "Possessions/GP",
                                "eFG%", "TOV%", "ORB%", "FTR"]]
        team_stats.to_csv("data/team_stats.txt", sep = "\t", index = False)
    # L'analisi prosegue nel file R "win_probability_analysis.R"
    
    

# Funzione principale della pagina
def analisi_tecnica():
    col1, col2, col3 = st.columns(3)
    with col1:
        button1 = st.button("Analisi dei gruppi", use_container_width = True)
    with col2:
        button2 = st.button("Paradosso di Simpson", use_container_width = True)
    with col3:
        button3 = st.button("Cosa serve per vincere", use_container_width = True)
    
    st.markdown("---")
    
    if button1:
        pca_analysis()
    elif button2:
        simpson_paradox()
    elif button3:
        win_analysis()
    else:
        st.success("Seleziona uno dei 3 bottoni soprastanti")
    
        
analisi_tecnica()
    

