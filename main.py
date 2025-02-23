import re
import smtplib
from flask import Flask, request, jsonify,json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import threading
from flask_cors import CORS

app = Flask(__name__)



#List of alllowed origins
allowed_origins =[
    "https://telex.im",
    "https://staging.telex.im",
    "https://telextest.im",
    "https://staging.telextest.im",
    
]

#enable CORS for specific oriigins

CORS(app,origins=allowed_origins)


@app.route("/",methods=["GET"])
def root():

    data={
        "app_name":"Email Notifier",
        "description":"It notifies the Admin when a username/user is called in a channel at a particular period of time",
        "type":"Output Integration",
        "category":"Email & Messaging"
    }



    return jsonify(data)












# Get current date and time
now = datetime.now()

# Format it as a string
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

print("Current Date and Time:", formatted_time)

admin_mail ='lawalhussein775@gmail.com'
# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "joshhearns37@gmail.com"
EMAIL_PASSWORD = ""  # Use App Password if 2FA is enabled

def send_email(to_email, mention):
    """Send a dummy email notification"""
    subject = f"Notification: You were mentioned!"
    body = f"Hello {mention},\n\nYou were mentioned in a message!\n\nBest,\nYour App"
    body=f"Hello Admin. {mention} was mentioned in the channel by {formatted_time} time"
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        server.quit()
        return f"Email sent to {to_email}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"






@app.route("/tick", methods=["POST"])
def detect_mentions():
    try:
        # Get the request data
        data = request.get_json()

        if not data:
            return json.dumps({"message": "Invalid JSON"}), 400  # Serialize response

        # Extract content
        content = data.get("message") or data.get("content")
        settings = data.get("settings", [])

        if not content:
            return json.dumps({"message": "Message content required"}), 400  # Serialize response

        # Extract mentions using regex
        mentions = re.findall(r"@(\w+)", content)

        if mentions:
            # Start a new thread to send email (Non-blocking)
            thread = threading.Thread(target=send_email, args=(admin_mail, mentions))
            thread.start()

        # Process settings
        processed_settings = [
            {
                "label": setting.get("label", "Unknown Label"),
                "type": setting.get("type", "Unknown Type"),
                "default": setting.get("default", ""),
                "required": setting.get("required", False),
            }
            for setting in settings
        ]

        # Create response dictionary
        response = {
            "message": content,
            "settings": processed_settings,
        }

        # Serialize response as a JSON string
        serialized_response = json.dumps(response)

        # Return the serialized string
        return serialized_response, 200  , {"Content-Type": "application/json"}
    
    except Exception as e:
        return json.dumps({"message": str(e)}), 500  # Ensure error response is a string






 

@app.route("/integration.json",methods=['GET'])
def jsonsetting():
    base_url =str(request.base_url).rstrip("/")


    return jsonify(
        
            {
    "data": {
        "date": {
            "created_at": "2025-02-21",
            "updated_at": "2025-02-21"
        },
        "descriptions": {
            "app_name": "Channel Name Notifier",
            "app_description": "is an integration that detects when a user's name or role is mentioned in a message and sends a notification (email or API alert) to them",
            "app_logo": "https://www.google.com/imgres?q=name%20notifier%20logo%20for%20api&imgurl=https%3A%2F%2Fwww.shutterstock.com%2Fimage-vector%2Fvector-multi-color-icon-webhook-600w-2545676463.jpg&imgrefurl=https%3A%2F%2Fwww.shutterstock.com%2Fsearch%2Fnotifier-logo&docid=ZHyur4VYW14V1M&tbnid=z1ir3cEwbaHJFM&vet=12ahUKEwi6x46DqNSLAxUQWEEAHWZbLSEQM3oECBsQAA..i&w=600&h=620&hcb=2&itg=1&ved=2ahUKEwi6x46DqNSLAxUQWEEAHWZbLSEQM3oECBsQAA",
            "app_url":"https://hng-task-output-telex-integrationn.onrender.com",
            "background_color": "#fff"
        },
        "integration_category": "Email & Messaging",
        "is_active": True,
        "integration_type": "output",
        "key_features": [
            "No Backend Required",
            "Easy Integration",
            "Email Notification",
            "Scalable and Secure"
        ],
        "author": "Lawal Hussein",
        "settings": [
            {
                "label": "Notification Type",
                "type": "Multi-Select",
                "description": "Description of the multi-select setting.",
                "default": "Email,API Alert",
                "required": True
            }
        ],
        "tick_url": "https://hng-task-output-telex-integrationn.onrender.com/tick",
        
    }
}

  
    )













if __name__ == '__main__':
    app.run(debug=True)



