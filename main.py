import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="원소 탐험대 (Periodic Table Explorer)", layout="wide")
st.title("🔬 원소 탐험대 (Periodic Table Explorer)")

# Load data from GitHub
@st.cache_data
def load_elements():
    url = "https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json"
    r = requests.get(url)
    data = r.json()
    return pd.json_normalize(data['elements'])

elements = load_elements()

# 색상 매핑
category_colors = {
    'alkali metal': '#FF6666',
    'alkaline earth metal': '#FFDEAD',
    'transition metal': '#FFD700',
    'post-transition metal': '#B0C4DE',
    'metalloid': '#66CDAA',
    'nonmetal': '#90EE90',
    'halogen': '#FFB6C1',
    'noble gas': '#87CEFA',
    'lanthanoid': '#E6E6FA',
    'actinoid': '#DDA0DD',
}

# 선택 상태
if "selected" not in st.session_state:
    st.session_state.selected = None

# 주기율표 표시
st.subheader("🧪 주기율표")
for period in range(1, 8):
    cols = st.columns(18)
    for group in range(1, 19):
        match = elements[(elements['xpos'] == group) & (elements['ypos'] == period)]
        if not match.empty:
            el = match.iloc[0]
            color = category_colors.get(el['category'], '#DDDDDD')
            if cols[group - 1].button(el['symbol'], key=f\"{el['symbol']}_{period}\"):
                st.session_state.selected = el['symbol']
            cols[group - 1].markdown(f\"\"\"<div style='text-align: center; font-size: 10px; background-color:{color}; border-radius: 8px; padding: 2px'>{el['number']}</div>\"\"\", unsafe_allow_html=True)
        else:
            cols[group - 1].write(\" \")

# 정보 표시
if st.session_state.selected:
    el = elements[elements['symbol'] == st.session_state.selected].iloc[0]
    st.markdown(f\"\"\"\n    ### 🌟 {el['name']} ({el['symbol']})\n    - **원자번호:** {el['number']}\n    - **원자 질량:** {el['atomic_mass']}\n    - **카테고리:** {el['category']}\n    - **전자 배열:** {el['electron_configuration']}\n    - **요약:** {el['summary']}\n\"\"\")
else:
    st.info(\"원소를 클릭해서 정보를 확인해보세요! 🧭\")
