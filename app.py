import streamlit as st
from textblob import TextBlob
import google.generativeai as genai

genai.configure(api_key="PASTE_YOUR_API_KEY_HERE")
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("AI Mental Wellness Support Assistant")

user_input = st.text_area("How are you feeling today?")

if st.button("Analyze"):

    analysis = TextBlob(user_input)
    polarity = analysis.sentiment.polarity

    response = model.generate_content(
        f"""
        User Message: {user_input}

        Sentiment Score: {round(polarity, 2)}

        You are a warm and empathetic wellness companion.

        Respond like a caring friend.

        Acknowledge the user's feelings.
        Give comforting and encouraging words.
        Suggest one practical step they can take.

        Do not ask follow-up questions.

        Do not say:
        "Is there anything else I can help with?"
        "Let me know if you need anything else."
        "Feel free to reach out again."

        End the response naturally.

        Keep the response under 120 words.
        """
    )

    st.subheader("💙 AI Wellness Response")
    st.write(response.text)

    st.subheader("📊 Mood Analysis")
    st.write("Sentiment Score:", round(polarity, 2))

    text = user_input.lower()

    if "stress" in text or "exam" in text or "pressure" in text:
        st.warning("Mood Detected: Stress 😟")
        st.write("Suggestions:")
        st.write("- Take a 10-minute break")
        st.write("- Drink some water")
        st.write("- Focus on one task at a time")

    elif "lonely" in text or "alone" in text:
        st.warning("Mood Detected: Loneliness 😔")
        st.write("Suggestions:")
        st.write("- Talk to a friend or family member")
        st.write("- Write your thoughts in a journal")
        st.write("- Spend time on a hobby")

    elif polarity > 0.4:
        st.success("Mood Detected: Happiness 😊")
        st.write("Suggestions:")
        st.write("- Celebrate your progress")
        st.write("- Share your happiness with others")
        st.write("- Keep doing what makes you feel good")

    elif polarity < -0.4:
        st.warning("Mood Detected: Sadness 😢")
        st.write("Suggestions:")
        st.write("- Listen to calming music")
        st.write("- Take a short walk")
        st.write("- Reach out to someone you trust")

    else:
        st.info("Mood Detected: Neutral 😐")
        st.write("Suggestions:")
        st.write("- Have a productive day")
        st.write("- Stay hydrated")
        st.write("- Take regular breaks")