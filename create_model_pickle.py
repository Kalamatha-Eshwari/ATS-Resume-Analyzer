import pickle
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def create_and_pickle_model():
   
    model = genai.GenerativeModel('gemini-1.5-flash')
    
   
    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)
    print("Model has been pickled successfully.")

if __name__ == "__main__":
    create_and_pickle_model()
