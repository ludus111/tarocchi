import streamlit as st
import random
import os
from PIL import Image

st.set_page_config(page_title="Tarocchi", page_icon="🔮", layout="centered")

arcani_maggiori = [
    "Il Matto", "Il Mago", "La Papessa", "L'Imperatrice", "L'Imperatore",
    "Il Papa", "Gli Amanti", "Il Carro", "La Forza", "L'Eremita",
    "La Ruota della Fortuna", "La Giustizia", "L'Appeso", "La Morte",
    "La Temperanza", "Il Diavolo", "La Torre", "La Stella", "La Luna",
    "Il Sole", "Il Giudizio", "Il Mondo"
]

disposizioni = {
    "singola": ["Risposta"],
    "si_no": ["Carta 1", "Carta 2", "Carta 3"],
    "tre_carte": ["Passato", "Presente", "Futuro"],
    "cinque_carte": ["Situazione attuale", "Ostacolo", "Passato recente", "Futuro prossimo", "Esito"],
    "ferro_di_cavallo": ["Passato", "Presente", "Futuro prossimo", "Te stesso/a", "Ambiente circostante", "Ostacoli o aiuti", "Esito finale"],
    "croce_celtica": ["Situazione attuale", "Sfida/ostacolo", "Base/radice", "Passato recente", "Obiettivo/meta possibile", "Futuro prossimo", "Te stesso/a", "Ambiente", "Speranze e paure", "Esito finale"],
    "relazionale": ["Tu", "L'altra persona", "La relazione", "Cosa ti serve", "Cosa serve all'altro/a", "Direzione futura"],
    "ruota_anno": [f"Mese {i+1}" for i in range(12)],
}

etichette_disposizioni = {
    "singola": "Carta singola (1 carta)",
    "si_no": "Sì o No (3 carte)",
    "tre_carte": "Tre carte - Passato/Presente/Futuro",
    "cinque_carte": "Cinque carte a croce",
    "ferro_di_cavallo": "Ferro di cavallo (7 carte)",
    "croce_celtica": "Croce celtica (10 carte)",
    "relazionale": "Stesa relazionale (6 carte)",
    "ruota_anno": "Ruota dell'anno (12 carte)",
}

def percorso_immagine(nome_carta):
    indice = arcani_maggiori.index(nome_carta)
    nome_file = f"immagini/{indice:02d}.jpg"
    return nome_file if os.path.exists(nome_file) else None

def carica_immagine_carta(nome_carta, orientamento):
    percorso = percorso_immagine(nome_carta)
    if percorso is None:
        return None
    img = Image.open(percorso)
    if orientamento == "rovesciata":
        img = img.rotate(180)
    return img

def pesca_carta_singola(carte_gia_pescate):
    disponibili = [c for c in arcani_maggiori if c not in carte_gia_pescate]
    carta = random.choice(disponibili)
    orientamento = random.choice(["dritta", "rovesciata"])
    return carta, orientamento

# --- Visualizzazione di una singola posizione (immagine nativa, cliccabile per ingrandire) ---

def mostra_posizione(etichetta, indice, carte):
    if indice in carte:
        nome_carta, orientamento = carte[indice]
        img = carica_immagine_carta(nome_carta, orientamento)
        if img is not None:
            st.image(img, caption=etichetta, use_container_width=True)
        else:
            st.write(f"**{etichetta}**")
            st.write("Immagine non ancora disponibile")
    else:
        st.markdown(
            f"<div style='background:#eee;border-radius:10px;min-height:160px;"
            f"display:flex;align-items:center;justify-content:center;color:#888;"
            f"text-align:center;padding:10px;font-size:13px;'>{etichetta}</div>",
            unsafe_allow_html=True,
        )

# --- Layout per ogni disposizione ---

def render_riga(nome_disposizione, carte):
    etichette = disposizioni[nome_disposizione]
    colonne = st.columns(len(etichette))
    for indice, (colonna, etichetta) in enumerate(zip(colonne, etichette)):
        with colonna:
            mostra_posizione(etichetta, indice, carte)

def render_cinque_carte(carte):
    etichette = disposizioni["cinque_carte"]
    sopra = st.columns(3)
    with sopra[1]:
        mostra_posizione(etichette[1], 1, carte)
    centro = st.columns(3)
    with centro[0]:
        mostra_posizione(etichette[2], 2, carte)
    with centro[1]:
        mostra_posizione(etichette[0], 0, carte)
    with centro[2]:
        mostra_posizione(etichette[3], 3, carte)
    sotto = st.columns(3)
    with sotto[1]:
        mostra_posizione(etichette[4], 4, carte)

def render_ferro_di_cavallo(carte):
    etichette = disposizioni["ferro_di_cavallo"]
    offset_px = [70, 40, 15, 0, 15, 40, 70]
    colonne = st.columns(7)
    for indice, (colonna, etichetta) in enumerate(zip(colonne, etichette)):
        with colonna:
            st.markdown(f"<div style='height:{offset_px[indice]}px'></div>", unsafe_allow_html=True)
            mostra_posizione(etichetta, indice, carte)

def render_relazionale(carte):
    etichette = disposizioni["relazionale"]
    riga1 = st.columns(3)
    for colonna, indice in zip(riga1, [0, 2, 1]):
        with colonna:
            mostra_posizione(etichette[indice], indice, carte)
    riga2 = st.columns(3)
    for colonna, indice in zip(riga2, [3, 5, 4]):
        with colonna:
            mostra_posizione(etichette[indice], indice, carte)

def render_croce_celtica(carte):
    etichette = disposizioni["croce_celtica"]
    area_croce, area_bastone = st.columns([3, 1])
    with area_croce:
        sopra = st.columns(3)
        with sopra[1]:
            mostra_posizione(etichette[4], 4, carte)
        centro = st.columns(3)
        with centro[0]:
            mostra_posizione(etichette[3], 3, carte)
        with centro[1]:
            mostra_posizione(etichette[0], 0, carte)
            mostra_posizione(etichette[1], 1, carte)
        with centro[2]:
            mostra_posizione(etichette[5], 5, carte)
        sotto = st.columns(3)
        with sotto[1]:
            mostra_posizione(etichette[2], 2, carte)
    with area_bastone:
        for indice in [9, 8, 7, 6]:
            mostra_posizione(etichette[indice], indice, carte)

def render_ruota_anno(carte):
    etichette = disposizioni["ruota_anno"]
    for inizio_riga in range(0, 12, 4):
        colonne = st.columns(4)
        for offset, colonna in enumerate(colonne):
            indice = inizio_riga + offset
            with colonna:
                mostra_posizione(etichette[indice], indice, carte)

def render_stesa(nome_disposizione, carte):
    if nome_disposizione in ("singola", "si_no", "tre_carte"):
        render_riga(nome_disposizione, carte)
    elif nome_disposizione == "cinque_carte":
        render_cinque_carte(carte)
    elif nome_disposizione == "ferro_di_cavallo":
        render_ferro_di_cavallo(carte)
    elif nome_disposizione == "relazionale":
        render_relazionale(carte)
    elif nome_disposizione == "croce_celtica":
        render_croce_celtica(carte)
    elif nome_disposizione == "ruota_anno":
        render_ruota_anno(carte)

# --- Stato persistente ---

if "carte" not in st.session_state:
    st.session_state.carte = {}
if "carte_pescate" not in st.session_state:
    st.session_state.carte_pescate = []
if "disposizione_corrente" not in st.session_state:
    st.session_state.disposizione_corrente = None

st.title("🔮 Tarocchi")

scelta = st.selectbox(
    "Scegli il metodo di lettura",
    options=list(etichette_disposizioni.keys()),
    format_func=lambda k: etichette_disposizioni[k],
)

if st.button("Inizia stesa"):
    st.session_state.disposizione_corrente = scelta
    st.session_state.carte = {}
    st.session_state.carte_pescate = []

if st.session_state.disposizione_corrente:
    nome_disposizione = st.session_state.disposizione_corrente
    etichette = disposizioni[nome_disposizione]
    completa = len(st.session_state.carte) >= len(etichette)

    if st.button("Pesca la prossima carta", disabled=completa):
        indice_corrente = len(st.session_state.carte)
        nome_carta, orientamento = pesca_carta_singola(st.session_state.carte_pescate)
        st.session_state.carte_pescate.append(nome_carta)
        st.session_state.carte[indice_corrente] = (nome_carta, orientamento)

    render_stesa(nome_disposizione, st.session_state.carte)

    if completa:
        st.success("Stesa completa!")
