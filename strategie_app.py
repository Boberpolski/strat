# strategie_app.py
import streamlit as st
import pandas as pd
from itertools import combinations_with_replacement
from pathlib import Path
import base64, textwrap

# ---------- ŚCIEŻKI DO ASSETÓW ----------
ROOT           = Path(__file__).parent
IMG_DIR        = ROOT / "images"
BACKGROUND_IMG = IMG_DIR / "bg.jpg"

# ---------- FUNKCJE POMOCNICZE ----------
def inject_css() -> None:
    css_parts: list[str] = []

    # tło
    if BACKGROUND_IMG.exists():
        mime = "image/png" if BACKGROUND_IMG.suffix.lower() == ".png" else "image/jpg"
        b64  = base64.b64encode(BACKGROUND_IMG.read_bytes()).decode()
        css_parts.append(textwrap.dedent(f"""
            body {{
                background: url("data:{mime};base64,{b64}") center/cover fixed;
            }}
            .stApp, body {{background-color: transparent !important;}}
        """))
    # ogólne style
    css_parts.append(textwrap.dedent("""
        .appview-container, .main {padding-top:40px;}
        .block-container {
            max-width:900px;
            background: rgba(0,0,0,0.60);
            padding: 40px 60px;
            border-radius: 16px;
            box-shadow: 0 0 25px rgba(0,0,0,0.8);
            margin-left: auto;
            margin-right: auto;
        }
        h1 {
            font-size:48px;
            margin-bottom:30px;
            text-align:center;
        }
        table {
            width:auto;
            margin:0 auto;
            font-size:18px;
        }
        th, td {text-align:center;}
        th {background:rgba(0,0,0,0.70); color:#fff;}
        td {background:rgba(0,0,0,0.55);}
        .stNumberInput, .stButton {
            display:flex; justify-content:center; margin-bottom:20px;
        }
        .stNumberInput>div>input {font-size:20px; height:42px;}
        .stButton>button {
            border-radius:12px; font-size:20px; padding:0.6em 2em;
            background:#e10600; color:white;
        }
        .stButton>button:hover {background:#ff3d2e;}
    """))

    st.markdown(f"<style>{''.join(css_parts)}</style>", unsafe_allow_html=True)

# ---------- IKONY MIESZANEK ----------
ICON_PATH = {k.upper(): IMG_DIR / f"{k}.png" for k in ("s", "m", "h")}
ICON_B64  = {k: "data:image/png;base64," + base64.b64encode(v.read_bytes()).decode()
             for k, v in ICON_PATH.items()}

# ---------- FLAGI ----------
FLAG_DIR = ROOT / "flags"
FLAGS_B64 = {f.stem.upper(): base64.b64encode(f.read_bytes()).decode()
             for f in FLAG_DIR.glob("*.png")}

def flag(code: str) -> str:
    return f'<img src="data:image/png;base64,{FLAGS_B64[code]}" width="32">'

# ---------- LOGA ZESPOŁÓW/AKADEMII ----------
LOGO_DIR = ROOT / "logos"
TEAM_ACADEMY_NAMES = {
    "MERCEDES": "mercedes", "RED BULL": "redbull", "FERRARI": "ferrari",
    "RACING POINT": "racingpoint", "MCLAREN": "mclaren", "ALFA ROMEO": "alfaromeo",
    "RENAULT": "renault", "HAAS": "haas", "ALPHA TAURI": "alphatauri",
    "WILLIAMS": "williams", "DAMS": "dams","VIRTUOSI": "virtuosi","ART GP": "artgp",
    "CARLIN": "carlin","CAMPOS": "campos","CHAROUZ": "charouz","HITECH": "hitech",
    "MP MOTORSPORT": "mpmotorsports","HWA RACELAB": "hwaracelab","TRIDENT": "trident",
    "PREMA": "prema","JENZER": "jenzer"
}
LOGOS_B64 = {name: ("data:image/png;base64," +
                    base64.b64encode((LOGO_DIR/f"{file}.png").read_bytes()).decode())
             if (LOGO_DIR/f"{file}.png").exists() else ""
             for name, file in TEAM_ACADEMY_NAMES.items()}

def logo_img(name: str) -> str:
    return f'<img src="{LOGOS_B64.get(name,"")}" width="32" style="vertical-align:middle;margin-left:4px;">' \
           if LOGOS_B64.get(name) else ""

# ---------- LOGIKA STRATEGII ----------
LIFE = {'S': 16, 'M': 24, 'H': 33}
def strategies(L: int, u: int = 2, o: int = 5, stints: int = 3):
    for k in range(1, stints + 1):
        for s in combinations_with_replacement(LIFE, k):
            total = sum(LIFE[c] for c in s)
            if L - u <= total <= L + o:
                yield s, total
#zespoły

# ---------- DANE ----------
def get_lineup(year: str, series: str) -> list[dict]:
    """Zwraca listę słowników z danymi kierowców (minimalny przykład)."""
    if year == "2020" and series == "Formula 1":
        return [
            {"KRAJ": flag("GB"), "NAZWISKO": "HAMILTON", "TEAM": "MERCEDES", "AKADEMIA": "-", "WIEK": 35, "RS": 8, "CO": 9, "OV": 9, "EX": 10, "QU": 9, "WE": 9, "CA": 9, "ST": 10, "OVR": 73, "KONTRAKT": 2020},
            {"KRAJ": flag("FI"), "NAZWISKO": "BOTTAS", "TEAM": "MERCEDES", "AKADEMIA": "-", "WIEK": 31, "RS": 9, "CO": 9, "OV": 8, "EX": 9, "QU": 8, "WE": 8, "CA": 9, "ST": 9, "OVR": 69, "KONTRAKT": 2021},
            {"KRAJ": flag("NL"), "NAZWISKO": "VERSTAPPEN", "TEAM": "RED BULL", "AKADEMIA": "RED BULL", "WIEK": 23, "RS": 9, "CO": 8, "OV": 9, "EX": 8, "QU": 9, "WE": 9, "CA": 9, "ST": 9, "OVR": 70, "KONTRAKT": 2020},
            {"KRAJ": flag("TH"), "NAZWISKO": "ALBON", "TEAM": "RED BULL", "AKADEMIA": "RED BULL", "WIEK": 24, "RS": 8, "CO": 8, "OV": 8, "EX": 7, "QU": 7, "WE": 8, "CA": 8, "ST": 8, "OVR": 62, "KONTRAKT": 2021},
            {"KRAJ": flag("MC"), "NAZWISKO": "LECLERC", "TEAM": "FERRARI", "AKADEMIA": "FERRARI", "WIEK": 23, "RS": 8, "CO": 9, "OV": 9, "EX": 7, "QU": 9, "WE": 8, "CA": 9, "ST": 9, "OVR": 68, "KONTRAKT": 2022},
            {"KRAJ": flag("DE"), "NAZWISKO": "VETTEL", "TEAM": "FERRARI", "AKADEMIA": "-", "WIEK": 33, "RS": 8, "CO": 8, "OV": 8, "EX": 10, "QU": 9, "WE": 9, "CA": 9, "ST": 9, "OVR": 70, "KONTRAKT": 2020},
            {"KRAJ": flag("MX"), "NAZWISKO": "PEREZ", "TEAM": "RACING POINT", "AKADEMIA": "-", "WIEK": 30, "RS": 8, "CO": 7, "OV": 7, "EX": 9, "QU": 7, "WE": 7, "CA": 8, "ST": 8, "OVR": 61, "KONTRAKT": 2020},
            {"KRAJ": flag("CA"), "NAZWISKO": "STROLL", "TEAM": "RACING POINT", "AKADEMIA": "-", "WIEK": 22, "RS": 9, "CO": 7, "OV": 8, "EX": 7, "QU": 7, "WE": 8, "CA": 7, "ST": 7, "OVR": 60, "KONTRAKT": 2023},
            {"KRAJ": flag("ES"), "NAZWISKO": "SAINZ", "TEAM": "MCLAREN", "AKADEMIA": "-", "WIEK": 28, "RS": 8, "CO": 7, "OV": 7, "EX": 8, "QU": 8, "WE": 8, "CA": 7, "ST": 8, "OVR": 61, "KONTRAKT": 2020},
            {"KRAJ": flag("GB"), "NAZWISKO": "NORRIS", "TEAM": "MCLAREN", "AKADEMIA": "MCLAREN", "WIEK": 21, "RS": 7, "CO": 8, "OV": 7, "EX": 7, "QU": 8, "WE": 7, "CA": 8, "ST": 8, "OVR": 60, "KONTRAKT": 2022},
            {"KRAJ": flag("FI"), "NAZWISKO": "RAIKKONEN", "TEAM": "ALFA ROMEO", "AKADEMIA": "-", "WIEK": 41, "RS": 6, "CO": 9, "OV": 7, "EX": 10, "QU": 8, "WE": 7, "CA": 9, "ST": 7, "OVR": 63, "KONTRAKT": "EMERYTURA"},
            {"KRAJ": flag("IT"), "NAZWISKO": "GIOVINAZZI", "TEAM": "ALFA ROMEO", "AKADEMIA": "FERRARI", "WIEK": 27, "RS": 7, "CO": 7, "OV": 7, "EX": 7, "QU": 8, "WE": 7, "CA": 8, "ST": 8, "OVR": 59, "KONTRAKT": 2021},
            {"KRAJ": flag("AU"), "NAZWISKO": "RICCIARDO", "TEAM": "RENAULT", "AKADEMIA": "-", "WIEK": 31, "RS": 8, "CO": 8, "OV": 9, "EX": 9, "QU": 8, "WE": 7, "CA": 8, "ST": 8, "OVR": 65, "KONTRAKT": 2020},
            {"KRAJ": flag("FR"), "NAZWISKO": "OCON", "TEAM": "RENAULT", "AKADEMIA": "-", "WIEK": 24, "RS": 7, "CO": 8, "OV": 7, "EX": 7, "QU": 8, "WE": 7, "CA": 8, "ST": 8, "OVR": 60, "KONTRAKT": 2020},
            {"KRAJ": flag("DK"), "NAZWISKO": "MAGNUSSEN", "TEAM": "HAAS", "AKADEMIA": "-", "WIEK": 28, "RS": 7, "CO": 7, "OV": 8, "EX": 8, "QU": 8, "WE": 7, "CA": 7, "ST": 7, "OVR": 59, "KONTRAKT": 2020},
            {"KRAJ": flag("FR"), "NAZWISKO": "GROSJEAN", "TEAM": "HAAS", "AKADEMIA": "-", "WIEK": 34, "RS": 7, "CO": 6, "OV": 7, "EX": 10, "QU": 8, "WE": 7, "CA": 8, "ST": 7, "OVR": 60, "KONTRAKT": 2020},
            {"KRAJ": flag("FR"), "NAZWISKO": "GASLY", "TEAM": "ALPHA TAURI", "AKADEMIA": "RED BULL", "WIEK": 24, "RS": 7, "CO": 8, "OV": 7, "EX": 7, "QU": 8,"WE": 7, "CA": 8, "ST": 8, "OVR": 60, "KONTRAKT": 2021},
            {"KRAJ": flag("RU"), "NAZWISKO": "KVYAT", "TEAM": "ALPHA TAURI", "AKADEMIA": "RED BULL", "WIEK": 26, "RS": 7, "CO": 7, "OV": 8, "EX": 8, "QU": 7, "WE": 7, "CA": 8, "ST": 8, "OVR": 60, "KONTRAKT": 2020},
            {"KRAJ": flag("GB"), "NAZWISKO": "RUSSELL", "TEAM": "WILLIAMS", "AKADEMIA": "MERCEDES", "WIEK": 22, "RS": 7, "CO": 8, "OV": 8, "EX": 7, "QU": 8, "WE": 7, "CA": 8, "ST": 8, "OVR": 61, "KONTRAKT": 2020},
            {"KRAJ": flag("CA"), "NAZWISKO": "LATIFI", "TEAM": "WILLIAMS", "AKADEMIA": "-", "WIEK": 24, "RS": 7, "CO": 7, "OV": 7, "EX": 6, "QU": 7, "WE": 6, "CA": 7, "ST": 7, "OVR": 54, "KONTRAKT": 2020},
        ]
    if year == "2020" and series == "Formula 2":
        return[
            {"KRAJ": flag("GB"), "NAZWISKO": "TICKTUM", "TEAM": "DAMS", "AKADEMIA": "MERCEDES", "WIEK": 21, "RS": 7, "CO": 5, "OV": 6, "EX": 6, "QU": 6, "WE": 6, "CA": 7, "ST": 6, "OVR": 49},
            {"KRAJ": flag("EE"), "NAZWISKO": "VIPS", "TEAM": "DAMS", "AKADEMIA": "RED BULL", "WIEK": 20, "RS": 6, "CO": 6, "OV": 7, "EX": 6, "QU": 6, "WE": 5, "CA": 6, "ST": 6, "OVR": 48},
            {"KRAJ": flag("GB"), "NAZWISKO": "ILOTT", "TEAM": "VIRTUOSI", "AKADEMIA": "FERRARI", "WIEK": 22, "RS": 6, "CO": 7, "OV": 6, "EX": 6, "QU": 7, "WE": 7, "CA": 6, "ST": 7, "OVR": 52},
            {"KRAJ": flag("CN"), "NAZWISKO": "ZHOU", "TEAM": "VIRTUOSI", "AKADEMIA": "RENAULT", "WIEK": 21, "RS": 6, "CO": 6, "OV": 5, "EX": 6, "QU": 7, "WE": 6, "CA": 7, "ST": 6, "OVR": 49},
            {"KRAJ": flag("NZ"), "NAZWISKO": "ARMSTRONG", "TEAM": "ART GP", "AKADEMIA": "FERRARI", "WIEK": 20, "RS": 6, "CO": 7, "OV": 6, "EX": 6, "QU": 6, "WE": 6, "CA": 7, "ST": 6, "OVR": 50},
            {"KRAJ": flag("DK"), "NAZWISKO": "LUNDGAARD", "TEAM": "ART GP", "AKADEMIA": "RENAULT", "WIEK": 19, "RS": 7, "CO": 6, "OV": 6, "EX": 6, "QU": 6, "WE": 6, "CA": 7, "ST": 6, "OVR": 50},
            {"KRAJ": flag("IN"), "NAZWISKO": "DARUVALA", "TEAM": "CARLIN", "AKADEMIA": "RED BULL", "WIEK": 22, "RS": 6, "CO": 7, "OV": 6, "EX": 6, "QU": 6, "WE": 6, "CA": 7, "ST": 6, "OVR": 50},
            {"KRAJ": flag("JP"), "NAZWISKO": "TSUNODA", "TEAM": "CARLIN", "AKADEMIA": "RED BULL", "WIEK": 20, "RS": 6, "CO": 5, "OV": 6, "EX": 5, "QU": 6, "WE": 5, "CA": 6, "ST": 7, "OVR": 46},
            {"KRAJ": flag("GB"), "NAZWISKO": "AITKEN", "TEAM": "CAMPOS", "AKADEMIA": "-", "WIEK": 25, "RS": 6, "CO": 6, "OV": 7, "EX": 6, "QU": 7, "WE": 6, "CA": 7, "ST": 7, "OVR": 52},
            {"KRAJ": flag("BR"), "NAZWISKO": "SAMAIA", "TEAM": "CAMPOS", "AKADEMIA": "-", "WIEK": 24, "RS": 5, "CO": 6, "OV": 7, "EX": 7, "QU": 6, "WE": 7, "CA": 8, "ST": 7, "OVR": 53},
            {"KRAJ": flag("CH"), "NAZWISKO": "DELETRAZ", "TEAM": "CHAROUZ", "AKADEMIA": "-", "WIEK": 23, "RS": 7, "CO": 7, "OV": 6, "EX": 6, "QU": 6, "WE": 6, "CA": 7, "ST": 6, "OVR": 51},
            {"KRAJ": flag("BR"), "NAZWISKO": "PIQUET", "TEAM": "CHAROUZ", "AKADEMIA": "-", "WIEK": 22, "RS": 6, "CO": 6, "OV": 7, "EX": 6, "QU": 6, "WE": 7, "CA": 6, "ST": 6, "OVR": 50},
            {"KRAJ": flag("JP"), "NAZWISKO": "MATSUSHITA", "TEAM": "MP MOTORSPORT", "AKADEMIA": "-", "WIEK": 27, "RS": 7, "CO": 7, "OV": 6, "EX": 6, "QU": 6, "WE": 6, "CA": 7, "ST": 6, "OVR": 51},
            {"KRAJ": flag("BR"), "NAZWISKO": "DRUGOVICH", "TEAM": "MP MOTORSPORT", "AKADEMIA": "-", "WIEK": 20, "RS": 5, "CO": 6, "OV": 4, "EX": 6, "QU": 8, "WE": 4, "CA": 4, "ST": 7, "OVR": 44},
            {"KRAJ": flag("RU"), "NAZWISKO": "MARKIELOV", "TEAM": "HWA RACELAB", "AKADEMIA": "-", "WIEK": 26, "RS": 7, "CO": 7, "OV": 6, "EX": 7, "QU": 6, "WE": 6, "CA": 7, "ST": 6, "OVR": 52},
            {"KRAJ": flag("FR"), "NAZWISKO": "ALESI", "TEAM": "HWA RACELAB", "AKADEMIA": "-", "WIEK": 21, "RS": 6, "CO": 7, "OV": 6, "EX": 6, "QU": 6, "WE": 6, "CA": 7, "ST": 6, "OVR": 50},
            {"KRAJ": flag("RU"), "NAZWISKO": "SHWARTZMAN", "TEAM": "PREMA", "AKADEMIA": "FERRARI", "WIEK": 21, "RS": 5, "CO": 6, "OV": 7, "EX": 6, "QU": 7, "WE": 6, "CA": 6, "ST": 6, "OVR": 49},
            {"KRAJ": flag("DE"), "NAZWISKO": "SCHUMACHER", "TEAM": "PREMA", "AKADEMIA": "FERRARI", "WIEK": 21, "RS": 6, "CO": 5, "OV": 6, "EX": 6, "QU": 5, "WE": 6, "CA": 7, "ST": 6, "OVR": 47},
            {"KRAJ": flag("IL"), "NAZWISKO": "NISSANY", "TEAM": "TRIDENT", "AKADEMIA": "WILLIAMS", "WIEK": 26, "RS": 4, "CO": 7, "OV": 5, "EX": 4, "QU": 4, "WE": 6, "CA": 7, "ST": 7, "OVR": 44},
            {"KRAJ": flag("JP"), "NAZWISKO": "SATO", "TEAM": "TRIDENT", "AKADEMIA": "-", "WIEK": 21, "RS": 5, "CO": 8, "OV": 7, "EX": 8, "QU": 6, "WE": 6, "CA": 5, "ST": 6, "OVR": 51},
            {"KRAJ": flag("RU"), "NAZWISKO": "MAZEPIN", "TEAM": "HITECH", "AKADEMIA": "-", "WIEK": 21, "RS": 6, "CO": 5, "OV": 6, "EX": 6, "QU": 6, "WE": 6, "CA": 6, "ST": 5, "OVR": 46},
            {"KRAJ": flag("IT"), "NAZWISKO": "GHIOTTO", "TEAM": "HITECH", "AKADEMIA": "-", "WIEK": 25, "RS": 7, "CO": 4, "OV": 6, "EX": 6, "QU": 6, "WE": 8, "CA": 6, "ST": 7, "OVR": 50}
        ]
    if year == "2020" and series == "Formula 3":
        return[
            {"KRAJ": flag("DK"), "NAZWISKO": "VESTI", "TEAM": "PREMA", "AKADEMIA": "-", "WIEK": 18, "RS": 5, "CO": 4, "OV": 7, "EX": 6, "QU": 5, "WE": 5, "CA": 6, "ST": 6, "OVR": 44},
            {"KRAJ": flag("AU"), "NAZWISKO": "PIASTRI", "TEAM": "PREMA", "AKADEMIA": "RENAULT", "WIEK": 19, "RS": 7, "CO": 5, "OV": 6, "EX": 4, "QU": 4, "WE": 4, "CA": 7, "ST": 4, "OVR": 41},
            {"KRAJ": flag("NZ"), "NAZWISKO": "LAWSON", "TEAM": "HITECH", "AKADEMIA": "RED BULL", "WIEK": 18, "RS": 6, "CO": 7, "OV": 6, "EX": 5, "QU": 6, "WE": 6, "CA": 6, "ST": 7, "OVR": 49},
            {"KRAJ": flag("NO"), "NAZWISKO": "HAUGER", "TEAM": "HITECH", "AKADEMIA": "RED BULL", "WIEK": 17, "RS": 6, "CO": 5, "OV": 5, "EX": 5, "QU": 6, "WE": 5, "CA": 5, "ST": 5, "OVR": 42},
            {"KRAJ": flag("FR"), "NAZWISKO": "POURCHAIRE", "TEAM": "ART GP", "AKADEMIA": "SAUBER", "WIEK": 17, "RS": 4, "CO": 6, "OV": 5, "EX": 7, "QU": 7, "WE": 5, "CA": 4, "ST": 6, "OVR": 44},
            {"KRAJ": flag("RU"), "NAZWISKO": "SMOLYAR", "TEAM": "ART GP", "AKADEMIA": "-", "WIEK": 19, "RS": 4, "CO": 4, "OV": 7, "EX": 5, "QU": 7, "WE": 6, "CA": 4, "ST": 7, "OVR": 44},
            {"KRAJ": flag("DE"), "NAZWISKO": "BECKMANN", "TEAM": "TRIDENT", "AKADEMIA": "-", "WIEK": 20, "RS": 7, "CO": 4, "OV": 4, "EX": 7, "QU": 4, "WE": 7, "CA": 5, "ST": 4, "OVR": 42},
            {"KRAJ": flag("DE"), "NAZWISKO": "ZENDELI", "TEAM": "TRIDENT", "AKADEMIA": "-", "WIEK": 21, "RS": 6, "CO": 6, "OV": 4, "EX": 4, "QU": 5, "WE": 4, "CA": 6, "ST": 6, "OVR": 41},
            {"KRAJ": flag("GB"), "NAZWISKO": "HUGHES", "TEAM": "HWA RACELAB", "AKADEMIA": "-", "WIEK": 26, "RS": 6, "CO": 6, "OV": 6, "EX": 7, "QU": 6, "WE": 7, "CA": 6, "ST": 6, "OVR": 50},
            {"KRAJ": flag("AU"), "NAZWISKO": "DOOHAN", "TEAM": "HWA RACELAB", "AKADEMIA": "RENAULT", "WIEK": 17, "RS": 5, "CO": 4, "OV": 7, "EX": 7, "QU": 4, "WE": 6, "CA": 7, "ST": 5, "OVR": 45},
            {"KRAJ": flag("NL"), "NAZWISKO": "VERSCHOOR", "TEAM": "MP MOTORSPORT", "AKADEMIA": "RED BULL", "WIEK": 20, "RS": 7, "CO": 6, "OV": 6, "EX": 6, "QU": 6, "WE": 7, "CA": 6, "ST": 6, "OVR": 50},
            {"KRAJ": flag("NL"), "NAZWISKO": "VISCAAL", "TEAM": "MP MOTORSPORT", "AKADEMIA": "-", "WIEK": 21, "RS": 7, "CO": 6, "OV": 7, "EX": 7, "QU": 4, "WE": 4, "CA": 5, "ST": 4, "OVR": 44},
            {"KRAJ": flag("IT"), "NAZWISKO": "NANNINI", "TEAM": "JENZER", "AKADEMIA": "-", "WIEK": 17, "RS": 6, "CO": 4, "OV": 4, "EX": 4, "QU": 6, "WE": 4, "CA": 6, "ST": 4, "OVR": 38},
            {"KRAJ": flag("AU"), "NAZWISKO": "WILLIAMS", "TEAM": "JENZER", "AKADEMIA": "-", "WIEK": 20, "RS": 5, "CO": 4, "OV": 4, "EX": 5, "QU": 6, "WE": 5, "CA": 4, "ST": 5, "OVR": 38},
            {"KRAJ": flag("DE"), "NAZWISKO": "SCHUMACHER", "TEAM": "CHAROUZ", "AKADEMIA": "SAUBER", "WIEK": 19, "RS": 6, "CO": 4, "OV": 7, "EX": 4, "QU": 6, "WE": 7, "CA": 6, "ST": 4, "OVR": 44},
            {"KRAJ": flag("CZ"), "NAZWISKO": "STANEK", "TEAM": "CHAROUZ", "AKADEMIA": "SAUBER", "WIEK": 16, "RS": 4, "CO": 5, "OV": 6, "EX": 6, "QU": 6, "WE": 4, "CA": 6, "ST": 4, "OVR": 41},
            {"KRAJ": flag("FR"), "NAZWISKO": "NOVALAK", "TEAM": "CARLIN", "AKADEMIA": "-", "WIEK": 20, "RS": 7, "CO": 4, "OV": 5, "EX": 4, "QU": 5, "WE": 5, "CA": 6, "ST": 6, "OVR": 42},
            {"KRAJ": flag("US"), "NAZWISKO": "DAS", "TEAM": "CARLIN", "AKADEMIA": "-", "WIEK": 20, "RS": 6, "CO": 4, "OV": 4, "EX": 4, "QU": 4, "WE": 7, "CA": 5, "ST": 4, "OVR": 38},
            {"KRAJ": flag("DE"), "NAZWISKO": "FLORSCH", "TEAM": "CAMPOS", "AKADEMIA": "-", "WIEK": 20, "RS": 6, "CO": 4, "OV": 5, "EX": 5, "QU": 7, "WE": 6, "CA": 7, "ST": 5, "OVR": 45},
            {"KRAJ": flag("AU"), "NAZWISKO": "PERONI", "TEAM": "CAMPOS", "AKADEMIA": "-", "WIEK": 21, "RS": 5, "CO": 4, "OV": 5, "EX": 4, "QU": 5, "WE": 4, "CA": 5, "ST": 4, "OVR": 36},
            {"KRAJ": flag("GB"), "NAZWISKO": "FEWTRELL", "TEAM": "DAMS", "AKADEMIA": "RENAULT", "WIEK": 21, "RS": 7, "CO": 5, "OV": 4, "EX": 7, "QU": 7, "WE": 5, "CA": 6, "ST": 7, "OVR": 48},
            {"KRAJ": flag("US"), "NAZWISKO": "SARGEANT", "TEAM": "DAMS", "AKADEMIA": "-", "WIEK": 20, "RS": 5, "CO": 5, "OV": 5, "EX": 4, "QU": 4, "WE": 5, "CA": 6, "ST": 7, "OVR": 41},
        ]
    return []

def get_teams(year: str, series: str) -> list[dict]:
    """Zwraca listę słowników z danymi kierowców (minimalny przykład)."""
    if year == "2020" and series == "Formula 1":
        return [
            {"KRAJ": flag("DE"), "TEAM": "MERCEDES", "SILNIK": "MERCEDES", "OVR": 560, "O+S": 649},
            {"KRAJ": flag("AT"), "TEAM": "RED BULL", "SILNIK": "HONDA", "OVR": 555, "O+S": 642},
            {"KRAJ": flag("IT"), "TEAM": "FERRARI", "SILNIK": "FERRARI", "OVR": 546, "O+S": 640},
            {"KRAJ": flag("GB"), "TEAM": "RACING POINT", "SILNIK": "MERCEDES", "OVR": 499, "O+S": 588},
            {"KRAJ": flag("GB"), "TEAM": "MCLAREN", "SILNIK": "RENAULT", "OVR": 490, "O+S": 575},
            {"KRAJ": flag("CH"), "TEAM": "ALFA ROMEO", "SILNIK": "FERRARI", "OVR": 445, "O+S": 539},
            {"KRAJ": flag("FR"), "TEAM": "RENAULT", "SILNIK": "RENAULT",  "OVR": 453, "O+S": 538},
            {"KRAJ": flag("US"), "TEAM": "HAAS", "SILNIK": "FERRARI", "OVR": 439, "O+S": 533},
            {"KRAJ": flag("IT"), "TEAM": "ALPHA TAURI", "SILNIK": "HONDA", "OVR": 425, "O+S": 512},
            {"KRAJ": flag("GB"), "TEAM": "WILLIAMS", "SILNIK": "MERCEDES", "OVR": 416, "O+S": 505}
        ]
    if year == "2020" and series == "Formula 2":
        return[
            {"KRAJ": flag("FR"), "TEAM": "DAMS"},
            {"KRAJ": flag("GB"), "TEAM": "VIRTUOSI"},
            {"KRAJ": flag("FR"), "TEAM": "ART GP"},
            {"KRAJ": flag("GB"), "TEAM": "CARLIN"},
            {"KRAJ": flag("ES"), "TEAM": "CAMPOS"},
            {"KRAJ": flag("CZ"), "TEAM": "CHAROUZ"},
            {"KRAJ": flag("NL"), "TEAM": "MP MOTORSPORT"},
            {"KRAJ": flag("DE"), "TEAM": "HWA RACELAB"},
            {"KRAJ": flag("IT"), "TEAM": "PREMA"},
            {"KRAJ": flag("IT"), "TEAM": "TRIDENT"},
            {"KRAJ": flag("GB"), "TEAM": "HITECH"},
        ]
    if year == "2020" and series == "Formula 3":
        return[
            {"KRAJ": flag("FR"), "TEAM": "DAMS"},
            {"KRAJ": flag("CH"), "TEAM": "JENZER"},
            {"KRAJ": flag("FR"), "TEAM": "ART GP"},
            {"KRAJ": flag("GB"), "TEAM": "CARLIN"},
            {"KRAJ": flag("ES"), "TEAM": "CAMPOS"},
            {"KRAJ": flag("CZ"), "TEAM": "CHAROUZ"},
            {"KRAJ": flag("NL"), "TEAM": "MP MOTORSPORT"},
            {"KRAJ": flag("DE"), "TEAM": "HWA RACELAB"},
            {"KRAJ": flag("IT"), "TEAM": "PREMA"},
            {"KRAJ": flag("IT"), "TEAM": "TRIDENT"},
            {"KRAJ": flag("GB"), "TEAM": "HITECH"},
        ]
    return []

def get_dc (year: str, series: str) -> list[dict]:
    """Zwraca listę słowników z danymi kierowców (minimalny przykład)."""
    if year == "2020" and series == "Formula 1":
        return [
            {"KRAJ": flag("GB"), "NAZWISKO": "HAMILTON", "PKT": 385, "P1": 8, "P2": 6, "P3": 3},
            {"KRAJ": flag("DE"), "NAZWISKO": "VETTEL", "PKT": 331, "P1": 5, "P2": 6, "P3": 4},
            {"KRAJ": flag("MC"), "NAZWISKO": "LECLERC", "PKT": 291, "P1": 4, "P2": 3, "P3": 1},
            {"KRAJ": flag("FI"), "NAZWISKO": "BOTTAS", "PKT": 274, "P1": 4, "P2": 2, "P3": 2},
            {"KRAJ": flag("NL"), "NAZWISKO": "VERSTAPPEN", "PKT": 251, "P1": 0, "P2": 2, "P3": 9},
            {"KRAJ": flag("TH"), "NAZWISKO": "ALBON", "PKT": 190, "P1": 0, "P2": 1, "P3": 2},
            {"KRAJ": flag("GB"), "NAZWISKO": "NORRIS", "PKT": 104, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("FR"), "NAZWISKO": "OCON", "PKT": 55, "P1": 0, "P2": 1, "P3": 0},
            {"KRAJ": flag("ES"), "NAZWISKO": "SAINZ", "PKT": 46, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("AU"), "NAZWISKO": "RICCIARDO", "PKT": 41, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("IT"), "NAZWISKO": "GIOVINAZZI", "PKT": 34, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("FR"), "NAZWISKO": "GASLY", "PKT": 34, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("FI"), "NAZWISKO": "RAIKONEN", "PKT": 29, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("MX"), "NAZWISKO": "PEREZ", "PKT": 15, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("CA"), "NAZWISKO": "STROLL", "PKT": 12, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("RU"), "NAZWISKO": "KVYAT", "PKT": 10, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("GB"), "NAZWISKO": "RUSSELL", "PKT": 10, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("FR"), "NAZWISKO": "GROSJEAN", "PKT": 6, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("DK"), "NAZWISKO": "MAGNUSSEN", "PKT": 2, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("CA"), "NAZWISKO": "LATIFI", "PKT": 1, "P1": 0, "P2": 0, "P3": 0}
        ]
    if year == "2020" and series == "Formula 2":
        return [
            {"KRAJ": flag("GB"), "NAZWISKO": "AITKEN", "PKT": 173, "P1": 4, "P2": 3, "P3": 0},
            {"KRAJ": flag("RU"), "NAZWISKO": "MARKIELOV", "PKT": 158, "P1": 4, "P2": 2, "P3": 0},
            {"KRAJ": flag("IN"), "NAZWISKO": "DARUVALA", "PKT": 119, "P1": 1, "P2": 2, "P3": 0},
            {"KRAJ": flag("IT"), "NAZWISKO": "GHIOTTO", "PKT": 95, "P1": 2, "P2": 1, "P3": 1},
            {"KRAJ": flag("NZ"), "NAZWISKO": "ARMSTRONG", "PKT": 80, "P1": 0, "P2": 0, "P3": 2},
            {"KRAJ": flag("RU"), "NAZWISKO": "SHWARTZMAN", "PKT": 68, "P1": 1, "P2": 0, "P3": 1},
            {"KRAJ": flag("CN"), "NAZWISKO": "ZHOU", "PKT": 66, "P1": 0, "P2": 1, "P3": 1},
            {"KRAJ": flag("JP"), "NAZWISKO": "SAMIA", "PKT": 59, "P1": 0, "P2": 0, "P3": 1},
            {"KRAJ": flag("GB"), "NAZWISKO": "ILOTT", "PKT": 58, "P1": 0, "P2": 1, "P3": 0},
            {"KRAJ": flag("JP"), "NAZWISKO": "MATSUSHITA", "PKT": 53, "P1": 0, "P2": 1, "P3": 1},
            {"KRAJ": flag("JP"), "NAZWISKO": "SATO", "PKT": 51, "P1": 0, "P2": 1, "P3": 1},
            {"KRAJ": flag("CH"), "NAZWISKO": "DELETRAZ", "PKT": 46, "P1": 0, "P2": 0, "P3": 3},
            {"KRAJ": flag("BR"), "NAZWISKO": "PIQUET", "PKT": 42, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("RU"), "NAZWISKO": "MAZEPIN", "PKT": 30, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("GB"), "NAZWISKO": "TICKTUM", "PKT": 29, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("DK"), "NAZWISKO": "LUNDGAARD", "PKT": 25, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("BR"), "NAZWISKO": "DRUGOVICH", "PKT": 20, "P1": 0, "P2": 0, "P3": 1},
            {"KRAJ": flag("DE"), "NAZWISKO": "SCHUMACHER", "PKT": 16, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("EE"), "NAZWISKO": "VIPS", "PKT": 15, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("FR"), "NAZWISKO": "ALESI", "PKT": 6, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("JP"), "NAZWISKO": "TSUNODA", "PKT": 3, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("IL"), "NAZWISKO": "NISSANY", "PKT": 0, "P1": 0, "P2": 0, "P3": 0}
        ]
    if year == "2020" and series == "Formula 3":
        return [
            {"KRAJ": flag("GB"), "NAZWISKO": "FEWTRELL", "PKT": 223, "P1": 7, "P2": 1, "P3": 2},
            {"KRAJ": flag("FR"), "NAZWISKO": "POURCHAIRE", "PKT": 116, "P1": 2, "P2": 0, "P3": 2},
            {"KRAJ": flag("NZ"), "NAZWISKO": "LAWSON", "PKT": 110, "P1": 1, "P2": 2, "P3": 2},
            {"KRAJ": flag("DE"), "NAZWISKO": "FLORSCH", "PKT": 108, "P1": 1, "P2": 2, "P3": 2},
            {"KRAJ": flag("GB"), "NAZWISKO": "HUGHES", "PKT": 106, "P1": 0, "P2": 4, "P3": 0},
            {"KRAJ": flag("NL"), "NAZWISKO": "VERSCHOOR", "PKT": 76, "P1": 0, "P2": 0, "P3": 2},
            {"KRAJ": flag("CZ"), "NAZWISKO": "STANEK", "PKT": 68, "P1": 0, "P2": 0, "P3": 1},
            {"KRAJ": flag("DK"), "NAZWISKO": "VESTI", "PKT": 67, "P1": 0, "P2": 0, "P3": 1},
            {"KRAJ": flag("FR"), "NAZWISKO": "NOVALAK", "PKT": 58, "P1": 1, "P2": 1, "P3": 0},
            {"KRAJ": flag("DE"), "NAZWISKO": "ZENDELI", "PKT": 50, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("RU"), "NAZWISKO": "SMOLYAR", "PKT": 43, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("DE"), "NAZWISKO": "BECKMANN", "PKT": 40, "P1": 0, "P2": 1, "P3": 0},
            {"KRAJ": flag("DE"), "NAZWISKO": "SCHUMACHER", "PKT": 32, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("NL"), "NAZWISKO": "VISCAAL", "PKT": 22, "P1": 0, "P2": 1, "P3": 0},
            {"KRAJ": flag("AU"), "NAZWISKO": "PERONI", "PKT": 17, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("US"), "NAZWISKO": "SARGEANT", "PKT": 16, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("NO"), "NAZWISKO": "HAUGER", "PKT": 13, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("AU"), "NAZWISKO": "PIASTRI", "PKT": 12, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("IT"), "NAZWISKO": "NANNINI", "PKT": 12, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("US"), "NAZWISKO": "DAS", "PKT": 12, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("AU"), "NAZWISKO": "DOOHAN", "PKT": 7, "P1": 0, "P2": 0, "P3": 0},
            {"KRAJ": flag("AU"), "NAZWISKO": "WILLIAMS", "PKT": 4, "P1": 0, "P2": 0, "P3": 0},
        ]
    return []

def get_cc (year: str, series: str) -> list[dict]:
    """Zwraca listę słowników z danymi kierowców (minimalny przykład)."""
    if year == "2020" and series == "Formula 1":
        return [
            {"KRAJ": flag("DE"), "TEAM": "MERCEDES", "PKT": 659, "MWM": 0},
            {"KRAJ": flag("IT"), "TEAM": "FERRARI", "PKT": 622, "MWM": 1},
            {"KRAJ": flag("AT"), "TEAM": "RED BULL", "PKT": 441, "MWM": -1},
            {"KRAJ": flag("GB"), "TEAM": "MCLAREN", "PKT": 150, "MWM": 1},
            {"KRAJ": flag("FR"), "TEAM": "RENAULT", "PKT": 96, "MWM": 2},
            {"KRAJ": flag("CH"), "TEAM": "ALFA ROMEO", "PKT": 63, "MWM": 0},
            {"KRAJ": flag("IT"), "TEAM": "ALPHA TAURI", "PKT": 44, "MWM": 2},
            {"KRAJ": flag("GB"), "TEAM": "RACING POINT", "PKT": 27, "MWM": -4},
            {"KRAJ": flag("GB"), "TEAM": "WILLIAMS", "PKT": 11, "MWM": 1},
            {"KRAJ": flag("US"), "TEAM": "HAAS", "PKT": 8, "MWM": -2}
        ]
    if year == "2020" and series == "Formula 2":
        return [
            {"KRAJ": flag("ES"), "TEAM": "CAMPOS", "PKT": 232},
            {"KRAJ": flag("DE"), "TEAM": "HWA RACELAB", "PKT": 164},
            {"KRAJ": flag("GB"), "TEAM": "HITECH", "PKT": 125},
            {"KRAJ": flag("GB"), "TEAM": "VIRTUOSI", "PKT": 124},
            {"KRAJ": flag("GB"), "TEAM": "CARLIN", "PKT": 122},
            {"KRAJ": flag("FR"), "TEAM": "ART GP", "PKT": 105},
            {"KRAJ": flag("CZ"), "TEAM": "CHAROUZ", "PKT": 88},
            {"KRAJ": flag("IT"), "TEAM": "PREMA", "PKT": 84},
            {"KRAJ": flag("NL"), "TEAM": "MP MOTORSPORT", "PKT": 73},
            {"KRAJ": flag("IT"), "TEAM": "TRIDENT", "PKT": 51},
            {"KRAJ": flag("FR"), "TEAM": "DAMS", "PKT": 44}
        ]
    if year == "2020" and series == "Formula 3":
        return [
            {"KRAJ": flag("FR"), "TEAM": "DAMS", "PKT": 239},
            {"KRAJ": flag("FR"), "TEAM": "ART GP", "PKT": 159},
            {"KRAJ": flag("ES"), "TEAM": "CAMPOS", "PKT": 125},
            {"KRAJ": flag("GB"), "TEAM": "HITECH", "PKT": 123},
            {"KRAJ": flag("DE"), "TEAM": "HWA RACELAB", "PKT": 113},
            {"KRAJ": flag("CZ"), "TEAM": "CHAROUZ", "PKT": 100},
            {"KRAJ": flag("NL"), "TEAM": "MP MOTORSPORT", "PKT": 98},
            {"KRAJ": flag("IT"), "TEAM": "TRIDENT", "PKT": 90},
            {"KRAJ": flag("IT"), "TEAM": "PREMA", "PKT": 79},
            {"KRAJ": flag("GB"), "TEAM": "CARLIN", "PKT": 70},
            {"KRAJ": flag("CH"), "TEAM": "JENZER", "PKT": 16},
        ]
    return []


# ------------------------------------------------------- WYSWIETLANIE POD‑KATEGORII --------------------------------------------------------------------

def show_lineup(year: str, series: str):
    data = get_lineup(year, series)
    if not data:
        st.info("Brak danych.")
        return

    for d in data:
        d["LOGO_TEAM"] = logo_img(d["TEAM"])
        d["LOGO_AKADEMIA"] = logo_img(d["AKADEMIA"]) if d["AKADEMIA"] != "-" else ""

    df = pd.DataFrame(data)
    df.insert(0, 'NR', range(1, len(df) + 1))

    df.rename(columns={"LOGO_TEAM": "zespół", "LOGO_AKADEMIA": "akademia"}, inplace=True)

    cols = df.columns.tolist()

    for col_to_remove in ["TEAM", "AKADEMIA", "RS", "CO", "OV", "EX", "QU", "WE", "CA", "ST"]:
        if col_to_remove in cols:
            cols.remove(col_to_remove)

    if "zespół" in cols:
        cols.remove("zespół")
    if "akademia" in cols:
        cols.remove("akademia")

    idx_nazwisko = cols.index("NAZWISKO")

    cols.insert(idx_nazwisko + 1, "zespół")
    cols.insert(idx_nazwisko + 2, "akademia")

    table_style = "background-color: rgba(200, 200, 200, 0.8);"
    html_table = df[cols].to_html(index=False, escape=False)
    html_table = html_table.replace('<table ', f'<table style="{table_style}" ')

    html_table = html_table.replace('<img ', '<img width="45" ')

    st.markdown(html_table, unsafe_allow_html=True)

def show_teams(year: str, series: str):
    data = get_teams(year, series)
    if not data:
        st.info("Brak danych.")
        return

    for d in data:
        d["TEAM"] = logo_img(d["TEAM"])

    df = pd.DataFrame(data)
    df.insert(0, 'NR', range(1, len(df) + 1))
    
    cols = df.columns.tolist()

    table_style = "background-color: rgba(200, 200, 200, 0.8);"
    html_table = df[cols].to_html(index=False, escape=False)
    html_table = html_table.replace('<table ', f'<table style="{table_style}" ')

    html_table = html_table.replace('<img ', '<img width="45" ')

    st.markdown(html_table, unsafe_allow_html=True)

def show_drivers_standings(year: str, series: str):
    data = get_dc(year, series)
    if not data:
        st.info("Brak danych.")
        return

    df = pd.DataFrame(data)
    df.insert(0, 'P', range(1, len(df) + 1))
    
    cols = df.columns.tolist()

    table_style = "background-color: rgba(200, 200, 200, 0.8);"
    html_table = df[cols].to_html(index=False, escape=False)
    html_table = html_table.replace('<table ', f'<table style="{table_style}" ')

    html_table = html_table.replace('<img ', '<img width="45" ')

    st.markdown(html_table, unsafe_allow_html=True)

def show_constructors_standings(year: str, series: str):
    data = get_cc(year, series)
    if not data:
        st.info("Brak danych.")
        return
    for d in data:
        d["TEAM"] = logo_img(d["TEAM"])

    df = pd.DataFrame(data)
    df.insert(0, 'P', range(1, len(df) + 1))
    
    cols = df.columns.tolist()

    table_style = "background-color: rgba(200, 200, 200, 0.8);"
    html_table = df[cols].to_html(index=False, escape=False)
    html_table = html_table.replace('<table ', f'<table style="{table_style}" ')

    html_table = html_table.replace('<img ', '<img width="45" ')

    st.markdown(html_table, unsafe_allow_html=True)

def show_legacy():               st.info("Legacy – w przygotowaniu")

# ---------- KONFIG STRONY ----------
st.set_page_config(page_title="Strategie opon", page_icon="🏎️", layout="centered")
inject_css()

# ---------- ZAKŁADKI GŁÓWNE ----------
tabs_main = st.tabs(["Kalkulator", "Fantasy", "Legacy"])

# ==================== KALKULATOR ====================
with tabs_main[0]:
    st.markdown("## 🏁 Strategie opon F1")
    laps = st.number_input("Okrążenia w wyścigu", min_value=1, step=1)
    if st.button("Pokaż strategie"):
        rows = []
        for stint, total in strategies(int(laps)):
            icons_html = " + ".join(f'<img src="{ICON_B64[c]}" width="36">' for c in stint)
            rows.append({"Strategia": icons_html, "Dystans": total, "Pit‑stopy": len(stint)-1})
        if rows:
            st.markdown(pd.DataFrame(rows).to_html(escape=False, index=False),
                        unsafe_allow_html=True)
        else:
            st.error("Brak strategii w podanym zakresie.")

# ==================== FANTASY ====================
with tabs_main[1]:
    st.markdown("## 🏆 Fantasy")

    col1, col2 = st.columns(2)
    with col1:
        year   = st.radio("Rok",    ["2020", "2021"], horizontal=True)
    with col2:
        series = st.radio("Seria",  ["Formula 1", "Formula 2", "Formula 3"], horizontal=True)

    sub_tabs = st.tabs(["Line‑up", "Zespoły", "Klasyfikacja kierowców",
                        "Klasyfikacja konstruktorów"])

    with sub_tabs[0]: show_lineup(year, series)
    with sub_tabs[1]: show_teams(year, series)
    with sub_tabs[2]: show_drivers_standings(year, series)
    with sub_tabs[3]: show_constructors_standings(year, series)

# ==================== LEGACY ====================
with tabs_main[2]:
    show_legacy()
