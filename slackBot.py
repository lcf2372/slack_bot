import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key from the environment variables
client2 = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize the Slack App with the bot token from environment variables
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

# Handle events where the bot is mentioned in a Slack channel
@app.event("app_mention")
def hello_command(ack, body, say, client):
    # Acknowledge the event to prevent timeouts
    ack()
    
    # Extract the message text from the event payload
    message = str(body['event']['blocks'][0]['elements'][0]['elements'][1]['text'])
    
    # Generate a response using the OpenAI GPT-3.5 Turbo model
    completion = client2.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are SuperBot, like the superman of AI, and love to help people. Your favorite color is blue."},
            {"role": "user", "content": message}
        ]
    )
    
    # Send the response back to the Slack channel
    say(str(completion.choices[0].message.content))

# Start the Slack bot using the Socket Mode token from environment variables
if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
