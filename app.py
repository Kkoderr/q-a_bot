import streamlit as st
from ragSys import RAG
from youtube_transcript import get_transcript
from bot import Bot
from dotenv import load_dotenv

load_dotenv()

st.title('Youtube Video QA')

video_link =  st.text_input('Enter Youtube Video Link')

def get_videoID(link: str):
    return link[link.find('?v=')+3:]


if 'rag' not in st.session_state:
    st.session_state['rag'] = None
if 'bot' not in st.session_state:
    st.session_state['bot'] = None
if 'transcript' not in st.session_state:
    st.session_state['transcript'] = None


if(st.button('Get Transcript')):

    if video_link:
        video_id = get_videoID(video_link)
        transcript = get_transcript(video_id)
        st.session_state.transcript = transcript
        st.success('Transcript Loaded!')
    else:
        st.error('Please enter a valid YouTube Video Link')


col1, col2 = st.columns(2)
with col1:
    if st.button('Get summary'):
        pass
with col2:
    if st.button('Chat with Video'):
        if st.session_state.transcript:
            rag = RAG(st.session_state.transcript)
            rag.build_rag()
            video_bot = Bot()
            st.session_state.rag = rag
            st.session_state.bot = video_bot
            st.success('ChatBot initialized Successfully!')
        else:
            st.error('Please get transcript first')

if st.session_state.bot and st.session_state.rag:
    st.subheader('Chat💬 ')

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input('')
    if st.button('Go!'):
        if user_question:
            response = st.session_state.bot.invoke(user_question, st.session_state.rag)
            answer = response.generated_response
            st.session_state.chat_history.append(('You',user_question))
            st.session_state.chat_history.append(('Bot',answer))
        else:
            st.warning('Please enter a question.')

    for speaker, message in st.session_state.chat_history:
        if speaker == 'You':
            st.markdown(f"**🧑‍💻 You:** {message}")
        else:
            st.markdown(f"**🤖 Bot:** {message}")






