# Pokémon Battle Simulator

## Reproducibility and Code
My web application brings the intense excitement of a Pokémon battle to life. It offers a fun, visually engaging, and data-driven experience, combining strategic gameplay with interactive visuals. Dive into the world of Pokémon as you simulate battles, analyze stats, and enjoy a dynamic platform that merges entertainment with insightful data analysis.

[View Pokémon Battle Simulator](https://drews-final-project.streamlit.app/) 

## Readme

### Introduction
The Pokémon Battle Simulator is an interactive, strategic tool designed to bring Pokémon battles to life using data-driven insights. This simulator allows users to compare and pit Pokémon against each other based on their key stats, such as HP, Attack, Defense, and more. By simulating turn-based battles, complete with speed-based move order and special attacks, the simulator provides an engaging and educational platform for Pokémon enthusiasts, competitive players, and data analysts.

### Problem to Solve
**Traditionally, Pokémon battle strategies require manual stat comparisons and theoretical planning, which can be time-consuming and cumbersome. The Pokémon Battle Simulator addresses these challenges by**:
- Automating the battle process based on Pokémon stats.
- Introducing speed-based move order and special attacks for strategic depth.
- Allowing users to visualize and analyze Pokémon stats dynamically during battles.
- Offering an interactive experience that bridges the gap between data analysis and gameplay.
- Without such a tool, enthusiasts must rely on static data sources and repetitive calculations, hindering strategic experimentation. The simulator simplifies this process and enhances understanding through real-time interaction and outcomes.

### Data/Operation Design
**Data Source**:
- Pokémon data is sourced from Pokémon Database, which was web-scraped using Python.
- Stats include HP, Attack, Defense, Speed, Sp. Attack, and Sp. Defense.
**Data Preparation**:
- The scraped data underwent cleaning and transformation for use in simulations.
- Calculated fields include damage values, special attack effects, and turn-based move order logic.
- Simulator Features:
**Speed-Based Move Order**:
- The Pokémon with the higher speed attacks first.
**Trun-Based Mechaics**:
- Pokémon alternate moves, with dynamic health updates displayed.
- The simulator dynamically displays the winner and updates a session-based win tracker.
**Interactive Health Bars**:
- Real-time health bars visualize the battle's progression.
  
**Custom Pokémon Selection**:

### Future Work
I am going to transform my Pokémon battle simulator by improving the experience with layers of realism, complexity, and strategic depth, making it not just a data visualization tool but a full-fledged Pokémon battle simulation platform. Enhancements will include team battles, realistic attack animations, and environment and type effects.
