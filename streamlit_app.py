# Import Python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
 
# Title for the app
st.title('🥤 Customize Your Smoothie! :cup_with_straw:')
st.write("Choose the fruit you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)
 
# Get Snowflake session and fruit data
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
 
# Show the multiselect dropdown
ingredients_List = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe
    ,max_selections=5
)
 
# If user selected any ingredients
if ingredients_List:
    # Create space-separated string of selected fruits
    ingredients_string = " ".join(ingredients_List)
 
    # Build insert statement with string wrapped in single quotes
    my_insert_stmt = (
        "insert into smoothies.public.orders(ingredients) "
        "values ('" + ingredients_string + "')"
    )
 
    # Show the final insert SQL
    st.write(my_insert_stmt)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """', '"""+name_on_order+ """')"""

    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit')
                                   
        
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
            
        st.success('Your Smoothie is ordered!', icon="✅")
