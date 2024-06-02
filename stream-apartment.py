import streamlit as st
import pandas as pd
import numpy as np
import pickle

#Configration Page
st.set_page_config("Customer Churn Prediction",page_icon=':information_desk_person:',layout='wide')
style = "<style>h2 {text-align: center};color=Red"
st.markdown(style,unsafe_allow_html=True)

if 'submited' not in st.session_state:
    st.session_state['submited'] = False
if 'predicted' not in st.session_state:
    st.session_state['predicted'] = False
def submit_button():
    st.session_state.submited = True
def cancel_button():
    st.session_state.submited = False
def predict_button():
    st.session_state['predicted'] = True
def reset_predict():
    st.session_state['predicted'] = False

#Function
def load_model():
    with open('Daegu_Apartment_XGB.sav','rb') as file:
        model = pickle.load(file)
    return model

def predict(data:pd.DataFrame):
    model = load_model()
    predict_price = model.predict(data)
    return predict_price

#Title and Note
st.title("Welcome to the Apartment Price Prediction App")
st.divider()

#Main Pages
#Membuat dua kolom
left_panel,right_panel = st.columns(2, gap='medium')
#Left Panel
left_panel.header('Information Panel')
#Membuat Tabs Overviews di left Panel
tabs1,tabs2,tabs3 = left_panel.tabs(['Overview','Analytic Approach','Model Summary'])
#Tabs1
tabs1.subheader('Overview')
tabs1.write("""
Apartment Price Prediction app helps businesss to calculate price of apartment that is located in Daegu, South Korea""")
tabs1.write("""
Why are Apartmen Price Apps So Important?

1. When we calculated manually about apartment price, it can spend a lot of time and accuracy of price can deviate greatly
2. This app will help to estimate cost of aparment rent fast based on the some features provided
""")
tabs1.write("""
What do Customer Churn Apps Do?

1. Track user behavior and engagement metrics to identify users who are disengaging.
2. Analyze user data to pinpoint potential causes of churn, like how long a customer has been with us and their contract type.
3. May enable targeted interventions to win back at-risk users, like personalized messages or exclusive offers.
""")
tabs1.write("""
Benefits of Customer Churn Apps

1. Determine the right price, which means the price is not too expensive and not too cheap
2. Efficiency of time
""")

#Tabs2
tabs2.subheader('Analytic Approach')
tabs2.write("""
So, what needs to be done to determine the right selling price for an apartment in the city of Daegu, South Korea is 
to carry out data analysis to explore and see patterns in the data and build a regression model as a method to test
whether there is an influence between various features and the selling price of the apartment. expressed in the form of a mathematical equation. 
The regression model formed can also predict the selling price of apartments and so can help new apartment owners to determine the selling price of apartments..
""")

#Tabs 3
tabs3.subheader("Model Summary")
tabs3.write("""
We used XGBoost Regressor because XGboost is the best model predicing data test with low error""")


#Right Panel
right_panel.header('Prediction')
right_panel.subheader('Information :')
placeholder = right_panel.empty()
input_container = placeholder.container()
right_panel.divider()
result_placeholder = right_panel.empty()
result_container = result_placeholder.container()
btn_placeholder = right_panel.empty()

left_input, right_input = input_container.columns(2)
#Left Feature
hallway_type = left_input.selectbox('Hallway Type', options=['terraced', 'mixed', 'corridor'])
time_to_subway = left_input.selectbox('Time to Subway', options=['0-5min', '5min-10min', '10min-15min', '15min-20min'])
subway_station = left_input.selectbox('Subway Station', options=['Kyungbuk-uni-hospital', 'Chil-sung-market', 'Bangoge', 'Sin-nam', 'Banwoldang', 'no_subway_nearby', 'Myung-duk', 'Daegu'])
num_facilities_nearby = left_input.number_input('Number of facilities nearby (ETC)', min_value=0, step=1)
num_facilites_nearby_publicoffice = left_input.number_input ('Number of facilites nearby (public office)', min_value=0, step=1)

#Right Feature
num_school_nearby = right_input.number_input('Number of School Nearby', min_value=0, step=1)
num_parkinglot = right_input.number_input('Number of Parking lot', min_value=0, step=1)
year_built = right_input.text_input('Year built')
num_facilities_apartment = right_input.number_input('Number of Facilities Apartment', min_value=0, step=1)
size = right_input.number_input('Size (sqf)', min_value=0)

data_list = {"Apartment Information":['Hallway Type', 'Time to Subway', 'Subway Station', 'Number of facilities nearby (ETC)', 'Number of facilites nearby (public office)',
                                        'Number of School Nearby', 'Number of Parking lot', 'Year built', 'Number of Facilities Apartment', 'Size (sqf)' ],
        "Value":[hallway_type, time_to_subway, subway_station, num_facilities_nearby, num_facilites_nearby_publicoffice, num_school_nearby, num_parkinglot, year_built, num_facilities_apartment, size]}

#Submit Button
btn_submit = btn_placeholder.button('Submit',use_container_width=True, on_click=submit_button)

if st.session_state['submited']:
    placeholder.dataframe(data_list, use_container_width=True)
    btn_after =  btn_placeholder.container()
    btn_predict = btn_after.button('Predict',use_container_width=True)
    btn_cancel = btn_after.button('Cancel',use_container_width=True,on_click=cancel_button)

    if btn_predict:
        data = {
        'HallwayType' : hallway_type,
        'TimeToSubway' : time_to_subway,
        'SubwayStation' : subway_station,
        'N_FacilitiesNearBy(ETC)' : num_facilities_nearby,
        'N_FacilitiesNearBy(PublicOffice)' : num_facilites_nearby_publicoffice,
        'N_SchoolNearBy(University)' : num_school_nearby,
        'N_Parkinglot(Basement)' : num_parkinglot,
        'YearBuilt' : year_built,
        'N_FacilitiesInApt' : num_facilities_apartment,
        'Size(sqf)' : size }
        data = pd.DataFrame(data, index=[1])
        prediction = predict(data)
        result_container.success(f'Predicted Price: ${prediction[0]:,.2f}')
        right_panel.balloons()
        btn_predict_again = btn_placeholder.button('Predict Again',use_container_width=True,on_click=cancel_button)
# if st.button('Predict Price'):
#     data = {
#     'HallwayType' : hallway_type,
#     'TimeToSubway' : time_to_subway,
#     'SubwayStation' : subway_station,
#     'N_FacilitiesNearBy(ETC)' : num_facilities_nearby,
#     'N_FacilitiesNearBy(PublicOffice)' : num_facilites_nearby_publicoffice,
#     'N_SchoolNearBy(University)' : num_school_nearby,
#     'N_Parkinglot(Basement)' : num_parkinglot,
#     'YearBuilt' : year_built,
#     'N_FacilitiesInApt' : num_facilities_apartment,
#     'Size(sqf)' : size }
#     data = pd.DataFrame(data, index=[1])
    
#     st.write(f'Predicted Price: ${prediction[0]:,.2f}')

#     btn_predict_again = btn_placeholder.button('Predict Again',use_container_width=True,on_click=cancel_button)
