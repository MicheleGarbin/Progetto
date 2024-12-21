import streamlit as st
import pydeck as pdk
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import TeamDetails
from PIL import Image
from icecream import ic


# Funzione per ottenere i dati delle squadre NBA
@st.cache_data
def get_nba_teams():
    nba_teams = teams.get_teams()
    return pd.DataFrame(nba_teams)


# Funzione per aggiungere latitudine e longitudine manualmente
@st.cache_data
def add_coordinates(data):
    coordinates = {
        "Atlanta Hawks": (33.7490, -84.3880),
        "Boston Celtics": (42.3601, -71.0589),
        "Brooklyn Nets": (40.6782, -73.9442),
        "Charlotte Hornets": (35.2271, -80.8431),
        "Chicago Bulls": (41.8781, -87.6298),
        "Cleveland Cavaliers": (41.4993, -81.6944),
        "Dallas Mavericks": (32.7767, -96.7970),
        "Denver Nuggets": (39.7392, -104.9903),
        "Detroit Pistons": (42.3314, -83.0458),
        "Golden State Warriors": (37.7749, -122.4194),
        "Houston Rockets": (29.7604, -95.3698),
        "Indiana Pacers": (39.7684, -86.1581),
        "Los Angeles Clippers": (34.0522, -118.2437),
        "Los Angeles Lakers": (34.0522, -118.2437),
        "Memphis Grizzlies": (35.1495, -90.0490),
        "Miami Heat": (25.7617, -80.1918),
        "Milwaukee Bucks": (43.0389, -87.9065),
        "Minnesota Timberwolves": (44.9778, -93.2650),
        "New Orleans Pelicans": (29.9511, -90.0715),
        "New York Knicks": (40.7128, -74.0060),
        "Oklahoma City Thunder": (35.4676, -97.5164),
        "Orlando Magic": (28.5383, -81.3792),
        "Philadelphia 76ers": (39.9526, -75.1652),
        "Phoenix Suns": (33.4484, -112.0740),
        "Portland Trail Blazers": (45.5051, -122.6750),
        "Sacramento Kings": (38.5816, -121.4944),
        "San Antonio Spurs": (29.4241, -98.4936),
        "Toronto Raptors": (43.651070, -79.347015),
        "Utah Jazz": (40.7608, -111.8910),
        "Washington Wizards": (38.9072, -77.0369)
    }
    data["latitude"] = data["full_name"].map(lambda name: coordinates[name][0])
    data["longitude"] = data["full_name"].map(lambda name: coordinates[name][1])
    return data


# Questa funzione restituisce un dataframe con dentro gli url dei vari loghi 
@st.cache_data
def get_logo_data():
    logo_data = {
        "Atlanta Hawks": "https://upload.wikimedia.org/wikipedia/it/e/ee/Atlanta_Hawks_logo2.svg",
        "Boston Celtics": "https://upload.wikimedia.org/wikipedia/it/d/d4/Boston_Celtics_logo.svg",
        "Brooklyn Nets": "https://cdn.nba.com/teams/uploads/sites/1610612751/2024/07/BKN_Primary.svg",
        "Charlotte Hornets": "https://upload.wikimedia.org/wikipedia/en/c/c4/Charlotte_Hornets_%282014%29.svg",
        "Chicago Bulls": "https://cdn.nba.com/teams/uploads/sites/1610612741/2021/10/bulls-svg.svg",
        "Cleveland Cavaliers": "Logos/cavs_logo.svg",
        "Dallas Mavericks": "https://upload.wikimedia.org/wikipedia/it/9/9b/Dallas_Mavericks_logo2.svg",
        "Denver Nuggets": "https://cdn.nba.com/teams/uploads/sites/1610612743/2021/11/dnuggets-primary-web.svg",
        "Detroit Pistons": "Logos/pistons_logo.svg",
        "Golden State Warriors": "https://cdn.nba.com/teams/uploads/sites/1610612744/2022/06/gsw-logo-1920.svg",
        "Houston Rockets": "Logos/rockets_logo.svg",
        "Indiana Pacers": "Logos/pacers_logo.svg",
        "Los Angeles Clippers": "Logos/clippers_logo.svg",
        "Los Angeles Lakers": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Los_Angeles_Lakers_logo.svg",
        "Memphis Grizzlies": "Logos/grizzlies_logo.svg",
        "Miami Heat": "Logos/heat_logo.svg",
        "Milwaukee Bucks": "https://upload.wikimedia.org/wikipedia/it/4/4a/Milwaukee_Bucks_logo.svg",
        "Minnesota Timberwolves": "https://cdn.nba.com/teams/uploads/sites/1610612750/2021/11/logo-1.svg",
        "New Orleans Pelicans": "https://cdn.nba.com/teams/uploads/sites/1610612740/2021/12/pelicans_primary_logo.svg",
        "New York Knicks": "https://upload.wikimedia.org/wikipedia/en/2/25/New_York_Knicks_logo.svg",
        "Oklahoma City Thunder": "https://upload.wikimedia.org/wikipedia/it/5/5d/Oklahoma_City_Thunder.svg",
        "Orlando Magic": "https://upload.wikimedia.org/wikipedia/it/b/bd/Orlando_Magic_logo2.svg",
        "Philadelphia 76ers": "https://upload.wikimedia.org/wikipedia/it/6/68/Philadelphia_76ers_logo2.svg",
        "Phoenix Suns": "https://cdn.nba.com/teams/uploads/sites/1610612756/2022/08/suns-logo.svg",
        "Portland Trail Blazers": "https://upload.wikimedia.org/wikipedia/en/2/21/Portland_Trail_Blazers_logo.svg",
        "Sacramento Kings": "https://upload.wikimedia.org/wikipedia/it/c/c7/SacramentoKings.svg",
        "San Antonio Spurs": "https://upload.wikimedia.org/wikipedia/it/a/a2/San_Antonio_Spurs.svg",
        "Toronto Raptors": "https://upload.wikimedia.org/wikipedia/it/e/e3/Toronto_Raptors_logo2.svg",
        "Utah Jazz": "https://upload.wikimedia.org/wikipedia/it/0/04/Utah_Jazz_logo_%282016%29.svg",
        "Washington Wizards": "https://upload.wikimedia.org/wikipedia/it/a/af/Washington_Wizards_logo2.svg"
    }
    return logo_data


# Questa funzione permette di ottenere tutte le statistiche generali
# di una squadra selezionata dall'utente
def get_info(selected_team, team_data):
    logo_data = get_logo_data()
    logo, description = st.columns(2)
    selected_team_id = team_data["id"].item()
    
    # Ricavo le informazioni di background sulla squadra selezionata
    background_team_info = TeamDetails(selected_team_id).team_background.get_data_frame()

    # Inserisco sulla parte sinistra dello schermo il logo della squadra
    logo.image(logo_data[selected_team], width = 300)
    # Inserisco sulla parte destra dello schermo un elenco puntato con 
    # alcune informazioni sulla squadra
    description.markdown(
        f"## {selected_team} ({team_data['abbreviation'].item()}) "
        )
    description.markdown(
        f"- **Stato:** {team_data['state'].item()}\n" \
        f"- **Anno di fondazione:** {team_data['year_founded'].item()}\n" \
        f"- **Arena:** {background_team_info['ARENA'].item()} ({background_team_info['ARENACAPACITY'].item()} posti)\n" \
        f"- **Proprietario:** {background_team_info['OWNER'].item()}\n" \
        f"- **General Manager:** {background_team_info['GENERALMANAGER'].item()}\n" \
        f"- **Allenatore:** {background_team_info['HEADCOACH'].item()}\n" \
        f"- **Squadra D-League associata:** {background_team_info['DLEAGUEAFFILIATION'].item()}" 
    )
    
    # Ottengo una breve descrizione della squadra
    team_description(selected_team_id)
    
    # Inserisco dei link alla fine della pagina
    nba_link = f"https://www.nba.com/{team_data['nickname'].item()}/"
    wiki_link = f"https://it.wikipedia.org/wiki/{team_data['full_name'].item().replace(' ','_')}"
    st.markdown(f""" 
        Altri link:
        - **[NBA.com]({nba_link})**
        - **[Wikipedia]({wiki_link})**
        """
    )


# Questa funzione fornisce un breve riassunto della storia di 
# una squadra dato in input l'id della squadra selezionata
def team_description(selected_team_id):
    # Mostro le informazioni sui campionati vinti
    championship_data = TeamDetails(selected_team_id).team_awards_championships.get_data_frame()
    team_rings = len(championship_data)
    if team_rings == 0:
        st.write("Questa squadra non ha ancora vinto un campionato")
    else:
        championship_trophy = "https://imagez.tmz.com/image/b5/o/2022/05/12/b56b50f62a67485baaf0c434cdf22504.jpg"
        st.markdown(f" **Numero di campionati vinti:** {team_rings}")
        if team_rings > 12:
            # Fanno eccezione i troppi campionati vinti da Celtics e Lakers
            rings_columns = st.columns(6)
            index = 0
            while index < team_rings:
                for i in range(6):
                    if index >= team_rings:
                        break
                    with rings_columns[i]:
                        st.image(championship_trophy, 
                                caption = championship_data['YEARAWARDED'].iloc[index])
                    index += 1
                    
                    
        else:
            rings_columns = st.columns(team_rings)
            for i in range(team_rings):
                with rings_columns[i]:
                    st.image(championship_trophy, 
                            caption = championship_data['YEARAWARDED'].iloc[i],
                            width = 80)
    
    # Mostro i titoli di conference
    conference_data = TeamDetails(selected_team_id).team_awards_conf.get_data_frame()
    conference_titles = len(conference_data)
    if conference_titles == 0:
        st.write("Questa squadra non ha ancora vinto un titolo di conference")
    else:
        st.markdown(f" **Numero di titoli di conference vinti:** {conference_titles}")
        
    # Mostro i titoli di divisione
    division_data = TeamDetails(selected_team_id).team_awards_div.get_data_frame()
    division_titles = len(division_data)
    if division_titles == 0:
        st.write("Questa squadra non ha ancora vinto un titolo di divisione")
    else:
        st.markdown(f" **Numero di titoli di divisione vinti:** {division_titles}")
        
    # Mostro i giocatori che sono stati eletti nella hall of fame
    hof_data = TeamDetails(selected_team_id).team_hof.get_data_frame()
    # Seleziono solo le colonne effettivamente interessanti
    hof_data = hof_data[['PLAYER', 'POSITION', 'SEASONSWITHTEAM']]
    # Rinomino la colonna 'SEASONWITHTHETEAM'
    hof_data = hof_data.rename(columns = {'SEASONSWITHTEAM': 'SEASONS WITH THE TEAM'})
    hof_link = "https://it.wikipedia.org/wiki/Membri_del_Naismith_Memorial_Basketball_Hall_of_Fame"
    st.markdown("---")
    st.write(f"Elenco giocatori eletti nella Hall of Fame che hanno vestito \
             la canotta della squadra selezionata:")
    st.dataframe(hof_data, hide_index = True)
    with st.expander(f"Clicca qui per avere maggiori informazioni \
                     sulla Hall of Fame"):
        st.write(f"L'Hall of Fame [(HOF)]({hof_link}) è un'istituzione che \
                racchiude coloro che hanno lasciato un'impronta indelebile nella \
                storia del basket mondiale. Questo onore non è destinato solamente \
                a giocatori o allenatori, ma a chiunque abbia dato un contributo \
                significativo a questo sport") 
    
    # Mostro i giocatori per cui la squadra ha ritirato la maglia 
    retired_jersey_data = TeamDetails(selected_team_id).team_retired.get_data_frame()
    # Seleziono solo le colonne effettivamente interessanti
    retired_jersey_data = retired_jersey_data[['PLAYER', 'POSITION',
                                              'JERSEY', 'SEASONSWITHTEAM']]
    # Rinomino la colonna 'SEASONWITHTHETEAM'
    hof_data = hof_data.rename(columns = {'SEASONSWITHTEAM': 'SEASONS WITH THE TEAM'})
    st.write("")
    st.write("Elenco maglie ritirate della squadra selezionata:")
    st.dataframe(retired_jersey_data, hide_index = True)
    with st.expander(f"Clicca qui per avere maggiori informazioni sul ritiro \
                     delle maglie"):
        st.write(f"Il ritiro di una maglia da parte di una squadra NBA è uno dei \
                massimi onori che una franchigia possa conferire a un giocatore. \
                Quando una maglia viene ritirata, nessun altro giocatore di quella \
                squadra può indossare il numero associato, come segno di rispetto \
                e riconoscimento per il contributo straordinario del giocatore \
                alla squadra e alla sua storia. Questo gesto non riguarda solo \
                i giocatori, ma anche altre figure significative all’interno \
                dell’organizzazione, come allenatori, dirigenti, o altre \
                personalità che hanno avuto un impatto fondamentale. Può \
                accadere che una squadra decida di ritirare un numero \
                di maglia per omaggiare un giocatore che non ha mai \
                giocato per tale squadra: l'esempio più lampante di ciò \
                è il ritiro della maglia numero 23 di Michael Jordan \
                da parte dei Miami Heat, squadra che Jordan ha affrontato \
                solo da avversario. ")
        
    social_media_data = TeamDetails(selected_team_id).team_social_sites.get_data_frame()
    st.markdown("---")
    # Creo una lista di link per i vari social ufficiali della squadra selezionata
    # Crea una lista di link con il formato desiderato
    elenco_link = f"Link ai social network ufficiali della \
                   squadra selezionata:\n"
    for index, row in social_media_data.iterrows():
        elenco_link += f"- [{row['ACCOUNTTYPE']}]({row['WEBSITE_LINK']})\n"
    st.markdown(elenco_link)
    

# Questa funzione mostra le statistiche di tutti i giocatori di una squadra
# secondo i vari parametri selezionati
def get_team_stats():
    pass


# Funzione principale per la mappa
def squadre():
    st.title("Sezione squadre")
    st.write("")

    # Ottieni e processa i dati
    nba_data = get_nba_teams()
    nba_data = add_coordinates(nba_data)
    
    # Impostazione della variabile di stato per la squadra selezionata
    if "selected_team" not in st.session_state:
        st.session_state["selected_team"] = None

    # Tooltip e visualizzazione interattiva
    tooltip = {
        "html": "{full_name}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    # Configurazione dello stato della vista
    view_state = pdk.ViewState(
        latitude = nba_data["latitude"].mean(),
        longitude = nba_data["longitude"].mean() - 3,
        zoom = 3,
        pitch = 0
    )

    # Layer con punti interattivi
    layer = pdk.Layer(
        "ScatterplotLayer",
        data = nba_data,
        get_position = ["longitude", "latitude"],
        get_color = [255, 255, 255, 255],
        get_radius = 40000,
        pickable = True,
        auto_highlight = True,
        tooltip = tooltip
    )

    # Configurazione della mappa
    deck = pdk.Deck(
        layers = [layer],
        initial_view_state = view_state,
        tooltip = tooltip
    )

    # Streamlit layout
    st.pydeck_chart(deck)
    
    # L'utente seleziona la squadra manualmente
    selected_team = st.selectbox("", nba_data["full_name"])
    st.write("")
    
    # Creo delle diverse tab, una per mostrare le caratteristiche generali della 
    # squadra selezionata, l'altra per mostrare le statistiche
    
    team_tabs = st.tabs(["Informazioni generali", "Statistiche"])
    with team_tabs[0]:
        # Filtro il dataframe per ottenere informazioni solamente
        # sulla squadra selezionata
        filtered_data = nba_data[nba_data["full_name"] == selected_team]
        get_info(selected_team, filtered_data)
    with team_tabs[1]:
        get_team_stats()
        
    
    
    
        
    
squadre()  


    
    
    
    
    
    
    
    
    
    
    
    
    




