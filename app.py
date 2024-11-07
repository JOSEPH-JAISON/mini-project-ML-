import math
import numpy as np
import pickle
import streamlit as st

#SET PAGE CONFIGURATION
st.set_page_config(page_title='IPL Score Predictor', layout="centered")

# Load the ML Model
filename = 'ml_model.pkl'
try:
    model = pickle.load(open(filename, 'rb'))
except FileNotFoundError:
    st.error("Model file not found. Please check the path to 'ml_model.pkl'.")

# Title of the page
st.markdown("<h1 style='text-align: center; color: white;'>IPL Score Predictor 2024</h1>", unsafe_allow_html=True)

# Description
with st.expander("Description"):
    st.info("""
        A Simple ML Model to predict IPL Scores between teams in an ongoing match. 
        For accuracy, predictions are only made if more than 5 overs have been played.
    """)

# Team Selection
batting_team = st.selectbox('Select the Batting Team', (
    'Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab',
    'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals',
    'Royal Challengers Bangalore', 'Sunrisers Hyderabad')
)
bowling_team = st.selectbox('Select the Bowling Team', (
    'Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab',
    'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals',
    'Royal Challengers Bangalore', 'Sunrisers Hyderabad')
)

# Ensure teams are different
if bowling_team == batting_team:
    st.error('Bowling and Batting teams should be different.')

# Encoding Team Names
team_encoding = {
    'Chennai Super Kings': [1, 0, 0, 0, 0, 0, 0, 0],
    'Delhi Daredevils': [0, 1, 0, 0, 0, 0, 0, 0],
    'Kings XI Punjab': [0, 0, 1, 0, 0, 0, 0, 0],
    'Kolkata Knight Riders': [0, 0, 0, 1, 0, 0, 0, 0],
    'Mumbai Indians': [0, 0, 0, 0, 1, 0, 0, 0],
    'Rajasthan Royals': [0, 0, 0, 0, 0, 1, 0, 0],
    'Royal Challengers Bangalore': [0, 0, 0, 0, 0, 0, 1, 0],
    'Sunrisers Hyderabad': [0, 0, 0, 0, 0, 0, 0, 1]
}
prediction_array = team_encoding[batting_team] + team_encoding[bowling_team]

# Overs and Runs Inputs with Validations
col1, col2 = st.columns(2)
with col1:
    overs = st.number_input(
        'Enter the Current Over (e.g., 5.0 to 19.5)',
        min_value=5.0, max_value=19.5, step=0.1
    )
    if overs % 1 > 0.5:
        st.error('Please enter a valid over input as one over contains only 6 balls.')

with col2:
    runs = st.number_input('Enter Current Runs', min_value=0, max_value=354, step=1)

# Wickets Fallen
wickets = st.slider('Enter Wickets fallen till now', 0, 9)

# Runs and Wickets in Last 5 Overs
col3, col4 = st.columns(2)
with col3:
    runs_in_prev_5 = st.number_input('Runs scored in the last 5 overs', min_value=0, max_value=runs, step=1)
with col4:
    wickets_in_prev_5 = st.number_input('Wickets taken in the last 5 overs', min_value=0, max_value=wickets, step=1)

# Prepare Prediction Array
prediction_array += [runs, wickets, overs, runs_in_prev_5, wickets_in_prev_5]
prediction_array = np.array([prediction_array])

# Predict Score
if st.button('Predict Score'):
    try:
        predict = model.predict(prediction_array)
        my_prediction = int(round(predict[0]))
        st.success(f'PREDICTED MATCH SCORE: {my_prediction - 5} to {my_prediction + 5}')
    except Exception as e:
        st.error(f"Error in prediction: {e}")
