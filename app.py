import streamlit as st
from ragSys import RAG
from youtube_transcript import get_transcript
from bot import Bot
from dotenv import load_dotenv

load_dotenv()

st.title('Youtube Video QA')

col1, spacer, col2 = st.columns([1,0.3,1])

with col1:

    video_link =  st.text_input('Enter Youtube Video Link', label_visibility='visible')
    if video_link.find('youtube.com/watch?v=') == -1:
        st.error('Invalid YouTube Video Link')
    else:
        st.markdown('<hr>', unsafe_allow_html=True)
        st.video(video_link)

    def get_videoID(link: str):
        return link[link.find('?v=')+3:]


    if 'rag' not in st.session_state:
        st.session_state['rag'] = None
    if 'bot' not in st.session_state:
        st.session_state['bot'] = None
    if 'transcript' not in st.session_state:
        st.session_state['transcript'] = None


    if video_link.find('youtube.com/watch?v=') != -1:
        video_id = get_videoID(video_link)
        transcript = get_transcript(video_id)
        st.session_state.transcript = transcript
        if st.session_state.transcript:
            pass
        else:
            st.error('Transcript Not Loaded!')
    else:
        st.error('Please enter a valid YouTube Video Link')

    if st.session_state.transcript:
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader('Summary')
        if st.session_state.bot:
            pass
        else:
            st.session_state.bot = Bot()
        summary = st.session_state.bot.invoke_summary(st.session_state.transcript)
        st.markdown(f"<p>{summary}</p>", unsafe_allow_html=True)

with col2:

    if st.button('Chat with Video') :
        st.session_state.chat_history = []
        if st.session_state.transcript:
            rag = RAG(st.session_state.transcript)
            rag.build_rag()
            st.session_state.rag = rag
        else:
            st.error('Please get transcript first')


    if st.session_state.bot and st.session_state.rag:
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader('Chat💬 ')

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        col3,col4 = st.columns([1,0.4])
        with col3:
            user_question = st.text_input('Ask Anything about Video...', label_visibility='collapsed')
        with col4:
            if st.button('Go'):
                if user_question:
                    response = st.session_state.bot.invoke_chat(user_question, st.session_state.rag)
                    answer = response.generated_response
                    st.session_state.chat_history = [('Bot',answer)] + st.session_state.chat_history
                    st.session_state.chat_history = [('You',user_question)] + st.session_state.chat_history
                else:
                    st.warning('Please enter a question.')

        st.markdown('<hr>', unsafe_allow_html=True)

        for speaker, message in st.session_state.chat_history:
            if speaker == 'You':
                st.markdown(f"**🧑‍💻 You:** {message}")
            else:
                st.markdown(f"**🤖 Bot:** {message}")






