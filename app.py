import streamlit as st
import random
import os
import math
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tarocchi", layout="centered")

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

def get_configurazione_layout(nome_disposizione):
    larghezza_carta, altezza_carta, figsize, extra_overlay = 0.14, 0.28, (11, 9), None

    if nome_disposizione in ("singola", "si_no", "tre_carte"):
        n = len(disposizioni[nome_disposizione])
        spazio = 0.04
        larghezza_totale = n * larghezza_carta + (n - 1) * spazio
        x_iniziale = (1 - larghezza_totale) / 2
        posizioni = {i: (x_iniziale + i * (larghezza_carta + spazio), 0.36) for i in range(n)}
        figsize = (max(4, 2.5 * n), 6)
    elif nome_disposizione == "cinque_carte":
        posizioni = {0: (0.43, 0.36), 1: (0.43, 0.68), 2: (0.16, 0.36), 3: (0.70, 0.36), 4: (0.43, 0.04)}
        figsize = (10, 9)
    elif nome_disposizione == "ferro_di_cavallo":
        posizioni = {0: (0.04, 0.05), 1: (0.17, 0.24), 2: (0.30, 0.40), 3: (0.44, 0.50),
                     4: (0.58, 0.40), 5: (0.71, 0.24), 6: (0.84, 0.05)}
        larghezza_carta, altezza_carta = 0.13, 0.24
        figsize = (13, 7)
    elif nome_disposizione == "relazionale":
        posizioni = {0: (0.08, 0.55), 1: (0.68, 0.55), 2: (0.38, 0.55),
                     3: (0.08, 0.15), 4: (0.68, 0.15), 5: (0.38, 0.15)}
        figsize = (11, 9)
    elif nome_disposizione == "ruota_anno":
        larghezza_carta, altezza_carta = 0.075, 0.15
        centro_x, centro_y, raggio = 0.5, 0.5, 0.37
        n = len(disposizioni[nome_disposizione])
        posizioni = {}
        for i in range(n):
            angolo = math.pi / 2 - i * (2 * math.pi / n)
            posizioni[i] = (centro_x + raggio * math.cos(angolo) - larghezza_carta / 2,
                             centro_y + raggio * math.sin(angolo) - altezza_carta / 2)
        figsize = (12, 12)
    elif nome_disposizione == "croce_celtica":
        posizioni = {0: (0.32, 0.36), 2: (0.32, 0.04), 3: (0.12, 0.36), 4: (0.32, 0.68),
                     5: (0.52, 0.36), 6: (0.80, 0.04), 7: (0.80, 0.28), 8: (0.80, 0.52), 9: (0.80, 0.76)}
        figsize = (11, 8.5)
        extra_overlay = {"indice_sovrapposto": 1, "indice_base": 0, "angolo": 90, "larghezza": 0.16, "altezza": 0.09}

    return posizioni, larghezza_carta, altezza_carta, figsize, extra_overlay

def disegna_stesa(nome_disposizione, carte):
    etichette = disposizioni[nome_disposizione]
    posizioni_grafiche, larghezza_carta, altezza_carta, figsize, extra_overlay = get_configurazione_layout(nome_disposizione)
    fig = plt.figure(figsize=figsize)
    for indice, etichetta in enumerate(etichette):
        if indice not in posizioni_grafiche:
            continue
        x, y = posizioni_grafiche[indice]
        ax = fig.add_axes([x, y, larghezza_carta, altezza_carta])
        ax.axis("off")
        if indice in carte:
            nome_carta, orientamento = carte[indice]
            img = carica_immagine_carta(nome_carta, orientamento)
            if img is not None:
                ax.imshow(img)
            else:
                ax.text(0.5, 0.5, "non disponibile", ha="center", va="center", fontsize=7, wrap=True)
            ax.set_title(etichetta, fontsize=7)
        else:
            ax.set_facecolor("#eeeeee")
            ax.text(0.5, 0.5, etichetta, ha="center", va="center", fontsize=7, wrap=True, color="#888888")
    if extra_overlay and extra_overlay["indice_sovrapposto"] in carte:
        nome_carta, orientamento = carte[extra_overlay["indice_sovrapposto"]]
        img = carica_immagine_carta(nome_carta, orientamento)
        if img is not None:
            img_ruotata = img.rotate(extra_overlay["angolo"], expand=True)
            x_centro, y_centro = posizioni_grafiche[extra_overlay["indice_base"]]
            lw, lh = extra_overlay["larghezza"], extra_overlay["altezza"]
            x_ov = x_centro + larghezza_carta / 2 - lw / 2
            y_ov = y_centro + altezza_carta / 2 - lh / 2
            ax_ov = fig.add_axes([x_ov, y_ov, lw, lh])
            ax_ov.imshow(img_ruotata)
            ax_ov.axis("off")
    return fig

# --- stato persistente tra un click e l'altro (in Colab erano variabili normali, qui servono session_state) ---
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

    fig = disegna_stesa(nome_disposizione, st.session_state.carte)
    st.pyplot(fig)

    if completa:
        st.success("Stesa completa!")
