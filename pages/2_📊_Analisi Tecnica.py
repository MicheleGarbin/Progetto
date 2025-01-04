import streamlit as st
import pandas as pd
import numpy as np
from nba_api.stats.endpoints import PlayerDashboardByShootingSplits, CommonPlayerInfo
from nba_api.stats.endpoints import LeagueGameFinder, BoxScoreTraditionalV2
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


@st.cache_data
def group_analysis():
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
    fig, ax = plt.subplots(figsize = (8, 6))
    ax.scatter(df_season_1_pca['PC1'], df_season_1_pca['PC2'], color = 'blue')
    for i, label in enumerate(df_season_1_pca["POSITION"]):
        ax.annotate(label, (df_season_1_pca['PC1'][i], df_season_1_pca['PC2'][i]),
                    textcoords = "offset points", xytext = (0, 5), ha = 'center', fontsize = 9)
    ax.set_xlabel('Componente principale 1 (PC1)')
    ax.set_ylabel('Componente principale 2 (PC2)')
    ax.set_title('Stagione 2003-2004')
    st.pyplot(fig)
    fig, ax = plt.subplots(figsize = (8, 6))
    ax.scatter(df_season_2_pca['PC1'], df_season_2_pca['PC2'], color = 'blue')
    for i, label in enumerate(df_season_2_pca['POSITION']):
        ax.annotate(label, (df_season_2_pca['PC1'][i], df_season_2_pca['PC2'][i]),
                    textcoords = "offset points", xytext = (0, 5), ha = 'center', fontsize = 9)
    ax.set_xlabel('Componente principale 1 (PC1)')
    ax.set_ylabel('Componente principale 2 (PC2)')
    ax.set_title('Stagione 2023-2024')
    st.pyplot(fig)    
    # Mi ricavo la matrice dei loadings per le rispettive PC
    st.write(pca_season_1.components_[:2])
    
    
    
def simpson_paradox():
    st.write("Ciao")


# Funzione principale della pagina
def analisi_tecnica():
    col1, col2, col3 = st.columns(3)
    with col1:
        button1 = st.button("Analisi dei gruppi", use_container_width = True)
    with col2:
        button2 = st.button("Paradosso di Simpson", use_container_width = True)
    with col3:
        button3 = st.button("", use_container_width = True)
    
    st.markdown("---")
    
    if button1:
        group_analysis()
    if button2:
        simpson_paradox()
        
        
analisi_tecnica()
    

