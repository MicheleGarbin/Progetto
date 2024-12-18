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
        "Washington Wizards": (38.9072, -77.0369),
    }
    data["latitude"] = data["full_name"].map(lambda name: coordinates[name][0])
    data["longitude"] = data["full_name"].map(lambda name: coordinates[name][1])
    return data


def load_image(image_url):
    response = requests.get(image_url)
    svg_data = response.content
    # Converti l'SVG in PNG usando cairosvg
    png_data = cairosvg.svg2png(bytestring=svg_data)
    # Salvo il PNG in memoria con Pillow
    image =  Image.open(io.BytesIO(png_data))
    # Ottengo le dimensioni
    width, height = image.size
    ratio = width / height
    # Restituisco l'immagine ridimensionata
    return image.resize((150, int(150 / ratio)))


# Funzione principale per la mappa
def squadre():
    st.title("Mappa delle Squadre NBA")

    # Ottieni e processa i dati
    nba_data = get_nba_teams()
    nba_data = add_coordinates(nba_data)
    
    # Impostazione della variabile di stato per la squadra selezionata
    if "selected_team" not in st.session_state:
        st.session_state["selected_team"] = None

    # Tooltip e visualizzazione interattiva
    tooltip = {
        "html": "<b>Squadra:</b> {full_name}",
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
    
    # Dati delle squadre NBA con immagini associate
    teams_data = {
        "Los Angeles Lakers": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Los_Angeles_Lakers_logo.svg",
        "Boston Celtics": "https://upload.wikimedia.org/wikipedia/it/d/d4/Boston_Celtics_logo.svg"
    }

    # Selezione della squadra tramite pulsante
    selected_team = None
    for team_name, image_url in teams_data.items():
        # Carica l'immagine
        img = load_image(image_url)
        
        # Mostra il pulsante con l'immagine e il nome
        if st.button(label = team_name, help = "Clicca per selezionare", key = team_name):
            selected_team = team_name
            
        # Mostra l'immagine della squadra
        st.image(img, caption=team_name)
        
    # Visualizza il team selezionato se c'è
    if selected_team:
        st.write(f"Squadra selezionata: {selected_team}")
    
    
    
    
    
    
    
    
    
    
    
    




