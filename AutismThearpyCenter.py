import streamlit as st
from PIL import Image
import base64
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
import pandas as pd
import time
import plotly.express as px
import json
import os
import re
import smtplib
from email.message import EmailMessage

def send_email(name, email, phone, message):
    try:
        msg = EmailMessage()
        msg['Subject'] = "New Contact Form Submission"
        msg['From'] = "your_email@example.com"
        msg['To'] = "your_destination_email@example.com"
        
        msg.set_content(f"""
        Name: {name}
        Email: {email}
        Phone: {phone}
        Message: {message}
        """)

        # Connect to SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            password= "kvhc dofx brsm roqw"
            smtp.login("hvparashar23@gmail.com", password)
            smtp.send_message(msg)

        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False


# =====================
# Helper functions for data persistence
# =====================

STORIES_FILE = "stories.json"
NEWSLETTER_FILE = "newsletter.json"

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def add_story(title, author, content):
    stories = load_json(STORIES_FILE)
    stories.insert(0, {"title": title, "author": author, "content": content})
    save_json(STORIES_FILE, stories)

def add_newsletter_email(email):
    emails = load_json(NEWSLETTER_FILE)
    if email not in emails:
        emails.append(email)
        save_json(NEWSLETTER_FILE, emails)
        return True
    return False

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# =====================
# Pytrends data fetching with retries
# =====================

def get_trends_data(keywords, timeframe='today 3-m', max_retries=5, sleep_time=60):
    pytrends = TrendReq(hl='en-IN', tz=330)
    attempt = 0
    while attempt < max_retries:
        try:
            pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo='IN', gprop='')
            time.sleep(5)
            data = pytrends.interest_over_time()
            return data
        except TooManyRequestsError:
            time.sleep(sleep_time)
            attempt += 1
        except Exception as e:
            st.error(f"Unexpected error fetching trends: {e}")
            break
    st.warning("Failed to fetch data after multiple retries.")
    return None

# =====================
# Streamlit Page Config & Background
# =====================

st.set_page_config(page_title="Hope for Kids", layout="wide")

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.unsplash.com/photo-1601582584281-910b3efb38b4");
    background-size: cover;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
}
[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# =====================
# Main Title
# =====================

st.title("🌈 Hope for Kids - Therapy & Support for Autistic Children")
st.markdown("""
Welcome to **Hope for Kids**, a nurturing space where we offer personalized therapy and support services
for children with autism. Our team of certified therapists is here to support your child’s journey.
""")

# =====================
# Tabs for main sections
# =====================

home, therapies, team, trends, stories, newsletter, contact = st.tabs([
    "🏠 Home",
    "🧠 Therapies",
    "👩‍⚕️ Our Team",
    "📊 Autistic Search Trends",
    "📖 Stories of Hope",
    "📰 Newsletter Signup",
    "📞 Contact Us"
])

# ======== HOME =========
with home:
    st.header("Why Choose Us")
    st.markdown("""
- ✅ Individual Attention
- ✅ Safe and Friendly Environment
- ✅ Experienced & Certified Therapists
- ✅ Affordable Packages
""")

# ======== THERAPIES =========
with therapies:
    st.header("🧠 Therapy Services We Offer")
    st.markdown("""
1. **Speech Therapy** – Enhancing communication skills  
2. **Occupational Therapy** – Helping kids perform daily activities  
3. **Behavioral Therapy (ABA)** – Improving social behavior  
4. **Sensory Integration** – Managing sensory processing difficulties  
5. **Play Therapy** – Expressing emotions through play  
""")

# ======== TEAM =========
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

# ======== PROPERTY TRENDS =========
with trends:
    st.header("📊 Autistic Kid Search Trend Analyzer")
    keywords = st.text_input("Enter keywords (comma separated)", "autistic kid")
    timeframe = st.selectbox("Select Timeframe", ["today 1-m", "today 3-m", "today 12-m", "all"])
    keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]

    if st.button("Get Trends"):
        if keyword_list:
            data = get_trends_data(keyword_list, timeframe=timeframe)
            if data is not None and not data.empty:
                df = data.reset_index()
                fig = px.line(df, x='date', y=keyword_list, title='Search Trends Over Time')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available. Try different keywords or timeframe.")
        else:
            st.warning("Please enter at least one keyword.")

# ======== STORIES =========
with stories:
    st.header("📖 Stories of Hope")

    # Story submission form
    with st.expander("Add a New Story"):
        with st.form("story_form"):
            title = st.text_input("Story Title")
            author = st.text_input("Author Name")
            content = st.text_area("Story Content")
            submitted = st.form_submit_button("Submit Story")

            if submitted:
                if title.strip() and author.strip() and content.strip():
                    add_story(title.strip(), author.strip(), content.strip())
                    st.success("Story added successfully! It will appear below.")
                else:
                    st.warning("Please fill all fields to submit a story.")

    # Load stories and paginate
    stories_data = load_json(STORIES_FILE)
    stories_per_page = 3
    total_pages = (len(stories_data) + stories_per_page - 1) // stories_per_page

    if total_pages == 0:
        st.info("No stories added yet. Be the first to add one!")
    else:
        page = st.number_input("Page", min_value=1, max_value=total_pages, step=1, value=1)
        start_idx = (page - 1) * stories_per_page
        end_idx = start_idx + stories_per_page

        for story in stories_data[start_idx:end_idx]:
            st.subheader(story['title'])
            st.caption(f"by {story['author']}")
            # Show first 250 characters, with read more option
            preview = story['content'][:250] + ("..." if len(story['content']) > 250 else "")
            st.write(preview)
            if len(story['content']) > 250:
                if st.button(f"Read More: {story['title']}"):
                    st.write(story['content'])

        st.caption(f"Showing page {page} of {total_pages}")

# ======== NEWSLETTER =========
with newsletter:
    st.header("📰 Subscribe to Our Newsletter")
    email = st.text_input("Enter your email")
    if st.button("Subscribe"):
        if is_valid_email(email):
            if add_newsletter_email(email):
                st.success("Subscribed successfully! Thank you.")
            else:
                st.info("You are already subscribed.")
        else:
            st.error("Please enter a valid email address.")

# ======== CONTACT =========
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
                st.success("Thank you! We'll get back to you shortly.")
                # Placeholder for email sending logic and WhatsApp notification
                # You can integrate your SMTP email or WhatsApp API here
            else:
                st.warning("Please fill all required fields.")

st.markdown("---")
st.caption("© 2025 Hope for Kids | Empowering Every Child")
