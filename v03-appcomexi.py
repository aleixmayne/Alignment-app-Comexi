import os
import base64
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import math

st.set_page_config(
    page_title="Comexi · Alignment System",
    page_icon="⬛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Outfit:wght@200;300;400;500;600;700;800;900&display=swap');

:root {
    --red:     #E3001B;
    --red-dim: rgba(227,0,27,0.12);
    --bg:      #F5F5F7;
    --bg2:     #FFFFFF;
    --bg3:     #EBEBED;
    --border:  #D8D8DC;
    --border2: #C4C4C8;
    --text:    #1A1A1E;
    --muted:   #6E6E78;
    --muted2:  #3A3A44;
    --green:   #00A862;
    --blue:    #0071E3;
}
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background: var(--bg) !important;
    color: var(--text);
}
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── Zero out ALL Streamlit padding everywhere ── */
.block-container,
.block-container > div,
.block-container > div > div,
section.main > div,
section.main > div > div,
[data-testid="stAppViewContainer"] > section > div,
[data-testid="stMain"] > div,
[data-testid="stMainBlockContainer"],
[data-testid="stMainBlockContainer"] > div,
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stHorizontalBlock"] {
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 100% !important;
}
.block-container { padding-top: 0 !important; padding-bottom: 4rem !important; }
/* Kill the top gap on Screen 2 between header and first element */
[data-testid="stMainBlockContainer"],
[data-testid="stMainBlockContainer"] > div,
[data-testid="stVerticalBlock"] {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* ══════════════════════════
   HEADER — truly full width
══════════════════════════ */
.cx-header {
    background: var(--bg2);
    border-bottom: 1px solid var(--border);
    padding: 0 4rem; height: 72px;
    width: 100vw;
    position: relative; left: 50%; right: 50%;
    margin-left: -50vw; margin-right: -50vw;
    display: flex; align-items: center; justify-content: space-between;
    overflow: hidden;
    box-shadow: 0 1px 0 var(--border);
}
.cx-header::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent 0%, var(--red) 30%, var(--red) 70%, transparent 100%);
    opacity: 0.6;
}
.cx-header-left { display: flex; align-items: center; gap: 1.2rem; }
.cx-logo { font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.5rem;
    color: var(--text); letter-spacing: 0.22em; text-transform: uppercase; }
.cx-logo-dot { width: 7px; height: 7px; background: var(--red); border-radius: 50%;
    display: inline-block; margin-left: 2px; vertical-align: middle; margin-bottom: 2px; }
.cx-header-sep { width: 1px; height: 28px; background: var(--border2); }
.cx-header-title { font-family: 'Outfit', sans-serif; font-weight: 300; font-size: 0.78rem;
    color: var(--muted2); letter-spacing: 0.2em; text-transform: uppercase; }

/* Color bar progress pills in header */
.cx-bar-progress { display: flex; align-items: center; gap: 0.5rem; }
.cx-bar-pill {
    font-family: 'DM Mono', monospace; font-size: 0.62rem; font-weight: 500;
    letter-spacing: 0.14em; text-transform: uppercase;
    padding: 0.22rem 0.65rem; border-radius: 3px;
    border: 1px solid var(--border2); color: var(--muted);
    background: transparent; transition: all 0.2s;
}
.cx-bar-pill.active { border-color: var(--red); color: var(--red); background: rgba(227,0,27,0.08); }
.cx-bar-pill.done   { border-color: var(--green); color: var(--green); background: rgba(0,201,122,0.08); }

.cx-header-right { display: flex; align-items: center; gap: 0.6rem;
    font-family: 'DM Mono', monospace; font-size: 0.72rem; color: var(--muted); letter-spacing: 0.08em; }
.cx-status-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--muted); }
.cx-status-dot.active { background: var(--green); box-shadow: 0 0 6px var(--green); }

/* ══════════════════════════
   BODY
══════════════════════════ */
.cx-body { padding: 0; }

/* Pulse animation for active dot */
@keyframes cx-pulse {
    0%   { box-shadow: 0 0 0 0 rgba(227,0,27,0.5); }
    70%  { box-shadow: 0 0 0 7px rgba(227,0,27,0); }
    100% { box-shadow: 0 0 0 0 rgba(227,0,27,0); }
}

/* SECTION LABEL */
.cx-section-label { font-family: 'DM Mono', monospace; font-size: 0.68rem; color: var(--muted);
    letter-spacing: 0.22em; text-transform: uppercase; margin-bottom: 0.8rem;
    display: flex; align-items: center; gap: 0.6rem; }
.cx-section-label::before { content: ''; display: inline-block; width: 18px; height: 1px;
    background: var(--red); opacity: 0.7; }

/* ══════════════════════════
   FILE UPLOADER
══════════════════════════ */
[data-testid="stFileUploader"] { width: 100% !important; margin-bottom: 0.5rem !important; }
[data-testid="stFileUploader"] > label { display: none !important; }
/* Compact single-row uploader box */
[data-testid="stFileUploader"] section {
    background: var(--bg2) !important; border: 1px solid var(--border2) !important;
    border-radius: 6px !important; padding: 0.85rem 1.4rem !important;
    min-height: unset !important;
    display: flex !important; flex-direction: row !important;
    align-items: center !important; justify-content: flex-start !important;
    gap: 1.2rem !important; width: 100% !important; cursor: pointer !important;
    transition: border-color 0.2s !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    overflow: visible !important; flex-wrap: nowrap !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: var(--red) !important; background: rgba(227,0,27,0.02) !important;
}
/* Hide the upload icon div */
[data-testid="stFileUploader"] section > div:first-child { display: none !important; }
[data-testid="stFileUploader"] section > div { display: flex !important; align-items: center !important; gap: 1.2rem !important; flex-direction: row !important; }
[data-testid="stFileUploader"] section button {
    background: var(--bg3) !important; color: var(--text) !important;
    border: 1px solid var(--border2) !important; border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.72rem !important;
    letter-spacing: 0.16em !important; text-transform: uppercase !important;
    padding: 0.4rem 1.2rem !important; width: auto !important; white-space: nowrap !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.06) !important;
    transition: border-color 0.18s !important; flex-shrink: 0 !important;
}
[data-testid="stFileUploader"] section button:hover {
    border-color: var(--red) !important; color: var(--red) !important;
}
[data-testid="stFileUploader"] section span,
[data-testid="stFileUploader"] section small,
[data-testid="stFileUploader"] section p {
    font-family: 'DM Mono', monospace !important; font-size: 0.68rem !important;
    font-weight: 400 !important; color: var(--muted) !important;
    letter-spacing: 0.08em !important; white-space: nowrap !important;
    overflow: hidden !important; text-overflow: ellipsis !important;
}

/* FILE BADGE */
.cx-file-badge {
    display: flex; align-items: center; gap: 0.6rem;
    background: rgba(0,201,122,0.08); border: 1px solid rgba(0,201,122,0.3);
    border-radius: 4px; padding: 0.55rem 1rem; margin-top: 0.7rem; margin-bottom: 1.2rem;
    font-family: 'DM Mono', monospace; font-size: 0.75rem;
    color: var(--green); letter-spacing: 0.06em;
}

/* ══════════════════════════
   SELECTBOX
══════════════════════════ */
[data-testid="stSelectbox"] { width: 100% !important; }
div[data-baseweb="select"] > div {
    background: var(--bg2) !important; border-color: var(--border2) !important; border-radius: 6px !important;
}
div[data-baseweb="select"] > div:hover { border-color: var(--red) !important; }
div[data-baseweb="select"] span, div[data-baseweb="select"] div { color: var(--text) !important; }
div[data-baseweb="select"] svg { fill: var(--muted) !important; }
div[data-baseweb="popover"] > div { background: var(--bg2) !important; border: 1px solid var(--border2) !important; box-shadow: 0 4px 16px rgba(0,0,0,0.1) !important; }
div[data-baseweb="popover"] li { background: var(--bg2) !important; color: var(--text) !important; }
div[data-baseweb="popover"] li:hover { background: var(--bg3) !important; }
div[data-baseweb="popover"] [aria-selected="true"] { background: rgba(227,0,27,0.08) !important; }

/* ══════════════════════════
   BUTTONS — white textured
══════════════════════════ */
.stButton > button {
    width: 100% !important;
    background: var(--bg2) !important;
    color: var(--text) !important;
    font-family: 'Outfit', sans-serif !important; font-size: 0.82rem !important;
    font-weight: 600 !important; letter-spacing: 0.18em !important; text-transform: uppercase !important;
    border: 1px solid var(--border2) !important; border-radius: 4px !important;
    padding: 0.8 rem 1.2 rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 0 0 1px rgba(0,0,0,0.04) !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: var(--bg3) !important;
    border-color: var(--text) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12) !important;
}
.stButton > button:disabled {
    background: var(--bg3) !important; color: var(--muted) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important; opacity: 0.6 !important;
}
.cx-ghost .stButton > button {
    background: transparent !important; color: var(--muted2) !important;
    border: 1px solid var(--border) !important; box-shadow: none !important;
}
.cx-ghost .stButton > button:hover { border-color: var(--text) !important; color: var(--text) !important; }
.cx-btn-dark .stButton > button {
    background: var(--bg3) !important; color: var(--muted) !important;
    border: 1px solid var(--border) !important; box-shadow: none !important;
}
.cx-btn-dark .stButton > button:hover { border-color: var(--text) !important; color: var(--text) !important; opacity: 1 !important; }

/* ══════════════════════════
   DIVIDER
══════════════════════════ */
.cx-divider { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }

/* ══════════════════════════
   HEAD TRACKER (8 dots only)
══════════════════════════ */
.cx-tracker {
    display: flex; align-items: center; margin-bottom: 1.6rem;
    background: var(--bg2); border: 1px solid var(--border);
    border-radius: 6px; padding: 1rem 2rem; justify-content: space-between;
}
.cx-tracker-head {
    display: flex; flex-direction: column; align-items: center;
    gap: 0.4rem; position: relative; flex: 1;
}
.cx-tracker-head:not(:last-child)::after {
    content: ''; position: absolute; top: 10px;
    left: calc(50% + 12px); right: calc(-50% + 12px);
    height: 1px; background: var(--border2); z-index: 0;
}
.cx-tracker-head.t-done::after { background: var(--green); opacity: 0.5; }
.cx-dot {
    width: 22px; height: 22px; border-radius: 50%;
    border: 1.5px solid var(--border2); background: var(--bg3);
    display: flex; align-items: center; justify-content: center;
    position: relative; z-index: 1;
    font-family: 'DM Mono', monospace; font-size: 0.62rem; color: var(--muted);
}
.cx-dot.t-done   { background: rgba(0,201,122,0.12); border-color: var(--green); color: var(--green); }
.cx-dot.t-active { background: var(--red); border-color: var(--red); color: white; animation: cx-pulse 1.5s infinite; }
.cx-dot-label { font-family: 'DM Mono', monospace; font-size: 0.58rem; color: var(--muted); letter-spacing: 0.08em; }
.cx-dot-label.t-active { color: var(--text); }
.cx-dot-label.t-done   { color: var(--green); }

/* ══════════════════════════
   VIDEO / ANIMATION BOX
══════════════════════════ */
.cx-anim-box {
    background: var(--bg2); border: 1px solid var(--border); border-radius: 6px;
    min-height: 300px; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    position: relative; overflow: hidden; margin-bottom: 1.6rem;
}
.cx-anim-box::before {
    content: ''; position: absolute; inset: 0;
    background-image: linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 40px 40px; opacity: 0.35;
}
/* Screen 3 native video player — simple full-width, natural ratio */
[data-testid="stVideo"] {
    width: 100% !important;
    border-radius: 6px !important;
    margin-bottom: 1.6rem !important;
    border: 1px solid var(--border) !important;
    overflow: hidden !important;
    background: #000 !important;
    display: block !important;
}
[data-testid="stVideo"] video {
    width: 100% !important;
    display: block !important;
    border-radius: 6px !important;
}

/* ══════════════════════════
   INSTRUCTION DATA PANEL
══════════════════════════ */
.cx-panel {
    background: var(--bg2); border: 1px solid var(--border);
    border-left: 3px solid var(--red); border-radius: 6px;
    overflow: hidden; margin-bottom: 1.4rem;
}
.cx-panel.ok { border-left-color: var(--green); }
.cx-panel-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 1.6rem; border-bottom: 1px solid var(--border);
    background: rgba(255,255,255,0.02);
}
.cx-panel-title {
    font-family: 'Outfit', sans-serif; font-size: 1.4rem; font-weight: 700;
    color: var(--text); letter-spacing: 0.06em; text-transform: uppercase;
}
.cx-panel-badge {
    font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 0.16em;
    text-transform: uppercase; padding: 0.25rem 0.7rem; border-radius: 3px;
}
.cx-panel-badge.fix { background: rgba(227,0,27,0.1); border: 1px solid var(--red-dim); color: var(--red); }
.cx-panel-badge.ok  { background: rgba(0,201,122,0.1); border: 1px solid rgba(0,201,122,0.4); color: var(--green); }
.cx-panel-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0; }
.cx-panel-cell {
    padding: 1.1rem 1.6rem;
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
}
.cx-panel-cell:nth-child(3n) { border-right: none; }
.cx-panel-cell:nth-last-child(-n+3) { border-bottom: none; }
.cx-cell-key {
    font-family: 'DM Mono', monospace; font-size: 0.62rem; color: var(--muted);
    letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 0.3rem;
}
.cx-cell-val {
    font-family: 'DM Mono', monospace; font-size: 1.3rem; font-weight: 500;
    color: var(--text); line-height: 1.1;
}
.cx-cell-val.big   { font-size: 1.8rem; }
.cx-cell-val.red   { color: var(--red); }
.cx-cell-val.blue  { color: var(--blue); }
.cx-cell-val.green { color: var(--green); font-size: 1rem; font-family: 'Outfit', sans-serif; font-weight: 500; }
.cx-cell-unit { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--muted); margin-left: 0.25rem; }

/* ══════════════════════════
   CHOOSE NEXT BAR SCREEN
══════════════════════════ */
.cx-nextbar {
    background: var(--bg2); border: 1px solid var(--border); border-radius: 6px;
    padding: 3rem 2rem; text-align: center; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.cx-nextbar::before {
    content: ''; position: absolute; inset: 0;
    background-image: linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 40px 40px; opacity: 0.2;
}
.cx-nextbar-icon { font-size: 2rem; margin-bottom: 0.8rem; position: relative; z-index: 1; }
.cx-nextbar-title {
    font-family: 'Outfit', sans-serif; font-size: 1.6rem; font-weight: 800;
    letter-spacing: 0.08em; text-transform: uppercase; color: var(--green);
    margin-bottom: 0.5rem; position: relative; z-index: 1;
}
.cx-nextbar-sub {
    font-family: 'Outfit', sans-serif; font-size: 0.88rem; font-weight: 300;
    color: var(--muted2); line-height: 1.7; position: relative; z-index: 1; margin-bottom: 1.5rem;
}

/* ══════════════════════════
   FINISH SCREEN
══════════════════════════ */
.cx-finish {
    background: var(--bg2); border: 1px solid var(--border); border-radius: 6px;
    padding: 4rem 2rem; text-align: center; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.cx-finish::before {
    content: ''; position: absolute; inset: 0;
    background-image: linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 40px 40px; opacity: 0.2;
}
.cx-finish-icon { font-size: 2.5rem; margin-bottom: 1rem; position: relative; z-index: 1; }
.cx-finish-title { font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.8rem; position: relative; z-index: 1; }
.cx-finish-sub { font-family: 'Outfit', sans-serif; font-size: 0.9rem; font-weight: 300;
    color: var(--muted2); line-height: 1.7; position: relative; z-index: 1; }

/* ══════════════════════════
   SUMMARY BAR (Screen 3 top)
══════════════════════════ */
.cx-summary {
    background: var(--bg2); border: 1px solid var(--border); border-radius: 6px;
    padding: 1.4rem 2rem; margin-bottom: 1.6rem;
    display: flex; align-items: center; justify-content: space-between; gap: 2rem;
}
.cx-summary-sep { width: 1px; height: 40px; background: var(--border2); }

/* ══════════════════════════
   RED SEPARATOR LINE
══════════════════════════ */
.cx-red-sep {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--red) 20%, var(--red) 80%, transparent);
    margin: 0 0 1.6rem 0; opacity: 0.5; border-radius: 1px;
}

/* ══════════════════════════
   MOVE LOG (4 columns)
══════════════════════════ */
.cx-movelog {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 0; border: 1px solid var(--border); border-radius: 6px;
    overflow: hidden; margin-top: 1.4rem;
    background: var(--bg2);
}
.cx-movelog-col { border-right: 1px solid var(--border); display: flex; flex-direction: column; background: var(--bg2); }
.cx-movelog-col:last-child { border-right: none; }
.cx-movelog-header {
    padding: 0.7rem 1rem; border-bottom: 1px solid var(--border); background: var(--bg3);
    font-family: 'DM Mono', monospace; font-size: 0.65rem;
    font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; text-align: center;
}
.cx-movelog-empty {
    padding: 1.2rem 0.8rem; text-align: center;
    font-family: 'DM Mono', monospace; font-size: 0.6rem;
    color: var(--border2); letter-spacing: 0.1em; text-transform: uppercase;
}
.cx-movelog-entry {
    padding: 0.55rem 0.8rem; border-bottom: 1px solid var(--border);
    display: flex; flex-direction: column; gap: 0.15rem;
    background: var(--bg2);
}
.cx-movelog-entry:last-child { border-bottom: none; }
.cx-movelog-phase { font-family: 'DM Mono', monospace; font-size: 0.58rem; letter-spacing: 0.14em; text-transform: uppercase; }
.cx-movelog-phase.yaw    { color: var(--red); }
.cx-movelog-phase.stitch { color: var(--blue); }
.cx-movelog-phase.ok     { color: var(--green); }
.cx-movelog-detail { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--text); letter-spacing: 0.04em; }
.cx-movelog-sub    { font-family: 'DM Mono', monospace; font-size: 0.58rem; color: var(--muted); letter-spacing: 0.04em; }

/* ══════════════════════════
   ERROR TOAST
══════════════════════════ */
.cx-error {
    display: flex; align-items: flex-start; gap: 1rem;
    background: rgba(227,0,27,0.07); border: 1px solid rgba(227,0,27,0.35);
    border-left: 3px solid var(--red); border-radius: 6px;
    padding: 1rem 1.4rem; margin-bottom: 0.6rem;
}
.cx-error-icon  { font-size: 1.1rem; color: var(--red); flex-shrink: 0; margin-top: 1px; }
.cx-error-title { font-family: 'Outfit', sans-serif; font-size: 0.9rem; font-weight: 600; color: var(--red); margin-bottom: 0.15rem; }
.cx-error-sub   { font-family: 'Outfit', sans-serif; font-size: 0.8rem; font-weight: 300; color: var(--muted2); line-height: 1.5; }

/* ══════════════════════════
   SVG SCHEMATIC BOX
══════════════════════════ */
.cx-schematic-box {
    background: var(--bg2); border: 1px solid var(--border); border-radius: 6px;
    min-height: 300px; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    position: relative; overflow: hidden; margin-bottom: 1.6rem; padding: 2rem;
}
.cx-schematic-box::before {
    content: ''; position: absolute; inset: 0;
    background-image: linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 40px 40px; opacity: 0.35;
}
.cx-sch-corner {
    position: absolute; top: 14px; left: 18px; z-index: 2;
    font-family: 'DM Mono', monospace; font-size: 0.65rem;
    color: var(--muted); letter-spacing: 0.12em; text-transform: uppercase;
}
.cx-sch-corner-r {
    position: absolute; top: 14px; right: 18px; z-index: 2;
    font-family: 'DM Mono', monospace; font-size: 0.65rem;
    color: var(--muted); letter-spacing: 0.1em; text-transform: uppercase;
}

/* ══════════════════════════
   BAR STATUS CARDS
══════════════════════════ */
.cx-bar-card {
    border-radius: 6px; border: 1px solid var(--border2);
    background: var(--bg2); padding: 1.4rem 1.2rem;
    display: flex; flex-direction: column; gap: 0.5rem;
    cursor: default; transition: border-color 0.2s, background 0.2s;
    position: relative; overflow: hidden;
}
.cx-bar-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: var(--border2); transition: background 0.2s;
}
.cx-bar-card.unknown  { border-color: var(--border2); }
.cx-bar-card.unknown::before { background: var(--border2); }
.cx-bar-card.active   { border-color: var(--red); background: rgba(227,0,27,0.04); }
.cx-bar-card.active::before  { background: var(--red); }
.cx-bar-card.yaw-done { border-color: #F5A623; background: rgba(245,166,35,0.04); }
.cx-bar-card.yaw-done::before { background: #F5A623; }
.cx-bar-card.all-done { border-color: var(--green); background: rgba(0,201,122,0.04); }
.cx-bar-card.all-done::before { background: var(--green); }
.cx-bar-card-name   { font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.1rem; letter-spacing: 0.12em; text-transform: uppercase; }
.cx-bar-card-status { font-family: 'DM Mono', monospace; font-size: 0.62rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--muted); }
.cx-bar-card-status.red    { color: var(--red); }
.cx-bar-card-status.yellow { color: #F5A623; }
.cx-bar-card-status.green  { color: var(--green); }

/* ══════════════════════════
   STANDBY SCREEN
══════════════════════════ */
.cx-standby {
    padding: 4rem 2rem; text-align: center;
    border: 1px solid var(--border); border-radius: 6px;
    background: var(--bg2); margin-bottom: 1rem;
    position: relative; overflow: hidden;
}
.cx-standby::before {
    content: ''; position: absolute; inset: 0;
    background-image: linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 40px 40px; opacity: 0.3;
}
.cx-standby-label {
    position: relative; z-index: 1;
    font-family: 'DM Mono', monospace; font-size: 0.75rem;
    letter-spacing: 0.35em; text-transform: uppercase; color: var(--muted);
}
.cx-standby-dash {
    position: relative; z-index: 1;
    font-family: 'DM Mono', monospace; font-size: 3rem;
    color: var(--border2); font-weight: 300; letter-spacing: 0.1em; margin-bottom: 0.5rem;
}

/* ══════════════════════════
   INTRO VIDEO SCREEN (Screen 2)
══════════════════════════ */
.cx-intro-screen {
    background: var(--bg2); border: 1px solid var(--border); border-radius: 6px;
    padding: 2rem; margin-bottom: 1.6rem; position: relative; overflow: hidden;
}
.cx-intro-screen::before {
    content: ''; position: absolute; inset: 0;
    background-image: linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 40px 40px; opacity: 0.15;
}
.cx-intro-label {
    font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--muted);
    letter-spacing: 0.25em; text-transform: uppercase; margin-bottom: 1rem;
    position: relative; z-index: 1;
    display: flex; align-items: center; gap: 0.6rem;
}
.cx-intro-label::before { content: ''; display: inline-block; width: 18px; height: 1px;
    background: var(--red); opacity: 0.7; }

/* Re-watch pause banner */
.cx-rewatch-banner {
    background: rgba(227,0,27,0.06); border: 1px solid rgba(227,0,27,0.2);
    border-left: 3px solid var(--red); border-radius: 6px;
    padding: 0.9rem 1.4rem; margin-bottom: 1.4rem;
    font-family: 'DM Mono', monospace; font-size: 0.68rem;
    color: var(--muted2); letter-spacing: 0.1em; text-transform: uppercase;
}

/* ══════════════════════════
   VIDEO IFRAME — flush with surrounding boxes
══════════════════════════ */
[data-testid="stCustomComponentV1"] {
    display: block !important;
    width: 100% !important;
    line-height: 0 !important;
    margin-bottom: 1.6rem !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}
[data-testid="stCustomComponentV1"] iframe {
    display: block !important;
    width: 100% !important;
    border: none !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    margin: 0 !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ALGORITHM — bisection (yaw + stitch)
# ─────────────────────────────────────────────

# YAW constants
YAW_TOLERANCE    = 10       # |slope * FACTOR| must be below this
YAW_FACTOR       = 24130
YAW_A_EST        = 0.147    # degrees of tilt per full screw turn
RAD2DEG          = 180 / np.pi

# STITCH constants
STITCH_TOLERANCE = 0.01     # mm — |dX| must be below this
STITCH_A_EST     = 0.0123   # mm of x displacement per full screw turn

OVERSHOOT_FACTOR = 1.2      # 20% overshoot for initial guess, can be increased if consistently undershooting, and decreased otherwise


def yaw_within_tolerance(slope):
    return abs(slope * YAW_FACTOR) < YAW_TOLERANCE

def stitch_within_tolerance(dx):
    return abs(dx) < STITCH_TOLERANCE


def _init_state(slopes: np.ndarray, dx_values: np.ndarray) -> dict:
    """
    Initialise bisection state for one colour bar (8 heads).
    Called once per colour on first CSV upload.
    """
    n = len(slopes)

    # Back-calculate where each screw physically is right now from the measured slope
    yaw_current = np.array([
        (-np.arctan(slopes[i]) * RAD2DEG) / YAW_A_EST
        for i in range(n)
    ])

    stitch_current = np.array([
        -dx_values[i] / STITCH_A_EST
        for i in range(n)
    ])

    return {
        'phase': 'yaw',   # 'yaw' | 'stitch' | 'done'
        'n': n,
        'iteration': 0,
        # YAW
        'yaw_slopes':           slopes.copy(),
        'yaw_left':             np.zeros(n),      # [0, 0, ...] left bracket in screw turns
        'yaw_right':            np.zeros(n),
        'yaw_f_left':           slopes.copy(),     # slope at left bracket
        'yaw_f_right':          np.zeros(n),       # will be filled after first overshoot
        'yaw_bracket_found':    np.array([False] * n),
        'yaw_current':          yaw_current,       # cumulative absolute screw position
        # STITCH
        'stitch_dx':            dx_values.copy(),
        'stitch_left':          np.zeros(n),
        'stitch_right':         np.zeros(n),
        'stitch_f_left':        dx_values.copy(),
        'stitch_f_right':       np.zeros(n),
        'stitch_bracket_found': np.array([False] * n),
        'stitch_current':       stitch_current,
    }


def _compute_moves(state: dict) -> list:
    """
    Compute screw adjustments for this iteration without mutating state.
    Returns a list of 8 move dicts.
    """
    n     = state['n']
    phase = state['phase']
    moves = []

    if phase == 'yaw':
        slopes        = state['yaw_slopes']
        current       = state['yaw_current']
        left          = state['yaw_left']
        right         = state['yaw_right']
        bracket_found = state['yaw_bracket_found']

        target = current.copy()
        for i in range(n):
            if yaw_within_tolerance(slopes[i]):
                target[i] = current[i]
                continue
            if not bracket_found[i]:
                # Intelligent overshoot
                alpha_needed_deg = -np.arctan(slopes[i]) * RAD2DEG
                turn_guess       = alpha_needed_deg / YAW_A_EST
                target[i]        = OVERSHOOT_FACTOR * turn_guess
            else:
                # Bisection
                target[i] = (left[i] + right[i]) / 2

        delta = target - current
        for i in range(n):
            within = yaw_within_tolerance(slopes[i])
            moves.append({
                'head_id':      i + 1,
                'phase':        'yaw',
                'needs_fix':    not within,
                'delta_turns':  float(delta[i]),
                'direction':    'CW' if delta[i] > 0 else 'CCW',
                'turns_abs':    float(abs(delta[i])),
                'metric_value': float(slopes[i]),
                'metric_label': 'slope',
                'within_tol':   within,
            })

    elif phase == 'stitch':
        dx_values     = state['stitch_dx']
        current       = state['stitch_current']
        left          = state['stitch_left']
        right         = state['stitch_right']
        bracket_found = state['stitch_bracket_found']

        target = current.copy()
        for i in range(n):
            if stitch_within_tolerance(dx_values[i]):
                target[i] = current[i]
                continue
            if not bracket_found[i]:
                # sign(screw_turn) = -sign(dx)
                turn_guess = -dx_values[i] / STITCH_A_EST
                target[i]  = OVERSHOOT_FACTOR * turn_guess
            else:
                target[i] = (left[i] + right[i]) / 2

        delta = target - current
        for i in range(n):
            within = stitch_within_tolerance(dx_values[i])
            moves.append({
                'head_id':      i + 1,
                'phase':        'stitch',
                'needs_fix':    not within,
                'delta_turns':  float(delta[i]),
                'direction':    'CW' if delta[i] > 0 else 'CCW',
                'turns_abs':    float(abs(delta[i])),
                'metric_value': float(dx_values[i]),
                'metric_label': 'dX',
                'within_tol':   within,
            })

    else:
        # done
        for i in range(n):
            moves.append({
                'head_id': i + 1, 'phase': 'done', 'needs_fix': False,
                'delta_turns': 0.0, 'direction': '—', 'turns_abs': 0.0,
                'metric_value': 0.0, 'metric_label': '—', 'within_tol': True,
            })

    return moves


def _update_state(state: dict, new_slopes: np.ndarray, new_dx: np.ndarray,
                  last_moves: list) -> dict:
    """
    Update brackets and positions after a new measurement CSV is uploaded.
    Advances phase yaw → stitch → done when all heads converge.
    """
    n     = state['n']
    phase = state['phase']

    state['iteration'] += 1

    if phase == 'yaw':
        left          = state['yaw_left']
        right         = state['yaw_right']
        f_left        = state['yaw_f_left']
        f_right       = state['yaw_f_right']
        bracket_found = state['yaw_bracket_found']

        # Back-calculate actual position from measured slope (accounts for human error)
        actual_position = np.array([
            (-np.arctan(new_slopes[i]) * RAD2DEG) / YAW_A_EST
            for i in range(n)
        ])

        for i in range(n):
            if yaw_within_tolerance(new_slopes[i]):
                continue
            if not bracket_found[i]:
                if f_left[i] * new_slopes[i] < 0:
                    # Bracket found — sign flip detected
                    right[i]         = actual_position[i]
                    f_right[i]       = new_slopes[i]
                    # left stays at 0 with f_left = initial slope
                    bracket_found[i] = True
                else:
                    # No sign flip → treat this as new base (to start closer to 0)
                    left[i]   = actual_position[i]
                    f_left[i] = new_slopes[i]
            else:
                # Standard bisection update
                mid = actual_position[i]
                if f_left[i] * new_slopes[i] > 0:
                    left[i]   = mid
                    f_left[i] = new_slopes[i]
                else:
                    right[i]   = mid
                    f_right[i] = new_slopes[i]

        state['yaw_slopes']        = new_slopes.copy()
        state['yaw_current']       = actual_position
        state['yaw_left']          = left
        state['yaw_right']         = right
        state['yaw_f_left']        = f_left
        state['yaw_f_right']       = f_right
        state['yaw_bracket_found'] = bracket_found

        # Advance to stitch if all yaw heads are within tolerance
        if all(yaw_within_tolerance(s) for s in new_slopes):
            state['phase']          = 'stitch'
            state['stitch_dx']      = new_dx.copy()
            state['stitch_f_left']  = new_dx.copy()
            state['stitch_current'] = np.array([
                -new_dx[i] / STITCH_A_EST for i in range(n)
            ])

    elif phase == 'stitch':
        left          = state['stitch_left']
        right         = state['stitch_right']
        f_left        = state['stitch_f_left']
        f_right       = state['stitch_f_right']
        bracket_found = state['stitch_bracket_found']

        # Back-calculate actual position from measured dX
        actual_position = np.array([
            -new_dx[i] / STITCH_A_EST for i in range(n)
        ])

        for i in range(n):
            if stitch_within_tolerance(new_dx[i]):
                continue
            if not bracket_found[i]:
                if f_left[i] * new_dx[i] < 0:
                    # Bracket found
                    right[i]         = actual_position[i]
                    f_right[i]       = new_dx[i]
                    bracket_found[i] = True
                else:
                    # No sign flip → treat this position as new left base
                    left[i]   = actual_position[i]
                    f_left[i] = new_dx[i]
            else:
                # Standard bisection update
                mid = actual_position[i]
                if f_left[i] * new_dx[i] > 0:
                    left[i]   = mid
                    f_left[i] = new_dx[i]
                else:
                    right[i]   = mid
                    f_right[i] = new_dx[i]

        state['stitch_dx']             = new_dx.copy()
        state['stitch_current']        = actual_position
        state['stitch_left']           = left
        state['stitch_right']          = right
        state['stitch_f_left']         = f_left
        state['stitch_f_right']        = f_right
        state['stitch_bracket_found']  = bracket_found

        # Advance to done if all stitch heads are within tolerance
        if all(stitch_within_tolerance(d) for d in new_dx):
            state['phase'] = 'done'

    return state


def _build_steps_from_moves(moves: list, color: str) -> list:
    """Convert _compute_moves() output to the step format the webapp UI expects."""
    steps = []
    for m in moves:
        phase = m['phase']
        if phase == 'yaw':
            steps.append({
                'phase': 'yaw', 'head_id': m['head_id'], 'color_bar': color,
                'yaw_turns': round(m['turns_abs'], 4), 'yaw_dir': m['direction'],
                'needs_yaw': m['needs_fix'],
                'stitch_turns': 0, 'stitch_dir': '—', 'needs_stitch': False,
            })
        elif phase == 'stitch':
            steps.append({
                'phase': 'stitch', 'head_id': m['head_id'], 'color_bar': color,
                'yaw_turns': 0, 'yaw_dir': '—', 'needs_yaw': False,
                'stitch_turns': round(m['turns_abs'], 4), 'stitch_dir': m['direction'],
                'needs_stitch': m['needs_fix'],
            })
        else:
            steps.append({
                'phase': 'done', 'head_id': m['head_id'], 'color_bar': color,
                'yaw_turns': 0, 'yaw_dir': '—', 'needs_yaw': False,
                'stitch_turns': 0, 'stitch_dir': '—', 'needs_stitch': False,
            })
    return steps


def run_algorithm(df: pd.DataFrame, color: str) -> list:
    """
    Initialise (or advance) the bisection state for one colour bar.
    On first upload: initialise state. On subsequent uploads: update state.
    """
    slopes    = df['slop'].values.astype(float)
    dx        = df['dX'].values.astype(float)
    state_key = f'algo_state_{color}'

    if state_key not in st.session_state or st.session_state[state_key] is None:
        # First call — initialise fresh state
        state = _init_state(slopes, dx)
    else:
        # Subsequent call — update existing state with new measurements
        prev_state = st.session_state[state_key]
        last_moves = st.session_state.get(f'algo_moves_{color}', [])
        state      = _update_state(prev_state, slopes, dx, last_moves)

    moves = _compute_moves(state)

    # Persist state and moves so the next upload can update correctly
    st.session_state[state_key]             = state
    st.session_state[f'algo_moves_{color}'] = moves

    steps         = _build_steps_from_moves(moves, color)
    current_phase = state['phase']

    if current_phase == 'yaw':
        return [s for s in steps if s['phase'] == 'yaw']
    elif current_phase == 'stitch':
        return [s for s in steps if s['phase'] == 'stitch']
    else:
        return steps


def build_steps(results: list) -> list:
    """Pass-through — run_algorithm already returns steps in the correct format."""
    return results


# ─────────────────────────────────────────────
#  MEDIA PATHS
# ─────────────────────────────────────────────
TEST_VIDEO  = "assets/video01.mp4"
INTRO_VIDEO = "assets/animation-screen2.mkv"
HOME_IMAGE  = "assets/decoracioweb03.jpeg"


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
BARS       = ["cyan", "magenta", "yellow", "black"]
BAR_COLORS = {'cyan': '#00B4D8', 'magenta': '#D62598', 'yellow': '#F5C400', 'black': '#888899'}

for k, v in {
    'results'          : None,
    'step'             : 0,
    'running'          : False,
    'finished'         : False,
    'printer_fixed'    : False,
    'selected_bar'     : 'cyan',
    'yaw_done_bars'    : [],
    'stitch_done_bars' : [],
    'show_next_bar'    : False,
    'uploaded_file_name': None,
    # 'standby' | 'intro_video' | 'steps'
    'screen'           : 'standby',
    # freezes step UI and shows video inline on screen 3
    'rewatch_video'    : False,
    'audit_log'        : [],
    'error_msg'        : None,
    'move_log'         : {'cyan': [], 'magenta': [], 'yellow': [], 'black': []},
    'bar_status'       : {'cyan': 'unknown', 'magenta': 'unknown', 'yellow': 'unknown', 'black': 'unknown'},
    'all_bar_results'  : {},
    # per-colour bisection state (None = not yet initialised)
    'algo_state_cyan':    None, 'algo_moves_cyan':    [],
    'algo_state_magenta': None, 'algo_moves_magenta': [],
    'algo_state_yellow':  None, 'algo_moves_yellow':  [],
    'algo_state_black':   None, 'algo_moves_black':   [],
    # only show SELECTED indicator after the user explicitly clicks a Select button
    'bar_explicitly_selected': False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
#  SVG PRINTHEAD SCHEMATIC
# ─────────────────────────────────────────────
def build_schematic_svg(active_head: int, done_heads: list, bar_color: str, phase: str) -> str:
    W, H     = 640, 220
    n        = 8
    pad_x    = 60
    head_w   = 44
    head_h   = 60
    spacing  = (W - 2 * pad_x - head_w) / (n - 1)
    rail_y   = H // 2
    rail_top = rail_y - head_h // 2 - 18
    rail_bot = rail_y + head_h // 2 + 18

    svg = (
        f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f'style="width:100%;max-width:600px;z-index:2;position:relative;">'
    )
    svg += (
        f'<rect x="{pad_x - 10}" y="{rail_top}" '
        f'width="{W - 2*pad_x + 20}" height="{rail_bot - rail_top}" '
        f'rx="8" fill="#EBEBED" stroke="{bar_color}" stroke-width="1.5" opacity="0.8"/>'
    )
    svg += (
        f'<text x="{W//2}" y="{rail_top - 8}" text-anchor="middle" '
        f'font-family="DM Mono,monospace" font-size="9" fill="{bar_color}" '
        f'letter-spacing="3" opacity="0.7">PRINTHEAD CARRIER RAIL</text>'
    )
    screw_label = "SCREW A — YAW" if phase == "yaw" else "SCREW B — STITCH"
    svg += (
        f'<text x="{W//2}" y="{rail_bot + 22}" text-anchor="middle" '
        f'font-family="DM Mono,monospace" font-size="9" fill="#6E6E78" letter-spacing="2">'
        f'{screw_label}</text>'
    )
    for i in range(n):
        hnum      = i + 1
        cx        = pad_x + i * spacing + head_w // 2
        hy        = rail_y - head_h // 2
        is_active = (hnum == active_head)
        is_done   = (hnum in done_heads)
        if is_active:
            fill, stroke, opacity, sw, tc = '#E3001B', '#E3001B', '1', '2', 'white'
        elif is_done:
            fill, stroke, opacity, sw, tc = 'rgba(0,168,98,0.12)', '#00A862', '0.9', '1.5', '#00A862'
        else:
            fill, stroke, opacity, sw, tc = '#FFFFFF', '#C4C4C8', '1', '1', '#9090A0'
        svg += (
            f'<rect x="{cx - head_w//2}" y="{hy}" width="{head_w}" height="{head_h}" '
            f'rx="5" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>'
        )
        nozzle_y = hy + head_h - 10
        for nd in range(4):
            nx = cx - 13 + nd * 9
            nc = stroke if (is_active or is_done) else '#D8D8DC'
            svg += f'<circle cx="{nx}" cy="{nozzle_y}" r="2.5" fill="{nc}" opacity="0.9"/>'
        if is_active:
            svg += (
                f'<rect x="{cx - head_w//2 - 5}" y="{hy - 5}" '
                f'width="{head_w + 10}" height="{head_h + 10}" '
                f'rx="8" fill="none" stroke="#E3001B" stroke-width="1" opacity="0.3" '
                f'stroke-dasharray="4 3"/>'
            )
        if is_done:
            svg += (
                f'<text x="{cx}" y="{hy + head_h//2 + 5}" text-anchor="middle" '
                f'font-size="16" fill="#00C97A">✓</text>'
            )
        else:
            svg += (
                f'<text x="{cx}" y="{hy + head_h//2 + 5}" text-anchor="middle" '
                f'font-family="DM Mono,monospace" font-size="14" font-weight="500" fill="{tc}">'
                f'{hnum}</text>'
            )
        svg += (
            f'<text x="{cx}" y="{rail_bot + 38}" text-anchor="middle" '
            f'font-family="DM Mono,monospace" font-size="9" fill="{tc}" letter-spacing="1">'
            f'H{hnum}</text>'
        )
        svg += (
            f'<line x1="{cx}" y1="{rail_bot}" x2="{cx}" y2="{rail_bot + 12}" '
            f'stroke="{stroke}" stroke-width="1" opacity="0.4"/>'
        )
    svg += '</svg>'
    return svg


# ─────────────────────────────────────────────
#  MOVE LOG
# ─────────────────────────────────────────────
def render_move_log():
    log = st.session_state.move_log
    if not any(log.values()):
        return
    cols_html = ''
    for b in BARS:
        bc      = BAR_COLORS[b]
        entries = log.get(b, [])
        header  = f'<div class="cx-movelog-header" style="color:{bc};">{b.upper()}</div>'
        if not entries:
            body = '<div class="cx-movelog-empty">—</div>'
        else:
            body = ''
            for e in entries:
                if e['ok']:
                    phase_cls = 'ok'
                    phase_lbl = f"{e['phase']} · Screw {e['screw']}"
                    detail    = f"H{e['head']} · Within tolerance"
                    sub       = '—'
                else:
                    phase_cls = e['phase'].lower()
                    phase_lbl = f"{e['phase']} · Screw {e['screw']}"
                    detail    = f"H{e['head']} · {e['turns']} rev"
                    sub       = e['dir']
                body += (
                    f'<div class="cx-movelog-entry">'
                    f'<div class="cx-movelog-phase {phase_cls}">{phase_lbl}</div>'
                    f'<div class="cx-movelog-detail">{detail}</div>'
                    f'<div class="cx-movelog-sub">{sub}</div>'
                    f'</div>'
                )
        cols_html += f'<div class="cx-movelog-col">{header}{body}</div>'
    st.markdown(
        f'<div style="margin-top:1.4rem;">'
        f'<div style="font-family:\'DM Mono\',monospace;font-size:0.6rem;color:var(--muted);'  
        f'letter-spacing:0.22em;text-transform:uppercase;margin-bottom:0.6rem;">Move Register</div>'
        f'<div class="cx-movelog">{cols_html}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def bar_pill_cls(bar: str) -> str:
    if bar in st.session_state.get('stitch_done_bars', []):
        return 'done'
    if bar == st.session_state.selected_bar and st.session_state.running:
        return 'active'
    if bar in st.session_state.get('yaw_done_bars', []):
        return 'active'
    return ''


def render_autoplay_video(path: str, height: int = 340,
                          full_bleed: bool = False,
                          show_skip: bool = False,
                          on_end_btn_label: str = None):
    """
    Autoplay, muted, no controls, no loop.
    full_bleed=True  — 16:10 ratio, edge-to-edge (Screen 2).
    full_bleed=False — fixed pixel height, boxed (Screen 3 rewatch).
    Skip is handled by a real st.button on the main page (not inside iframe).
    """
    if not path or not os.path.exists(path):
        st.markdown(
            f'<div class="cx-schematic-box" style="min-height:220px;">'
            f'<div style="position:relative;z-index:2;text-align:center;">'
            f'<div style="font-family:DM Mono,monospace;font-size:0.65rem;'
            f'color:var(--muted);letter-spacing:0.2em;text-transform:uppercase;">'
            f'VIDEO NOT FOUND &mdash; <code style="font-size:0.62rem;">{path}</code>'
            f'</div></div></div>',
            unsafe_allow_html=True
        )
        return

    ext  = os.path.splitext(path)[1].lower()
    mime = {".mp4": "video/mp4", ".webm": "video/webm", ".mkv": "video/mp4"}.get(ext, "video/mp4")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    if full_bleed:
        # Pure video, no skip logic — SKIP button is a real Streamlit button below.
        # JS sizes iframe to: viewport_height - 72px (header) - 64px (skip button).
        html = (
            "<!DOCTYPE html><html><head><style>"
            "*{margin:0;padding:0;box-sizing:border-box;}"
            "html,body{background:#000;width:100%;height:100%;overflow:hidden;}"
            "video{position:fixed;top:0;left:0;width:100%;height:100%;"
            "object-fit:cover;display:block;}"
            "</style></head><body>"
            f'<video id="v" autoplay muted playsinline>'
            f'<source src="data:{mime};base64,{b64}" type="{mime}"></video>'
            "<script>"
            "var BTN=64;"
            "function fit(){"
            "  var vh=window.parent.innerHeight-72-BTN;"
            "  if(vh<200)vh=window.parent.innerHeight-72;"
            "  if(window.frameElement)window.frameElement.style.height=vh+'px';"
            "  document.documentElement.style.height=vh+'px';"
            "  document.body.style.height=vh+'px';}"
            "fit();"
            "window.addEventListener('resize',fit);"
            "setTimeout(fit,40);setTimeout(fit,300);"
            "document.getElementById('v').play().catch(function(){});"
            "</script></body></html>"
        )
        components.html(html, height=620)
    else:
        h = height
        html = (
            "<!DOCTYPE html><html><head><style>"
            f"*{{margin:0;padding:0;box-sizing:border-box;}}"
            f"html,body{{background:#D8D8D8;width:100%;height:{h}px;overflow:hidden;}}"
            f"video{{width:100%;height:{h}px;object-fit:cover;display:block;border-radius:6px;}}"
            "</style></head><body>"
            f'<video id="v" autoplay muted playsinline>'
            f'<source src="data:{mime};base64,{b64}" type="{mime}"></video>'
            "<script>"
            "var vid=document.getElementById('v');vid.play().catch(function(){});"
            "</script></body></html>"
        )
        components.html(html, height=h)


def render_bar_summary(phase: str = 'yaw'):
    """Bar analysis summary — shown at the top of Screen 3.
    Shows only the YAW block during yaw phase, only STITCH during stitch phase.
    """
    steps  = st.session_state.results
    bar    = st.session_state.selected_bar
    bar_col = BAR_COLORS.get(bar, '#888')

    def head_chips(steps_list, needs_key):
        html = ''
        for s in steps_list:
            needs = s[needs_key]
            col2  = 'var(--red)' if needs else 'var(--green)'
            html += (
                f'<div style="width:32px;height:32px;border-radius:4px;'
                f'background:{col2}22;border:1px solid {col2};'
                f'display:flex;align-items:center;justify-content:center;'
                f'font-family:DM Mono,monospace;font-size:0.6rem;color:{col2};">'
                f'H{s["head_id"]}</div>'
            )
        return html

    if phase == 'yaw':
        rel_steps  = [s for s in steps if s['phase'] == 'yaw'][:8]
        n_fix      = sum(1 for s in rel_steps if s['needs_yaw'])
        n_ok       = 8 - n_fix
        phase_lbl  = 'YAW &nbsp;&mdash;&nbsp; Screw A'
        chips_html = head_chips(rel_steps, 'needs_yaw')
    else:
        rel_steps  = [s for s in steps if s['phase'] == 'stitch'][:8]
        n_fix      = sum(1 for s in rel_steps if s['needs_stitch'])
        n_ok       = 8 - n_fix
        phase_lbl  = 'STITCH &nbsp;&mdash;&nbsp; Screw B'
        chips_html = head_chips(rel_steps, 'needs_stitch')

    st.markdown(
        f'<div class="cx-summary">'
        f'<div style="display:flex;flex-direction:column;gap:0.3rem;min-width:90px;">'
        f'<div style="font-family:\'Outfit\',sans-serif;font-size:1.3rem;font-weight:700;color:{bar_col};">{bar.upper()}</div>'
        f'<div style="font-family:\'DM Mono\',monospace;font-size:0.6rem;color:var(--muted);letter-spacing:0.2em;">BAR ANALYSIS</div>'
        f'</div>'
        f'<div class="cx-summary-sep"></div>'
        f'<div style="flex:1;">'
        f'<div style="font-family:\'DM Mono\',monospace;font-size:0.6rem;color:var(--muted);'
        f'letter-spacing:0.18em;text-transform:uppercase;margin-bottom:0.6rem;">'
        f'{phase_lbl} &nbsp;&mdash;&nbsp; '
        f'<span style="color:var(--red);">{n_fix} fix</span>'
        f' &nbsp;/&nbsp; <span style="color:var(--green);">{n_ok} OK</span>'
        f'</div>'
        f'<div style="display:flex;gap:0.35rem;flex-wrap:wrap;">{chips_html}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
_is_running    = st.session_state.running or st.session_state.show_next_bar
status_cls     = "active" if _is_running else ""
status_txt     = "SYSTEM ACTIVE" if _is_running else "STANDBY"
bar_pills_html = ""
for b in BARS:
    bar_pills_html += f'<div class="cx-bar-pill {bar_pill_cls(b)}">{b}</div>'

st.markdown(
    f'<div class="cx-header">'
    f'<div class="cx-header-left">'
    f'<div class="cx-logo">COMEXI<span class="cx-logo-dot"></span></div>'
    f'<div class="cx-header-sep"></div>'
    f'<div class="cx-header-title">Printhead Adjustment UI</div>'
    f'</div>'
    f'<div class="cx-bar-progress">{bar_pills_html}</div>'
    f'<div class="cx-header-right">'
    f'<div class="cx-status-dot {status_cls}"></div>'
    f'{status_txt}'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="cx-body">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  SCREEN 2 — rendered OUTSIDE col_body for true full-bleed
# ══════════════════════════════════════════════════════════
if st.session_state.screen == 'intro_video':

    # ── Full-bleed video — sticks to top, sized to leave room for button ──
    st.markdown(
        '<div style="width:100vw;position:relative;left:50%;margin-left:-50vw;overflow:hidden;">',
        unsafe_allow_html=True
    )
    render_autoplay_video(INTRO_VIDEO, full_bleed=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── SKIP button — full-width, below the animation ──
    st.markdown(
        '<div style="width:100vw;position:relative;left:50%;margin-left:-50vw;">',
        unsafe_allow_html=True
    )
    st.markdown("""<style>
    .cx-skip-row > div[data-testid="stButton"] > button {
        width: 100% !important;
        height: 64px !important;
        background: #1A1A1E !important;
        color: #ffffff !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.32em !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 0 !important;
        border-top: 1px solid rgba(255,255,255,0.12) !important;
        box-shadow: none !important;
        cursor: pointer !important;
        transition: background 0.15s !important;
    }
    .cx-skip-row > div[data-testid="stButton"] > button:hover {
        background: #2a2a2e !important;
    }
    </style>""", unsafe_allow_html=True)
    st.markdown('<div class="cx-skip-row">', unsafe_allow_html=True)
    if st.button("SKIP  ▶▶", key="skip_btn"):
        st.session_state.screen        = 'steps'
        st.session_state.running       = True
        st.session_state.rewatch_video = False
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)


# Inject per-screen background color + hide overflow on Screen 2
if st.session_state.screen == 'intro_video':
    st.markdown(
        '<style>'
        '.stApp,.stApp>div,[class*="css"],html,body{background:#D8D8D8 !important;}'
        '</style>',
        unsafe_allow_html=True
    )
elif st.session_state.screen == 'steps':
    st.markdown(
        '<style>.stApp,.stApp>div,[class*="css"],html,body{background:#D8D8D8 !important;}</style>',
        unsafe_allow_html=True
    )
# Screen 1 keeps --bg (#F5F5F7) which is already the default

_l, col_body, _r = st.columns([1, 16, 1])

with col_body:

    # ══════════════════════════════════════════════════════════
    #  SCREEN 1 — STANDBY
    #  CSV upload + bar selector cards. No analysis preview here.
    # ══════════════════════════════════════════════════════════
    if st.session_state.screen == 'standby':

        st.markdown('<div class="cx-section-label">Data Input</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Drag and drop csv here",
            type=["csv"],
            label_visibility="visible",
        )
        if uploaded_file:
            st.markdown(
                f'<div class="cx-file-badge">&#10003; &nbsp;{uploaded_file.name} &mdash; ready</div>',
                unsafe_allow_html=True
            )

        if st.session_state.get('error_msg'):
            title, detail = st.session_state.error_msg
            st.markdown(
                f'<div class="cx-error"><div class="cx-error-icon">&#9888;</div>'
                f'<div><div class="cx-error-title">{title}</div>'
                f'<div class="cx-error-sub">{detail}</div></div></div>',
                unsafe_allow_html=True
            )

        # ── HOME IMAGE (replaces standby box) ──
        if os.path.exists(HOME_IMAGE):
            with open(HOME_IMAGE, "rb") as _img_f:
                _img_b64 = base64.b64encode(_img_f.read()).decode()
            _img_ext  = os.path.splitext(HOME_IMAGE)[1].lower()
            _img_mime = {".jpeg": "image/jpeg", ".jpg": "image/jpeg",
                         ".png": "image/png", ".webp": "image/webp"}.get(_img_ext, "image/jpeg")
            st.markdown(
                f'<div style="width:100%;border-radius:6px;overflow:hidden;'
                f'margin-top:1.2rem;margin-bottom:1.8rem;border:1px solid var(--border);line-height:0;">'
                f'<img src="data:{_img_mime};base64,{_img_b64}" '
                f'style="width:100%;height:auto;display:block;border-radius:6px;" '
                f'alt="Comexi Alignment System"/>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="cx-standby" style="min-height:120px;">'
                f'<div class="cx-standby-label" style="font-size:0.65rem;">'
                f'Image not found &mdash; <code>{HOME_IMAGE}</code>'
                f'</div></div>',
                unsafe_allow_html=True
            )

        if st.button("Process CSV  &#8594;", use_container_width=True):
            if uploaded_file is None:
                st.session_state.error_msg = (
                    "No file uploaded",
                    "Please drag and drop a CSV file or use BROWSE FILES before processing."
                )
                st.rerun()
            else:
                st.session_state.error_msg = None
                df_all = pd.read_csv(uploaded_file)
                df_all['color'] = df_all['color'].str.lower()
                all_results = {}
                for b in BARS:
                    df_b = df_all[df_all['color'] == b]
                    if not df_b.empty:
                        df_b = df_b.sort_values('headInBarIndex').reset_index(drop=True)
                        all_results[b] = build_steps(run_algorithm(df_b, b))
                st.session_state.all_bar_results = all_results
                bar = st.session_state.selected_bar
                st.session_state.results       = all_results.get(bar, [])
                st.session_state.step          = 0
                st.session_state.running       = False
                st.session_state.finished      = False
                st.session_state.printer_fixed = False
                st.session_state.show_next_bar = False
                # Update bar statuses from newly processed CSV
                for b in BARS:
                    bsteps = all_results.get(b, [])
                    if bsteps:
                        yn = sum(1 for s in bsteps if s['phase'] == 'yaw'    and s['needs_yaw'])
                        sn = sum(1 for s in bsteps if s['phase'] == 'stitch' and s['needs_stitch'])
                        if yn == 0 and sn == 0:
                            st.session_state.bar_status[b] = 'done'
                        elif yn > 0:
                            st.session_state.bar_status[b] = 'needs_yaw'
                        else:
                            st.session_state.bar_status[b] = 'needs_stitch'
                # → Screen 2 (intro video)
                st.session_state.screen = 'intro_video'
                st.rerun()

        # Bar selector cards — select which bar to work on first
        st.markdown(
            '<div style="font-family:\'DM Mono\',monospace;font-size:0.65rem;color:var(--muted);'
            'letter-spacing:0.22em;text-transform:uppercase;margin-top:1.8rem;margin-bottom:0.8rem;">'
            'Select color bar to work on</div>',
            unsafe_allow_html=True
        )
        bar_status = st.session_state.bar_status
        card_cols  = st.columns(4)
        for i, b in enumerate(BARS):
            with card_cols[i]:
                bc     = BAR_COLORS[b]
                st_v   = bar_status[b]
                is_sel = (b == st.session_state.selected_bar)
                if st_v == 'unknown':        card_cls, status_lbl, sc = 'unknown',  'UNKNOWN',      ''
                elif st_v == 'needs_yaw':    card_cls, status_lbl, sc = 'active',   'NEEDS YAW',    'red'
                elif st_v == 'needs_stitch': card_cls, status_lbl, sc = 'yaw-done', 'NEEDS STITCH', 'yellow'
                else:                        card_cls, status_lbl, sc = 'all-done', 'ALIGNED',      'green'
                sel_indicator = (
                    "<div style='font-family:DM Mono,monospace;font-size:0.55rem;"
                    "color:var(--muted);margin-top:0.3rem;letter-spacing:0.1em;'>SELECTED ▲</div>"
                ) if is_sel and st.session_state.get('bar_explicitly_selected', False) else ""
                st.markdown(
                    f'<div class="cx-bar-card {card_cls}">'
                    f'<div class="cx-bar-card-name" style="color:{bc};">{b.upper()}</div>'
                    f'<div class="cx-bar-card-status {sc}">{status_lbl}</div>'
                    f'{sel_indicator}'
                    f'</div>',
                    unsafe_allow_html=True
                )
                if st.button("Select", key=f"sel_{b}", use_container_width=True):
                    st.session_state.selected_bar = b
                    st.session_state.bar_explicitly_selected = True
                    st.rerun()

    # ══════════════════════════════════════════════════════════
    #  SCREEN 3 — STEPS
    #  Bar analysis summary at top, then step-by-step walkthrough.
    #  Re-watch button freezes the UI and shows intro video inline.
    # ══════════════════════════════════════════════════════════
    elif st.session_state.screen == 'steps':

        # ── RE-WATCH MODE: video shown, everything else frozen ──
        if st.session_state.rewatch_video:
            st.markdown(
                '<div class="cx-rewatch-banner">'
                '&#9654;&nbsp;&nbsp; Alignment overview — step flow is paused'
                '</div>',
                unsafe_allow_html=True
            )
            # Autoplay, no controls, no loop — no auto-advance (user resumes manually)
            render_autoplay_video(INTRO_VIDEO, height=320)
            st.markdown('<div class="cx-ghost">', unsafe_allow_html=True)
            resume_clicked = st.button("&#9654; Resume Steps", use_container_width=True, key="resume_steps_btn")
            st.markdown('</div>', unsafe_allow_html=True)
            if resume_clicked:
                st.session_state.rewatch_video = False
                st.rerun()
            st.stop()

        # ── CHOOSE NEXT BAR ──
        if st.session_state.show_next_bar:
            cur_bar      = st.session_state.selected_bar
            yaw_done     = st.session_state.yaw_done_bars
            stitch_done  = st.session_state.stitch_done_bars
            all_bar_res  = st.session_state.all_bar_results

            worked_bars = set(yaw_done) | set(stitch_done)

            def bar_needs_work(b):
                """True only if this bar has actual adjustments for the technician to make."""
                steps = all_bar_res.get(b, [])
                if not steps:
                    return False
                algo_state = st.session_state.get(f'algo_state_{b}')
                if algo_state and algo_state.get('phase') == 'done':
                    return False
                return any(s.get('needs_yaw') or s.get('needs_stitch') for s in steps)

            bars_with_pending_steps = [
                b for b in BARS
                if b != cur_bar
                and b not in worked_bars
                and bar_needs_work(b)
            ]

            # Determine if ALL bars have been worked this round → need new CSV
            all_done_this_round = len(bars_with_pending_steps) == 0

            if not all_done_this_round:
                # Still bars to work on — show picker
                st.markdown(
                    f'<div class="cx-nextbar">'
                    f'<div class="cx-nextbar-icon" style="color:var(--green);">&#10003;</div>'
                    f'<div class="cx-nextbar-title">{cur_bar.upper()} — Phase Complete</div>'
                    f'<div class="cx-nextbar-sub">'
                    f'All 8 heads on <strong style="color:var(--text);">{cur_bar.upper()}</strong> have been adjusted.<br>'
                    f'Select another bar to continue. No new CSV needed — calculations are already done.'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                btn_cols = st.columns(4)
                for i, b in enumerate(BARS):
                    with btn_cols[i]:
                        is_cur       = (b == cur_bar)
                        already_done = (b in worked_bars and b != cur_bar)
                        has_pending  = (b in bars_with_pending_steps)
                        if is_cur or already_done:
                            st.markdown('<div class="cx-btn-dark">', unsafe_allow_html=True)
                            st.button(f"✓ {b.upper()}", key=f"bar_{b}", use_container_width=True, disabled=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        elif has_pending:
                            if st.button(f"→ {b.upper()}", key=f"bar_{b}", use_container_width=True):
                                st.session_state.selected_bar  = b
                                st.session_state.results       = all_bar_res[b]
                                st.session_state.step          = 0
                                st.session_state.show_next_bar = False
                                st.session_state.running       = True
                                st.rerun()
                        else:
                            st.markdown('<div class="cx-ghost">', unsafe_allow_html=True)
                            st.button(f"{b.upper()}", key=f"bar_{b}", use_container_width=True, disabled=True)
                            st.markdown('</div>', unsafe_allow_html=True)

            else:
                # All bars done this round → upload new CSV
                st.markdown(
                    f'<div class="cx-nextbar">'
                    f'<div class="cx-nextbar-icon" style="color:var(--blue);">&#8635;</div>'
                    f'<div class="cx-nextbar-title">Round Complete — New Measurement Required</div>'
                    f'<div class="cx-nextbar-sub">'
                    f'All adjustments for this round have been applied to all 4 bars.<br>'
                    f'Re-measure the machine and upload a new CSV to determine the next steps.'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                new_csv_upload_err = st.session_state.get('next_csv_error')
                if new_csv_upload_err:
                    st.markdown(
                        f'<div class="cx-error"><div class="cx-error-icon">&#9888;</div>'
                        f'<div><div class="cx-error-title">No file uploaded</div>'
                        f'<div class="cx-error-sub">Please upload fresh measurements before continuing.</div>'
                        f'</div></div>',
                        unsafe_allow_html=True
                    )
                new_csv = st.file_uploader("Upload new measurement CSV", type=["csv"], key="next_csv")
                if st.button("Process New CSV  &#8594;", use_container_width=True):
                    if new_csv is None:
                        st.session_state['next_csv_error'] = True
                        st.rerun()
                    else:
                        st.session_state['next_csv_error'] = False
                        df_all = pd.read_csv(new_csv)
                        df_all['color'] = df_all['color'].str.lower()
                        all_results = {}
                        for b in BARS:
                            df_b = df_all[df_all['color'] == b]
                            if not df_b.empty:
                                df_b = df_b.sort_values('headInBarIndex').reset_index(drop=True)
                                all_results[b] = build_steps(run_algorithm(df_b, b))
                        # Update bar statuses strictly from what the new CSV says
                        for b in BARS:
                            bsteps = all_results.get(b, [])
                            if bsteps:
                                yn = sum(1 for s in bsteps if s['phase'] == 'yaw'    and s['needs_yaw'])
                                sn = sum(1 for s in bsteps if s['phase'] == 'stitch' and s['needs_stitch'])
                                if yn == 0 and sn == 0:
                                    st.session_state.bar_status[b] = 'done'
                                elif yn > 0:
                                    st.session_state.bar_status[b] = 'needs_yaw'
                                else:
                                    st.session_state.bar_status[b] = 'needs_stitch'
                        # Check if everything is fully aligned
                        all_aligned = all(
                            st.session_state.bar_status.get(b) == 'done' for b in BARS
                        )
                        st.session_state.all_bar_results = all_results
                        # Reset round tracking
                        st.session_state.yaw_done_bars    = []
                        st.session_state.stitch_done_bars = []
                        if all_aligned:
                            st.session_state.finished      = True
                            st.session_state.printer_fixed = True
                            st.session_state.running       = False
                            st.session_state.show_next_bar = False
                        else:
                            # Jump to first bar that needs work
                            for b in BARS:
                                if st.session_state.bar_status.get(b) != 'done':
                                    st.session_state.selected_bar = b
                                    st.session_state.results      = all_results.get(b, [])
                                    break
                            st.session_state.step          = 0
                            st.session_state.show_next_bar = False
                            st.session_state.running       = True
                        st.rerun()

            render_move_log()

        # ── FINISHED ──
        elif st.session_state.finished:
            st.markdown("""
            <div class="cx-finish">
                <div class="cx-finish-icon">&#9711;</div>
                <div class="cx-finish-title" style="color:var(--green);">Printer Aligned</div>
                <div class="cx-finish-sub">All heads on all 4 colour bars are within tolerance.<br>
                The system is ready for production.</div>
            </div>""", unsafe_allow_html=True)

            if st.button("&#8617;  New Cycle", use_container_width=True):
                for k, v in {
                    'results': None, 'step': 0, 'running': False,
                    'finished': False, 'printer_fixed': False,
                    'show_next_bar': False, 'screen': 'standby',
                    'rewatch_video': False,
                    'yaw_done_bars': [], 'stitch_done_bars': [],
                    'audit_log': [],
                    'move_log': {'cyan': [], 'magenta': [], 'yellow': [], 'black': []},
                    'bar_status': {'cyan': 'unknown', 'magenta': 'unknown', 'yellow': 'unknown', 'black': 'unknown'},
                    'all_bar_results': {},
                }.items():
                    st.session_state[k] = v
                # Clear per-colour bisection state so next upload starts fresh
                for _b in BARS:
                    st.session_state[f'algo_state_{_b}'] = None
                    st.session_state[f'algo_moves_{_b}'] = []
                st.session_state.bar_explicitly_selected = False
                st.rerun()

        # ── ACTIVE STEPS ──
        elif st.session_state.running and st.session_state.results:
            steps    = st.session_state.results
            total    = len(steps)
            step_idx = st.session_state.step
            current  = steps[step_idx]
            phase    = current['phase']
            head_num = current['head_id']

            phase1_steps     = [s for s in steps if s['phase'] == 'yaw']
            N_HEADS          = 8
            cur_pos          = step_idx   # step_idx always 0-based within the current phase
            display_bar      = current['color_bar'] if current['color_bar'] != 'unknown' else st.session_state.selected_bar
            display_bar_col  = BAR_COLORS.get(display_bar, '#888')
            display_bar_name = display_bar.upper()

            # ── BAR ANALYSIS SUMMARY at top of Screen 3 ──
            render_bar_summary(phase=phase)

            # ── RE-WATCH INTRO BUTTON — top right, ghost style ──
            _, rw_btn_col = st.columns([9, 3])
            with rw_btn_col:
                st.markdown('<div class="cx-ghost">', unsafe_allow_html=True)
                if st.button("&#9654; Rewatch animation", use_container_width=True, key="rewatch_btn"):
                    st.session_state.rewatch_video = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            # ── VIDEO / ANIMATION BOX ──
            anim_corner = f"HEAD {head_num} &middot; {'YAW' if phase == 'yaw' else 'STITCH'}"
            if TEST_VIDEO and os.path.exists(TEST_VIDEO):
                with open(TEST_VIDEO, 'rb') as _vf:
                    st.video(_vf.read())
            else:
                done_so_far = list(range(1, cur_pos + 1))
                svg_html    = build_schematic_svg(head_num, done_so_far, display_bar_col, phase)
                st.markdown(
                    f'<div class="cx-schematic-box">'
                    f'<span class="cx-sch-corner">{anim_corner}</span>'
                    f'<span class="cx-sch-corner-r">{display_bar_name}</span>'
                    f'{svg_html}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            # ── HEAD TRACKER — 8 dots ──
            dots_html = ""
            for i in range(N_HEADS):
                if i < cur_pos:
                    dcls = "t-done";   inner = "&#10003;"; lcls = "t-done";   hcls = "t-done"
                elif i == cur_pos:
                    dcls = "t-active"; inner = str(i + 1); lcls = "t-active"; hcls = "t-active"
                else:
                    dcls = "";         inner = str(i + 1); lcls = "";          hcls = ""
                dots_html += (
                    f'<div class="cx-tracker-head {hcls}">'
                    f'<div class="cx-dot {dcls}">{inner}</div>'
                    f'<div class="cx-dot-label {lcls}">H{i+1}</div>'
                    f'</div>'
                )
            st.markdown(f'<div class="cx-tracker">{dots_html}</div>', unsafe_allow_html=True)

            # ── RED SEPARATOR ──
            st.markdown('<div class="cx-red-sep"></div>', unsafe_allow_html=True)

            # ── INSTRUCTION DATA PANEL ──
            if phase == 'yaw':
                screw_id, screw_name = "A", "YAW"
                turns     = current['yaw_turns']
                direction = current['yaw_dir']
                needs_fix = current['needs_yaw']
            else:
                screw_id, screw_name = "B", "STITCH"
                turns     = current['stitch_turns']
                direction = current['stitch_dir']
                needs_fix = current['needs_stitch']

            dir_cls   = "red" if direction == "CW" else "blue"
            dir_sym   = "&#8635; Clockwise" if direction == "CW" else "&#8634; Counter-Clockwise"
            badge_cls = "fix" if needs_fix else "ok"
            badge_txt = "ADJUSTMENT REQUIRED" if needs_fix else "WITHIN TOLERANCE"
            panel_cls = "cx-panel" if needs_fix else "cx-panel ok"
            phase_txt = "01 &mdash; YAW" if phase == 'yaw' else "02 &mdash; STITCH"

            if needs_fix:
                cells_html = (
                    f'<div class="cx-panel-cell">'
                    f'<div class="cx-cell-key">Head Number</div>'
                    f'<div class="cx-cell-val" style="font-size:3rem;font-weight:800;line-height:1;color:var(--text);">{head_num}</div>'
                    f'</div>'
                    f'<div class="cx-panel-cell">'
                    f'<div class="cx-cell-key">Color Bar</div>'
                    f'<div class="cx-cell-val" style="color:{display_bar_col};font-size:1.5rem;font-weight:700;">{display_bar_name}</div>'
                    f'</div>'
                    f'<div class="cx-panel-cell">'
                    f'<div class="cx-cell-key">Phase</div>'
                    f'<div class="cx-cell-val" style="font-size:1rem;">{phase_txt}</div>'
                    f'</div>'
                    f'<div class="cx-panel-cell">'
                    f'<div class="cx-cell-key">Screw Turns</div>'
                    f'<div class="cx-cell-val big">{turns}<span class="cx-cell-unit">rev</span></div>'
                    f'</div>'
                    f'<div class="cx-panel-cell" style="grid-column:span 2;">'
                    f'<div class="cx-cell-key">Direction</div>'
                    f'<div class="cx-cell-val {dir_cls}" style="font-size:1.4rem;">{dir_sym}</div>'
                    f'</div>'
                )
            else:
                cells_html = (
                    f'<div class="cx-panel-cell">'
                    f'<div class="cx-cell-key">Head Number</div>'
                    f'<div class="cx-cell-val" style="font-size:3rem;font-weight:800;line-height:1;color:var(--text);">{head_num}</div>'
                    f'</div>'
                    f'<div class="cx-panel-cell">'
                    f'<div class="cx-cell-key">Color Bar</div>'
                    f'<div class="cx-cell-val" style="color:{display_bar_col};font-size:1.5rem;font-weight:700;">{display_bar_name}</div>'
                    f'</div>'
                    f'<div class="cx-panel-cell">'
                    f'<div class="cx-cell-key">Phase</div>'
                    f'<div class="cx-cell-val" style="font-size:1rem;">{phase_txt}</div>'
                    f'</div>'
                    f'<div class="cx-panel-cell" style="grid-column:span 3;">'
                    f'<div class="cx-cell-key">Status</div>'
                    f'<div class="cx-cell-val green" style="font-size:1.1rem;">&#10003; No adjustment needed &mdash; head is within tolerance</div>'
                    f'</div>'
                )

            st.markdown(
                f'<div class="{panel_cls}">'
                f'<div class="cx-panel-header">'
                f'<div class="cx-panel-title">Screw {screw_id} &mdash; {screw_name}</div>'
                f'<div class="cx-panel-badge {badge_cls}">{badge_txt}</div>'
                f'</div>'
                f'<div class="cx-panel-grid">{cells_html}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

            # ── NEXT STEP ──
            st.markdown('<div class="cx-ghost">', unsafe_allow_html=True)
            if st.button("Next Step  &#8594;", use_container_width=True):
                entry = {
                    'head' : head_num,
                    'phase': phase.upper(),
                    'screw': screw_id,
                    'turns': turns if needs_fix else 0,
                    'dir'  : direction if needs_fix else '—',
                    'ok'   : not needs_fix,
                }
                bar_key = display_bar.lower()
                if bar_key in st.session_state.move_log:
                    st.session_state.move_log[bar_key].append(entry)

                next_idx = step_idx + 1
                if next_idx >= total:
                    # This bar has finished its current phase (yaw OR stitch)
                    bar_k = current['color_bar'] if current['color_bar'] != 'unknown' else st.session_state.selected_bar
                    if phase == 'yaw':
                        if bar_k not in st.session_state.yaw_done_bars:
                            st.session_state.yaw_done_bars.append(bar_k)
                    else:
                        if bar_k not in st.session_state.stitch_done_bars:
                            st.session_state.stitch_done_bars.append(bar_k)
                    st.session_state.show_next_bar = True
                    st.session_state.running       = False
                    st.rerun()
                else:
                    st.session_state.step = next_idx
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            render_move_log()

st.markdown('</div>', unsafe_allow_html=True)
