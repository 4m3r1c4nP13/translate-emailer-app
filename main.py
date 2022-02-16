import os
from datetime import date, datetime

# Import Sendgrid info
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

# Required Flask Libraries
from flask import Flask, request, render_template, redirect, send_from_directory

# Import Google Datastore API
from google.cloud import datastore

# Import Google Translate API
from google.cloud import translate_v2 as translate

# Initialize global variable
translate_client = translate.Client()
client = datastore.Client()
kind = 'Custinfo'

# Start Flask app
app = Flask(__name__)

# Static directory for css
@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

# Home Page (will show all the customers in the datastore)
@app.route('/', methods=['GET'])
def index():
    query1 = client.query(kind=kind)
    query1.add_filter("Class", "=", "z81")
    query2 = client.query(kind=kind)
    query2.add_filter("Class", "=", "z82")
    class1 = list(query1.fetch())
    class2 = list(query2.fetch())
    return render_template('index.html', class1=class1, class2=class2)


# Create
@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # Put customer record
        complete_key = client.key(kind, data['Last'])
        customer = datastore.Entity(key=complete_key)
        customer.update({
            'Class': data['Class'],
            'First': data['First'],
            'Last': data['Last'],
            'email': data['email'],
            "lang": data['lang'],
        })
        client.put(customer)

        # Redirect to customer page
        return redirect("/read/" + data['Last'])

    else:
        # GET - Render customer creation form
        return render_template('create.html')


# Read
@app.route('/read/<name>', methods=['GET'])
def read(name):
    key = client.key(kind, name)
    customer = client.get(key)
    return render_template('customer.html', first=customer['First'], last=customer['Last'], email=customer['email'],
                           lang=customer['lang'], Class=customer['Class'])


# Update
@app.route('/update/<name>', methods=['GET', 'POST'])
def update(name):
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        key = client.key(kind, name)
        customer = client.get(key)

        customer['Class'] = data['Class']
        customer['email'] = data['email']
        customer['lang'] = data['lang']
        client.put(customer)

        # Redirect to customer page
        return redirect("/read/" + name)

    else:
        # Get customer data
        key = client.key(kind, name)
        customer = client.get(key)

        # Renders update page with existing data
        return render_template('update.html', first=customer['First'], email=customer['email'], lang=customer['lang'],
                               last=customer['Last'], Class=customer['Class'])


# Delete
@app.route('/delete/<name>', methods=['GET'])
def delete(name):
    # Delete Customer Record
    key = client.key(kind, name)
    client.delete(key)

    # Redirect to index page
    return redirect('/')


#Compose Message - GET
@app.route('/compose', methods=['GET'])
def compose():
    return render_template('compose.html')


#Compose Message - POST
@app.route('/compose-message', methods=['POST'])
def compose_message():
    data = request.form.to_dict(flat=True)
    sendEmail(data)
    return redirect('/')

def sendEmail(data):
    sg = sendgrid.SendGridAPIClient('[SENDGRID KEY]')
    from_email = Email('[SENDGRID EMAIL]', '[DISLAY NAME]')
    subject_input = data['subject']
    message_input = data['message']
    now = datetime.now().strftime("%m/%d/%Y, %I:%M %p")
    Class = data['Class']

    query1 = client.query(kind=kind)
    query1.add_filter("Class", "=", "z81")
    query2 = client.query(kind=kind)
    query2.add_filter("Class", "=", "z82")
    if Class == 'z81':
        results = list(query1.fetch())
    elif Class == 'z82':
        results = list(query2.fetch())
    else:
        results = list()

    for contact in results:
        lang = contact['lang']
        langw = "English"
        if lang == 'en':
            langw = 'English'
        elif lang == 'de':
            langw = "German"
        elif lang == 'fr':
            langw = "French"
        elif lang == 'es':
            langw = "Spanish"
        elif lang == 'it':
            langw = "Italian"
        elif lang == 'hi':
            langw = "Hindi"
        header1 = f"Your assigned language is: {langw}"
        header2 = "Classroom blog: http://uconnstamfordslp.blogspot.com/"

        subject = f"{subject_input}, {now}, {langw}"

        # Translate subject and message of email
        subject = translate_client.translate(subject, target_language=lang)['translatedText']

        header1 = translate_client.translate(header1, target_language=lang)['translatedText']
        header2 = translate_client.translate(header2, target_language=lang)['translatedText']
        now = translate_client.translate(now, target_language=lang)['translatedText']
        message_input = translate_client.translate(message_input, target_language=lang)['translatedText']

        message = f"{header1}\n" \
                  f"{header2}\n" \
                  f"\n{now}\n\n" \
                  f"{message_input}"

        to_email = contact['email']
        content = Content("text/plain", message)

        mail = Mail(from_email, to_email, subject, content)
        mail.reply_to = '[REPLY EMAIL]'
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        response = sg.client.mail.send.post(request_body=mail_json)

        # For debugging
        print(response.status_code)

#---------------------------------

# Server listening on port 8080
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
