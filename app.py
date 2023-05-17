import streamlit as st
import time
import joblib
import sklearn

st.title("Zomato Bangalore Restaurants")
st.write("This is a web app to predict if a restaurant is recommended / successful or not")

approx_cost = st.number_input("Approx Cost (for two people)",0,100000,step=1)
votes = st.number_input("Votes",0,1000000,step=1)
online_order = st.radio("Does it support online order?",["Yes","No"])
book_table = st.radio("Does it support table reservation?",["Yes","No"])
listed_in_type = st.selectbox("What is the type of meal?",["Cafes","Delivery","Desserts","Dine-out","Drinks & nightlife","Pubs and bars","Buffet"])
listed_in_city = st.selectbox("What is the neighborhood in which the restaurant is listed?",["Banashankari","Bannerghatta Road","Basavanagudi","Bellandur","Brigade Road","Brookefield","Church Street","Electronic City","Frazer Town","HSR","Indiranagar","JP Nagar","Jayanagar","Kalyan Nagar","Kammanahalli","Koramangala 4th Block","Koramangala 5th Block","Koramangala 6th Block","Koramangala 7th Block","Lavelle Road","MG Road","Malleshwaram","Marathahalli","New BEL Road","Old Airport Road","Rajajinagar","Residency Road","Sarjapur Road","Whitefield","BTM"])

if (online_order == 'Yes'):
    online_order = 1
elif (online_order == 'No'):
    online_order = 0

if (book_table == 'Yes'):
    book_table = 1
elif (book_table == 'No'):
    book_table = 0

def get_listed_in_type(listed_in_type):
    if (listed_in_type == 'Cafes'):
        return [1, 0, 0, 0, 0, 0]
    elif (listed_in_type == 'Delivery'):
        return [0, 1, 0, 0, 0, 0]
    elif (listed_in_type == 'Desserts'):
        return [0, 0, 1, 0, 0, 0]
    elif (listed_in_type == 'Dine-out'):
        return [0, 0, 0, 1, 0, 0]
    elif (listed_in_type == 'Drinks & nightlife'):
        return [0, 0, 0, 0, 1, 0]
    elif (listed_in_type == 'Pubs and bars'):
        return [0, 0, 0, 0, 0, 1]
    elif (listed_in_type == 'Buffet'):
        return [0, 0, 0, 0, 0, 0]

def get_listed_in_city(listed_in_city):
    if (listed_in_city == 'Banashankari'):
        return [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Bannerghatta Road'):
        return [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Basavanagudi'):
        return [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Bellandur'):
        return [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Brigade Road'):
        return [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Brookefield'):
        return [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Church Street'):
        return [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Electronic City'):
        return [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Frazer Town'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'HSR'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Indiranagar'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'JP Nagar'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Jayanagar'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Kalyan Nagar'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Kammanahalli'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Koramangala 4th Block'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Koramangala 5th Block'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Koramangala 6th Block'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Koramangala 7th Block'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Lavelle Road'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'MG Road'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Malleshwaram'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Marathahalli'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'New BEL Road'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    elif (listed_in_city == 'Old Airport Road'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    elif (listed_in_city == 'Rajajinagar'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    elif (listed_in_city == 'Residency Road'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    elif (listed_in_city == 'Sarjapur Road'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    elif (listed_in_city == 'Whitefield'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    elif (listed_in_city == 'BTM'):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

row_data = [approx_cost, votes, online_order, book_table]
row_data.extend(get_listed_in_type(listed_in_type))
row_data.extend(get_listed_in_city(listed_in_city))

model = joblib.load("model.h5")
scaler = joblib.load("scaler.h5")

if st.button("Predict"):
    prediction = model.predict(scaler.transform([row_data]))
    if prediction == 0:
        with st.spinner('Wait for it...'):
            time.sleep(1)
        st.write("This restaurant is not good for you!")
        st.success('Done!')
    else:
        with st.spinner('Wait for it...'):
            time.sleep(1)
        st.write("This restaurant is good for you!")
        st.success('Done!')