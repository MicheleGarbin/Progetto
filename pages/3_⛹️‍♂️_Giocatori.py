import streamlit as st
import polars as pl
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.patches import Circle, Rectangle, Arc
from matplotlib import cm
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, shotchartdetail, ShotChartDetail
from mplbasketball import Court


# Questa funzione prende in input l'id di riconoscimento di un giocatore
# e fornisce i dati relativi a tale giocatore
def get_player_data(player_id):
    player_data = playercareerstats.PlayerCareerStats(player_id = player_id)
    data = player_data.get_data_frames()[0]  # ottengo il primo dataframe
    return pl.DataFrame(data)  # converto in Polars
        
        
# Questa funzione riporta sulla pagina streamlit le statistiche 
# individuali richieste
def get_player_stats(player_data, selected_season, season_type_choice, per_mode):
    if selected_season == "Tutte":
        if  season_type_choice == "Regular Season":
            df = pl.DataFrame(player_data.career_totals_regular_season.get_data_frame())
            st.write(df.select(
                df.columns[df.columns.index("GP"):]
            ))
        elif season_type_choice == "Playoffs":
            df = pl.DataFrame(player_data.career_totals_post_season.get_data_frame())
            st.write(df.select(
                df.columns[df.columns.index("GP"):]
            ))
    else:
        if season_type_choice == "Regular Season":
            df = pl.DataFrame(player_data.season_totals_regular_season.get_data_frame())
            st.write(df
                     .filter(pl.col("SEASON_ID") == selected_season)
                     .select(
                         df.columns[df.columns.index("GP"):]
                     )
                    )
            st.write("Qui vengono mostrati i posizionamenti del giocatore nelle varie categorie rispetto a tutta la lega: ")
            df = pl.DataFrame(player_data.season_rankings_regular_season.get_data_frame())
            if per_mode == "Totals":
                st.write(df
                        .filter(pl.col("SEASON_ID") == selected_season)
                        .select(
                            df.columns[df.columns.index("RANK_MIN"):]
                        )
                        )
            elif per_mode == "PerGame":  
                st.write(df
                        .filter(pl.col("SEASON_ID") == selected_season)
                        .select(
                            df.columns[df.columns.index("RANK_PG_MIN"):]
                        )
                        )
            else: 
                st.write(df
                        .filter(pl.col("SEASON_ID") == selected_season)
                        .select(
                            df.columns[df.columns.index("RANK_PMIN_MIN"):]
                        )
                        )
        elif season_type_choice == "Playoffs":
            df = pl.DataFrame(player_data.season_totals_post_season.get_data_frame())
            st.write(df
                     .filter(pl.col("SEASON_ID") == selected_season)
                     .select(
                         df.columns[df.columns.index("GP"):]
                     )
                    )
            st.write("Qui vengono mostrati i posizionamenti del giocatore nelle varie categorie rispetto a tutta la lega")
            df = pl.DataFrame(player_data.season_rankings_post_season.get_data_frame())
            if per_mode == "Totals":
                st.write(df
                        .filter(pl.col("SEASON_ID") == selected_season)
                        .select(
                            df.columns[df.columns.index("RANK_MIN"):]
                        )
                        )
            elif per_mode == "PerGame":  
                st.write(df
                        .filter(pl.col("SEASON_ID") == selected_season)
                        .select(
                            df.columns[df.columns.index("RANK_PG_MIN"):]
                        )
                        )
            else: 
                st.write(df
                        .filter(pl.col("SEASON_ID") == selected_season)
                        .select(
                            df.columns[df.columns.index("RANK_PMIN_MIN"):]
                        )
                        )


# Questa funzione restituisce il dataframe con tutte le informazioni sul tiro 
# per un certo giocatore secondo la stagione, la fase della stagione e 
# i minuti rimanenti sul cronometro
def get_player_shot_chart(selected_player_id, shot_type, selected_season, season_type_choice, game_segment, minutes_left, seasons):
    if selected_season == "Tutte":
        shot_chart_data = pd.DataFrame()
        if game_segment == "-":
            if game_segment == "-":
                for season in seasons:
                    season_shot_chart = shotchartdetail.ShotChartDetail(
                        team_id = 0,
                        player_id = selected_player_id,
                        season_type_all_star = season_type_choice,
                        context_measure_simple = shot_type,
                        season_nullable = season
                    ).get_data_frames()[0]
                    shot_chart_data = pd.concat([shot_chart_data, season_shot_chart], axis = 0)
        elif game_segment == "Second Half":
            if minutes_left == "-":
                for season in seasons:
                    season_shot_chart = shotchartdetail.ShotChartDetail(
                        team_id = 0,
                        player_id = selected_player_id,
                        season_type_all_star = season_type_choice,
                        context_measure_simple = shot_type,
                        game_segment_nullable = game_segment,
                        season_nullable = season
                    ).get_data_frames()[0]
                    shot_chart_data = pd.concat([shot_chart_data, season_shot_chart], axis = 0)
            else:
                for season in seasons:
                    season_shot_chart = shotchartdetail.ShotChartDetail(
                        team_id = 0,
                        player_id = selected_player_id,
                        season_type_all_star = season_type_choice,
                        context_measure_simple = shot_type,
                        game_segment_nullable = game_segment,
                        clutch_time_nullable = minutes_left,
                        season_nullable = season
                    ).get_data_frames()[0]
                    shot_chart_data = pd.concat([shot_chart_data, season_shot_chart], axis = 0)
        else:
            for season in seasons:
                season_shot_chart = shotchartdetail.ShotChartDetail(
                    team_id = 0,
                    player_id = selected_player_id,
                    season_type_all_star = season_type_choice,
                    context_measure_simple = shot_type,
                    game_segment_nullable = game_segment,
                    season_nullable = season
                ).get_data_frames()[0]
                shot_chart_data = pd.concat([shot_chart_data, season_shot_chart], axis = 0)
    else:
        if game_segment == "-":
                shot_chart_data = shotchartdetail.ShotChartDetail(
                    team_id = 0,
                    player_id = selected_player_id,
                    season_nullable = selected_season,
                    season_type_all_star = season_type_choice,
                    context_measure_simple = shot_type
                ).get_data_frames()[0]
        elif game_segment == "Second Half":
            if minutes_left == "-":
                shot_chart_data = shotchartdetail.ShotChartDetail(
                    team_id = 0,
                    player_id = selected_player_id,
                    season_nullable = selected_season,
                    season_type_all_star = season_type_choice,
                    context_measure_simple = shot_type,
                    game_segment_nullable = game_segment
                ).get_data_frames()[0]
            else:
                shot_chart_data = shotchartdetail.ShotChartDetail(
                    team_id = 0,
                    player_id = selected_player_id,
                    season_type_all_star = season_type_choice,
                    context_measure_simple = shot_type,
                    clutch_time_nullable = minutes_left,
                    game_segment_nullable = game_segment,
                    season_nullable = selected_season
                ).get_data_frames()[0]
        else:
            shot_chart_data = shotchartdetail.ShotChartDetail(
                    team_id = 0,
                    player_id = selected_player_id,
                    season_nullable = selected_season,
                    season_type_all_star = season_type_choice,
                    context_measure_simple = shot_type,
                    game_segment_nullable = game_segment
                ).get_data_frames()[0]
    return shot_chart_data
        
        
# Questa funzione, dato un elenco di stagioni, restituisce lo shot chart di
# tutti i giocatori che hanno giocato in nba in tali stagioni
def get_league_shot_chart(selected_player_id, selected_season, shot_type, season_type_choice, game_segment, minutes_left, seasons):
    if selected_season == "Tutte":
        league_shot_chart_data = pd.DataFrame()
        if game_segment == "-":
            if game_segment == "-":
                for season in seasons:
                    season_shot_chart = ShotChartDetail(
                        team_id = 0,
                        player_id = selected_player_id,
                        season_type_all_star = season_type_choice,
                        context_measure_simple = shot_type,
                        season_nullable = season
                    ).league_averages.get_data_frame()
                    league_shot_chart_data = pd.concat([league_shot_chart_data, season_shot_chart], axis = 0)
        elif game_segment == "Second Half":
            if minutes_left == "-":
                for season in seasons:
                    season_shot_chart = ShotChartDetail(
                        team_id = 0,
                        player_id = selected_player_id,
                        season_type_all_star = season_type_choice,
                        context_measure_simple = shot_type,
                        game_segment_nullable = game_segment,
                        season_nullable = season
                    ).league_averages.get_data_frame()
                    league_shot_chart_data = pd.concat([league_shot_chart_data, season_shot_chart], axis = 0)
            else:
                for season in seasons:
                    season_shot_chart = ShotChartDetail(
                        team_id = 0,
                        player_id = selected_player_id,
                        season_type_all_star = season_type_choice,
                        context_measure_simple = shot_type,
                        game_segment_nullable = game_segment,
                        clutch_time_nullable = minutes_left,
                        season_nullable = season
                    ).league_averages.get_data_frame()
                    league_shot_chart_data = pd.concat([league_shot_chart_data, season_shot_chart], axis = 0)
        else:
            for season in seasons:
                season_shot_chart = ShotChartDetail(
                    team_id = 0,
                    player_id = selected_player_id,
                    season_type_all_star = season_type_choice,
                    context_measure_simple = shot_type,
                    game_segment_nullable = game_segment,
                    season_nullable = season
                ).league_averages.get_data_frame()
                league_shot_chart_data = pd.concat([league_shot_chart_data, season_shot_chart], axis = 0)
    else:
        if game_segment == "-":
                league_shot_chart_data = ShotChartDetail(
                    team_id = 0,
                    player_id = selected_player_id,
                    season_nullable = selected_season,
                    season_type_all_star = season_type_choice,
                    context_measure_simple = shot_type
                ).league_averages.get_data_frame()
        elif game_segment == "Second Half":
            if minutes_left == "-":
                league_shot_chart_data = ShotChartDetail(
                    team_id = 0,
                    player_id = selected_player_id,
                    season_nullable = selected_season,
                    season_type_all_star = season_type_choice,
                    context_measure_simple = shot_type,
                    game_segment_nullable = game_segment
                ).league_averages.get_data_frame()
            else:
                league_shot_chart_data = ShotChartDetail(
                    team_id = 0,
                    player_id = selected_player_id,
                    season_type_all_star = season_type_choice,
                    context_measure_simple = shot_type,
                    clutch_time_nullable = minutes_left,
                    game_segment_nullable = game_segment,
                    season_nullable = selected_season
                ).league_averages.get_data_frame()
        else:
            league_shot_chart_data = ShotChartDetail(
                    team_id = 0,
                    player_id = selected_player_id,
                    season_nullable = selected_season,
                    season_type_all_star = season_type_choice,
                    context_measure_simple = shot_type,
                    game_segment_nullable = game_segment
                ).league_averages.get_data_frame()
    return league_shot_chart_data
   

# Questa funzione mi permette di disegnare la metà campo su cui 
# rappresenterò i tiri scelti
def draw_court(ax = None, color = "black", lw = 2, outer_lines = False):
    # Se non viene fornito un oggetto axes su cui tracciare, utilizza semplicemente quello corrente
    if ax is None:
        ax = plt.gca()

    # Ora serve creare le varie parti che compongono il campo da basket

    # Creazione del canestro: il diametro di un canestro è di 18", per cui il raggio è di 9", 
    # che corrisponde al valore 7.5 nel nostro sistema di cooordinate
    hoop = Circle((0, 0), radius = 7.5, linewidth = lw, color = color, fill = False)
    # Creazione tabellone
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth = lw, color = color)

    # Creazione del pitturato: creiamo il pitturato esterno impostando
    # una larghezza di 16ft e un'altezza di 19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth = lw, color = color,
                          fill = False)
    # Creazione della pitturato interno con lunghezza 12ft e altezza 19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth = lw, color = color,
                          fill = False)

    # Creazione dell'arco superiore del tiro libero
    top_free_throw = Arc((0, 142.5), 120, 120, theta1 = 0, theta2 = 180,
                         linewidth = lw, color = color, fill = False)
    # Creazione dell'arco inferiore del tiro libero
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1 = 180, theta2 = 0,
                            linewidth = lw, color = color, linestyle = "dashed")
    # Creazione della RA(Restricted Area), è un arco distante mento di 4ft 
    # dal centro del canestro
    restricted = Arc((0, 0), 80, 80, theta1 = 0, theta2 = 180, linewidth = lw,
                     color = color)

    # Creazione della linea da tre punti: creazione delle linee da tre punti laterali (da qui 
    # avvengono i cosidetti "tiri dall'angolo"). La lunghezza di queste linee è di 14ft
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth = lw,
                               color = color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth = lw, color = color)
    # Creazione del centro dell'arco da 3 punti distante 23'9" dal canestro 
    three_arc = Arc((0, 0), 475, 475, theta1 = 22, theta2 = 158, linewidth = lw,
                    color = color)

    # Creazione degli archi relativi al centro del campo e al logo
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1 = 180, theta2 = 0,
                           linewidth = lw, color = color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1 = 180, theta2 = 0,
                           linewidth = lw, color = color)

    # Salvo gli elementi appena costruiti in una lista
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Disegno la linea di metà campo, la linea di fondo e le linee laterali
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Aggiungiamo tutti questi elementi al grafico sottostante
    for element in court_elements:
        ax.add_patch(element)

    return ax


# Questa funzione crea una heatmap dei tiri del giocatore scelto. Per farlo, 
# raccoglie le coordinate dei tiri e stima la densità tramite il metodo del 
# nucleo, per poi colorare ciascun punto della metà campo in base alla 
# densità stimata 
def heatmap(shot_chart_data, selected_player_name, selected_season, shot_type, season_type_choice, game_segment, minutes_left): 
    plt.figure(figsize=(12, 11))
    ax = sns.kdeplot(
        data = shot_chart_data,
        x = "LOC_X",
        y = "LOC_Y",
        fill = True,
        thresh = 0,
        levels = 100,
        cmap = "mako"
    ).axes
    
    # Aggiungo un titolo al grafico
    if selected_season == "-":
        selected_season = "All Time"
    if season_type_choice == "Regular Season":
        season_type_choice = "RS"
    else:
        season_type_choice = "PO"
    if game_segment == "-":
        plt.title(f"{selected_player_name} ({shot_type}) | {season_type_choice} {selected_season}" , 
                  fontsize = 18, color = "black")
    elif game_segment != "Second Half":
        plt.title(f"{selected_player_name} ({shot_type}) | {season_type_choice} {selected_season} | {game_segment}" , 
                  fontsize = 18, color = "black")
    elif minutes_left != "-":
        plt.title(f"{selected_player_name} ({shot_type}) in the {minutes_left} | {season_type_choice} {selected_season}" , 
                  fontsize = 18, color = "black")
    else:
        plt.title(f"{selected_player_name} ({shot_type}) | {season_type_choice} {selected_season} | {game_segment}" , 
                  fontsize = 18, color = "black")
    
    draw_court(ax, color = "white", lw = 1)
    
    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 422.5)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(labelbottom = False, labelleft = False)
    
    # Aggiungo la colorbar orizzontale
    sm = plt.cm.ScalarMappable(cmap = "mako", norm = plt.Normalize())
    sm.set_array([])
    cbar = plt.colorbar(sm, ax = ax, orientation = "horizontal", pad = 0.05)
    # Rimuovo le etichette della colorbar: i valori non sono utili a fini interpretativi poichè
    # indicano la densità stimata dal metodo del kernel, a noi ci interessa comparare 
    # le zone di tiro in senso relativo e non in senso assoluto
    cbar.set_ticks([])
    # Aggiungo del testo sulla colorbar per facilitare la lettura del grafico
    cbar.ax.text(0, 1.1, "Bassa", ha = "center", va = "bottom", fontsize = 12, color = "black")
    cbar.ax.text(0.5, 1.1, "Frequenza di tiro", ha = "center", va = "bottom", fontsize = 15, color = "black")
    cbar.ax.text(1, 1.1, "Alta", ha = "center", va = "bottom", fontsize = 12, color = "black")

    # Vidualizzo il grafico
    st.pyplot(plt)
    
    
# Questa funzione disegna 100 esagoni sulla metà campo, ciascuno dei quali 
# si riferisce a un insieme di tiri che il giocatore prende da quella posizione. 
# La grandezza degli esagoni individua la quantità dei tiri di quel cluster 
# presenti nel dataframe. Il colore invece, determina se la percentuale di 
# realizzazione di quei tiri sia superiore o inferiore a quella calcolata 
# per i tiri simili (nel senso di tipo, anno, momento della stagione, ecc...) 
# effettutati da tutta la lega
def hexmap(shot_chart_data, league_shot_chart_data, selected_player_name, selected_season, shot_type, season_type_choice, game_segment, minutes_left):
    # Convertiamo da pollici a piedi
    shot_chart_data["LOC_X"] = shot_chart_data["LOC_X"] / 12
    shot_chart_data["LOC_Y"] = shot_chart_data["LOC_Y"] / 12
    # Trasformiamo le coordinate in valori utilizzabili per l'oggetto Court
    shot_chart_data["LOC_X"] = -shot_chart_data["LOC_X"] * 1.2
    shot_chart_data["LOC_Y"] = -shot_chart_data["LOC_Y"] + 39
    
    # Crea la corte NBA
    court = Court(court_type = "nba", origin = "center", units = "ft")
    fig, ax = court.draw(orientation = "vu")
    
    # Prepara i dati per il clustering
    X = shot_chart_data[["LOC_X", "LOC_Y"]]
    # Esegui KMeans clustering
    kmeans = KMeans(n_clusters = 100, random_state = 42)
    shot_chart_data['Cluster'] = kmeans.fit_predict(X)
    # Calcola la percentuale di realizzazione per ogni cluster
    cluster_data = (
        shot_chart_data.groupby("Cluster")
        .agg(
            SHOT_COUNT=("SHOT_ATTEMPTED_FLAG", "sum"),
            MADE_COUNT=("SHOT_MADE_FLAG", "sum"),
            LOC_X=("LOC_X", "mean"),
            LOC_Y=("LOC_Y", "mean"),
            SHOT_ZONE_BASIC=("SHOT_ZONE_BASIC", lambda x: x.value_counts().idxmax()), 
            SHOT_ZONE_AREA=("SHOT_ZONE_AREA", lambda x: x.value_counts().idxmax())
        )
    )
    cluster_data["FG_PCT"] = cluster_data["MADE_COUNT"] / cluster_data["SHOT_COUNT"]
    # Filtra i cluster con almeno 5 tiri
    cluster_data = cluster_data[cluster_data["SHOT_COUNT"] >= 5]
    
    # Compariamo le statistiche di tiro di un singolo giocatore con quelle medie della lega.
    # Uniamo i due dataframe in base alle colonne SHOT_ZONE_BASIC e SHOT_ZONE_AREA:
    merged_data = (
        cluster_data
            .groupby(["SHOT_ZONE_BASIC", "SHOT_ZONE_AREA"])
            .agg(
                SHOT_COUNT = ("SHOT_COUNT", "sum"),  
                MADE_COUNT = ("MADE_COUNT", "sum"),     
                FG_PCT = ("FG_PCT", "mean")       
            )
            .reset_index() 
            .merge(league_shot_chart_data, 
                                     on = ["SHOT_ZONE_BASIC", "SHOT_ZONE_AREA"], 
                                     suffixes=('_player', '_league'))
    ) 
    # Salvo in una colonna la differenza tra la percentuale di un giocatore al tiro in una 
    # determinata zona e la percentuale media della lega nella zona stessa        
    merged_data["DIFF_PCT"] = merged_data["FG_PCT_player"] - merged_data["FG_PCT_league"]
    # Lista dei colori
    color_list = ["#4169e1", "#add8e6", "#d3d3d3", "#e9967a", "#b22222"]
    # Condizioni per i valori di DIFF_PCT
    conditions = [
        merged_data["DIFF_PCT"] < -0.075,
        (merged_data["DIFF_PCT"] >= -0.075) & (merged_data["DIFF_PCT"] < -0.025),
        (merged_data["DIFF_PCT"] >= -0.025) & (merged_data["DIFF_PCT"] <= 0.025),
        (merged_data["DIFF_PCT"] > 0.025) & (merged_data["DIFF_PCT"] <= 0.075),
        merged_data["DIFF_PCT"] > 0.075,
    ]
    # Assegnazione dei colori
    merged_data["COLOR"] = np.select(conditions, color_list)
    # Effettua un merge tra cluster_data e merged_data usando SHOT_ZONE_BASIC e SHOT_ZONE_AREA
    merged_for_color = cluster_data.merge(
        merged_data[["SHOT_ZONE_BASIC", "SHOT_ZONE_AREA", "COLOR"]],
        on = ["SHOT_ZONE_BASIC", "SHOT_ZONE_AREA"],
        how = "left"
    )
    # Aggiorna la colonna "COLOR" in cluster_data con i valori corrispondenti
    cluster_data["COLOR"] = merged_for_color["COLOR"]
    # Creo la cmap corrispondente per il grafico; per i valori Nan inserisco il bianco
    custom_cmap = ListedColormap(cluster_data["COLOR"].fillna("#FFFFFF").to_list(), name = "custom_cmap")
    # Aggiungo gli esagoni con dimensioni e colori basati sui cluster
    
    ax.scatter(
        cluster_data["LOC_X"],
        cluster_data["LOC_Y"],
        c = cluster_data["FG_PCT"],
        s = np.array((cluster_data["SHOT_COUNT"] / cluster_data["SHOT_COUNT"].sum()) * 1e4),
        cmap = custom_cmap,
        alpha = 0.6,
        marker = "h",
        edgecolors = "none",  # Rimuove i bordi
    )
    
    # Creazione della colorbar personalizzata
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size = "5%", pad = 0.1)
    colors = mcolors.ListedColormap(color_list)
    # Eseguo la visualizzazione della colorbar
    bounds = np.linspace(0, 1, len(color_list) + 1)  # Crea i limiti per ciascun colore
    norm = mcolors.BoundaryNorm(bounds, len(color_list))
    cbar = fig.colorbar(plt.cm.ScalarMappable(cmap = colors, norm = norm), 
                        cax = cax, boundaries = bounds, ticks = np.linspace(0, 1, len(color_list)))
    # Aggiungo etichette personalizzate alle posizioni specificate
    cbar.set_ticks([0, 0.1, 0.3, 0.5, 0.7, 0.9, 1])  
    cbar.set_ticklabels(["Below Average", "-10%", "-5%", "Average", "+5%", "+10%", "Above Average"])
    
    # Aggiungo il titolo al grafico
    if selected_season == "-":
        selected_season = "All Time"
    if season_type_choice == "Regular Season":
        season_type_choice = "RS"
    else:
        season_type_choice = "PO"
    if game_segment == "-":
        title = f"{selected_player_name} | {season_type_choice} {selected_season}"
    elif minutes_left != "-":
        title = f"{selected_player_name} | {season_type_choice} {selected_season} with {minutes_left}" 
    else:
        title = f"{selected_player_name} | {season_type_choice} {selected_season} | {game_segment}" 
    ax.set_title(title + "\n" + f"{shot_type[:-1]}% VS League {shot_type[:-1]}%", fontsize = 16, color = "black", loc = "center") 
    
    # Visualizzo il grafico tramite Streamlit
    st.pyplot(fig)
    
    
# Questa funzione è il cuore della pagina. Dà la possibilità all'utente di 
# scegliere un giocatore, il tipo di tiro e altri parametri per produrre 
# dei grafici intuitivi ma potenti a livello di informazione contenuta
def giocatori():
    st.title("Sezione giocatori")
    st.write("")
    
    # Ottengo un elenco di tutti i giocatori
    player_dict = players.get_players()
    
    # Scelta del giocatore
    selected_player_name = st.selectbox("Seleziona un giocatore", [player["full_name"] for player in player_dict])
    selected_player_id = next(player for player in player_dict if player["full_name"] == selected_player_name)["id"]
    # Seleziona il PerMode
    per_mode = st.selectbox("Seleziona il PerMode: ", ["Totals", "PerGame", "Per36"])
    
    # Ottengo le informazioni richeiste
    player_data = playercareerstats.PlayerCareerStats(player_id = selected_player_id, 
                                                      per_mode36 = per_mode)
    
    # Scelta dell'anno
    seasons = player_data.nba_response.get_data_sets()
    # Tra tutte le stagioni seleziono quelle in cui il giocatore scelto compare nei dati della RS
    seasons = [subset[1] for subset in seasons["SeasonTotalsRegularSeason"]["data"]]
    selected_season = st.selectbox("Seleziona la stagione: ", ["Tutte"] + seasons)
    # Scelta del momento della stagione da considerare 
    season_type_choice = st.selectbox("Seleziona il tipo di stagione: ", ["Regular Season", "Playoffs"])
    
    st.write("")
    
    st.write("Qui vengono mostrate le statistiche desiderate: ")
    # Mostro le statistiche richieste per il giocatore scelto
    get_player_stats(player_data, selected_season, season_type_choice, per_mode)
    
    st.write("")
    
    # Scelta dei parametri per lo shot chart
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        shot_type = st.selectbox("Parametro da valutare: ", ["FGM", "FGA", "FG3M", "FG3A"])
    with col2:
        game_segment = st.selectbox("Momento della partita: ", ["-", "First Half", "Overtime", "Second Half"], index = 0)
    with col3:
        if game_segment == "Second Half":
            minutes_left = st.selectbox("Minuti nel clutch: ", ["-", "Last 5 Minutes", "Last 4 Minutes", "Last 3 Minutes",
                                            "Last 2 Minutes", "Last 1 Minute", "Last 30 Seconds",
                                            "Last 10 Seconds"], index = 0)
        else:
            minutes_left = ""
      
    # Ottengo lo shot chart per il giocatore desiderato in base a quanto richiesto sopra
    shot_chart_data = get_player_shot_chart(selected_player_id, shot_type, selected_season,
                                            season_type_choice, game_segment, minutes_left, seasons)
    
    
    # Mostro lo shot chart solo se ho dei dati disponibili
    if shot_chart_data.empty:
        st.markdown("""
                    **I dati non sono disponibili per vari motivi, tra cui:**
                    - il giocatore appartiene a un'epoca in cui non venivano tracciate le statistiche avanzate sul tiro
                    - il giocatore non ha giocato/non ha tirato nelle partite per cui si vogliono estrarre i dati
                    """)
    elif len(shot_chart_data) < 500:
        # Con questo tipo di grafico distingiuamo tra tiri segnati e sbagliati in base
        # a ciò che l'utente ha richiesto
        if shot_type.endswith("M"):
            shot_chart_data = shot_chart_data[shot_chart_data["SHOT_MADE_FLAG"] == 1]
        # Do la possibilità all'utente di escludere i tiri dalla RA
        RA_cond = st.checkbox("Rimuovi i tiri dalla Restricted Area")
        if RA_cond:
            # Rimuovo i tiri della RA dal dataframe
            shot_chart_data = shot_chart_data[shot_chart_data["SHOT_ZONE_BASIC"] != "Restricted Area"]
        st.write("")
        heatmap(shot_chart_data, selected_player_name, selected_season, shot_type,
                season_type_choice, game_segment, minutes_left)
    else:
        st.write("")
        # Otteniamo lo shot chart di tutti i giocatori presenti nella lega nel periodo selezionato
        league_shot_chart_data = get_league_shot_chart(selected_player_id, 
                                                        selected_season, 
                                                        shot_type, season_type_choice, 
                                                        game_segment, minutes_left, seasons)
        hexmap(shot_chart_data, league_shot_chart_data, selected_player_name, 
               selected_season, shot_type, season_type_choice, game_segment, minutes_left)
    
    
giocatori()
 
    
    
            
            
            
    
    
    
    
    

        
        
        
        

    
    
    
        
    
    
    
    
    

    
    
    
    
    
    
    


