import streamlit as st
from textblob import TextBlob
import google.generativeai as genai
import pandas as pd
import os
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Mental Wellness Support Assistant",
    page_icon="🧠",
    layout="wide"
)

# ---------------- GEMINI ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- CREATE HISTORY FILE ----------------
if not os.path.exists("history.csv"):
    df = pd.DataFrame(
        columns=[
            "Date",
            "User Input",
            "Mood",
            "Sentiment Score"
        ]
    )
    df.to_csv("history.csv", index=False)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp{
background:radial-gradient(circle at top,#35104d,#12061d,#090312);
color:white;
}

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

.main-title{
text-align:center;
font-size:58px;
font-weight:700;
color:#d8b4fe;
text-shadow:0 0 30px #b84cff;
}

.sub-title{
text-align:center;
font-size:22px;
color:#e5d9ff;
margin-bottom:30px;
}

.glass{
background:rgba(255,255,255,.06);
backdrop-filter:blur(18px);
border:1px solid rgba(255,255,255,.15);
border-radius:20px;
padding:25px;
box-shadow:0 0 25px rgba(168,85,247,.4);
margin-bottom:20px;
}

[data-testid="stTextArea"] textarea{
background:#2b1d3a !important;
color:white !important;
caret-color:white !important;
border:1px solid #9d4edd !important;
border-radius:15px !important;
font-size:18px !important;
}

[data-testid="stTextArea"] textarea::placeholder{
color:#b8a7d9 !important;
}

.stButton>button{
width:100%;
height:55px;
border:none;
border-radius:15px;
background:linear-gradient(90deg,#7b2ff7,#c86dd7);
color:white;
font-size:18px;
font-weight:bold;
}

.stButton>button:hover{
background:linear-gradient(90deg,#c86dd7,#7b2ff7);
box-shadow:0 0 20px #d946ef;
}

[data-testid="stSidebar"]{
background:#12061d;
border-right:1px solid #5b21b6;
}

[data-testid="stSidebar"] *{
color:white;
}

[data-testid="metric-container"]{
background:rgba(255,255,255,.06);
border-radius:18px;
padding:18px;
box-shadow:0 0 20px rgba(168,85,247,.4);
}

.stSuccess{
background:rgba(16,185,129,.2);
border-radius:15px;
}

.stInfo{
background:rgba(59,130,246,.2);
border-radius:15px;
}

.stWarning{
background:rgba(234,179,8,.2);
border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🧠 Wellness AI")

    st.markdown("---")

    st.success("✔ Gemini AI")

    st.success("✔ Mood Detection")

    st.success("✔ Sentiment Analysis")

    st.success("✔ Mood History")

    st.success("✔ Charts")

    st.markdown("---")

    st.markdown("""
### 🌿 Daily Wellness Tips

✅ Drink enough water

✅ Sleep 7-8 hours

✅ Practice deep breathing

✅ Exercise regularly

✅ Spend time with loved ones
""")

# ---------------- HEADER ----------------

st.markdown("""
<h1 class="main-title">
🧠 AI Mental Wellness Support Assistant
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p class="sub-title">
Your Personal Mental Wellness Companion 💜
</p>
""", unsafe_allow_html=True)

# ---------------- INPUT ----------------


user_input = st.text_area(
    "💬 How are you feeling today?",
    height=180,
    placeholder="Example: I feel stressed because of exams..."
)


# ---------------- BUTTON ----------------

if st.button("🧠 Analyze My Mood", use_container_width=True):

    if user_input.strip() == "":
        st.error("Please enter something first.")
        st.stop()

    analysis = TextBlob(user_input)

    polarity = analysis.sentiment.polarity

    text = user_input.lower()

    response = model.generate_content(f"""
User Message:
{user_input}

Sentiment Score:
{round(polarity,2)}

You are a warm and empathetic wellness companion.

Respond like a caring friend.

Acknowledge the user's feelings.

Give comforting words.

Suggest ONE practical activity.

Do not ask follow-up questions.

Keep the response under 120 words.
""")
        # ---------------- RESPONSE SECTION ----------------

    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown(
            f"""
<div class="glass">

<h2>💙 AI Wellness Response</h2>

{response.text}

</div>
""",
            unsafe_allow_html=True,
        )

    with col2:

        st.metric("📊 Sentiment Score", round(polarity, 2))

        mood = "Neutral"

        stress_words = [
            "stress", "stressed", "exam", "pressure",
            "overwhelmed", "anxious", "worried", "tension"
        ]

        lonely_words = [
            "lonely", "alone", "isolated",
            "ignored", "left out"
        ]

        happy_words = [
            "happy", "joy", "joyful", "great",
            "awesome", "fantastic", "wonderful",
            "grateful", "cheerful", "excited"
        ]

        sad_words = [
            "sad", "cry", "crying",
            "heartbroken", "upset",
            "depressed", "miserable",
            "hopeless"
        ]

        if any(word in text for word in stress_words):

            mood = "Stress"

            st.warning("### 😟 Stress")

            tips = [
                "🧘 Take a 10-minute break",
                "💧 Drink some water",
                "🎯 Focus on one task at a time"
            ]

        elif any(word in text for word in lonely_words):

            mood = "Loneliness"

            st.warning("### 😔 Loneliness")

            tips = [
                "📞 Talk to a friend or family member",
                "📖 Write your thoughts in a journal",
                "🎨 Spend time on a hobby"
            ]

        elif any(word in text for word in happy_words) or polarity > 0.4:

            mood = "Happiness"

            st.success("### 😊 Happiness")

            tips = [
                "🎉 Celebrate your progress",
                "💜 Share your happiness",
                "🌟 Keep doing what makes you smile"
            ]

        elif any(word in text for word in sad_words) or polarity < -0.4:

            mood = "Sadness"

            st.warning("### 😢 Sadness")

            tips = [
                "🎵 Listen to calming music",
                "🚶 Take a short walk",
                "🤝 Reach out to someone you trust"
            ]

        else:

            mood = "Neutral"

            st.info("### 😐 Neutral")

            tips = [
                "💧 Stay hydrated",
                "🌱 Maintain a balanced routine",
                "☕ Take regular breaks"
            ]

    # ---------------- SUGGESTIONS CARD ----------------

    st.markdown(
        """
<div class="glass">

<h2>💡 Personalized Suggestions</h2>
""",
        unsafe_allow_html=True,
    )

    for tip in tips:
        st.markdown(f"- {tip}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- SAVE HISTORY ----------------

    new_record = pd.DataFrame({

        "Date": [
            datetime.now().strftime("%d-%m-%Y %H:%M")
        ],

        "User Input": [
            user_input
        ],

        "Mood": [
            mood
        ],

        "Sentiment Score": [
            round(polarity, 2)
        ]

    })

    history = pd.read_csv("history.csv")

    history = pd.concat(
        [history, new_record],
        ignore_index=True
    )

    history.to_csv(
        "history.csv",
        index=False
    )
        # ---------------- LOAD HISTORY ----------------

    history = pd.read_csv("history.csv")

    if not history.empty:

        history["Date"] = pd.to_datetime(
            history["Date"],
            dayfirst=True
        )

        history = history.sort_values("Date")

        st.markdown("---")

        st.markdown(
            """
<div class="glass">

<h2>📜 Mood History</h2>

</div>
""",
            unsafe_allow_html=True
        )

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("## 📈 Sentiment Trend")

            st.line_chart(
                history.set_index("Date")["Sentiment Score"]
            )

        with col2:

            st.markdown("## 😊 Mood Distribution")

            mood_count = history["Mood"].value_counts()

            st.bar_chart(mood_count)

    # ---------------- CLEAR HISTORY ----------------

    st.markdown("")

    if st.button(
        "🗑️ Clear Mood History",
        use_container_width=True
    ):

        empty_df = pd.DataFrame(
            columns=[
                "Date",
                "User Input",
                "Mood",
                "Sentiment Score"
            ]
        )

        empty_df.to_csv(
            "history.csv",
            index=False
        )

        st.success("Mood history cleared successfully!")

        st.rerun()

# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown(
    """
<div style="text-align:center;
padding:20px;
color:#d8b4fe;
font-size:16px;">

🧠 <b>AI Mental Wellness Support Assistant</b><br><br>

Made with ❤️ using
<b>Streamlit</b> •
<b>Gemini AI</b> •
<b>TextBlob</b>

</div>
""",
    unsafe_allow_html=True
)
