import streamlit as st
from together_ai import generate_study_material
from quiz_helper import generate_quiz
from ocr_helper import extract_text_from_image
import speech_recognition as sr

# -------------------------------
# Page Setup & Session State
# -------------------------------
st.set_page_config(page_title="📚 AI Study Assistant", layout="wide")
if "selected_chat_index" not in st.session_state:
    st.session_state.selected_chat_index = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
    st.session_state.score = 0

# -------------------------------
# Sidebar Chat History
# -------------------------------

with st.sidebar:
    st.header("🗂️ Chat Topics")

    if st.session_state.chat_history:
        st.markdown("""
        <style>
            .topic-link {
                padding: 8px 12px;
                margin-bottom: 8px;
                background-color: black;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
            }
            .topic-link:hover {
                background-color: #dbe3ec;
            }
        </style>
        """, unsafe_allow_html=True)

        

        for i, (user_msg, _) in enumerate(reversed(st.session_state.chat_history)):
            # Actual index in original order
            actual_index = len(st.session_state.chat_history) - i - 1

            if st.button(f"🔹 {user_msg[:60]}", key=f"chat_topic_{actual_index}"):
                st.session_state.selected_chat_index = actual_index
                st.session_state.selected_chat_index = len(st.session_state.chat_history) - 1
        if st.button("🗑️ Clear Topics"):
            st.session_state.chat_history.clear()
            st.session_state.selected_chat_index = None
    else:
        st.info("No chats yet.")



# -------------------------------
# Title
# -------------------------------
st.markdown("<h1 style='text-align: center;'>🧠 AI Study Assistant</h1>", unsafe_allow_html=True)

# -------------------------------
# TABS for Study & Quiz Modes
# -------------------------------
tab1, tab2 = st.tabs(["📖 Study Mode", "🧪 Quiz Mode"])

# -------------------------------
# STUDY MODE TAB
# -------------------------------
with tab1:
    st.subheader("📘 Study Material Generator")

    # OCR Input
    uploaded_image = st.file_uploader("📷 Upload image (optional):", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        try:
            st.session_state.user_input = extract_text_from_image(uploaded_image)
            st.success("✅ Text extracted from image.")
        except Exception as e:
            st.error(f"❌ OCR Error: {e}")

    # Speech Input
    def record_audio():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎤 Speak now...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.session_state.user_input = text
            st.success(f"📝 You said: {text}")
        except sr.UnknownValueError:
            st.error("😕 Couldn't understand the audio.")
        except sr.RequestError:
            st.error("❌ API unavailable or request error.")

    input_mode = st.radio("Choose Input Mode", ["🎙️ Speak", "⌨️ Type"], horizontal=True)
    if input_mode == "🎙️ Speak":
        if st.button("🎤 Start Recording", key="record_button"):
            record_audio()

    manual_input = st.text_area("✍️ Enter or edit your topic:", value=st.session_state.user_input, key="study_input")


    if st.button("🚀 Generate", key="generate_study"):
        if manual_input.strip() == "":
            st.warning("Please provide input to generate study material.")
        else:
            with st.spinner("Generating study material..."):
              try:
                  response = generate_study_material(manual_input)
                  st.success("✅ Study material generated!")
                  st.write(response)

                # Update session input and chat history correctly
                  
                  st.session_state.chat_history.append((manual_input, response))
                  st.session_state.selected_chat_index = len(st.session_state.chat_history) - 1
              except Exception as e:
                  st.error(f"❌ Error: {e}")
if st.session_state.selected_chat_index is not None:
    user_msg, ai_msg = st.session_state.chat_history[st.session_state.selected_chat_index]
    st.markdown("---")
    st.subheader("📜 Selected Chat")
    st.markdown(f"**🧑 You:** {user_msg}")
    st.markdown(f"**🤖 AI:** {ai_msg}")
if st.session_state.selected_chat_index is not None:
    if st.button("🔙 Back to main"):
        st.session_state.selected_chat_index = None


# -------------------------------
# QUIZ MODE TAB
# -------------------------------
with tab2:
    st.subheader("🧪 Interactive Quiz Mode")

    quiz_topic = st.text_input("📚 Enter a topic for the quiz")
    if st.button("🎯 Generate Quiz", key="generate_quiz"):
        if not quiz_topic.strip():
            st.warning("Please enter a topic for the quiz.")
        else:
            quiz_data = generate_quiz(quiz_topic)
            st.session_state.quiz_data = quiz_data
            st.session_state.quiz_submitted = False
            st.session_state.score = 0

    if "quiz_data" in st.session_state and not st.session_state.quiz_submitted:
        with st.form("quiz_form"):
            selected_answers = []
            all_answered = True

            for i, q in enumerate(st.session_state.quiz_data):
                st.markdown(f"**Q{i+1}: {q['question']}**")
                options = ["-- Select an answer --"] + q["options"]
                selected = st.selectbox(f"Choose one for Q{i+1}:", options, key=f"quiz_q_{i}")
                if selected == "-- Select an answer --":
                    all_answered = False
                selected_answers.append(selected)

            submitted = st.form_submit_button("✅ Submit Quiz")
            if submitted:
                if not all_answered:
                    st.warning("⚠️ Please answer all questions.")
                else:
                    score = sum(
                        1 for i, q in enumerate(st.session_state.quiz_data)
                        if selected_answers[i] == q["answer"]
                    )
                    st.session_state.quiz_submitted = True
                    st.session_state.score = score

    if st.session_state.quiz_submitted:
        st.success(f"🎉 Your Score: {st.session_state.score} / {len(st.session_state.quiz_data)}")
        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"**Q{i+1}: {q['question']}**")
            st.markdown(f"✅ Correct Answer: **{q['answer']}**")
