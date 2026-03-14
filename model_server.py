"""
PATHU PATTU MODEL TEST SERVER
==============================
Standalone Flask server to test the AI model.
Runs on http://localhost:5000 (separate from main site on port 3000)

Run: python model_server.py
Then open: http://localhost:5000
"""

from flask import Flask, request, jsonify, render_template_string
from pathu_pattu_model import PathuPattuModel, PathuPattuRAG
import time, os

API_KEY = "AIzaSyBK4euzK8NqQao7QY9O8101j9hFyjnNFOY"
KB_PATH = "knowledge_base_ocr.json"

app = Flask(__name__)

# Load the RAG model once on startup
print("⚙️  Loading Pathu Pattu AI Model...")
model = PathuPattuModel(API_KEY, KB_PATH)
ok = model.load()
if ok:
    s = model.rag.get_stats()
    print(f"✅ Model ready! {s['total_chunks']} pages indexed, {s['index_terms']:,} terms.")
else:
    print("⚠️  Knowledge base not found. Retrieval will be skipped.")

# ---- HTML Test UI ----
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pathu Pattu AI — Model Test</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Serif+Tamil:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root {
    --primary: #7c3aed;
    --primary-light: #a78bfa;
    --secondary: #db2777;
    --bg: #0f0a1a;
    --surface: #1a1030;
    --surface2: #231846;
    --border: rgba(167,139,250,0.2);
    --text: #e2d9f3;
    --muted: #9687b8;
    --user-bg: linear-gradient(135deg, #7c3aed, #db2777);
    --bot-bg: #1a1030;
    --radius: 16px;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { 
    font-family: 'Inter', sans-serif;
    background: var(--bg); 
    color: var(--text);
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* Header */
  .header {
    padding: 1rem 1.5rem;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-shrink: 0;
  }
  .header-icon { font-size: 2rem; }
  .header-info h1 { 
    font-size: 1.1rem; 
    font-weight: 700; 
    background: linear-gradient(135deg, var(--primary-light), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .header-info p { font-size: 0.78rem; color: var(--muted); margin-top: 2px; }
  .status-badge {
    margin-left: auto;
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 600;
    background: rgba(52,211,153,0.15);
    color: #34d399;
    border: 1px solid rgba(52,211,153,0.3);
  }

  /* Main layout */
  .main { display: flex; flex: 1; overflow: hidden; }

  /* Sidebar */
  .sidebar {
    width: 260px;
    flex-shrink: 0;
    background: var(--surface);
    border-right: 1px solid var(--border);
    padding: 1rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  .sidebar h3 { 
    font-size: 0.7rem; 
    text-transform: uppercase; 
    letter-spacing: 0.1em;
    color: var(--muted);
    margin-bottom: 0.25rem;
  }
  .quick-btn {
    width: 100%;
    text-align: left;
    padding: 0.6rem 0.8rem;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text);
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s;
    line-height: 1.4;
  }
  .quick-btn:hover { 
    background: rgba(124,58,237,0.2); 
    border-color: var(--primary);
    transform: translateX(3px);
  }
  .stats-box {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.75rem;
    font-size: 0.8rem;
    color: var(--muted);
    line-height: 1.7;
  }
  .stats-box span { color: var(--primary-light); font-weight: 600; }
  .lang-toggle {
    display: flex;
    gap: 0.5rem;
  }
  .lang-btn {
    flex: 1;
    padding: 0.5rem;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--surface2);
    color: var(--muted);
    cursor: pointer;
    font-size: 0.8rem;
    transition: all 0.2s;
  }
  .lang-btn.active {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
  }

  /* Chat area */
  .chat-area { 
    flex: 1; 
    display: flex; 
    flex-direction: column;
    overflow: hidden;
  }
  .messages { 
    flex: 1; 
    padding: 1.5rem; 
    overflow-y: auto; 
    display: flex; 
    flex-direction: column; 
    gap: 1rem; 
  }
  .message { display: flex; gap: 0.75rem; max-width: 85%; }
  .message.user { align-self: flex-end; flex-direction: row-reverse; }
  .message.bot { align-self: flex-start; }

  .avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
  }
  .user .avatar { background: var(--user-bg); }
  .bot .avatar  { background: var(--surface2); border: 1px solid var(--border); }

  .bubble {
    padding: 0.85rem 1.1rem;
    border-radius: var(--radius);
    line-height: 1.65;
    font-size: 0.9rem;
  }
  .user .bubble {
    background: var(--user-bg);
    color: white;
    border-bottom-right-radius: 4px;
  }
  .bot .bubble {
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    border-bottom-left-radius: 4px;
    font-family: 'Noto Serif Tamil', 'Inter', sans-serif;
  }
  .bot .bubble pre {
    white-space: pre-wrap; 
    font-family: inherit;
    font-size: 0.88rem;
  }

  /* Retrieved pages indicator */
  .retrieval-info {
    font-size: 0.72rem;
    color: var(--muted);
    padding: 0.3rem 0.6rem;
    background: rgba(124,58,237,0.08);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 6px;
    margin-top: 0.4rem;
    display: inline-block;
  }

  /* Typing indicator */
  .typing { display: flex; gap: 6px; align-items: center; padding: 0.85rem 1.1rem; }
  .typing span { 
    width: 8px; height: 8px; 
    background: var(--primary-light);
    border-radius: 50%;
    animation: bounce 1.2s infinite;
  }
  .typing span:nth-child(2) { animation-delay: 0.2s; }
  .typing span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-8px); }
  }

  /* Input bar */
  .input-bar {
    padding: 1rem 1.5rem;
    border-top: 1px solid var(--border);
    background: var(--surface);
    display: flex;
    gap: 0.75rem;
    align-items: flex-end;
    flex-shrink: 0;
  }
  textarea {
    flex: 1;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    color: var(--text);
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
    font-family: inherit;
    resize: none;
    outline: none;
    max-height: 120px;
    transition: border-color 0.2s;
  }
  textarea:focus { border-color: var(--primary); }
  textarea::placeholder { color: var(--muted); }

  .send-btn {
    width: 44px; height: 44px;
    border-radius: 12px;
    border: none;
    background: var(--user-bg);
    color: white;
    font-size: 1.1rem;
    cursor: pointer;
    transition: transform 0.2s, opacity 0.2s;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }
  .send-btn:hover { transform: scale(1.05); }
  .send-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

  /* Welcome */
  .welcome {
    text-align: center;
    padding: 3rem 2rem;
    color: var(--muted);
  }
  .welcome h2 { 
    font-size: 1.5rem;
    background: linear-gradient(135deg, var(--primary-light), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
  }
  .welcome p { font-size: 0.88rem; line-height: 1.6; }
  
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 100px; }
</style>
</head>
<body>

<div class="header">
  <div class="header-icon">📚</div>
  <div class="header-info">
    <h1>Pathu Pattu AI — Model Test</h1>
    <p id="modelInfo">Loading model stats...</p>
  </div>
  <div class="status-badge">🟢 Standalone Test</div>
</div>

<div class="main">
  <div class="sidebar">
    <h3>Language</h3>
    <div class="lang-toggle">
      <button class="lang-btn active" id="langEn" onclick="setLang('en')">English</button>
      <button class="lang-btn" id="langTa" onclick="setLang('ta')">தமிழ்</button>
    </div>

    <h3 style="margin-top:0.5rem">Quick Questions</h3>
    <button class="quick-btn" onclick="ask('What is Pathu Pattu?')">What is Pathu Pattu?</button>
    <button class="quick-btn" onclick="ask('Who wrote Thirumurugaatruppadai?')">Who wrote Thirumurugaatruppadai?</button>
    <button class="quick-btn" onclick="ask('What is the shortest book?')">Shortest book?</button>
    <button class="quick-btn" onclick="ask('Tell me about Karikal Chola')">Karikal Chola</button>
    <button class="quick-btn" onclick="ask('What flowers are in Kurinjipattu?')">Flowers in Kurinjipattu</button>
    <button class="quick-btn" onclick="ask('Describe the city of Puhar')">City of Puhar</button>
    <button class="quick-btn" onclick="ask('Who rediscovered Pathu Pattu from palm leaves?')">Who rediscovered it?</button>
    <button class="quick-btn" onclick="ask('What is Maduraikkaanchi about?')">Maduraikkaanchi</button>
    <button class="quick-btn" onclick="ask('பத்துப்பாட்டு என்றால் என்ன?')">📌 பத்துப்பாட்டு என்றால் என்ன?</button>
    <button class="quick-btn" onclick="ask('திருமுருகாற்றுப்படை பற்றி சொல்லுங்கள்')">📌 திருமுருகாற்றுப்படை</button>

    <h3 style="margin-top:0.5rem">Model Stats</h3>
    <div class="stats-box" id="statsBox">Loading...</div>
  </div>

  <div class="chat-area">
    <div class="messages" id="messages">
      <div class="welcome">
        <h2>🤖 பத்துப்பாட்டு AI</h2>
        <p>Ask any question about the 10 Sangam Tamil classics.<br>
        The model searches <strong>814 OCR-extracted pages</strong> to find answers.</p>
      </div>
    </div>
    <div class="input-bar">
      <textarea id="input" rows="1" placeholder="Ask about Pathu Pattu... (Enter to send, Shift+Enter for newline)"
        onkeydown="handleKey(event)" oninput="autoResize(this)"></textarea>
      <button class="send-btn" id="sendBtn" onclick="sendMessage()">➤</button>
    </div>
  </div>
</div>

<script>
let currentLang = 'en';
let isLoading = false;

// Load stats on startup
fetch('/stats').then(r => r.json()).then(data => {
  document.getElementById('modelInfo').textContent = 
    `${data.pages.toLocaleString()} pages · ${data.terms.toLocaleString()} terms indexed`;
  document.getElementById('statsBox').innerHTML = 
    `Pages indexed: <span>${data.pages}</span><br>` +
    `Unique terms: <span>${data.terms.toLocaleString()}</span><br>` +
    `Avg chars/page: <span>${data.avg_chars.toLocaleString()}</span><br>` +
    `OCR coverage: <span>${data.coverage}</span>`;
}).catch(() => {
  document.getElementById('modelInfo').textContent = 'Model loaded';
  document.getElementById('statsBox').textContent = 'Could not load stats';
});

function setLang(lang) {
  currentLang = lang;
  document.getElementById('langEn').classList.toggle('active', lang === 'en');
  document.getElementById('langTa').classList.toggle('active', lang === 'ta');
}

function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

function ask(question) {
  document.getElementById('input').value = question;
  sendMessage();
}

function addMessage(text, type) {
  const msgs = document.getElementById('messages');
  // Remove welcome if present
  const welcome = msgs.querySelector('.welcome');
  if (welcome) welcome.remove();
  
  const div = document.createElement('div');
  div.className = `message ${type}`;
  const icon = type === 'user' ? '👤' : '🤖';
  div.innerHTML = `
    <div class="avatar">${icon}</div>
    <div class="bubble"><pre>${escHtml(text)}</pre></div>
  `;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
  return div;
}

function addBotMessage(text, pagesFound) {
  const msgs = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = 'message bot';
  div.innerHTML = `
    <div class="avatar">🤖</div>
    <div>
      <div class="bubble"><pre>${escHtml(text)}</pre></div>
      ${pagesFound ? `<div class="retrieval-info">📄 Retrieved ${pagesFound} relevant pages from the book</div>` : ''}
    </div>
  `;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function showTyping() {
  const msgs = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = 'message bot';
  div.id = 'typing';
  div.innerHTML = `
    <div class="avatar">🤖</div>
    <div class="bubble typing"><span></span><span></span><span></span></div>
  `;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function hideTyping() {
  const t = document.getElementById('typing');
  if (t) t.remove();
}

function escHtml(text) {
  return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

async function sendMessage() {
  if (isLoading) return;
  const input = document.getElementById('input');
  const question = input.value.trim();
  if (!question) return;

  input.value = '';
  input.style.height = 'auto';
  isLoading = true;
  document.getElementById('sendBtn').disabled = true;

  addMessage(question, 'user');
  showTyping();

  try {
    const res = await fetch('/ask', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ question, language: currentLang })
    });
    const data = await res.json();
    hideTyping();
    addBotMessage(data.answer || data.error || 'No response', data.pages_found);
  } catch(err) {
    hideTyping();
    addBotMessage('⚠️ Could not reach model server. Is it running?', 0);
  }

  isLoading = false;
  document.getElementById('sendBtn').disabled = false;
  input.focus();
}
</script>
</body>
</html>
"""

# ---- API Endpoints ----

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/stats")
def stats():
    s = model.rag.get_stats()
    total_pages = 821
    return jsonify({
        "pages": s["total_chunks"],
        "terms": s["index_terms"],
        "avg_chars": s["avg_chars"],
        "coverage": f"{s['total_chunks']}/{total_pages} pages ({int(s['total_chunks']/total_pages*100)}%)"
    })

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    language = data.get("language", "en")
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    # Retrieval-only mode: find pages, then try Gemini
    results = model.rag.search(question, top_k=5)
    pages_found = len(results)
    
    # Try to get an answer with retries
    for attempt in range(3):
        try:
            answer = model.answer(question, language=language, top_k=5)
            
            # --- SAVE INTERACTION FOR FINE-TUNING ---
            try:
                dataset_entry = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "question": question,
                    "pages_retrieved": pages_found,
                    "answer": answer,
                    "engine": "Pattu LLM Main Server"
                }
                with open("qa_dataset.jsonl", "a", encoding="utf-8") as f:
                    # Note: we use json module which is imported as _json in pathu_pattu_model but we can just import json at top of file
                    import json
                    f.write(json.dumps(dataset_entry, ensure_ascii=False) + "\n")
                print(f"💾 Saved Q&A to qa_dataset.jsonl for future fine-tuning!")
            except Exception as e:
                print(f"Error saving dataset: {e}")
                
            return jsonify({"answer": answer, "pages_found": pages_found})
        except Exception as e:
            err = str(e)
            if "429" in err and attempt < 2:
                time.sleep(30)  # Wait 30s before retry
            else:
                # Return the retrieved text as fallback
                if results:
                    raw = model.rag.build_context(results, max_chars=2000)
                    return jsonify({
                        "answer": f"[API quota exceeded — showing raw book text from {pages_found} pages:]\n\n{raw}",
                        "pages_found": pages_found
                    })
                return jsonify({"answer": f"Error: {err}", "pages_found": 0})

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  🚀 PATHU PATTU MODEL TEST SERVER")
    print("  Open: http://localhost:5000")
    print("="*50 + "\n")
    app.run(port=5000, debug=False)
