import streamlit as st 
import pandas as pd
import os
import random

# === CSS STYLE (fond noir + sidebar gris) ===
st.markdown("""
    <style>
    /* Backgrounds */
    body, .stApp, .block-container {
        background-color: #000000;
    }

    section[data-testid="stSidebar"] {
        background-color: #1c1c1c;
    }

    /* Text and headers */
    h1, h2, h3, h4, p, label, span {
        color: white !important;
    }

    /* Buttons */
    div.stButton > button:first-child {
        background-color: #1DB954 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
    }

    /* Inputs */
    input[type="text"], input[type="number"], textarea, select {
        border: 2px solid #1DB954 !important;
        border-radius: 5px !important;
        padding: 8px !important;
        color: white !important;
        background-color: #1a1a1a !important;
    }

    input:focus, textarea:focus, select:focus {
        border-color: #1DB954 !important;
        box-shadow: 0 0 10px #1DB954 !important;
    }

    /* Sliders */
    .stSlider > div > div > div {
        background: #1DB954 !important;
    }
    </style>
""", unsafe_allow_html=True)

# === FUNCTIONS ===
def random_color():
    return f"#{random.randint(0, 255):02X}{random.randint(0, 255):02X}{random.randint(0, 255):02X}"

def format_number(n):
    return " ".join(str(int(n))[::-1][i:i+3] for i in range(0, len(str(int(n))), 3))[::-1]

def display_artist_card(artist_name):
    result = enriched_df[enriched_df["name"].str.lower() == artist_name.lower()]
    if not result.empty:
        row = result.iloc[0]
        bg_color = random_color()
        listeners = format_number(row['followers'])
        genres = row['genres'].replace(',', ' | ') if pd.notna(row['genres']) else ""
        st.markdown(f"""
    <div style='
        border: 2px solid #1DB954; 
        border-radius: 10px; 
        padding: 10px; 
        text-align: center; 
        background-color: {random_color()}; 
        color: white; 
        width: 300px; 
        height: 480px;
        margin: 15px auto;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    '>
        <div>
            <a href='{row['spotify_url']}' target='_blank'>
                <img src='{row['pictureURL']}' width='180' height='180' style='border-radius: 15px; object-fit: cover; margin-bottom: 10px;'>
            </a>
            <h1 style='font-size: 20px; margin: 5px 0;'>{row['name']}</h1>
            <p style='font-size: 16px; font-weight: bold; margin: 5px 0; line-height: 1.2;'>{genres}</p>
        </div>
        <div>
            <p style='font-size: 13px; margin: 5px 0;'><b>Monthly Listeners:</b> {listeners}</p>
            <a href='{row['spotify_url']}' target='_blank' style='color: #1DB954; text-decoration: none; font-weight: bold;'>View on Spotify</a>
            <br><br>
            <button style='
                background-color: white; 
                color: #1DB954; 
                font-weight: bold; 
                padding: 6px 12px; 
                border: none; 
                border-radius: 5px; 
                margin: 4px 4px;
                cursor: pointer;
            '>➕ Add to Playlist</button>
            <button style='
                background-color: #1DB954; 
                color: white; 
                font-weight: bold; 
                padding: 6px 12px; 
                border: none; 
                border-radius: 5px; 
                margin: 4px 4px;
                cursor: pointer;
            ' onclick="window.open('{row['spotify_url']}', '_blank')">🎧 Listen Preview</button>
        </div>
    </div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"❌ No enriched data found for: **{artist_name}**")

def display_artist_grid(artists_list, cols_per_row=2):
    for i in range(0, len(artists_list), cols_per_row):
        cols = st.columns(min(cols_per_row, len(artists_list[i:])))
        for j, artist in enumerate(artists_list[i:i+cols_per_row]):
            with cols[j]:
                display_artist_card(artist)

# === LOAD DATA ===
base_path = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_all_data():
    method_df = pd.read_csv(os.path.join(base_path, "Totaluserbased.csv"))
    artists_df = pd.read_csv(os.path.join(base_path, "artists_gp2.csv"))
    popularity_df = pd.read_csv(os.path.join(base_path, "best_artists_names.csv"))
    content_df = pd.read_csv(os.path.join(base_path, "user_recommended_artists_modified.csv"))
    clustered_df = pd.read_csv(os.path.join(base_path, "clustered_user_based_modified (1).csv"))
    enriched_df = pd.read_csv(os.path.join(base_path, "artistes_spotify.csv"))
    return method_df, artists_df, popularity_df, content_df, clustered_df, enriched_df

method_df, artists_df, popularity_df, content_df, clustered_df, enriched_df = load_all_data()

artists_df["id"] = artists_df["id"].astype(str)
method_df.index = method_df.index.astype(str)
clustered_df["userID"] = clustered_df["userID"].astype(str)

# === UI ===
st.markdown("""
<div style="display: flex; align-items: center; gap: 15px;">
    <a href="https://open.spotify.com" target="_blank">
        <img src="https://imgs.search.brave.com/FwvslqIfrJSkk_ce4dcoqQ-eCB4CoZ1iJQUytek5GFA/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly91cGxv/YWQud2lraW1lZGlh/Lm9yZy93aWtpcGVk/aWEvY29tbW9ucy8x/LzE5L1Nwb3RpZnlf/bG9nb193aXRob3V0/X3RleHQuc3Zn" 
             width="45" 
             style="margin-bottom: 4px;" />
    </a>
    <h1 style="color: white;">Artist Recommender</h1>
</div>
""", unsafe_allow_html=True)

# Sidebar title with Spotify logo
st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 10px;">
    <img src="https://imgs.search.brave.com/FwvslqIfrJSkk_ce4dcoqQ-eCB4CoZ1iJQUytek5GFA/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly91cGxv/YWQud2lraW1lZGlh/Lm9yZy93aWtpcGVk/aWEvY29tbW9ucy8x/LzE5L1Nwb3RpZnlf/bG9nb193aXRob3V0/X3RleHQuc3Zn" 
         width="25" style="margin-bottom: 2px;" />
    <h3 style="margin: 0; color: white;">Navigation</h3>
</div>
<div style="height: 20px;"></div>
""", unsafe_allow_html=True)

# Espace entre sections
st.sidebar.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
menu_option = st.sidebar.selectbox("Choose a category:", ["Recommendation Methods", "Ultimate Spotify Recommender"], key="category_selector")
st.sidebar.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)  # Espace vertical

# CSS animation + intro
st.markdown("""
<style>
@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 1.2s ease-out;
}
</style>

<div class="fade-in" style="text-align: left; font-size: 18px; line-height: 1.6; color: white; max-width: 800px; margin: 0 auto;">
    <em>Experience a smarter way to discover music. Choose your favorite recommendation method, enter your Spotify-style username, and let us unveil artists that match your unique musical taste.</em>
</div>

<div style='height: 40px;'></div>
""", unsafe_allow_html=True)

if menu_option == "Recommendation Methods":
    sub_option = st.sidebar.radio("Select a method:", ["Popularity Based", "Content User Based", "Total User Based", "Cluster User Based"])

    if sub_option == "Popularity Based":
        st.header("🔥 Popularity-Based Recommendation")
        top_5_popular = popularity_df.nlargest(5, popularity_df.columns[0])
        top_artists_popular = top_5_popular[popularity_df.columns[2]].tolist()
        st.subheader("🔥 Recommended popular artists:")
        display_artist_grid(top_artists_popular)

    elif sub_option == "Content User Based":
        st.header("🧠 Content-Based Recommendation")
        username = st.text_input("Enter your username")
        if username and username in content_df["userID"].astype(str).values:
            user_recommendations = content_df[content_df["userID"].astype(str) == username]["recommended_artists"].head(5).tolist()
            user_recommendations = [artist.replace("'", "").strip("[]").split(', ') for artist in user_recommendations]
            user_recommendations = [item for sublist in user_recommendations for item in sublist]
            st.subheader("🎧 Your recommendations:")
            display_artist_grid(user_recommendations)

    elif sub_option == "Total User Based":
        st.header("🔍 User-Based Recommendation")
        username = st.text_input("Enter your username")
        if username and username in method_df["userID"].astype(str).values:
            top_ids = method_df[method_df["userID"].astype(str) == username][["1st", "2nd", "3rd", "4th", "5th"]].values.flatten()
            top_ids = [str(x) for x in top_ids]
            top_artists = artists_df[artists_df["id"].isin(top_ids)]["name"].tolist()
            st.subheader("🎧 Your recommendations:")
            display_artist_grid(top_artists)

    elif sub_option == "Cluster User Based":
        st.header("📊 Cluster-Based Recommendation")
        username = st.text_input("Enter your username")
        if username and username in clustered_df["userID"].astype(str).values:
            user_cluster = clustered_df[clustered_df["userID"].astype(str) == username][["1st", "2nd", "3rd", "4th", "5th"]].values.flatten()
            user_cluster = [str(x) for x in user_cluster]
            top_artists_cluster = artists_df[artists_df["id"].isin(user_cluster)]["name"].tolist()
            st.subheader("📊 Recommended artists via clustering:")
            display_artist_grid(top_artists_cluster)

elif menu_option == "Ultimate Spotify Recommender":
    st.header("🚀 Ultimate Spotify Recommender")
    username = st.text_input("Enter your username")
    if username:
        recommended_artists = set()
        if username in method_df.index:
            user_scores = method_df.loc[username]
            top_5 = user_scores.nlargest(5)
            artist_ids = top_5.index.astype(str).values
            top_artists = artists_df[artists_df["id"].isin(artist_ids)]["name"].tolist()
            recommended_artists.update(top_artists)
        if username in content_df["userID"].astype(str).values:
            user_recommendations = content_df[content_df["userID"].astype(str) == username]["recommended_artists"].head(5).tolist()
            user_recommendations = [artist.replace("'", "").strip("[]").split(', ') for artist in user_recommendations]
            user_recommendations = [item for sublist in user_recommendations for item in sublist]
            recommended_artists.update(user_recommendations)
        if username in clustered_df["userID"].astype(str).values:
            user_cluster = clustered_df[clustered_df["userID"].astype(str) == username][["1st", "2nd", "3rd", "4th", "5th"]].values.flatten()
            user_cluster = [str(x) for x in user_cluster]
            top_artists_cluster = artists_df[artists_df["id"].isin(user_cluster)]["name"].tolist()
            recommended_artists.update(top_artists_cluster)
        st.subheader("🎵 Final recommendations:")
        final_recommendations = list(recommended_artists)[:5]
        display_artist_grid(final_recommendations)