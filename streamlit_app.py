import streamlit as st
import pandas as pd
import requests
import snowflake.connector 
from urllib.error import URLError

st.title("Healthy Diner")

st.header("Breakfast Menu")

st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

st.dataframe(fruits_to_show)

def fruit_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
   fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

st.header("Fruity vice fruit advice")
try: 
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("Please select a fruit to get informantion")
  else:
    func_data = fruit_data(fruit_choice)
    st.dataframe(func_data)
   
except URLError as e:
 st.error()
st.header("Fruit load list")
def get_fruit_load():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * from fruit_load_list")
      return my_cur.fetchall()

if st.button("Get fruit load list "):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   
   my_data_rows =  get_fruit_load()
   st.dataframe(my_data_rows)

def insert_row_snowflake(nfruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values ('from streamlit')")
      return "Thanks for adding " + nfruit
      

add_user_choice = st.text_input('What fruit would you like to add?')
if st.button("Add a fruit to list"):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   bck_from_connector = insert_row_snowflake(add_user_choice)
   st.text(bck_from_connector)

