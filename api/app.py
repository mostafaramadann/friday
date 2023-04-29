from dotenv import load_dotenv
from flask import Flask, request
from controllers.AgentController import message_openai_agent, message_alpaca_agent, message_flan_agent
from google_auth_oauthlib.flow import InstalledAppFlow
from agents import GSCOPES,REDIRECT
load_dotenv()  # take environment variables from .env.

app = Flask(__name__)

#@app.route("/")
#def hello():
#    return "Hello, World!"

@app.route("/chat", methods=["POST"])
def friday():
    chat_history = request.json["chat-history"]
    
    return {"role": "assistant", "message": message_openai_agent(chat_history)}

@app.route('/')
def callback():
    flow = InstalledAppFlow.from_client_secrets_file(
        '3.json', GSCOPES,redirect_uri=REDIRECT)
    parts = request.url.split(":")
    url = None
    if parts[0][-1]!="s":
        url = parts[0]+"s:"+"".join([part for part in parts[1:]])
    print(url)
    flow.fetch_token(authorization_response=url)
    creds = flow.credentials
    print(creds.scopes)
    with open('token.json', 'w') as f:
            f.write(creds.to_json())

    return "Authorization successful" 
    

@app.route("/chat-flan", methods=["POST"])
def friday_flan():
    chat_history = request.json["chat-history"]

    return {"role": "assistant", "message": message_alpaca_agent(chat_history)}

@app.route("/chat-alpaca", methods=["POST"])
def friday_alpaca():
    chat_history = request.json["chat-history"]

    return {"role": "assistant", "message": message_flan_agent(chat_history)}

if __name__ == "__main__":
    app.run(debug=True,port=5000)
