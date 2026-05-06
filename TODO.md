# TODO - College Inquiry Chatbot (Streamlit UI)

- [ ] Create `app.py` as Streamlit frontend
- [ ] Configure Streamlit page (title/icon/wide layout)
- [ ] Inject custom CSS for clean white background + chat bubble styling + sticky input
- [ ] Initialize and persist `ResponseEngine` + chat history in `st.session_state`
- [ ] Implement sidebar: logo placeholder, About, Suggested Questions buttons, Chat Statistics, Clear Chat, Download Chat History
- [ ] Implement main chat area: render messages with timestamps, bot/user alignment, confidence badge under bot messages, follow-up chips after latest bot
- [ ] Add helper functions for rendering and computing statistics/export
- [ ] Run `streamlit run app.py` (if dependencies/models are present)
- [x] Create `utils/config.py` DB_PATH entry for SQLite storage
- [ ] Create `src/database.py` with `ChatDatabase` SQLite integration
- [ ] Update `src/response_engine.py` to persist logs via `ChatDatabase.log_conversation()`
- [ ] Smoke test: run `python -c "from src.response_engine import ResponseEngine; ResponseEngine().get_response('Hi')"`

