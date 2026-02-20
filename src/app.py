import streamlit as st
import requests

BACKEND_URL = "https://ic6b4z8qin.ap-southeast-1.awsapprunner.com/api/v1/chat"
BACKEND_BASE_URL = "https://ic6b4z8qin.ap-southeast-1.awsapprunner.com"

st.set_page_config(
    page_title="LeaseMate Policy Assistant",
    page_icon="🏠",
    layout="centered"
)

st.title("🏠 LeaseMate Policy Assistant")
st.caption("General Policy | JES | REASONING")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question about your lease policies"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    with st.spinner("Searching policies..."):
        try:
            response = requests.post(
                BACKEND_URL,
                json={"prompt": prompt},
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()

                answer = data.get("answer", "No answer returned.")
                sources = data.get("sources", [])

                with st.chat_message("assistant"):

                    st.markdown("### Answer")
                    st.markdown(answer)

                    if sources:
                        with st.expander("📌 Sources"):
                            for src in sources:
                                file_name = src.get("file_name", "Unknown document")
                                download_url = src.get("download_url")

                                st.markdown(f"**📄 {file_name}**")

                                if download_url:
                                    full_url = f"{BACKEND_BASE_URL}{download_url}"
                                    st.markdown(
                                        f"[⬇️ Source]({full_url})",
                                        unsafe_allow_html=True
                                    )

                                st.markdown("---")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            else:
                st.error("❌ Backend returned an error.")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Connection failed: {e}")
