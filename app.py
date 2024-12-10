import streamlit as st
import pandas as pd
import random

# Load the Pokémon data
@st.cache
def load_data():
    data = pd.read_csv('pokemon_stats.csv')
    return data

pokemon_data = load_data()

# App Title
st.title("Pokémon Battle Simulator")

# Sidebar for Pokémon selection
st.sidebar.header("Select Pokémon")
pokemon1_name = st.sidebar.selectbox("Choose your Pokémon:", pokemon_data['Name'])
pokemon2_name = st.sidebar.selectbox("Choose opponent Pokémon:", pokemon_data['Name'])

# Display selected Pokémon details
pokemon1 = pokemon_data[pokemon_data['Name'] == pokemon1_name].iloc[0]
pokemon2 = pokemon_data[pokemon_data['Name'] == pokemon2_name].iloc[0]

st.subheader("Pokémon Stats")
col1, col2 = st.columns(2)

with col1:
    st.image(pokemon1['Image URL'], caption=pokemon1['Name'])
    st.write(f"Type: {pokemon1['Type']}")
    st.write(f"HP: {pokemon1['HP']}, Attack: {pokemon1['Attack']}, Defense: {pokemon1['Defense']}")
    st.write(f"Sp. Atk: {pokemon1['Sp. Atk']}, Sp. Def: {pokemon1['Sp. Def']}, Speed: {pokemon1['Speed']}")

with col2:
    st.image(pokemon2['Image URL'], caption=pokemon2['Name'])
    st.write(f"Type: {pokemon2['Type']}")
    st.write(f"HP: {pokemon2['HP']}, Attack: {pokemon2['Attack']}, Defense: {pokemon2['Defense']}")
    st.write(f"Sp. Atk: {pokemon2['Sp. Atk']}, Sp. Def: {pokemon2['Sp. Def']}, Speed: {pokemon2['Speed']}")

# Battle simulation
if st.button("Start Battle"):
    st.subheader("Battle Log")
    pokemon1_hp = pokemon1['HP']
    pokemon2_hp = pokemon2['HP']

    while pokemon1_hp > 0 and pokemon2_hp > 0:
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
            break
        elif pokemon2_hp <= 0:
            st.write(f"🏆 {pokemon1['Name']} wins!")
            break
            