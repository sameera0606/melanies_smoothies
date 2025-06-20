# Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col
 
st.title('🥤 Customize Your Smoothie! :cup_with_straw:')
st.write("Choose the fruit you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)
 
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
 
ingredients_List = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe
    ,max_selections=5
)
 
if ingredients_List:
  
    ingredients_string = " ".join(ingredients_List)
 
    
    my_insert_stmt = (
        "insert into smoothies.public.orders(ingredients) "
        "values ('" + ingredients_string + "')"
    )
 
   
    st.write(my_insert_stmt)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '"""+name_on_order+ """')"""

    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit')
                                   
        
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
            
        st.success('Your Smoothie is ordered!', icon="✅")
