import streamlit as st
import pydeck as pdk
import pandas as pd
from nba_api.stats.static import teams
from PIL import Image
import requests
import io
import cairosvg


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


# Questa funzione restituisce un'immagine presa da un link/path ridimensionata
def load_image(svg_file):
    # Tratto in maniera diversa i file svg che prendo da internet rispetto 
    # a quelli che ho nella cartella locale Logos
    if svg_file[0] == "h":
        response = requests.get(svg_file)
        svg_file = response.content
    else:
        with open(svg_file, "rb") as f:
            svg_file = f.read()
    # Converti l'SVG in PNG usando cairosvg
    png_data = cairosvg.svg2png(bytestring = svg_file)
    # Salvo il PNG in memoria con Pillow
    image =  Image.open(io.BytesIO(png_data))
    # Ottengo le dimensioni
    width, height = image.size
    ratio = width / height
    # Restituisco l'immagine ridimensionata
    return image.resize((150, int(150 / ratio)))


# Questa funzione restituisce un dataframe con dentro gli url dei vari loghi 
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
    st.write("")
    
    logo_data = get_logo_data()
    for team_name in logo_data:
        st.write(team_name)
        st.image(load_image(logo_data[team_name]))
        
    
    


    
    
    
    
    
    
    
    
    
    
    
    
    




