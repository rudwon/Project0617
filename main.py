import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="원소 탐험대 (Periodic Table Explorer)", layout="wide")
st.markdown("""
    <style>
    .element-button {
        font-weight: bold;
        border-radius: 10px;
        border: none;
        width: 60px;
        height: 60px;
        color: white;
    }
    .info-box {
        background-color: #f0f4f8;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌟 원소 탐험대 (Periodic Table Explorer)")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json"
    r = requests.get(url)
    data = r.json()
    return pd.json_normalize(data['elements'])

data = load_data()

category_colors = {
    'alkali metal': '#e74c3c',
    'alkaline earth metal': '#f39c12',
    'transition metal': '#3498db',
    'post-transition metal': '#9b59b6',
    'metalloid': '#1abc9c',
    'nonmetal': '#2ecc71',
    'halogen': '#e67e22',
    'noble gas': '#9b59b6',
    'lanthanoid': '#34495e',
    'actinoid': '#7f8c8d',
    'unknown': '#bdc3c7'
}

if 'selected_element' not in st.session_state:
    st.session_state.selected_element = None

st.subheader("🧪 주기율표")

for period in range(1, 8):
    cols = st.columns(18)
    for group in range(1, 19):
        match = data[(data['xpos'] == group) & (data['ypos'] == period)]
        if not match.empty:
            el = match.iloc[0]
            color = category_colors.get(el['category'], '#95a5a6')
            btn_style = f"background-color:{color};"
            if cols[group - 1].button(el['symbol'], key=el['symbol']):
                st.session_state.selected_element = el['symbol']
            cols[group - 1].markdown(f"""
                <div style='{btn_style} border-radius:6px; padding:4px; text-align:center; font-size:10px; color:white;'>
                    {el['number']}
                </div>""", unsafe_allow_html=True)
        else:
            cols[group - 1].write(" ")

if st.session_state.selected_element:
    el = data[data['symbol'] == st.session_state.selected_element].iloc[0]
    st.markdown("""
        <div class="info-box">
            <h2>{name} ({symbol})</h2>
            <p><strong>원자번호:</strong> {number}</p>
            <p><strong>원자 질량:</strong> {atomic_mass}</p>
            <p><strong>카테고리:</strong> {category}</p>
            <p><strong>전자배열:</strong> {electron_configuration}</p>
            <p><strong>요약:</strong> {summary}</p>
        </div>
    """.format(
        name=el['name'],
        symbol=el['symbol'],
        number=el['number'],
        atomic_mass=el['atomic_mass'],
        category=el['category'],
        electron_configuration=el['electron_configuration'],
        summary=el['summary']), unsafe_allow_html=True)
else:
    st.info("원소를 클릭하면 상세 정보를 확인할 수 있습니다 🔎")
