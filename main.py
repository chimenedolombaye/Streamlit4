import streamlit as st
import nltk
from nltk.chat.util import Chat, reflections
import speech_recognition as sr

# Téléchargez les ressources nécessaires pour nltk
nltk.download('punkt')

# Chargez le fichier texte pour l'algorithme du chatbot

chatbot_data = open("chatbot_data.txt", "r").readlines()
pairs = [line.split('|') for line in chatbot_data]

# Prétraitez les données pour l'algorithme du chatbot
chatbot = Chat(pairs, reflections)

# Fonction pour transcrire la parole en texte
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Parlez maintenant...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        st.write("Transcription en cours...")
        try:
            text = recognizer.recognize_google(audio, language="fr-FR")
            st.write("Texte transcrit : {}".format(text))
            return text
        except sr.UnknownValueError:
            st.write("Impossible de comprendre l'audio.")
            return ""
        except sr.RequestError as e:
            st.write("Erreur lors de la requête à l'API Google : {}".format(e))
            return ""

# Fonction du chatbot qui prend à la fois le texte et la parole de l'utilisateur
def chatbot_response(input_text):
    if input_text.lower() == "parole":
        text_input = speech_to_text()
    else:
        text_input = input_text
    response = chatbot.respond(text_input)
    return response

# Créez une application Streamlit
def main():
    st.title("Chatbot avec Reconnaissance Vocale")

    user_input = st.text_input("Saisissez votre message ici :")

    if st.button("Envoyer"):
        st.write("Vous : {}".format(user_input))
        bot_response = chatbot_response(user_input)
        st.write("Chatbot : {}".format(bot_response))

if __name__ == "__main__":
    main()
