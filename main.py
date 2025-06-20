import streamlit as st
import pandas as pd
import requests
from googletrans import Translator

st.set_page_config(page_title="원소 탐험대 (Periodic Table Explorer)", layout="wide")

# CSS 스타일
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
    return pd.json_normalize(r.json()['elements'])

data = load_data()
translator = Translator()

def translate_and_simplify(text):
    try:
        translated = translator.translate(text, src='en', dest='ko').text
        # 문장을 마침표 기준으로 나누고 첫 문장만 사용
        simple = translated.split('.')[0] + '.' if '.' in translated else translated
        return simple
    except:
        return "간단한 설명을 가져오지 못했습니다."

korean_names = {
    'H': '수소', 'He': '헬륨', 'Li': '리튬', 'Be': '베릴륨', 'B': '붕소',
    'C': '탄소', 'N': '질소', 'O': '산소', 'F': '플루오린', 'Ne': '네온',
    'Na': '나트륨', 'Mg': '마그네슘', 'Al': '알루미늄', 'Si': '규소', 'P': '인',
    'S': '황', 'Cl': '염소', 'Ar': '아르곤', 'K': '칼륨', 'Ca': '칼슘'
}

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

for period in range(1, 10):
    cols = st.columns(18)
    for group in range(1, 19):
        match = data[(data['xpos'] == group) & (data['ypos'] == period)]
        if not match.empty:
            el = match.iloc[0]
            color = category_colors.get(el['category'], '#95a5a6')
            btn_style = f"background-color:{color};"

            if cols[group - 1].button(el['symbol'], key=el['symbol']):
                st.session_state.selected_element = el['symbol']

            cols[group - 1].markdown(
                f"<div style='{btn_style} border-radius:6px; padding:4px; text-align:center; font-size:10px; color:white;'>"
                f"{el['number']}"
                "</div>",
                unsafe_allow_html=True
            )
        else:
            cols[group - 1].write(" ")

if st.session_state.selected_element:
    el = data[data['symbol'] == st.session_state.selected_element].iloc[0]
    symbol = el['symbol']
    name_kr = korean_names.get(symbol, el['name'])
    summary_kr = translate_and_simplify(el['summary'])

    st.markdown(f"""
        <div class="info-box">
            <h2>{name_kr} ({symbol})</h2>
            <p><strong>원자번호:</strong> {el['number']}</p>
            <p><strong>원자 질량:</strong> {el['atomic_mass']}</p>
            <p><strong>카테고리:</strong> {el['category']}</p>
            <p><strong>전자배열:</strong> {el['electron_configuration']}</p>
            <p><strong>간단한 설명 (한글):</strong> {summary_kr}</p>
        </div>
    """, unsafe_allow_h
