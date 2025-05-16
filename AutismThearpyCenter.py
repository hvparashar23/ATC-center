import streamlit as st
from PIL import Image
import base64
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage
# Uncomment if using Twilio for WhatsApp
# from twilio.rest import Client

# --- Functions ---

def save_contact_form(name, email, phone, message):
    file = "contact_submissions.csv"
    data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Message": message
    }
    if os.path.exists(file):
        df = pd.read_csv(file)
        df = df.append(data, ignore_index=True)
    else:
        df = pd.DataFrame([data])
    df.to_csv(file, index=False)

def send_email_notification(name, email, phone, message):
    msg = EmailMessage()
    msg['Subject'] = f"New Contact Form Submission from {name}"
    msg['From'] = "your_gmail@gmail.com"  # Replace with your Gmail
    msg['To'] = "hvparashar23@gmail.com"
    msg.set_content(f"""
You have a new contact form submission:

Name: {name}
Email: {email}
Phone: {phone}
Message: {message}
""")
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            password1 = 'kvhc dofx brsm roqw'.replace('\xa0',' ')
            smtp.login('hvparashar23@gmail.com',password1)  # Replace with your app password
            smtp.send_message(msg)
        print("Email sent!")
    except Exception as e:
        print("Failed to send email:", e)

# Uncomment and fill your Twilio credentials to enable WhatsApp messaging
# def send_whatsapp_message(message_body):
#     account_sid = 'your_twilio_account_sid'
#     auth_token = 'your_twilio_auth_token'
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         from_='whatsapp:+14155238886',  # Twilio Sandbox number
#         body=message_body,
#         to='whatsapp:+91yourphonenumber'  # Your WhatsApp number with country code
#     )
#     print("WhatsApp message sent:", message.sid)

# --- Streamlit App ---

# Page Configuration
st.set_page_config(page_title="Hope for Kids", layout="wide")

# Background CSS
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://images.unsplash.com/photo-1601582584281-910b3efb38b4");
    background-size: cover;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
}}
[data-testid="stHeader"] {{
    background: rgba(0, 0, 0, 0);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title Section
st.title("🌈 Hope for Kids - Therapy & Support for Autistic Children")
st.markdown("""
Welcome to **Hope for Kids**, a nurturing space where we offer personalized therapy and support services
for children with autism. Our team of certified therapists is here to support your child’s journey.
""")

# Tabs
home, therapies, team, contact = st.tabs(["🏠 Home", "🧠 Therapies", "👩‍⚕️ Our Team", "📞 Contact Us"])

# Home Tab
with home:
    st.header("Why Choose Us")
    st.markdown("""
- ✅ Individual Attention
- ✅ Safe and Friendly Environment
- ✅ Experienced & Certified Therapists
- ✅ Affordable Packages
""")

# Therapies Tab
with therapies:
    st.header("🧠 Therapy Services We Offer")
    st.markdown("""
1. **Speech Therapy** – Enhancing communication skills
2. **Occupational Therapy** – Helping kids perform daily activities
3. **Behavioral Therapy (ABA)** – Improving social behavior
4. **Sensory Integration** – Managing sensory processing difficulties
5. **Play Therapy** – Expressing emotions through play
""")

# Team Tab
with team:
    st.header("👩‍⚕️ Meet Our Experts")
    col1, col2 = st.columns(2)

    with col1:
        st.image("https://randomuser.me/api/portraits/women/44.jpg", width=150)
        st.subheader("Vinita")
        st.caption("Lead Speech Therapist, 10+ years experience")

    with col2:
        st.image("https://randomuser.me/api/portraits/men/45.jpg", width=150)
        st.subheader("Sachin")
        st.caption("Occupational Therapist, Pediatric Specialist")

# Contact Tab
with contact:
    st.header("📞 Get in Touch with Us")
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        phone = st.text_input("Your Phone")
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("Send Message")

        if submitted:
            if name and email and message:
                save_contact_form(name, email, phone, message)
                send_email_notification(name, email, phone, message)
                # Uncomment below to enable WhatsApp message sending
                # send_whatsapp_message(f"New contact form submission from {name}, Email: {email}, Phone: {phone}")

                st.success("Thank you! We'll get back to you shortly.")
            else:
                st.warning("Please fill all required fields.")

st.markdown("---")
st.caption("© 2025 Hope for Kids | Empowering Every Child")
