import streamlit as st
import pandas as pd
import reverse_geocoder as rg
from geopy.geocoders import Nominatim
import country_converter as coco


st.write("""
# Anti-Podal Location Calculator
### By Aditya Kakarla
Anti-podal locations are places on opposite sides of the globe. Simply enter your location.
""")

# ORIGINAL
# latitude = st.number_input("""
# What's your latitude?
# """, min_value=-90, max_value=90)

# longitude = st.number_input("""
# What's your longitude?
# """, min_value=-180, max_value=180)

# NEW w/ geopy

geolocator = Nominatim(user_agent="MyApp")

city = st.text_input("""
Where do you live?
""")

if city != "":
    location = geolocator.geocode(city)
    latitude = location.latitude
    longitude = location.longitude
else:
    latitude = 0
    longitude = 0

# Rest of code that calculates anti-podal location

if longitude >= 0:
    metricDictionary = {'lat': [latitude, -latitude], 'lon': [longitude, -(180-longitude)]}
    newLatitude = -latitude
    newLongitude = -(180-longitude)
else:
    metricDictionary = {'lat': [latitude, -latitude], 'lon': [longitude, 180+longitude]}
    newLatitude = -latitude
    newLongitude = 180+longitude

map_data = pd.DataFrame(data=metricDictionary)

st.map(map_data)

newCity = geolocator.reverse((newLatitude, newLongitude))

if newCity:
    antipodalCountry = newCity.raw['address']['country']
    st.write("""
    Your antipodal country is 
    """ + coco.convert(names=antipodalCountry, to='name_short'))
else:
    newLocation = rg.search((newLatitude, newLongitude), mode=1)
    antipodalCountry = newLocation[0]['cc']

    territoryConversion = {'AX': 'FI', 'AS': 'US', 'AI': 'GB', 'AW': 'NL', 'BM': 'GB', 'BQ': 'NL',
                           'BV': 'NO', 'IO': 'GB', 'KY': 'GB', 'CX': 'AU', 'CC': 'AU', 'CK': 'NZ',
                           'CW': 'NL', 'FK': 'GB', 'FO': 'DK', 'GF': 'FR', 'PF': 'FR','TF': 'FR',
                           'GI': 'GB', 'gl': 'DK', 'GP': 'FR', 'GU': 'US', 'GG': 'GB', 'HM': 'AU',
                           'IM': 'GB', 'JE': 'GB', 'MO': 'CN', 'MQ': 'FR', 'YT': 'FR', 'MS': 'GB',
                           'NC': 'FR', 'NU': 'NZ', 'NF': 'AU', 'MP': 'US', 'PN': 'GB', 'PR': 'US',
                           'RE': 'FR', 'BL': 'FR', 'SH': 'GB', 'MF': 'FR', 'PM': 'FR', 'SX': 'NL',
                           'GS': 'GB', 'SJ': 'NO', 'TK': 'NZ', 'TC': 'GB', 'UM': 'US', 'VG': 'GB',
                           'VI': 'US', 'WF': 'FR'}

    if antipodalCountry in territoryConversion:
        st.write("""
        You landed in the ocean. The closest antipodal country is
        """ + coco.convert(names=territoryConversion[antipodalCountry], to='name_short')
        + """ ("""
        + coco.convert(names=antipodalCountry, to='name_short')
        + """)""")
    else:
        st.write("""
        You landed in the ocean. The closest antipodal country is 
        """ + coco.convert(names=antipodalCountry, to='name_short'))
