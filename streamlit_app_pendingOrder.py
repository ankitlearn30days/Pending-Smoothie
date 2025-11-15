# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f" :cup_with_straw: Pending Smoothie Order :cup_with_straw: ")
st.write("""Order that needs to be field""")


#name_on_order = st.text_input("Name Of the Smoothie : ")
#st.write("The Name of your Smoothie will be : ", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if my_dataframe:
    editable_df=st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted:
        
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        try:
            og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
            st.sucess("Order(s) Upadtes !" , icon = '👍')
        except:
            st.write("Something went wrong. ")
else:
    st.success("There is no pending order right now " , icon = '👍')
            
            
        
    

        
        

