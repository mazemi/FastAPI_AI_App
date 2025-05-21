
COLUMNS = {
    "year": "Year in four digit",
    "month": "Name of the month",
    "period": "Round on data collection, 50 is round 50 and so on",
    "region": "Region name",
    "province": "Province name",
    "district": "District name",
    "wheat_unit_price": "Price of wheat per unit",
    "rice_unit_price": "Price of rice per unit",
    "pulses_lentils_unit_price": "Price of lentils per unit",
    "pulses_beans_unit_price": "Price of beans per unit",
    "pulses_split_peas_unit_price": "Price of split peas per unit",
    "veg_oil_unit_price": "Price of vegetable oil per unit",
    "sugar_unit_price": "Price of sugar per unit",
    "salt_unit_price": "Price of salt per unit",
    "cotton_cloth_unit_price": "Price of cotton cloth per unit",
    "toothbrush_adult_unit_price": "Price of adult toothbrush per unit",
    "toothpaste_unit_price": "Price of toothpaste per unit",
    "soap_unit_price": "Price of soap per unit",
    "sanitary_pad_unit_price": "Price of sanitary pad per unit",
    "pen_unit_price": "Price of pen per unit",
    "notebook_unit_price": "Price of notebook per unit",
    "safe_water_unit_price": "Price of safe drinking water per unit",
    "lpg_unit_price": "Price of LPG (cooking gas) per unit",
    "diesel_unit_price": "Price of diesel per unit",
    "petrol_unit_price": "Price of petrol per unit",
    "cooking_pot_unit_price": "Price of cooking pot per unit",
    "water_container_unit_price": "Price of water container per unit",
    "firewood_unit_price": "Price of firewood per unit",
    "coal_unit_price": "Price of coal per unit",
    "blanket_unit_price": "Price of blanket per unit",
    "winter_jacket_unit_price": "Price of winter jacket per unit",
    "partner": "Name of the data collection partner or organization",
    "method": "Method of data collection which is in_person or remotely",
    "items_available_marketplace_wheat": "Availability of wheat in the marketplace",
    "food_price_change": "Change in food prices which can be decrease, increase, stayed_same, dont_know",
    "buy_rate": "USD Currency exchange buy rate",
    "sell_rate": "USD Currency exchange sell rate"
}


def get_table_schema():
    schema_text = 'list of all valid column names in the survey table:\n'
    for col, desc in COLUMNS.items():
        schema_text += f"- {col}: {desc}\n"
    return schema_text

