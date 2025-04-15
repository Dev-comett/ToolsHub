import streamlit as st
import requests
from streamlit_option_menu import option_menu
from bs4 import BeautifulSoup
import re
import streamlit.components.v1 as components
import streamlit as st
import os
# --- Config ---
st.set_page_config(page_title="ToolsHub", layout="wide", page_icon="😎")

TOMORROW_API_KEY = st.secrets["TOMORROW_API_KEY"]
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
SERP_API_KEY = st.secrets["SERP_API_KEY"]


TOMORROW_API_KEY = os.environ.get("TOMORROW_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
SERP_API_KEY = os.environ.get("SERP_API_KEY")


st.markdown("""
    <style>
    body, .stApp {
        background-color: #111;
        color: #f5f5f5;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stTextInput > div > div > input {
        background-color: #1f1f1f;
        color: #fff;
    }
    .stButton > button {
        background-color: #ff9900;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .stButton > button:hover {
        background-color: #e68a00;
    }
    h1, h2, h3 {
        color: #ff9900;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #222;
        color: #fff;
        border-radius: 8px 8px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff9900;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# --- Currency Conversion ---
def convert_usd_to_inr(usd_price):
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        rate = response.json()["rates"].get("INR")
        return round(float(usd_price.strip("$").replace(",", "")) * rate, 2)
    except:
        return None

# --- Sidebar Navigation ---
# --- Sidebar ---
with st.sidebar:
    st.markdown("""
        <style>
        /* Sidebar Background */
        [data-testid="stSidebar"] {
            background: linear-gradient(160deg, #1a1a1a 0%, #1f1f1f 100%);
            box-shadow: 4px 0 15px rgba(0,0,0,0.3);
            padding-top: 2rem;
        }

        /* Sidebar Title */
        .sidebar-title {
            font-size: 28px;
            font-weight: bold;
            color: #ff9900;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Sidebar Icons + Buttons */
        .st-emotion-cache-6qob1r {
            padding-left: 10px;
        }

        /* Sidebar Menu Item Styling */
        .st-emotion-cache-1n76uvr {
            border-radius: 10px;
            transition: background-color 0.3s ease;
        }

        .st-emotion-cache-1n76uvr:hover {
            background-color: #ff9900 !important;
            color: black !important;
        }

        /* Remove sidebar image spacing */
        .st-emotion-cache-1kyxreq img {
            margin: 0 auto 0.5rem;
            display: block;
        }
        </style>
    """, unsafe_allow_html=True)

    
    st.markdown("<div class='sidebar-title'>ToolsHub</div>", unsafe_allow_html=True)

    selected = option_menu(
    menu_title=None,
    options=["Home😴", "Web Scraper🔎", "More Tools🪄"],
    icons=["house-fill", "search", "wrench"],  # Removed watch icon; changed "tools" to "wrench" for better match
    default_index=0,
    orientation="vertical",
    styles={
        "container": {
            "padding": "0!important",
            "background-color": "transparent",
            "box-shadow": "inset 0 0 15px #00000080",
            "border-radius": "10px"
        },
        "icon": {
            "color": "#ff9900",
            "font-size": "20px",
        },
        "nav-link": {
            "color": "#e0e0e0",
            "font-size": "16px",
            "text-align": "left",
            "margin": "8px 0",
            "border-radius": "12px",
            "padding": "12px 16px",
            "transition": "0.3s",
        },
        "nav-link:hover": {
            "background-color": "#2e2e2e",
            "color": "#ff9900",
        },
        "nav-link-selected": {
            "background-color": "#ff9900",
            "color": "black",
            "font-weight": "bold",
            "box-shadow": "0 0 10px #ff9900",
        },
    }
)

# --- Home Page ---
# --- Home Page ---
if selected == "Home😴":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <div style='padding: 1rem; background-color: #1c1c1c; border-radius: 15px; text-align: center;'>
                <img src='banner.png' width='300' style='margin-bottom: 20px;' />
                <h2 style='color: #ff9900;'>Welcome to ToolsHub</h2>
                <p style='color:#ccc;'>Your all-in-one smart utility dashboard for web, docs & AI tools.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("🌡️ Weather")
        city = st.text_input("Enter city", "New York")
        if city:
            try:
                url = f"https://api.tomorrow.io/v4/weather/realtime?location={city}&apikey={TOMORROW_API_KEY}"
                data = requests.get(url).json()
                weather = data['data']['values']
                st.success(f"{city.title()}: {weather['temperature']}°C, Humidity: {weather['humidity']}%, Wind: {weather['windSpeed']} kph")
            except Exception as e:
                st.warning("Weather not available or error occurred.")

        st.subheader("📰 Top News")
        keyword = st.text_input("News category/keyword", "technology")
        if keyword:
            try:
                url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={NEWS_API_KEY}&language=en&sortBy=publishedAt&pageSize=5"
                news_data = requests.get(url).json()
                for article in news_data.get("articles", []):
                    st.markdown(f"**[{article['title']}]({article['url']})**")
                    st.caption(article.get("description", "No description available."))
            except Exception as e:
                st.warning("News API error.")

# --- Web Scraper ---
elif selected == "Web Scraper🔎":
    st.title("🔍 Web Scraper")
    tab1, tab2 = st.tabs(["Advance Scraper", "Live Website Scraper"])

    with tab1:
        st.subheader("Looking For Something?")
        query = st.text_input("Enter Search Query")
        if st.button("Scrape it 🔨") and query:
            try:
                url = f"https://serpapi.com/search.json?q={query}&engine=google&api_key={SERP_API_KEY}"
                search_res = requests.get(url).json()
                for item in search_res.get("organic_results", []):
                    st.markdown(f"**[{item.get('title', 'No Title')}]({item.get('link', '#')})**")
                    snippet = item.get("snippet", "")
                    st.caption(snippet)

                    match = re.search(r'\$\d+[,.]?\d*', snippet)
                    if match:
                        inr_price = convert_usd_to_inr(match.group())
                        st.info(f"💰 Price: ₹{inr_price} (from source)")
            except Exception as e:
                st.error(f"Search error: {e}")

    with tab2:
        st.subheader(" Want Something? Try Out Any URL!")
        raw_url = st.text_input("Enter URL", "example.com")
        if st.button("Scrape it 🔨 ") and raw_url:
            try:
                url = f"https://{raw_url}" if not raw_url.startswith("http") else raw_url
                headers = {'User-Agent': 'Mozilla/5.0'}
                soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
                st.markdown(f"Extracted from [{url}]({url}):")
                for i, para in enumerate(soup.find_all('p')[:10]):
                    text = para.get_text(strip=True)
                    if text:
                        st.markdown(f"**{i+1}.** {text}")
            except Exception as e:
                st.error(f"Scraping error: {e}")
# --- More Tools ---
elif selected == "More Tools🪄":
    st.title("More Tools")
    st.markdown("Explore our powerful, dedicated micro-apps below:")

    st.markdown("""
        <style>
        .tool-card {
            background-color: #1c1c1c;
            padding: 1.2rem;
            border-radius: 15px;
            margin-bottom: 1rem;
            transition: box-shadow 0.3s ease;
            border: 1px solid #333;
        }
        .tool-card:hover {
            box-shadow: 0 0 15px #ff9900;
        }
        .tool-title {
            font-size: 1.2rem;
            font-weight: bold;
            color: #ff9900;
            margin-bottom: 0.5rem;
        }
        .tool-desc {
            color: #ccc;
            margin-bottom: 1rem;
        }
        .tool-link {
            background-color: #ff9900;
            color: white;
            font-weight: bold;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            text-decoration: none;
        }
        .tool-link:hover {
            background-color: #e68a00;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

    tools_data = [
        {
            "title": "🖼️ Image Toolbox",
            "desc": "Convert, compress, and edit images on the fly with smart tools.",
            "url": "https://image-toolbox-mfvwj5zan5ekwjcue5ixva.streamlit.app/"
        },
        {
            "title": "🔗 URL Shortener & Tools",
            "desc": "Shorten long URLs and access link analytics with ease.",
            "url": "https://url-short-c7rz4j2gnzkbyswqxmbdcc.streamlit.app/"
        },
        {
            "title": "📈 Trend Analysis & Finance Tracker",
            "desc": "Track financial trends, stock movements, and perform quick analysis.",
            "url": "https://finance-trend-analyzer-3utxdfymwgpemuweapwvou.streamlit.app/"
        },
        {
            "title": "📄 Document Toolbox",
            "desc": "Convert, split, and merge PDFs or other documents seamlessly.",
            "url": "https://document-converter-xcj22b88qyoz9q3guavayv.streamlit.app/"
        },
        {
            "title": "🤖 AI Toolbox",
            "desc": "Utilize cutting-edge AI tools for summarization, chat, and more.",
            "url": "https://ai-tool-box-ufxmrwbbnykfwfscmmhnfa.streamlit.app/"
        },
    ]

    for tool in tools_data:
        st.markdown(f"""
        <div class="tool-card">
            <div class="tool-title">{tool['title']}</div>
            <div class="tool-desc">{tool['desc']}</div>
            <a href="{tool['url']}" target="_blank" class="tool-link">Open App 🚀</a>
        </div>
        """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<style>
footer {visibility: hidden;}
</style>
<hr style='border-color: #333;'>
<div style='text-align:center; padding:10px; color:#888'>
    Made with ❤️ by <strong style='color:#ff9900;'>Dev</strong> |
    <a style='color:#ff9900;' href='https://github.com/dev-comett'>GitHub</a> •
    <a style='color:#ff9900;' href='https://www.linkedin.com/in/dev-ice'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)
