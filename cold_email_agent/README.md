# Cold Email Outreach Automation System

Welcome! This system helps you automatically find prospects and send cold emails to them. It is designed to be easy to use and safe for your email account.

## 1. How to get a Gmail App Password
To allow this program to send emails from your Gmail account, you need to create an "App Password". This is safer than using your real password.
1. Go to your Google Account (myaccount.google.com).
2. Click on **Security** on the left panel.
3. Scroll down to "How you sign in to Google" and ensure **2-Step Verification** is turned ON.
4. Search for "App Passwords" in the search bar at the top, or find it under 2-Step Verification settings.
5. Create a new App Password (you can name it "Cold Email Agent").
6. Google will give you a 16-character password. **Copy this and save it**, as you won't be able to see it again!

## 2. Install Dependencies
You need to install some tools to run this script. Open your "Terminal" or "Command Prompt", navigate to this folder, and run:
```bash
pip install -r requirements.txt
```

## 3. Configure the System (.env)
1. In this folder, you will see a file named `.env.example`.
2. Copy this file and name the copy `.env`.
3. Open `.env` in any text editor (like Notepad or TextEdit).
4. Fill in your details:
   - `SENDER_EMAIL`: Your actual Gmail address.
   - `SENDER_PASSWORD`: The 16-character App Password you generated in Step 1.
   - Update your name, phone, etc., if needed.

## 4. Run the Agent
To start finding prospects and sending emails, open your Terminal in this folder and run:
```bash
python run_agent.py
```

## 5. Add Custom Prospects Manually
The system creates a file called `prospects.csv` where it stores people it finds. 
You can open this file in Excel or Google Sheets and manually add new rows with people's email addresses and company names. The system will process them just like the ones it finds automatically.

## 6. Rate Limiting (Why it's important!)
To ensure Google doesn't block your email address for sending spam, this tool has built-in speed limits:
- It sends a maximum of **20 emails per hour**.
- It waits **3 minutes** between each email.
- It sends a maximum of **50 emails per day**.
These limits are set to keep your account safe and maintain a high deliverability rate (so your emails land in the inbox, not the spam folder).

## 7. Legal Disclaimer
This software is for educational and legitimate business-to-business (B2B) networking purposes. It is your responsibility to comply with laws such as the CAN-SPAM Act (US) or similar laws in your country. Always ensure your emails offer value, include a clear way to opt out, and are sent to relevant businesses.
