import streamlit as st
import requests

st.set_page_config(page_title="AI Support Assistant", layout="centered")

st.title("AI Customer Support Assistant")
st.caption("Offline AI assistant with intent detection, tool routing, and short-term memory.")

st.markdown("""
This prototype uses:
- FastAPI backend
- Ollama local AI model
- Streamlit frontend
- Mock hotel and flight tools
- Memory for follow-up questions
""")

st.info("Try: show hotels in dubai → then: show cheaper ones")
st.info("Try: find flights to london → then: show cheaper ones")

user_message = st.text_input("Type your message")

if st.button("Send"):

    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"message": user_message}
    )

    result = response.json()

    st.success(result["message"])

    if result["ui_type"] == "hotel_page":

        hotels = result["data"]["hotels"]

        for hotel in hotels:
            with st.container(border=True):
                st.subheader(hotel["name"])
                st.write("Price:", hotel["price"])
                st.write("Rating:", hotel["rating"])

    elif result["ui_type"] == "flight_page":

        flights = result["data"]["flights"]

        for flight in flights:
            with st.container(border=True):
                st.subheader(flight["airline"])
                st.write("Price:", flight["price"])
                st.write("Destination:", flight["destination"])

    else:
        st.write(result["data"])