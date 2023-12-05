import keyword
import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader
import random
import pypdf
import pyttsx3
import requests
import json
from google.oauth2 import service_account
import googlemaps

# Set Streamlit page configuration
st.set_page_config(page_title="Healthcare Bot", page_icon="👩‍⚕️", layout="centered", initial_sidebar_state="auto", menu_items=None)

# Set OpenAI API key
openai.api_key = "YOUR_API_KEY"
#api_key = "AIzaSyDG2A-JEySKjaDMqNPSEgdA_EOusVsjeFM"
def speak_response(response_content):
    engine = pyttsx3.init()
    engine.say(response_content)
    engine.runAndWait()

api_key = "apikey 5fihyYtS6JwVICEuSzrMtG:3YcxAGXrrHIia132kOGdY1"

# Example coordinates (replace with the user's location)
latitude = 12.904103491581367
longitude = 77.63332323453498

# Define API endpoint for nearby pharmacies
api_url = f"https://api.collectapi.com/health/dutyPharmacy?ilce=%C3%87ankaya&il=Ankara"

# Set up headers with the API key
headers = {
    'content-type': "application/json",
    'authorization': f"apikey {api_key}"
}



#Define your client
##gmaps = googlemaps.Client(key=api_key)
#Define your search
#places_results = gmaps.places_nearby(location = "12.904103491581367, 77.63332323453498" , radius= 40000, open_now = False, type = "pharmacy" )

#for place in places_results["results"]:
 #   my_fields= ['name', 'formatted_phone_number', 'type']
#    place_details = gmaps.place(fields = my_fields)



# Display title and introductory message
st.title("Have a Convo with your Healthcare Bot")
st.write("Arguments generate heat, and discussion throws light. In argument, it is seen who is right, and in discussion, it is seen what is RIGHT!")


# Initialize chat messages history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I hope you're doing well. How may I help you?"}
    ]

# Cache resource to load data (assuming this is a heavy operation)
@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="I am not as intelligent as you - hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(
            llm=OpenAI(model="gpt-3.5-turbo", temperature=0.01, system_prompt="You are an expert Digital doctor who gives curing tips, Assume all input prompts to be with respect to the input data, Don't answer anything apart from Healthcare and wellness related"))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

# Load data when needed
index = load_data()

#waiting responses
waiting_messages = [
                "Hold on, let me think...",
                "Just a moment, processing your request...",
                "Thinking of the best response...",
                "Analyzing the information...",
                "Give me a second, I'm working on it...",
            ]




voice_checkbox = st.checkbox("🔊")

# Initialize the chat engine
if "chat_engine" not in st.session_state.keys():
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# User input prompt
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# If last message is not from the assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner(random.choice(waiting_messages)):
            user_input = st.session_state.messages[-1]["content"].lower()

            # Possible responses
            greeting_responses = [
                "Hello! How can I assist you today?",
                "Hi there! What can I do for you?",
                "Greetings! How may I help you?",
                "Hey! I'm here to help with any healthcare questions.",
                "Good day! What brings you here for a chat?",
            ]

            farewell_responses = [
                "You're welcome! If you have more questions, feel free to ask. Goodbye!",
                "Goodbye! Take care.",
                "Farewell! If you need assistance in the future, don't hesitate to reach out.",
                "Until next time! Stay healthy and happy.",
                "Take care! If you ever need advice, I'll be here.",
            ]

            engaging_responses = [
                "Got it!.",
                "Is there anything else?.",
                "Great! How can I assist you further?.",
                "I hope you're happy! May I know how can I assist you further?.",
            ]

            # Custom responses based on user input
            if any(keyword in user_input for keyword in ["hi", "hello", "greet"]):
                response_content = random.choice(greeting_responses)
            elif any(keyword in user_input for keyword in ["ok", "great", "nice", "cool"]):
                response_content = random.choice(engaging_responses)
        
            elif any(keyword in user_input for keyword in ["book", "schedule appointment", "looking for appointment", "need an appointment"]):
                response_content = "Our Team is still working on importing the appointments form in the same window. As of now, you can click above and get scheduled for your appointment."
                st.link_button("Go to appointment form", "https://appointments-pesu-healthcare.streamlit.app/")
            
            elif any(keyword in user_input for keyword in ["I am suffering from ", "Disease Diagnosis" , "symptomps", "I'm not feeling well.",
                                                                "I have some symptoms. Can you help me figure out what might be wrong?",
                                                                "Feeling sick, need advice." ]):
                response_content="Please click the below button for disease dignosis"
                st.link_button("Disease Diagnosis", "https://disease-diagnosis-pesu.streamlit.app/")
            
            
            elif any(keyword in user_input for keyword in ["medical", "pharmacy", "hospital"]):
                response_content = place_details
           
           
            else:
                # Use chat engine to generate response
                response = st.session_state.chat_engine.chat(prompt)
                response_content = response.response
            # Display response content
            st.write(response_content)
            if voice_checkbox:
                speak_response(response_content)
        
           
           
            # Append the response to the chat history
        message = {"role": "assistant", "content": response_content}
        st.session_state.messages.append(message)







          
