"""
Streamlit webapp with an OpenAI chatbot

# Running

1. Create a secrets file examples/.streamlit/secrets.toml with your OpenAI API key
```
OPENAI_API_KEY="sk-..." # your actual key
```

2. Launch the webapp
```
cd examples/ 
streamlit run webapp.py
```

"""

import streamlit as st
import phospho
from openai import OpenAI
from openai.types.chat import ChatCompletionChunk
from openai._streaming import Stream


st.title("ChatGPT-like clone")

# Initialize phospho
phospho.init(
    api_key=st.secrets["PHOSPHO_API_KEY"], project_id=st.secrets["PHOSPHO_PROJECT_ID"]
)
phospho.config.BASE_URL = "https://phospho-backend-zxs3h5fuba-ew.a.run.app/v0"

# Initialize the LLM provider
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    new_message = {"role": "user", "content": prompt}
    st.session_state.messages.append(new_message)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_str_response = ""
        # Construct a query to OpenAI
        full_prompt = {
            # model is the OpenAI model we use, eg. "gpt-3.5-turbo"
            "model": st.session_state["openai_model"],
            # messages contains the whole chat history
            "messages": [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            # stream asks to return a Stream object
            "stream": True,
        }
        # Call OpenAI API and get a stream
        streaming_response: Stream[
            ChatCompletionChunk
        ] = client.chat.completions.create(**full_prompt)
        # If we iterate on streaming_response, we get a token by token response
        for response in streaming_response:
            # We add the return additional token to full_response (displayed by streamlit)
            # full_str_response += response.choices[0].delta.content or ""
            print(response)

            # TODO
            # We can log each individual response in phospho
            # phospho takes care of aggregating the tokens
            logged_content = phospho.log(input=full_prompt, output=response)
            full_str_response = logged_content["output"]
            # Display this in streamlit
            message_placeholder.markdown(full_str_response + "▌")

        # Logging only the text of the output to phospho
        # phospho.log(input=full_prompt, output=full_str_response)
        message_placeholder.markdown(full_str_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_str_response}
    )
