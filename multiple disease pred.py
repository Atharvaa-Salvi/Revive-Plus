# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 08:55:43 2024

@author: Vikram Salvi
"""

import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import requests
from opencage.geocoder import OpenCageGeocode 

symptom_database = {
    "Flu": ["fever", "cough", "sore throat", "body aches"],
    "Cold": ["runny nose", "sneezing", "cough", "sore throat"],
    "Diabetes": ["increased thirst", "frequent urination", "fatigue"],
    "COVID-19": ["fever", "cough", "shortness of breath", "loss of taste"],
    "Migraine": ["headache", "nausea", "sensitivity to light"],
    "Allergy": ["sneezing", "itchy eyes", "runny nose"],
    "Gastroenteritis": ["diarrhea", "vomiting", "stomach pain"],
    "Asthma": ["shortness of breath", "wheezing", "coughing"],
    "Hypertension": ["headache", "shortness of breath", "nosebleeds"],
    "Heart Disease": ["chest pain", "shortness of breath", "nausea"],
    "Pneumonia": ["cough", "fever", "difficulty breathing"],
    "Appendicitis": ["abdominal pain", "nausea", "vomiting"],
    "Kidney Infection": ["pain in the back", "frequent urination", "fever"],
    "Thyroid Disorders": ["weight changes", "fatigue", "mood changes"],
    "Depression": ["sadness", "loss of interest", "fatigue"],
    "Anxiety": ["nervousness", "restlessness", "rapid heartbeat"],
    "Acid Reflux": ["heartburn", "regurgitation", "difficulty swallowing"],
    "Urinary Tract Infection": ["painful urination", "frequent urination"],
    "Arthritis": ["joint pain", "stiffness", "swelling"],
    "Osteoporosis": ["bone fractures", "back pain"],
    "Skin Problems": ["rash", "itching", "dry skin", "redness", "swelling"],
    "High Blood Sugar": ["increased thirst", "frequent urination", "blurred vision"],
    "Low Blood Sugar": ["shakiness", "sweating", "confusion"],
    "Jaundice": ["yellowing of skin", "yellowing of eyes", "dark urine"],
    "Cholera": ["severe diarrhea", "vomiting", "dehydration"],
}

# Medication database
medication_database = {
    "Flu": ["Paracetamol", "Ibuprofen", "Cough syrup"],
    "Cold": ["Antihistamines", "Decongestants"],
    "Diabetes": ["Metformin", "Insulin"],
    "COVID-19": ["Antiviral medications", "Supportive care"],
    "Migraine": ["Triptans", "Ibuprofen"],
    "Allergy": ["Antihistamines", "Nasal sprays"],
    "Gastroenteritis": ["Rehydration solutions", "Antiemetics"],
    "Asthma": ["Inhalers", "Corticosteroids"],
    "Hypertension": ["ACE inhibitors", "Beta-blockers"],
    "Heart Disease": ["Statins", "Aspirin"],
    "Pneumonia": ["Antibiotics", "Cough medicine"],
    "Appendicitis": ["Surgery (removal)", "Pain relief"],
    "Kidney Infection": ["Antibiotics", "Pain relief"],
    "Thyroid Disorders": ["Levothyroxine", "Antithyroid medications"],
    "Depression": ["Antidepressants", "Therapy"],
    "Anxiety": ["Benzodiazepines", "SSRIs"],
    "Acid Reflux": ["Proton pump inhibitors", "Antacids"],
    "Urinary Tract Infection": ["Antibiotics", "Pain relief"],
    "Arthritis": ["NSAIDs", "DMARDs"],
    "Osteoporosis": ["Calcium supplements", "Bisphosphonates"],
    "Skin Problems": ["Hydrocortisone cream", "Antihistamines"],
    "High Blood Sugar": ["Insulin", "Metformin"],
    "Low Blood Sugar": ["Glucose tablets", "Fruit juice"],
    "Jaundice": ["Treat underlying cause", "Supportive care"],
    "Cholera": ["Oral rehydration salts", "Antibiotics"],
}

diet_database = {
    "Diabetes": [
        "Choose whole grains over refined grains.",
        "Include non-starchy vegetables in every meal.",
        "Opt for lean proteins like chicken, fish, or legumes.",
        "Limit sugary drinks and high-calorie snacks.",
        "Monitor portion sizes and carbohydrate intake."
    ],
    "Heart Disease": [
        "Eat a variety of fruits and vegetables.",
        "Choose whole grains and high-fiber foods.",
        "Include healthy fats, such as avocados and olive oil.",
        "Limit saturated fats, trans fats, and cholesterol.",
        "Reduce salt intake."
    ],
    "Hypertension": [
        "Increase potassium-rich foods (bananas, sweet potatoes).",
        "Limit sodium intake (avoid processed foods).",
        "Include whole grains, fruits, and vegetables.",
        "Opt for low-fat dairy products.",
        "Limit alcohol consumption."
    ],
    "High Cholesterol": [
        "Eat more soluble fiber (oats, beans, lentils).",
        "Choose healthy fats (olive oil, avocados).",
        "Include fatty fish rich in omega-3s.",
        "Limit saturated and trans fats.",
        "Add nuts and seeds to your diet."
    ],
    "Weight Management": [
        "Focus on portion control.",
        "Choose nutrient-dense foods over calorie-dense foods.",
        "Incorporate physical activity into your daily routine.",
        "Stay hydrated with water instead of sugary drinks.",
        "Plan meals and snacks ahead of time."
    ],
    "General Health": [
        "Eat a balanced diet with a variety of foods.",
        "Limit added sugars and salt.",
        "Choose whole, minimally processed foods.",
        "Include plenty of fruits and vegetables.",
        "Stay hydrated with plenty of water."
    ]
}

def get_diet_recommendations(condition):
    return diet_database.get(condition, ["No recommendations available for this condition."])

# Function to check symptoms and suggest medications
def check_symptoms(user_symptoms):
    potential_conditions = []
    medications = []
    
    for condition, condition_symptoms in symptom_database.items():
        if any(symptom in user_symptoms for symptom in condition_symptoms):
            potential_conditions.append(condition)
            medications.append(medication_database.get(condition, []))
    
    return potential_conditions, medications

API_KEY = '9f75dc416d5e4aefa2e49afd114b9b85'


def homepage():
    # Add website title and description
    st.markdown(
    "<h1 style='text-align: center; color: black;'>Welcome to <span style='color:gold;'>REVIVE PLUS</span> - Your Health Companion</h1>",
    unsafe_allow_html=True,
)
    st.subheader("Empowering You with AI-driven Health Insights")
    
    # Add a descriptive paragraph
    st.markdown("""
    **REVIVE PLUS** is designed to simplify and enhance your healthcare experience. With advanced AI models and symptom-checking features, 
    we provide personalized health assessments, diet recommendations, and access to nearby medical facilities. This tool empowers you to make informed, proactive decisions about your health from the convenience of your device.
    """)
    
    # Optionally add an image or logo
    image = Image.open("C:/Users/Vikram Salvi/Downloads/p_78a7e4fa-92db-11ef-9455-aac38811e8c2_wm.png")  # Replace with your image path
    st.image(image, use_column_width=True)
    
   

diabetes_model = pickle.load(open('C:/Users/Vikram Salvi/Desktop/Multiple Disease Prediction/saved models/diabetes_model.sav','rb'))

heart_disease_model = pickle.load(open('C:/Users/Vikram Salvi/Desktop/Multiple Disease Prediction/saved models/heart_disease_model.sav','rb'))

parkinsons_model = pickle.load(open('C:/Users/Vikram Salvi/Desktop/Multiple Disease Prediction/saved models/parkinsons_model.sav', 'rb'))


def get_coordinates(location):
    """Fetch latitude and longitude for a given location using OpenCage API."""
    geocoder = OpenCageGeocode(API_KEY)
    result = geocoder.geocode(location)
    if result:
        return (result[0]['geometry']['lat'], result[0]['geometry']['lng'])
    else:
        return (None, None)

def find_nearby_osm(facility_type, latitude, longitude, radius):
    """Find nearby facilities using OpenStreetMap API."""
    url = f"https://overpass-api.de/api/interpreter?data=[out:json];(node['amenity'='{facility_type}'](around:{radius},{latitude},{longitude}););out;"
    response = requests.get(url)
    data = response.json()
    
    # Return the elements found in the data
    return data.get('elements', [])

# Streamlit Sidebar Menu
with st.sidebar:
    selected = option_menu('REVIVE PLUS',

                           ['Home','Find Nearby Facilities','Symptom Checker','Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Parkinsons Prediction','Breast Cancer','Diet Recommendations'],
                           menu_icon='hospital-fill',
                           icons=['House','activity', 'heart', 'person','virus2','map'],
                           default_index=0)
    
if selected == 'Home':
    homepage()
    
elif selected == 'Find Nearby Facilities':
    st.title("Find Nearby Healthcare Facilities in Mumbai")
    st.write("Enter your current location to find the nearest healthcare facilities.")

    # User input for location
    user_location = st.text_input("Enter your current location (e.g., address, landmark, or postal code):")

    # Facility selection
    facility_type = st.selectbox("Select the type of facility:", ["hospital", "pharmacy", "doctor"])

    # Search Radius
    radius = st.slider("Select Search Radius (in kilometers):", min_value=1, max_value=10, value=5, step=1)

    # Button to trigger search
    if st.button("Search Nearby"):
        if user_location:
            latitude, longitude = get_coordinates(user_location)

            if latitude is not None and longitude is not None:
                # Convert radius from kilometers to meters
                radius_meters = radius * 1000
                
                # Call your find_nearby_osm function
                places = find_nearby_osm(facility_type, latitude, longitude, radius_meters)

                if places:
                    st.write(f"Nearby {facility_type.capitalize()}s:")
                    for place in places:
                        # Use get() to avoid KeyError
                        display_name = place.get('tags', {}).get('name', 'Unnamed Place')  # Default if 'name' not found
                        lat = place.get('lat', 'No latitude')  # Default if 'lat' not found
                        lon = place.get('lon', 'No longitude')  # Default if 'lon' not found

                        st.write(display_name)
                        st.write(f"Latitude: {lat}, Longitude: {lon}")
                        st.write("---")
                else:
                    st.write("No results found.")
            else:
                st.write("Location not found. Please check your input.")
        else:
            st.write("Please enter your current location.")
            
elif selected == 'Symptom Checker':
    st.title("Symptom Checker and Medication")
    st.write("Select your symptoms:")

    # User input for symptoms
    symptoms = list({symptom for sublist in symptom_database.values() for symptom in sublist})

    selected_symptoms = st.multiselect("Symptoms", symptoms)

    # Button to check symptoms
    if st.button("Check Symptoms"):
        if selected_symptoms:
            results, medications = check_symptoms(selected_symptoms)
            if results:
                st.write("Potential conditions based on your symptoms:")
                for condition, meds in zip(results, medications):
                    st.write(f"- **{condition}**")
                    st.write("  Suggested Medications: ", ", ".join(meds) if meds else "No medications available.")
            else:
                st.write("No matching conditions found. Please consult a healthcare provider.")
        else:
            st.write("Please select at least one symptom.") 
            
    uploaded_image = st.file_uploader("Upload an image of your symptom", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)
            
elif selected == 'Diabetes Prediction':

    # page title
    st.title('Diabetes Prediction')

    # getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')

    with col2:
        Glucose = st.text_input('Glucose Level')

    with col3:
        BloodPressure = st.text_input('Blood Pressure value')

    with col1:
        SkinThickness = st.text_input('Skin Thickness value')

    with col2:
        Insulin = st.text_input('Insulin Level')

    with col3:
        BMI = st.text_input('BMI value')

    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

    with col2:
        Age = st.text_input('Age of the Person')


    # code for Prediction
    diab_diagnosis = ''

    # creating a button for Prediction

    if st.button('Diabetes Test Result'):

        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                      BMI, DiabetesPedigreeFunction, Age]

        user_input = [float(x) for x in user_input]

        diab_prediction = diabetes_model.predict([user_input])

        if diab_prediction[0] == 1:
            diab_diagnosis = 'The person is diabetic'
        else:
            diab_diagnosis = 'The person is not diabetic'

    st.success(diab_diagnosis)

# Heart Disease Prediction Page
elif selected == 'Heart Disease Prediction':

    # page title
    st.title('Heart Disease Prediction')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')

    with col2:
        sex = st.text_input('Sex')

    with col3:
        cp = st.text_input('Chest Pain types')

    with col1:
        trestbps = st.text_input('Resting Blood Pressure')

    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl')

    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')

    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')

    with col3:
        exang = st.text_input('Exercise Induced Angina')

    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')

    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')

    with col3:
        ca = st.text_input('Major vessels colored by flourosopy')

    with col1:
        thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

    # code for Prediction
    heart_diagnosis = ''

    # creating a button for Prediction

    if st.button('Heart Disease Test Result'):

        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

        user_input = [float(x) for x in user_input]

        heart_prediction = heart_disease_model.predict([user_input])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person is having heart disease'
        else:
            heart_diagnosis = 'The person does not have any heart disease'

    st.success(heart_diagnosis)

# Parkinson's Prediction Page
elif selected == "Parkinsons Prediction":

    # page title
    st.title("Parkinson's Disease Prediction")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')

    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')

    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')

    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)')

    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

    with col1:
        RAP = st.text_input('MDVP:RAP')

    with col2:
        PPQ = st.text_input('MDVP:PPQ')

    with col3:
        DDP = st.text_input('Jitter:DDP')

    with col4:
        Shimmer = st.text_input('MDVP:Shimmer')

    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

    with col1:
        APQ3 = st.text_input('Shimmer:APQ3')

    with col2:
        APQ5 = st.text_input('Shimmer:APQ5')

    with col3:
        APQ = st.text_input('MDVP:APQ')

    with col4:
        DDA = st.text_input('Shimmer:DDA')

    with col5:
        NHR = st.text_input('NHR')

    with col1:
        HNR = st.text_input('HNR')

    with col2:
        RPDE = st.text_input('RPDE')

    with col3:
        DFA = st.text_input('DFA')

    with col4:
        spread1 = st.text_input('spread1')

    with col5:
        spread2 = st.text_input('spread2')

    with col1:
        D2 = st.text_input('D2')

    with col2:
        PPE = st.text_input('PPE')

    # code for Prediction
    parkinsons_diagnosis = ''

    # creating a button for Prediction    
    if st.button("Parkinson's Test Result"):

        user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                      RAP, PPQ, DDP,Shimmer, Shimmer_dB, APQ3, APQ5,
                      APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]

        user_input = [float(x) for x in user_input]

        parkinsons_prediction = parkinsons_model.predict([user_input])

        if parkinsons_prediction[0] == 1:
            parkinsons_diagnosis = "The person has Parkinson's disease"
        else:
            parkinsons_diagnosis = "The person does not have Parkinson's disease"

    st.success(parkinsons_diagnosis)
    
    
elif selected == 'Breast Cancer':

    # page title
    st.title('Breast Cancer Classification')
    
    
elif selected == 'Diet Recommendations':
    st.title("Diet Recommendations")
    st.write("Select your health condition to get personalized diet advice:")

    # User input for health condition
    health_conditions = list(diet_database.keys())
    selected_condition = st.selectbox("Select a health condition:", health_conditions)

    # Button to get recommendations
    if st.button("Get Recommendations"):
        recommendations = get_diet_recommendations(selected_condition)
        st.write(f"**Diet Recommendations for {selected_condition}:**")
        for recommendation in recommendations:
            st.write(f"- {recommendation}")