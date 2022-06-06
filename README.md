# Translate Emailer App 

An web application that is used to send out translated email to multiple groups of recipients.

## Features

- User can import or manually store customers' information on the application's built in database.
- User can easily make changes to any customer's info on the app.
- User can compose the email in any languages and customers will receive the translated version based on their language preferences. 


## Installation

This guide assume that user already have a [Google Cloud Account](https://console.cloud.google.com). 

### Set up a SendGrid Account

1. Go to [SendGrid's Sign Up Page](https://signup.sendgrid.com) and open a new account.
2. Once logged in, on the main screen, click `Create a Single Sender`.
3. Fill out the `Create a Sender` page.
4. Confirm your email (User might need to add Two-Factor Authenticator).
5. Once email is verified, on the right panel, choose `Email API`. Under the drop-down menu, choose `Integration Guide`.
6. Choose `Web API`
7. Choose `Python`
8. On `Create an API key` section, enter a name for your key, then click `Create Key`
9. Copy this key

That's all you will need for this step.

### Create a new project on Google Cloud Platform

1. Navigate to the search box on the top bar and search for `Create a Project`
2. Enter the name for your project then click `Create`
3. From the project drop-down selector, copy `ID` of the project that you just created, then choose to switch to that project.
4. Activate the `Cloud Shell` by clicking the logo to the left of the search box 
5. On the terminal, run the command (replace [PROJECT-ID] with the `ID` that you just copied)
```bat
gcloud config set project [PROJECT-ID]
```
You have just set up the environment to deploy the project! 

### Enable Google Translate API

1. Navigate to the search box and search for `Cloud Translation API`
2. Click the result under `Marketplace`
3. Enable the API

### Clone and edit the project

1. On the terminal, run the command
```bat
git clone https://github.com/4m3r1c4nP13/translate-emailer-app.git
```
2. Navigate to `Open Editor`
3. Once entered the `Editor`, on the left menu, navigate to folder `translate-emailer-app`
4. Open the `config.py` file under `translate-emailer-app`
5. Follow the instruction in the `config` file and fill out all required variables.
6. Save all file
7. Now, go back to the terminal, run the command
```bat
cd ~/translate-emailer-app/ && gcloud app deploy && gcloud app browse
```
11. If the region selection pops up on the terminal, choose `17`. Then choose `Y`

Wait about 3 minutes for the terminal to finish deploying. Then click the application link to launch the App Engine.
