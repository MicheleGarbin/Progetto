import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from nba_api.stats.endpoints import LeagueLeaders
from sklearn.linear_model import LinearRegression


st.set_page_config(
    page_title = "NBA App",
    page_icon = "🏀"
)

st.title("L'evoluzione del gioco del basket")

st.sidebar.success("Seleziona una pagina tra quelle indicate sopra")

# Introduzione generale
st.markdown("""
            Negli ultimi 40 anni sono avvenuti dei cambiamenti radicali, che
            hanno modificato per sempre lo stile di gioco di questo sport.
            Ciò è dovuto a vari fattori tra cui: l'introduzione di nuove
            regole, l'applicazione della statistica e informatica e il fatto 
            che i giocatori hanno via via allargato il proprio skillset. 
            In seguito vengono mostrati i passaggi chiave che hanno permesso 
            tutto questo.
            """)

st.markdown("---")

# L'introduzione della linea da 3 e gli anni '80
st.markdown("""
            ## Gli anni '80: una rivoluzione silenziosa
            
            L'NBA introdusse la linea da tre punti all'alba della 
            stagione 1979-1980. L’obiettivo era aumentare il dinamismo 
            del gioco e premiare la distanza e la precisione, ma 
            inizialmente il tiro da tre fu visto più come una curiosità 
            che una vera arma tattica. Il gioco rimase incentrato sui lunghi 
            dominanti e sulle conclusioni ravvicinate, con le triple usate 
            quasi esclusivamente allo scadere dei 24 secondi dell'azione.
            """
)
col1, col2 = st.columns([2, 1])
image_url = "https://golfdigest.sports.sndimg.com/content/dam/images/golfdigest/fullset/2020/02/06/5e3c512120782d0008895e43_GettyImages-912730536.jpg.rend.hgtvcom.966.544.suffix/1581450522179.jpeg"
with col1:
    st.markdown("""        
                E' interessante soffermarsi su uno degli scorer più prolifici
                di quegli anni: Larry Bird. Egli conduce la classifica della 
                decade per triple segnate con 649; un buon tiratore nel basket 
                moderno raggiunge questo tragurado in sole due stagioni. 
                Nonostante avesse delle buone percentuali, Larry Legend
                tentava a malapena 3 triple a partita. Stiamo parlando 
                di un giocatore 3 volte campione del 3-Point Contest,
                universalmente riconosciuto come uno dei tiratori 
                più forti della storia del basket; figurarsi gli 
                altri giocatori quanto poco usassero il tiro oltre l'arco.
                """)
with col2:
    st.image(image_url, caption = "Larry Bird al 3-Point Contest del 1988")
    
# Gli anni '90: Reggie Miller e l'attacco a triangolo
st.markdown("""
            ## Gli anni '90: il dominio Bulls 
            """)
col1, col2 = st.columns([2, 1])
image_url = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhjWjdN6VF4dTkDekXkJINJYrbTzeu1dNYFLqc6l-9OOBnrEt8ZziTpg0rVKwpyul2V6YXneBrtFSt5YAd2zyd78p45vSu5nWENvE9BmWvgcWxzNHNXvjJ6Kwnl6LXzRQzrztbUAaDt-bQ/s1600/download.jpg"
with col1:
    st.markdown("""
                6 titoli in 8 anni. Questi sono i numeri che Michael Jordan,
                Scottie Pippen e Phil Jackson possono vantare. Proprio 
                quest'ultimo, assieme al suo vice Tex Winter, ha dato via
                a un nuovo modo di vedere il basket: l'attacco a triangolo.
                E' un sistema offensivo altamente dinamico e basato su principi 
                di spacing, letture e movimenti sincronizzati tra i giocatori: 
                una volta che si forma il triangolo (i vertici in questo caso
                sono giocatori o in post o sul perimetro) ci sono 33 sviluppi possibili
                che lo rendono quasi imprevedibile. Questa filosofia di gioco 
                ha permesso a Jackson di vincere altri 5 anelli nella
                decade successiva.
                """)
with col2:
    st.image(image_url, caption = "Esempio di attacco a triangolo")
col1, col2 = st.columns([2, 1])
image_url = "https://www.si.com/.image/t_share/MTY4MTg2NjkxMTg4ODkyOTQ1/2000-0607-reggie-miller--kobe-bryant-001158700jpg.jpg"
with col1:
    st.markdown("""
                Un giocatore di quell'epoca tra i più impattanti di sempre 
                per quanto riguarda il tiro da 3 è sicuramente Reggie Miller.
                Egli giocava quasi come una shooting guard moderna: prendeva un 
                numero di tiri da tre a partita impensabile per l'epoca, tanto 
                che tuttora è sesto all - time per triple segnate in carriera;
                era capace di muoversi senza palla, correva su e giù per
                il campo, spesso navigando tra i blocchi. Nonostante giocasse un basket 
                inusuale per l'epoca è comunque entrato nell'HOF, lasciando
                un segno indelebile nella storia di questo sport.
                """)    
with col2:
    st.image(image_url, caption = "Miller marcato da Kobe")
    
st.markdown("---")

# Daryl Morey e Mike D'Antoni
st.markdown("""
            ## Moreyball: il basket diventa data-driven
            
            Leggendo il titolo appare lampante l'analogia con "Moneyball", 
            il famoso film (ispirato a una storia vera) in cui il GM 
            di una squadra di baseball rende la propria squadra competitiva 
            basando le decisioni sui dati. Daryl Morey ha dato il via alla
            stessa rivoluzione nel basket. 

            Se si analizza il numero di punti atteso per tiro e si considerano
            delle buone percentuali di realizzazione si ottengono i seguenti
            risultati:
            """)
data = {
    "Tipo di tiro": ["Tiro dal pitturato", "Tiro dal midrange", "Tiro da tre"],
    "Punti per tiro": [2, 2, 3],
    "Percentuale al tiro": ["60%", "50%", "40%"],
    "Punti attesi per tiro": [1.2, 1.0, 1.2]
}
shot_type = pd.DataFrame(data)
st.dataframe(shot_type, hide_index = True)
st.markdown("""
            Semplificando molto, si può notare che i tiri più efficienti
            siano soprattutto layup/schiacciate e tiri da tre; una volta capita
            l'importanza di questi tiri, Morey cominciò ad insistere affinchè
            la sua squadra, gli Houston Rockets, li utilizzasse di più. 
            
            Oltre alla scelta di tiro, le statistiche mostrano che,
            aumentando il numero di possessi e a parità di efficienza 
            offensiva, si possono produrre più punti; si deve cercare inoltre 
            di generare punti in transizione, sfruttando il fatto che la 
            difesa non sia ben schierata. Il primo a capire 
            questo fu Mike D'Antoni che, con i Phoenix Suns, introdusse la
            filosofia "7 seconds or less", ossia: cercare di tirare nei primi
            7 secondi di un'azione per avere più possessi e sfruttare la
            transizione per generare più punti. 
            
            Nel 2016 proprio D'Antoni raggiunge Morey a Houston in qualità
            di allenatore. Il mondo delle analytics aveva già fatto passo da 
            gigante rispetto a un decennio prima, ma proprio ai Rockets
            queste due grandi menti danno vita a un nuovo modo di intendere un
            quintetto: nasce il "gioco della palla piccola". Esso si basava su una 
            lineup senza centri tradizionali, sostituendoli con giocatori più agili 
            e versatili, in grado di spaziare il campo e tirare da tre punti. 
            Houston schierò per diverse partite giocatori sotto i 2 metri, riuscendo
            nell'intento di contenere squadre con giocatori molto più alti e fisici.
            Il giocatore chiave in questo sistema fu James Harden, che divenne 
            il fulcro dell’attacco, spesso agendo come playmaker e creando gioco 
            dal pick and roll. Harden è stato un maestro negli isolamenti, capace
            di sfruttare come nessuno prima il tiro in stepback, ossia
            il tiro preceduto da un passo all'indietro che permette all'attaccante
            di crearsi spazio dal difensore.
            
            """)
col1, col2, col3 = st.columns(3)
with col1:
    image_url = "https://cdn.nba.com/manage/2023/05/morey-iso051723.jpg"
    st.image(image_url, caption = "Daryl Morey, attuale BPA dei 76ers", width = 220)
with col2:
    image_url = "https://static.independentespanol.com/s3fs-public/thumbnails/image/2020/09/03/16/gettyimages-1028896540.jpg?quality=75&width=1250&crop=3%3A2%2Csmart&auto=webp"
    st.image(image_url, caption = "Steve Nash entra nell'HOF", width = 190)
with col3:
    image_url = "https://a1.espncdn.com/combiner/i?img=%2Fphoto%2F2020%2F0901%2Fr664851_2_1296x729_16%2D9.jpg&w=1140&cquality=40&format=jpg"
    st.image(image_url, caption = "Harden esegue uno stepback")

st.write("")

# Anni 2010:
st.markdown("""
            ## Curry e i Warriors: un modello di basket vincente
            """)
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
            "Il Michael Jordan dei giorni nostri": è così che Steve Kerr,
            allenatore dei Warriors, ha definito Steph Curry.
            Curry è stato fondamentale nella rivoluzione del gioco del basket, 
            in particolare nel rendere il tiro da tre punti una parte centrale 
            dell’attacco NBA. Le sue straordinarie capacità di tiro a lunga distanza, 
            la rapidità nel rilascio e la capacità di segnare con alta precisione 
            anche sotto pressione hanno trasformato il ruolo della guardia e cambiato 
            per sempre l’approccio offensivo delle squadre.
            """)        
with col2:
    image_url = "https://i.pinimg.com/736x/aa/7d/cb/aa7dcbbb6b5aac46e39ebed56d2ffd3c.jpg"
    st.image(image_url, caption = "MVP all'unanimità, unico all-time")
st.markdown("""
            Il basket dei Warriors si basa sì sul tiro da 3 punti, ma 
            soprattutto sull'idea di "motion offense": i lunghi si muovono 
            per portare blocchi e ricevere al gomito in high - post, fornendo
            spesso assist per i compagni; le guardie cercano di disorientare 
            la difesa muovendosi il più possibile, che sia passando dai blocchi 
            per ricevere e tirare da tre o con tagli sotto canestro 
            per dei comodi layup. Steve Kerr ha ideato questo sistema
            basandosi sia sui propri giocatori ma anche sull'attacco a 
            triangolo visto sopra: egli ha giocato infatti sotto la guida 
            di Phil Jackson dal '94 al '98. 
            
            La ricerca del tiro da 3 favorisce molto lo spacing: più i giocatori 
            sono distanti, più spazi ci sono e più opzioni ha chi attacca.
            I movimenti/giochi possibili diventano tanti e i giocatori 
            devono essere in grado di scegliere il migliore, come nell'attacco
            dei Bulls. Una volta rodato, il gioco diventa fluido e difficilmente 
            arginabile.
            
            Tutto questo ha portato i Warriors a 6 finali e 4 titoli
            nell'arco di 8 anni. Tutte le squadre NBA da lì a poco 
            hanno ricercato molto di più il tiro da 3 e il basket 
            "positionless", ossia con giocatori capaci di saper fare 
            un po' di tutto. L'efficienza offensiva registrata nelle ultime
            stagioni non è mai stata così alta.
            """)

st.markdown("---")

# Al giorno d'oggi
st.markdown("""
            ## Qual è la situazione attuale?
            
            Il tiro da tre punti, oltre all'aumento dei possessi, è in continua
            evoluzione: sembra che il boom della scorsa decade non sia bastato. 
            Il volume di tiri da tre continua ad aumentare, così come l'efficienza
            offensiva: l'NBA sta attirando sempre più talenti da tutto il mondo
            con uno skillset molto superiore al giocatore medio di 20 anni fa.
            Il midrange non è più utilizzato dalla maggior
            parte dei giocatori da anni (fanno eccezioni giocatori 
            "old school" come Durant, DeRozan e Booker). Il gioco offensivo delle
            squadre passerà sempre più per il tiro da 3 punti e per l'aumento dei
            possessi fintanto che tiri più complicati verranno realizzati. 
            
            Negli anni l'NBA ha sempre di più favorito l'attacco, rimuovendo
            ad esempio l'handcheck, ovvero la possibilità per il difensore di
            posare le mani e direzionare il portatore di palla; negli ultimi 
            anni vengono fischiati molti falli al tiro, soprattutto verso le
            superstar. 
            
            Fintanto che:
            - l'abilità generale nel realizzare i tiri da 3 non giunge a un limite
            - le chiamate arbitrali favoriscono l'attacco piuttosto che la difesa
            
            il volume di tiri da tre tentati e l'efficienza offensiva 
            difficilmente diminuiranno.
            """)

st.write("")
# Ricavo il numero di tiri da tre tentati da ogni squadra nella lega
# Creo un elenco delle stagioni da considerare
season_list = []
for i in range(1979, 2024):
    season = f"{i}-{i + 1}"
    season_list.append(season[:5] + season[7:])
# Creo una lista vuota dove ciascun elemento mi rappresenta il numero di
# tiri tentati in una determinata stagione; siccome questi dati servono per
# un grafico che viene sempre mostrato, me li salvo in un file a parte
# per evitare di fare 45 chiamate ogni volta all'API. Di seguito è riportata
# la procedura che ha portato alla creazione del file con i suddetti dati
if False:
    three_point_volume = []
    for season in season_list:
        # Ricavo i leader per ogni statistica della lega, in sostanza 
        # un elenco completo dei giocatori con i rispettivi valori
        # per le metriche principali, tra cui il numero di tiri da tre tentati
        league_leaders = LeagueLeaders(season = season).league_leaders.get_data_frame()
        # Mi salvo nella lista complessiva il numero di tiri da tre tentati in
        # una certa stagione, ovvero la somma dei tiri da tre tentati da 
        # ciascun giocatore
        three_point_volume.append(league_leaders["FG3A"].sum())
    file_name = "data/three_point_volume.txt"
    with open(file_name, "w") as file:
        for elemento in three_point_volume:
            file.write(str(elemento) + "\n")
# Salvo in una lista le informazioni sui tiri da tre punti tentati
# nella varie stagioni contenute in data/three_point_volume
with open("data/three_point_volume.txt", "r") as file:
    three_point_volume = [int(line.strip()) for line in file.readlines()]
# Salvo in un dataframe le varie stagioni e il numero di tiri da tre tentati 
# in ciascuna di queste
three_point_volume = pd.DataFrame({
    "Stagione": season_list,
    "3PFGA": three_point_volume
})

# Preparazione dei dati per la regressione
# Converto l'asse x (stagioni) in numeri per la regressione
x = np.array(range(len(three_point_volume))).reshape(-1, 1)
y = three_point_volume["3PFGA"]  
model = LinearRegression()
model.fit(x, y)
# Predizione dei valori di y con il modello
three_point_volume["Previsione"] = model.predict(x)
# Estrazione di R^2 (indice della bontà d'adattamento)
r_squared = model.score(x, y)

chart = (
    alt.Chart(three_point_volume)
    .mark_line(point = True, color = "#00FF00")  
    .encode(
        x = alt.X("Stagione:N", axis = alt.Axis(title = "🟢 Valori osservati\t\t\t\t🟡 Retta di regressione stimata")),  
        y = alt.Y("3PFGA:Q", title = "Tiri da 3 punti tentati"),
        tooltip = ["Stagione", "3PFGA"]
    )
    .properties(
        title = f"Tiri da tre punti tentati per ogni stagione (R² = {r_squared:.2f})"
    )
)
regression_line = (
    alt.Chart(three_point_volume)
    .mark_line(strokeDash = [5, 5], color = "#FFFF00")
    .encode(
        x = alt.X("Stagione:N", title = ""),
        y = alt.Y("Previsione:Q", title = "")
    )
)
st.altair_chart(chart + regression_line, use_container_width = True)

st.markdown("""
            Il trend è visibilmente lineare e positivo; l'adattamento
            secondo R - quadro è molto buono. Emergono
            tuttavia dei punti "anomali", per i quali serve 
            fare alcune precisazioni:
            - nelle stagioni 1995-96 e 1996-97 la NBA diminuì la 
              distanza della linea da tre di 54 cm; questo portò molti
              più giocatori ad utilizzare il tiro oltre l'arco. Dal 1998 
              la distanza tornò ad essere 7.24 metri e il valore osservato
              segue il trend generale.
            - l'inizio della stagione 1998-99 fu posticipato 
              per uno sciopero generale dei giocatori; le squadre giocarono
              32 partite in meno di Regular Season.
            - nella stagione 2011-12 fu indetto uno nuovo sciopero dei giocatori:
              le partite giocate furono solamente 66.
            - a causa del covid da marzo 2020 a luglio 2020 non si giocò
              nessuna partita; nella stagione 2019-20 e in quella successiva
              le squadre giocarono almeno 72 partite per stagione.
            """)














