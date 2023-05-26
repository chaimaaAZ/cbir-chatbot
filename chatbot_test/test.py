import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from streamlit_bokeh_events import streamlit_bokeh_events
from google.cloud import dialogflow


if "prompts" not in st.session_state:
    st.session_state["prompts"] = [{"role": "system", "content": "You are a helpful assistant. Answer as concisely as possible with a little humor expression."}]

project_id = "tidy-tine-387913"
credentials_path = "tidy-tine-387913-2e8dac2ce6ca.json"

client = dialogflow.SessionsClient.from_service_account_json(credentials_path)

def generate_response(prompt):
    if "prompts" not in st.session_state:
        st.session_state["prompts"] = [{"role": "system", "content": "You are a helpful assistant. Answer as concisely as possible with a little humor expression."}]
    else:
        st.session_state["prompts"].append({"role": "user", "content": prompt})

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google_cloud(audio, credentials_json=open(credentials_path).read())
        st.session_state['prompts'].append({"role": "user", "content": user_input})

        # Use Dialogflow to generate a response
        session = client.session_path(project_id, "unique-session-id")
        text_input = dialogflow.TextInput(text=user_input, language_code="en")
        query_input = dialogflow.QueryInput(text=text_input)
        response = client.detect_intent(session=session, query_input=query_input)

        # Extract the response from the Dialogflow API result
        assistant_response = response.query_result.fulfillment_text
        st.session_state['prompts'].append({"role": "assistant", "content": assistant_response})

        return assistant_response

    except sr.UnknownValueError:
        print("Google Cloud Speech-to-Text could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Cloud Speech-to-Text service; {e}")

sound = BytesIO()

placeholder = st.container()

placeholder.title("Fakihi's Voice ChatBot")
stt_button = Button(label='SPEAK', button_type='success', margin = (5, 5, 5, 5), width=200)


stt_button.js_on_event("button_click", CustomJS(code="""
    var value = "";
    var rand = 0;
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en';

    document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'start'}));
    
    recognition.onspeechstart = function () {
        document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'running'}));
    }
    recognition.onsoundend = function () {
        document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'stop'}));
    }
    recognition.onresult = function (e) {
        var value2 = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
                rand = Math.random();
                
            } else {
                value2 += e.results[i][0].transcript;
            }
        }
        document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: {t:value, s:rand}}));
        document.dispatchEvent(new CustomEvent("GET_INTRM", {detail: value2}));

    }
    recognition.onerror = function(e) {
        document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'stop'}));
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    bokeh_plot = stt_button,
    events="GET_TEXT,GET_ONREC,GET_INTRM",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

tr = st.empty()

if 'input' not in st.session_state:
    st.session_state['input'] = dict(text='', session=0)

tr.text_area("Your input", value=st.session_state['input']['text'])

if result:
    if "GET_TEXT" in result:
        if result.get("GET_TEXT")["t"] != '' and result.get("GET_TEXT")["s"] != st.session_state['input']['session'] :
            st.session_state['input']['text'] = result.get("GET_TEXT")["t"]
            tr.text_area("**Your input**", value=st.session_state['input']['text'])
            st.session_state['input']['session'] = result.get("GET_TEXT")["s"]
            pass 
        
    if "GET_INTRM" in result:
        if result.get("GET_INTRM") != '':
            tr.text_area("**Your input**", value=st.session_state['input']['text']+' '+result.get("GET_INTRM"))
            pass
    if "GET_ONREC" in result:
        if result.get("GET_ONREC") == 'start':
            placeholder.image("recon.gif")
            st.session_state['input']['text'] = ''
        elif result.get("GET_ONREC") == 'running':
            placeholder.image("recon.gif")
        elif result.get("GET_ONREC") == 'stop':
            placeholder.image("recon.jpg")
            if st.session_state['input']['text'] != '':
                input = st.session_state['input']['text']
                output = generate_response(input)
                print("Generated response:", output)  # Add this line for debugging
                st.write("**ChatBot:**")
                st.write(output)
                st.session_state['input']['text'] = ''

                tts = gTTS(output, lang='en', tld='com')
                tts.write_to_fp(sound)
                st.audio(sound)

                st.session_state['prompts'].append({"role": "user", "content":input})
                st.session_state['prompts'].append({"role": "assistant", "content":output})
                pass