import google.generativeai as genai
from google.generativeai import types
import json
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

fastapi_url = "http://127.0.0.1:8000"


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

genai.configure(
    api_key=GEMINI_API_KEY
)

create_appointment = {
    "name": "create_appointment_in_fastapi",
    "description": "Create an appointment in FastAPI",
    "parameters": {
        "type" : "object",
        "properties":{
            "id": {
                "type": "string",
                "description": "Every Customer has a unique id eg. '1','2',etc ",
            },
            "name":{
                "type":"string",
                "description": "name of the customer."
            },
            "email":{
                "type":"string",
                "description" : "email of customer"
            },
            "appointment_time":{
                "type" : "string",
                "format" : "date-time",
                "description": "Appointment time of the customer in ISO 8601 format."
            },
            "status":{
                "type":"string",
                "enum" : ["approved", "rejected", "pending"],
                "description": "Status of the appointment, default is 'pending'."
            }
        },
        "required": ["id","name", "email", "appointment_time"]
    }
}

def create_appointment_in_fastapi( id: str, name: str, email:str, appointment_time: str, status: str = "pending"):
    """ Calls the fastapi /create endpoint to make a new appointment.
    This function sends a POST request to the FastAPI server with the appointment details.
    """
    payload = {
        "id" : id,
        "name": name,
        "email": email,
        "appointment_time": appointment_time,
        "status": status
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"{fastapi_url}/create", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error calling FastAPI: {e.response.status_code} - {e.response.text}")
        return {"error": f"Failed to create appointment : {e.response.json().get('detail',e.response.text )}" }
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: Could not connect to FastAPI server at {fastapi_url}. Is it running?")
        return {"error": "Could not connect to the appointment service. Please ensure the backend is running."}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred: {e}"}

create_Appoint = types.Tool(
    function_declarations=[create_appointment]
)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    tools=[create_Appoint]
)

def chat_with_gemini():
    chat=model.start_chat()
    print("Welcome to the Appointment Booking System!")
    print("You can ask me to create an appointment request.")
    print("Type 'exit' to quit the chat.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Exiting the chat. Goodbye!")
            break

        try:
            response = chat.send_message(user_input)

            if response.candidates and response.candidates[0].content.parts:
                function_call = None
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call'):
                        function_call = part.function_call
                        break

                if function_call:
                    print(f"\nGemini wants to call function: {function_call.name} with args: {function_call.args}")

                    if function_call.name == "create_appointment_in_fastapi":
                        tool_response = create_appointment_in_fastapi(**function_call.args)
                        print(f"Tool response from FastAPI: {tool_response}")

                        gemini_final_response = chat.send_message(
                            genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name="create_appointment_in_fastapi",
                                    response=tool_response
                                )
                            )
                        )
                        print(f"Gemini: {gemini_final_response.text}")
                    else:
                        print(f"Error: Unknown function call requested by Gemini: {function_call.name}")
                        print(response.text if response.text else "Gemini did not provide a direct text response.")
                else:
                    print(f"Gemini: {response.text}")
            else:
                print(f"Gemini: {response.text}")

        except Exception as e:
            print(f"An error occurred during Gemini interaction: {e}")

if __name__ == "__main__":
    chat_with_gemini()
