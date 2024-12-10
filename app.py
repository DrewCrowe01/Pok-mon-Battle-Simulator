import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from io import BytesIO
import requests
import numpy as np

# Load the Pokémon data with updated caching
@st.cache_data
def load_data():
    data = pd.read_csv('pokemon_stats.csv')
    return data

pokemon_data = load_data()

# Apply custom CSS for Pokémon font
def set_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        .pokemon-title {
            font-family: 'Press Start 2P', cursive;
            font-size: 2.5em;
            color: #ffcb05;
            text-shadow: 2px 2px 4px #2a75bb;
            text-align: center;
        }

        .stat-box {
            padding: 10px;
            margin: 10px 0;
            border: 2px solid;
            border-radius: 8px;
            text-align: left;
            font-weight: bold;
            font-size: 14px;
        }

        .stat-box img {
            vertical-align: middle;
            margin-right: 8px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

set_custom_css()

# Add the Pokémon-themed title
st.markdown('<div class="pokemon-title">Pokémon Battle Simulator</div>', unsafe_allow_html=True)

# Sidebar for Pokémon selection
st.sidebar.header("Select Pokémon")
pokemon1_name = st.sidebar.selectbox("Choose your Pokémon:", pokemon_data['Name'])
pokemon2_name = st.sidebar.selectbox("Choose opponent Pokémon:", pokemon_data['Name'])

# Display selected Pokémon details
pokemon1 = pokemon_data[pokemon_data['Name'] == pokemon1_name].iloc[0]
pokemon2 = pokemon_data[pokemon_data['Name'] == pokemon2_name].iloc[0]

# Pokémon-type-specific colors
type_colors = {
    "Fire": "#F08030", "Water": "#6890F0", "Grass": "#78C850",
    "Electric": "#F8D030", "Ice": "#98D8D8", "Fighting": "#C03028",
    "Poison": "#A040A0", "Ground": "#E0C068", "Flying": "#A890F0",
    "Psychic": "#F85888", "Bug": "#A8B820", "Rock": "#B8A038",
    "Ghost": "#705898", "Dragon": "#7038F8", "Dark": "#705848",
    "Steel": "#B8B8D0", "Fairy": "#EE99AC", "Normal": "#A8A878"
}

# Function to fetch Pokémon image
def get_pokemon_image(url):
    response = requests.get(url)
    return plt.imread(BytesIO(response.content))

# Function to plot radar chart
def plot_radar_chart(pokemon, ax):
    stats = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    values = [pokemon[stat] for stat in stats]
    values += values[:1]  # Close the radar chart

    angles = np.linspace(0, 2 * np.pi, len(stats), endpoint=False).tolist()
    angles += angles[:1]

    # Get Pokémon's type color
    primary_type = pokemon['Type'].split(",")[0].strip()
    color = type_colors.get(primary_type, "gray")

    # Plot data
    ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
    ax.fill(angles, values, color=color, alpha=0.25)

    # Add labels
    ax.set_yticks([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(stats, fontsize=12, color=color)

    # Add Pokémon image
    img = get_pokemon_image(pokemon['Image URL'])
    imagebox = OffsetImage(img, zoom=0.35)
    ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False, xycoords='axes fraction')
    ax.add_artist(ab)

    # Set title
    ax.set_title(pokemon['Name'], size=16, weight='bold', color=color, position=(0.5, 1.1))

# Win Tracker: Initialize or update win counts
if "win_counts" not in st.session_state:
    st.session_state.win_counts = {}

def update_win_counts(winner):
    if winner not in st.session_state.win_counts:
        st.session_state.win_counts[winner] = 0
    st.session_state.win_counts[winner] += 1

# Themed stats display function
def display_pokemon_stats(pokemon, color):
    st.markdown(
        f"""
        <div class="stat-box" style="border-color:{color}; color: {color};">
            HP: {pokemon['HP']}<br>
            <img src="https://img.icons8.com/color/48/000000/sword.png"/> Attack: {pokemon['Attack']}<br>
            <img src="https://img.icons8.com/color/48/000000/shield.png"/> Defense: {pokemon['Defense']}<br>
            <img src="https://img.icons8.com/color/48/000000/fire-element.png"/> Sp. Atk: {pokemon['Sp. Atk']}<br>
            <img src="https://img.icons8.com/color/48/000000/water-element.png"/> Sp. Def: {pokemon['Sp. Def']}<br>
            <img src="https://img.icons8.com/color/48/000000/speed.png"/> Speed: {pokemon['Speed']}
        </div>
        """,
        unsafe_allow_html=True,
    )

# Display Pokémon stats as radar charts
col1, col2 = st.columns(2)

# Radar Chart and Stats for Pokémon 1
with col1:
    st.image(pokemon1['Image URL'], caption=pokemon1['Name'])
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    plot_radar_chart(pokemon1, ax)
    st.pyplot(fig)

    # Display stats below the radar chart
    primary_type_color1 = type_colors.get(pokemon1['Type'].split(",")[0].strip(), "gray")
    display_pokemon_stats(pokemon1, primary_type_color1)

# Radar Chart and Stats for Pokémon 2
with col2:
    st.image(pokemon2['Image URL'], caption=pokemon2['Name'])
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    plot_radar_chart(pokemon2, ax)
    st.pyplot(fig)

    # Display stats below the radar chart
    primary_type_color2 = type_colors.get(pokemon2['Type'].split(",")[0].strip(), "gray")
    display_pokemon_stats(pokemon2, primary_type_color2)

# Function to display health bar
def health_bar(current_hp, max_hp):
    percentage = current_hp / max_hp
    bar = f"{'█' * int(percentage * 20):<20}"  # Scales to 20 characters
    return f"{bar} {current_hp}/{max_hp} HP"

# Battle simulation
if st.button("Start Battle"):
    st.subheader("Battle Log")
    pokemon1_hp = pokemon1['HP']
    pokemon2_hp = pokemon2['HP']
    max_pokemon1_hp = pokemon1['HP']
    max_pokemon2_hp = pokemon2['HP']

    while pokemon1_hp > 0 and pokemon2_hp > 0:
        # Display health bars
        st.write(f"{pokemon1['Name']} HP: {health_bar(pokemon1_hp, max_pokemon1_hp)}")
        st.write(f"{pokemon2['Name']} HP: {health_bar(pokemon2_hp, max_pokemon2_hp)}")

        # Determine turn order based on Speed
        if pokemon1['Speed'] >= pokemon2['Speed']:
            attacker, defender = pokemon1, pokemon2
            attacker_hp, defender_hp = pokemon1_hp, pokemon2_hp
        else:
            attacker, defender = pokemon2, pokemon1
            attacker_hp, defender_hp = pokemon2_hp, pokemon1_hp

        # Calculate damage
        damage = max(1, attacker['Attack'] - defender['Defense'])
        defender_hp -= damage

        # Log the attack
        st.write(f"{attacker['Name']} attacks {defender['Name']} for {damage} damage!")
        st.write(f"{defender['Name']} has {max(0, defender_hp)} HP remaining.")

        # Update HP
        if attacker['Name'] == pokemon1['Name']:
            pokemon2_hp = defender_hp
        else:
            pokemon1_hp = defender_hp

        # Check for knockout
        if pokemon1_hp <= 0:
            st.write(f"🏆 {pokemon2['Name']} wins!")
            update_win_counts(pokemon2['Name'])
            break
        elif pokemon2_hp <= 0:
            st.write(f"🏆 {pokemon1['Name']} wins!")
            update_win_counts(pokemon1['Name'])
            break

# Display the win tracker
st.sidebar.header("Win Tracker")
if st.session_state.win_counts:
    for pokemon, wins in st.session_state.win_counts.items():
        st.sidebar.write(f"{pokemon}: {wins} wins")
