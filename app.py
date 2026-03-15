import json
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import requests
import streamlit as st

API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL_ID = "meta-llama/Llama-3.2-1B-Instruct"

st.set_page_config(page_title="My AI Chat", layout="wide")
st.title("My AI Chat")

CHAT_DIR = Path("chats")
CHAT_DIR.mkdir(exist_ok=True)
MEMORY_PATH = Path("memory.json")


def _now_label() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def _new_chat() -> dict:
    return {
        "id": uuid4().hex,
        "title": "New Chat",
        "created_at": _now_label(),
        "messages": [],
    }


def _chat_path(chat_id: str) -> Path:
    return CHAT_DIR / f"{chat_id}.json"


def _save_chat(chat: dict) -> None:
    path = _chat_path(chat["id"])
    path.write_text(json.dumps(chat, ensure_ascii=True, indent=2))


def _load_chats() -> list[dict]:
    chats = []
    for path in sorted(CHAT_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue
        if "id" not in data:
            data["id"] = path.stem
        if "title" not in data:
            data["title"] = "New Chat"
        if "created_at" not in data:
            data["created_at"] = _now_label()
        if "messages" not in data:
            data["messages"] = []
        chats.append(data)
    return chats


def _load_memory() -> dict:
    if not MEMORY_PATH.exists():
        return {}
    try:
        data = json.loads(MEMORY_PATH.read_text())
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _save_memory(memory: dict) -> None:
    MEMORY_PATH.write_text(json.dumps(memory, ensure_ascii=True, indent=2))


def _parse_json_from_text(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return {}
        try:
            data = json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError:
            return {}
    return data if isinstance(data, dict) else {}


def _extract_memory(hf_token: str, user_message: str) -> dict:
    headers = {"Authorization": f"Bearer {hf_token}"}
    prompt = (
        "Extract any personal traits or preferences from this user message as JSON. "
        "If none, return {}. Only return JSON. Use simple keys like name, interests, "
        "preferred_language, communication_style, or favorites."
    )
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": 128,
        "temperature": 0,
    }
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    if response.status_code != 200:
        return {}
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return _parse_json_from_text(content)

hf_token = st.secrets.get("HF_TOKEN", "")
if not hf_token:
    st.error(
        "Missing Hugging Face token. Add HF_TOKEN to .streamlit/secrets.toml to run the app."
    )
    st.stop()

if "chats_loaded" not in st.session_state:
    st.session_state.chats = _load_chats()
    st.session_state.chats_loaded = True

if "active_chat_id" not in st.session_state:
    if st.session_state.chats:
        st.session_state.active_chat_id = st.session_state.chats[0]["id"]
    else:
        first_chat = _new_chat()
        st.session_state.chats.append(first_chat)
        st.session_state.active_chat_id = first_chat["id"]
        _save_chat(first_chat)

if "memory" not in st.session_state:
    st.session_state.memory = _load_memory()


def _get_active_chat() -> dict:
    for chat in st.session_state.chats:
        if chat["id"] == st.session_state.active_chat_id:
            return chat
    return {}


def _set_active_chat(chat_id: str) -> None:
    st.session_state.active_chat_id = chat_id


def _delete_chat(chat_id: str) -> None:
    st.session_state.chats = [
        chat for chat in st.session_state.chats if chat["id"] != chat_id
    ]
    path = _chat_path(chat_id)
    if path.exists():
        path.unlink()
    if st.session_state.active_chat_id == chat_id:
        if st.session_state.chats:
            st.session_state.active_chat_id = st.session_state.chats[0]["id"]
        else:
            st.session_state.active_chat_id = ""

with st.sidebar:
    st.header("Chats")
    if st.button("New Chat", use_container_width=True):
        new_chat = _new_chat()
        st.session_state.chats.insert(0, new_chat)
        st.session_state.active_chat_id = new_chat["id"]
        _save_chat(new_chat)

    chat_list = st.container(height=360)
    with chat_list:
        if not st.session_state.chats:
            st.caption("No chats yet. Start a new one!")
        for chat in st.session_state.chats:
            is_active = chat["id"] == st.session_state.active_chat_id
            cols = st.columns([0.78, 0.22])
            label = f"{chat['title']}  \n{chat['created_at']}"
            with cols[0]:
                st.button(
                    label,
                    key=f"select_{chat['id']}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary",
                    on_click=_set_active_chat,
                    args=(chat["id"],),
                )
            with cols[1]:
                st.button(
                    "✕",
                    key=f"delete_{chat['id']}",
                    use_container_width=True,
                    on_click=_delete_chat,
                    args=(chat["id"],),
                )
    with st.expander("User Memory", expanded=True):
        if st.session_state.memory:
            st.json(st.session_state.memory)
        else:
            st.caption("No saved traits yet.")
        if st.button("Clear Memory", use_container_width=True):
            st.session_state.memory = {}
            _save_memory(st.session_state.memory)

active_chat = _get_active_chat()
messages = active_chat.get("messages", []) if active_chat else []

if not active_chat:
    st.info("Start a new chat from the sidebar to begin.")
    st.stop()

for message in messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_prompt = st.chat_input("Type your message...")
if user_prompt:
    if active_chat["title"] == "New Chat":
        active_chat["title"] = user_prompt[:30].strip() or "New Chat"
    active_chat["messages"].append({"role": "user", "content": user_prompt})
    _save_chat(active_chat)
    with st.chat_message("user"):
        st.write(user_prompt)

    headers = {"Authorization": f"Bearer {hf_token}"}
    api_messages = active_chat["messages"]
    if st.session_state.memory:
        memory_block = json.dumps(st.session_state.memory, ensure_ascii=True, indent=2)
        system_prompt = (
            "You are a helpful assistant. Personalize responses using this user memory:\n"
            f"{memory_block}"
        )
        api_messages = [{"role": "system", "content": system_prompt}] + api_messages
    payload = {
        "model": MODEL_ID,
        "messages": api_messages,
        "max_tokens": 256,
        "stream": True,
    }

    try:
        response = requests.post(
            API_URL, headers=headers, json=payload, timeout=30, stream=True
        )
        if response.status_code != 200:
            detail = ""
            try:
                detail = json.dumps(response.json(), ensure_ascii=True)
            except Exception:
                detail = response.text
            st.error(
                "API request failed. Check your token, rate limits, and network connection."
            )
            st.code(detail)
        else:
            with st.chat_message("assistant"):
                placeholder = st.empty()
                streamed_text = ""
                for raw_line in response.iter_lines(decode_unicode=True):
                    if not raw_line:
                        continue
                    if not raw_line.startswith("data: "):
                        continue
                    data_str = raw_line[len("data: ") :].strip()
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        delta = chunk["choices"][0]["delta"].get("content", "")
                    except (json.JSONDecodeError, KeyError, IndexError, TypeError):
                        continue
                    if not delta:
                        continue
                    streamed_text += delta
                    placeholder.write(streamed_text)
                    time.sleep(0.02)

            active_chat["messages"].append(
                {"role": "assistant", "content": streamed_text}
            )
            _save_chat(active_chat)
            try:
                extracted = _extract_memory(hf_token, user_prompt)
            except requests.RequestException:
                extracted = {}
            if extracted:
                st.session_state.memory.update(extracted)
                _save_memory(st.session_state.memory)
    except requests.RequestException as exc:
        st.error("Network error while contacting the Hugging Face API.")
        st.code(str(exc))
    except (KeyError, IndexError, TypeError) as exc:
        st.error("Unexpected response format from the Hugging Face API.")
        st.code(str(exc))
