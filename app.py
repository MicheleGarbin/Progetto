import streamlit as st

from main_page import main_page
from analisi_tecnica import analisi_tecnica
from squadre import squadre
from giocatori import giocatori

title = st.sidebar.selectbox(
    "",
    ["Pagina principale", "Analisi tecnica", "Squadre", "Giocatori"]
)

if title == "Pagina principale":
    main_page()
elif title == "Analisi tecnica":
    analisi_tecnica()
elif title == "Squadre":
    squadre()
else:
    giocatori()
    




    


