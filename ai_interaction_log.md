### Task 1: (setup)
**Prompt:** Hello! I am completing a coding assignment. here is the introduction and setup needed before we begin the tasks: Week 10: ChatGPT Clone with Streamlit + Hugging Face
In this assignment you will build a functional ChatGPT-style chat application using Streamlit and the Hugging Face Inference API. Your goal is to:

Connect to the Hugging Face Inference Router API and display model responses.
Implement multi-turn conversations with chat persistence and session management.
Add response streaming and a persistent user memory panel.
Setup
Before you begin coding, set up your project carefully. You need follow each step in order to complete this assignment. AI tools will struggle to complete this in one go, and you will end up stuck in a debugging loop

1. Create your project folder in VS Code
Open VS Code.
Choose File > Open Folder… and create/open your assignment folder.
In the VS Code Explorer panel:
To create a new file, click the New File icon.
To create a new folder, click the New Folder icon.
If you need a nested folder such as .streamlit, create the folder first, then create files inside it.
Create this project structure before you start:

your-project/
├── app.py
├── requirements.txt
├── memory.json
├── ai_interaction_log.md
├── chats/
└── .streamlit/
    ├── config.toml
    └── secrets.toml
You may create additional helper files if you want, but the files above should exist from the start.

2. Create and use a virtual environment (Ask your coding assistant to do this for you)
For this assignment, use a Python virtual environment named .venv. Install packages and run Streamlit from that environment.

Create the virtual environment:

python -m venv .venv
Activate it:

macOS / Linux
source .venv/bin/activate
Windows PowerShell
.venv\Scripts\Activate.ps1
Install the required packages:

pip install streamlit requests
Add them to requirements.txt:

streamlit
requests
Run your app from the same virtual environment:

streamlit run app.py
3. Create your Streamlit configuration files
Create .streamlit/secrets.toml and add your Hugging Face token:

HF_TOKEN = "paste_your_hugging_face_token_here"
Create .streamlit/config.toml for your app theme/configuration. You may customize the values, but a file like this should exist:

[theme]
base = "dark"
primaryColor = "#ef4444"
backgroundColor = "#0f172a"
secondaryBackgroundColor = "#1e293b"
textColor = "#f8fafc"
font = "Helvetica"
4. Development expectations
Build the assignment incrementally. Complete one part at a time and test it before moving on.
Do not try to generate the full final app in one step.
The reference UI is included in the description of task 1.
Use native Streamlit components for the UI. CSS-based solutions are not allowed for this assignment.
The Hugging Face Inference API is free but rate-limited, so expect occasional delays or temporary errors.

**AI output:**
Sounds good — this is a fun build, and I’ve gotten your setup squared away so we can move into Task 1 cleanly.

What I completed

Created the virtual environment at .venv.
Installed required packages (streamlit, requests) into that environment.
Filled in requirements.txt with:
streamlit
requests
Created the Streamlit config files and populated them:
.streamlit/secrets.toml with a placeholder HF_TOKEN
.streamlit/config.toml with the theme values you provided

**Verfication Note:**
the set up looks correct. I will proceed to the next step and test more then. 

### Task 2: (Github setup)
**Prompt:**
I opened a repository through github, can you check it worked?
**AI Response:**
Totally — and nice work getting the repo created. Based on the local git info:

Remote origin is set to https://github.com/adrisner-maker/Week-10-assignment-.git.
Your branch is main and it’s tracking origin/main.
Working tree is clean (no uncommitted changes).
**Verification Note:**
Everything looks to be setup correctly and I have access to Github


### Task 3: (Task 1, Part A)
**Prompt:**
great job. here are the instructions for task 1: Task 1: Core Chat Application (100 points)
Goal: Build the foundational ChatGPT-style app in four progressive stages. Complete each part before moving to the next — each part extends the previous one.

The diagram below shows the expected layout your app should match. Your implementation does not need to be pixel-perfect, but all elements must appear in the correct locations.

Chat app layout

Part A: Page Setup & API Connection (20 points)
Requirements:

Use st.set_page_config(page_title="My AI Chat", layout="wide").
Load your Hugging Face token using st.secrets["HF_TOKEN"]. The token must never be hardcoded in app.py.
If the token is missing or empty, display a clear error message in the app. The app must not crash.
Send a single hardcoded test message (e.g. "Hello!") to the Hugging Face API using the loaded token and display the model’s response in the main area.
Handle API errors gracefully (missing token, invalid token, rate limit, network failure) with a user-visible message rather than a crash.
Success criteria (Part A): Running streamlit run app.py with a valid .streamlit/secrets.toml sends a test message and displays the model’s reply. Running it without the secrets file shows an error message instead of crashing.

**AI Response:**
What’s done (Part A)

st.set_page_config(page_title="My AI Chat", layout="wide")
Loads HF_TOKEN from st.secrets (never hardcoded)
Shows a clear error and stops if token is missing
Sends a hardcoded Hello! message to the Hugging Face Inference Router
Displays the model response
Handles API/network errors gracefully

**Verification Note:**
I had to go through a lot of errors with this step because I had extra lines in secrets.toml that were preventing the token from being read and outputting errors. Once I fixed this and ran .venv/bin/activate streamlit run app.py It opened a webpage with an AI chat displays a response. 

## Task 4: (Task 1, Part B)
**Input**
yes please, here are the directions again: Part B: Multi-Turn Conversation UI (30 points)
Requirements:

Extend Part A to replace the hardcoded test message with a real input interface.
Use native Streamlit chat UI elements. Render messages with st.chat_message(...) and collect user input with st.chat_input(...).
Add a fixed input bar at the bottom of the main area.
Store the full conversation history in st.session_state. After each exchange, append both the user message and the assistant response to the history.
Send the full message history with each API request so the model maintains context.
Render the conversation history above the input bar using default Streamlit UI elements rather than CSS-based custom chat bubbles.
The message history must scroll independently of the input bar — the input bar stays visible at all times.
Success criteria (Part B): Sending multiple messages in a row produces context-aware replies (e.g. the model remembers the user’s name from an earlier message). Messages are displayed with correct styling and the input bar remains fixed.

 

Example UI:

Screenshot 2026-03-13 at 12.07.20 PM.png
**AI Response**
Awesome — Part B is in place now, and we stayed within the native Streamlit chat components.

What’s included now

st.chat_message(...) to render the conversation
st.chat_input(...) fixed input bar at the bottom
Full message history stored in st.session_state.messages
Full history sent to the API each turn for context
Graceful error handling preserved
Updated file

app.py
**Verification Note**
I ran streamlit and entered "My name is Ally" then asked "What's my name?" and the AI responses were valid. 

## Task 5: (Task 1, Part C)
**Input:**
Everything looks good now, lets move to part C: Part C: Chat Management (25 points)
Requirements:

Add a New Chat button to the sidebar that creates a fresh, empty conversation and adds it to the sidebar chat list.
Use the native Streamlit sidebar (st.sidebar) for chat navigation.
The sidebar shows a scrollable list of all current chats, each displaying a title and timestamp.
The currently active chat must be visually highlighted in the sidebar.
Clicking a chat in the sidebar switches to it without deleting or overwriting any other chats.
Each chat entry must have a ✕ delete button. Clicking it removes the chat from the list. If the deleted chat was active, the app must switch to another chat or show an empty state.
Success criteria (Part C): Multiple chats can be created, switched between, and deleted independently. The active chat is always visually distinct.
**AI Response:**
What you now have

Sidebar chat list with timestamps
“New Chat” button creates a fresh conversation
Active chat is visually highlighted
Click any chat to switch
Delete button (✕) removes a chat and switches safely if needed
Updated file

app.py
**Verification Note:**
I created multiple chats and all of the replys are distinct and I can switch between chats. 

## Task 6: (Task 1, Part D)
**Input:**
everything works now! lets move on to part D: Part D: Chat Persistence (25 points)
Requirements:

Each chat session is saved as a separate JSON file inside a chats/ directory. Each file must store at minimum: a chat ID, a title or timestamp, and the full message history.
On app startup, all existing files in chats/ are loaded and shown in the sidebar automatically.
Returning to a previous chat and continuing the conversation must work correctly.
Deleting a chat (✕ button) must also delete the corresponding JSON file from chats/.
A generated or summarized chat title is acceptable and encouraged. The title does not need to be identical to the first user message.
Success criteria (Part D): Closing and reopening the app shows all previous chats intact in the sidebar. Continuing a loaded chat works correctly. Deleting a chat removes its file from disk.
**AI Response:**
Each chat saves to chats/<chat_id>.json
All chats are loaded from disk on app start
Deleting a chat removes its JSON file
Continuing an old chat works normally
Updated file

app.py
**Verification Note:**
Closing and reopening the app shows all previous chats intact in the sidebar. There are a lot of connection errors however, and I think clicking control+C after every step is needed.

## Task 7: (Task 2: Response Streaming)
**Input:**
Lets move on to task #2: Task 2: Response Streaming (20 points)
Goal: Display the model’s reply token-by-token as it is generated instead of waiting for the full response.

Requirements
Use the stream=True parameter in your API request and handle the server-sent event stream.
In Streamlit, use native Streamlit methods such as st.write_stream() or manually update a placeholder with st.empty() as chunks arrive.
The full streamed response must be saved to the chat history once streaming is complete.
Hint: Add stream=True to your request payload and set stream=True on the requests.post() call. The response body will be a series of data: lines in SSE format.

Note: Very small models such as meta-llama/Llama-3.2-1B-Instruct may stream so quickly that the output appears to arrive all at once. If your app is correctly receiving multiple streamed chunks but the effect is too fast to notice, you are required to add a very short delay between rendering chunks so the streaming behavior is visible in the UI.

Success criteria: Responses appear incrementally in the chat interface and are correctly saved to history.
**AI Response:**
Added stream=True to the payload and the request.
Streamed SSE chunks and rendered them incrementally.
Added a tiny delay so the streaming is visible.
Saved the full streamed response to chat history once complete.
Updated file

app.py
**Verification Note:**
I talked with the chat bot for a while and Responses appear incrementally in the chat interface and are correctly saved to history.

## Task 8: (Task 3: User Memory)
**Input:**
wonderful work, here is the task task: Task 3: User Memory (20 points)
Goal: Extract and store user preferences from conversations, then use them to personalize future responses.

Requirements
After each assistant response, make a second lightweight API call asking the model to extract any personal traits or preferences mentioned by the user in that message.
Extracted traits are stored in a memory.json file. Example categories might include name, preferred language, interests, communication style, favorite topics, or other useful personal preferences.
The sidebar displays a User Memory expander panel showing the currently stored traits.
Include a native Streamlit control to clear/reset the saved memory.
Stored memory is injected into the system prompt of future conversations so the model can personalize responses.
Implementation note: The categories above are only examples for reference. It is up to you to decide what traits to store, how to structure your memory.json, how to merge or update existing memory, and how to incorporate that memory into future prompts, as long as the final app clearly demonstrates persistent user memory and personalization.

Hint: A simple memory extraction prompt might look like: “Given this user message, extract any personal facts or preferences as a JSON object. If none, return {}”

Success criteria: User traits are extracted, displayed in the sidebar, and used to personalize subsequent responses.
**AI Response:**
After each assistant response, we make a second API call to extract traits from the latest user message.
Extracted traits are merged into memory.json.
Sidebar now has a User Memory expander with a Clear Memory button.
Memory is injected into the system prompt so future responses can personalize.
Updated file

app.py
**Verification Note:**
The first time I tested, the user memory was not being updated. the parser now attempts to extract the first {...} block even if the model adds extra text. Extraction prompt is more explicit about keys. temperature=0 for more deterministic JSON. I tested again and the user memory now updates in the panal and responses are personalized. 
