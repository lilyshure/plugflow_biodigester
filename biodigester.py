import streamlit as st
import numpy as np

# Define translation dictionary
translations = {
    "en": {
        "title": "Plug-Flow Biodigester Production Calculator",
        "inputs_section": "Calculating Daily Inputs",
        "feedstock_type": "Feedstock Type",
        "daily_input_food": "Daily Food Waste (kg)",
        "daily_input_agriculture": "Daily Input Mass of Agricultural Residue",
        "type_cow": "Type of Cow",
        "cow_options": {
            "Dairy Cow": "Dairy Cow",
            "Beef Cow": "Beef Cow",
            
        },
        "number_dairy": "Number of Dairy Cows",
        "number_beef": "Number of Beef Cows",
        "number_pigs": "Number of Pigs",
        "pigs_mass": "Average Mass of Pigs",
        "chicken_options": {
            "Layer": "Layer",
            "Broiler": "Broiler",
            
        },
        "type_chicken": "Type of Chicken",
        "number_broilers": "Number of Boilers",
        "number_layers": "Number of Layers",
        "daily_input": "Estimated Daily Input",
        "water_input": "Daily Water Input (m³)",
        "biodigester_conditions": "Biodigester Conditions",
        "temperature": "Temperature (°C)",
        "volume": "Volume of Biodigester (m³)",
        "water_error": "Water input should not equal 0.",
        "temperature_error": "Temperature is out of range.",
        "retention_error": "Retention Time is out of range.",
        "results": "Results",
        "retention_time": "Estimated Hydraulic Retention Time",
        "days": "days",
        "biogas_production": "Daily Biogas Production",
        "methane_production": "Daily Methane Production",
        "energy_potential": "Daily Energy Potential",
        "references": "References",
        "kg_day": "kg/day",
        "m3_day": "m³/day",
        "MJ": "MJ",
        "feedstock_options": {
            "Cow Manure": "Cow Manure",
            "Pig Manure": "Pig Manure",
            "Chicken Manure": "Chicken Manure",
            "Food Waste": "Food Waste",
            "Agricultural Residue": "Agricultural Residue"
        },
    },
    "es": {
        "title": "Calculadora de Producción de Biodigestor de Flujo Pistón",
        "inputs_section": "Cálculo de Entradas Diarias",
        "feedstock_type": "Tipo de Materia Prima",
        "daily_input_food": "Desperdicio de Comida Diario (kg)",
        "daily_input_agriculture": "Masa de Entrada Diaria de Residuos Agrícolas",
        "type_cow": "Tipo de Vaca",
        "cow_options": {
            "Dairy Cow": "Vaca Lechera",
            "Beef Cow": "Vaca de Carne",
            
        },
        "number_dairy": "Número de Vacas Lecheras",
        "number_beef": "Número de Vacas de Carne", 
        "number_pigs": "Número de Cerdos",
        "pigs_mass": "Masa Promedio de Cerdos",
        "chicken_options": {
            "Layer": "Gallina Ponedora",
            "Broiler": "Pollo de Engorde",
            
        },
        "number_broilers": "Número de Pollos de Engorde",
        "number_layers": "Número de Gallinas Ponedoras",
        "type_chicken": "Tipo de Gallina",
        "daily_input": "Estimación de la Entrada Diaria",
        "water_input": "Entrada Diaria de Agua (m³)",
        "biodigester_conditions": "Condiciones del Biodigestor",
        "temperature": "Temperatura (°C)",
        "volume": "Volumen del Biodigestor (m³)",
        "water_error": "La entrada diaria de agua no debe ser igual a 0.",
        "temperature_error": "La temperatura está fuera del rango.",
        "retention_error": "El tiempo de retención está fuera del rango.",
        "results": "Resultados",
        "retention_time": "Tiempo de Retención Hidráulico Estimado",
        "days": "días",
        "biogas_production": "Producción Diaria de Biogás",
        "methane_production": "Producción Diaria de Metano",
        "energy_potential": "Potencial Energético Diario",
        "references": "Referencias",
        "kg_day": "kg/día",
        "m3_day": "m³/día",
        "MJ": "MJ",
        "feedstock_options": {
            "Cow Manure": "Estiércol de Vaca",
            "Pig Manure": "Estiércol de Cerdo",
            "Chicken Manure": "Estiércol de Pollo",
            "Food Waste": "Residuos de Comida",
            "Agricultural Residue": "Residuos Agrícolas"
        },
    }
}

# Language selection
language = st.sidebar.selectbox("Select Language / Seleccione el Idioma", ["English", "Español"])
lang_code = "en" if language == "English" else "es"

st.title(translations[lang_code]["title"])

# Measuring Inputs of Biodigester
st.header(translations[lang_code]["inputs_section"])

inputs=0 #keep track of waste
VS=0 #keep track of volatile solids

#From plant waste
feedstock_options_dict = {
    "Cow Manure": translations[lang_code]["feedstock_options"]["Cow Manure"],
    "Pig Manure": translations[lang_code]["feedstock_options"]["Pig Manure"],
    "Chicken Manure": translations[lang_code]["feedstock_options"]["Chicken Manure"],
    "Food Waste": translations[lang_code]["feedstock_options"]["Food Waste"],
    "Agricultural Residue": translations[lang_code]["feedstock_options"]["Agricultural Residue"],
}

feedstock_options = st.multiselect(
    translations[lang_code]["feedstock_type"], 
    list(feedstock_options_dict.values())  # Show translated values
)

# Convert selected translated options back to English for internal logic
selected_feedstock_original = [key for key, value in feedstock_options_dict.items() if value in feedstock_options]

if "Food Waste" in selected_feedstock_original:
    waste_input = st.number_input(
    translations[lang_code]["daily_input_food"], 
    min_value=0.0
)
    inputs+=waste_input
    VS+=0.08*waste_input

if "Agricultural Residue" in selected_feedstock_original:
    residue_input = st.number_input(
    translations[lang_code]["daily_input_agriculture"], 
    min_value=0.0
)
    inputs+=residue_input
    VS+=0.26*residue_input



#From Animal Waste
if "Cow Manure" in selected_feedstock_original:
    cow_options_dict = {
        "Dairy Cow": translations[lang_code]["cow_options"]["Dairy Cow"],
        "Beef Cow": translations[lang_code]["cow_options"]["Beef Cow"],
    }

    cow_options = st.multiselect(
        translations[lang_code]["type_cow"], 
        list(cow_options_dict.values())
    )

    selected_cow_original = [
        key for key, value in cow_options_dict.items() if value in cow_options
    ]

    if "Dairy Cow" in selected_cow_original:
        cows_dairy = st.number_input(
    translations[lang_code]["number_dairy"], 
    min_value=0,step=1
)
        inputs += cows_dairy*36*231/453
        VS+=1.42*cows_dairy
    if "Beef Cow" in selected_cow_original:
        cows_beef = st.number_input(
    translations[lang_code]["number_beef"], 
    min_value=0,step=1
)
        inputs += cows_beef*27*231/453
        VS+=1.42*cows_beef

if "Pig Manure" in selected_feedstock_original:
    pigs = st.number_input(
    translations[lang_code]["number_pigs"], 
    min_value=0,step=1
)
    pigs_mass=st.number_input(
    translations[lang_code]["pigs_mass"], 
    min_value=0
)
    inputs+=pigs*pigs_mass*33/453
    VS+=1*pigs

if "Chicken Manure" in selected_feedstock_original:
    chicken_options_dict = {
        "Layer": translations[lang_code]["chicken_options"]["Layer"],
        "Broiler": translations[lang_code]["chicken_options"]["Broiler"],
    }

    chicken_options = st.multiselect(
        translations[lang_code]["type_chicken"], 
        list(chicken_options_dict.values())
    )

    selected_chicken_original = [
        key for key, value in chicken_options_dict.items() if value in chicken_options
    ]
    if "Broiler" in selected_chicken_original:
        chickens_broiler = st.number_input(
        translations[lang_code]["number_broilers"], 
        min_value=0,step=1
    )
        inputs += chickens_broiler*36*3/453
        VS+=0.0277*chickens_broiler
    if "Layer" in selected_chicken_original:
        chickens_layer = st.number_input(
        translations[lang_code]["number_layers"], 
        min_value=0,step=1
    )
        inputs += chickens_layer*27*2/453
        VS+=0.0277*chickens_layer


#Return the amount of daily inputs
st.write(f'{translations[lang_code]["daily_input"]}: {round(inputs, 2)} {translations[lang_code]["kg_day"]}')


water_input = st.number_input(
    f'{translations[lang_code]["water_input"]}', 
    min_value=0.0
)

#Biodigester Conditions
st.header("Biodigester Conditions")

temp = st.number_input(
    translations[lang_code]["temperature"], 
    min_value=0.0
)
volume = st.number_input(
    translations[lang_code]["volume"], 
    min_value=0.0
)

#Biogas Calculations
#Calculate Y
if water_input!=0:  
    retention_time=volume/(water_input+inputs*0.001)
else:
    retention_time=0
# Define the biogas production values as a dictionary
biogas_data = {
    (16, 18): [5.41, 4.73, 4.21, 3.79, 3.44, 3.16, 2.91, 2.71, 2.53, 2.37, 2.23, 2.10, 1.99, 1.89, 1.80, 1.72, 1.65, 1.58, 1.52],
    (19, 21): [7.98, 6.79, 5.90, 5.22, 4.69, 4.25, 3.88, 3.58, 3.32, 3.09, 2.89, 2.72, 2.57, 2.43, 2.30, 2.19, 2.09, 2.00, 1.92],
    (22, 24): [10.83, 8.99, 7.68, 6.70, 5.95, 5.35, 4.86, 4.45, 4.10, 3.81, 3.55, 3.33, 3.13, 2.95, 2.80, 2.66, 2.53, 2.41, 2.31],
    (25, 27): [13.59, 11.09, 9.37, 8.11, 7.15, 6.39, 5.78, 5.27, 4.85, 4.49, 4.18, 3.91, 3.67, 3.46, 3.27, 3.10, 2.95, 2.81, 2.69],
    (28, 30): [15.91, 12.88, 10.82, 9.33, 8.20, 7.32, 6.60, 6.02, 5.53, 5.11, 4.75, 4.44, 4.17, 3.93, 3.71, 3.52, 3.34, 3.19, 3.04],
    (31, 33): [18.33, 14.74, 12.32, 10.59, 9.28, 8.26, 7.44, 6.77, 6.21, 5.74, 5.33, 4.98, 4.67, 4.40, 4.15, 3.94, 3.74, 3.56, 3.40],
}

# Define retention time ranges
retention_time_ranges = list(range(6, 101, 5))

def get_biogas_production(temp, retention_time):
    # Find the correct temperature range
    temp_range = next((key for key in biogas_data.keys() if key[0] <= temp <= key[1]), None)
    if temp_range is None:
        raise ValueError("Temperature out of range")

    # Find the correct retention time index
    retention_index = next((i for i, v in enumerate(retention_time_ranges) if v <= retention_time < v + 5), None)
    if retention_index is None:
        raise ValueError("Retention time out of range")

    # Assign the corresponding value
    return biogas_data[temp_range][retention_index]

# Example usage
if water_input!=0 and 16<=temp<=33 and 6<=retention_time<=101:
    y = get_biogas_production(temp, retention_time)
if water_input==0:
    st.write(f'{translations[lang_code]["water_error"]}')
    y=0
if temp<16 or temp>33:
    st.write(f'{translations[lang_code]["temperature_error"]}')
    y=0
if retention_time<6 or retention_time>101:
    st.write(f'{translations[lang_code]["retention_error"]}')
    y=0


    
    


# Calculate S
feedstock_input=water_input+inputs*0.001
if feedstock_input !=0:
    s=VS/feedstock_input
else:
    s=0

#Calculate Biogas Production
    
if y!=0 and s!=0 and volume!=0:
    G = y * s * volume / 1000
else:
    G=0

# Methane fraction estimation using 65%
methane=0.65*G

#Energy Production
E=methane*34


# Display results
st.header(f'{translations[lang_code]["results"]}')
st.write(f'{translations[lang_code]["retention_time"]}: {round(retention_time, 2)} {translations[lang_code]["days"]}')
st.write(f'{translations[lang_code]["biogas_production"]}: {round(G, 2)} m³')
st.write(f'{translations[lang_code]["methane_production"]}: {round(methane, 2)} m³')
st.write(f'{translations[lang_code]["energy_potential"]}: {round(E, 2)} MJ')



#Works Cited 

st.header(f'{translations[lang_code]["references"]}')
'''1. **Chastain, John, et al.** *Swine Manure Production and Nutrient Content.* Jan. 2003. [Link](https://www.clemson.edu/extension/agronomy/Manure-Nutrient-Content.pdf)

2. **Elsayed, Samah.** *Measuring Small-Scale Biogas Capacity and Production.* International Renewable Energy Agency. https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2016/IRENA_Statistics_Measuring_small-scale_biogas_2016.pdf

3. **ISA Brown - ISA.** ISA, 2025. [Link](https://www.isa-poultry.com/en/product/isa-brown/?utm_source=chatgpt.com) 

4. **National Chicken Council | U.S. Broiler Performance.** National Chicken Council, 15 Feb. 2022. [Link](https://www.nationalchickencouncil.org/about-the-industry/statistics/u-s-broiler-performance/?utm_source=chatgpt.com) 

5. **Tańczuk, Mariusz, et al.** "Assessment of the Energy Potential of Chicken Manure in Poland." *Energies*, vol. 12, no. 7, 1 Apr. 2019, p. 1244. [Link](https://doi.org/10.3390/en12071244)
            
6. **University, Utah State.** "How Much Manure Does Livestock Produce?" *Utah State University Extension*. [Link](https://extension.usu.edu/agwastemanagement/manure-management/how-much-manure).'''


st.markdown("#### For the full list of calculations behind these estimates, click [here](https://docs.google.com/document/d/1QA3a9SXzwhQ8iy3iP71Rz3ZJpS6_sW8mncNtXUSj1kY/edit?usp=sharing).")
