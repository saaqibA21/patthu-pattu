"""
PATHU PATTU — LOCAL MODEL SERVER (No API, No Gemini)
=====================================================
Serves the custom-built model at http://localhost:5000

Run: python local_model_server.py
"""

from flask import Flask, request, jsonify, render_template_string
from local_model import LocalPathuPattuModel

app = Flask(__name__)

print("⚙️  Loading local Pathu Pattu model (no API required)...")
model = LocalPathuPattuModel()
ok = model.load()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pathu Pattu AI — Local Custom Model</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Serif+Tamil:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root {
    --primary: #059669;
    --primary-light: #34d399;
    --secondary: #0891b2;
    --bg: #0a0f1a;
    --surface: #111827;
    --surface2: #1f2937;
    --border: rgba(52,211,153,0.15);
    --text: #e2f0ea;
    --muted: #6b8f7a;
    --radius: 14px;
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
  .header {
    padding: 0.9rem 1.5rem;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 1rem; flex-shrink: 0;
  }
  .header-icon { font-size: 1.8rem; }
  .header-info h1 {
    font-size: 1rem; font-weight: 700;
    background: linear-gradient(135deg, var(--primary-light), var(--secondary));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .header-info p { font-size: 0.75rem; color: var(--muted); margin-top: 2px; }
  .badge {
    margin-left: auto; padding: 0.25rem 0.75rem; border-radius: 100px;
    font-size: 0.72rem; font-weight: 600;
    background: rgba(52,211,153,0.12); color: var(--primary-light);
    border: 1px solid rgba(52,211,153,0.25);
  }
  .main { display: flex; flex: 1; overflow: hidden; }
  .sidebar {
    width: 250px; flex-shrink: 0;
    background: var(--surface); border-right: 1px solid var(--border);
    padding: 1rem; overflow-y: auto;
    display: flex; flex-direction: column; gap: 0.6rem;
  }
  .sidebar h3 {
    font-size: 0.68rem; text-transform: uppercase;
    letter-spacing: 0.08em; color: var(--muted); margin-bottom: 0.15rem;
  }
  .quick-btn {
    width: 100%; text-align: left;
    padding: 0.55rem 0.75rem;
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 8px; color: var(--text); font-size: 0.8rem;
    cursor: pointer; transition: all 0.2s; line-height: 1.4;
  }
  .quick-btn:hover { background: rgba(5,150,105,0.15); border-color: var(--primary); transform: translateX(2px); }
  .info-card {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 8px; padding: 0.7rem; font-size: 0.78rem;
    color: var(--muted); line-height: 1.8;
  }
  .info-card span { color: var(--primary-light); font-weight: 600; }
  .offline-badge {
    background: rgba(5,150,105,0.1); border: 1px solid rgba(5,150,105,0.2);
    border-radius: 8px; padding: 0.5rem 0.75rem;
    font-size: 0.75rem; color: var(--primary-light); text-align: center;
    font-weight: 500;
  }
  .chat-area { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
  .messages {
    flex: 1; padding: 1.5rem; overflow-y: auto;
    display: flex; flex-direction: column; gap: 1rem;
  }
  .message { display: flex; gap: 0.6rem; max-width: 90%; }
  .message.user { align-self: flex-end; flex-direction: row-reverse; }
  .message.bot  { align-self: flex-start; }
  .avatar {
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
  }
  .user .avatar { background: linear-gradient(135deg, #059669, #0891b2); }
  .bot  .avatar { background: var(--surface2); border: 1px solid var(--border); }
  .bubble {
    padding: 0.8rem 1rem; border-radius: var(--radius);
    font-size: 0.875rem; line-height: 1.7;
  }
  .user .bubble {
    background: linear-gradient(135deg, #059669, #0891b2);
    color: white; border-bottom-right-radius: 3px;
  }
  .bot .bubble {
    background: var(--surface2); border: 1px solid var(--border);
    color: var(--text); border-bottom-left-radius: 3px;
    font-family: 'Noto Serif Tamil', 'Inter', sans-serif;
    white-space: pre-wrap;
  }
  .source-tag {
    font-size: 0.7rem; color: var(--muted); margin-top: 0.4rem;
    display: flex; align-items: center; gap: 0.4rem;
  }
  .source-tag span {
    background: rgba(52,211,153,0.1); border: 1px solid rgba(52,211,153,0.2);
    border-radius: 4px; padding: 0.1rem 0.4rem; color: var(--primary-light);
    font-weight: 500;
  }
  .confidence-bar {
    display: inline-block; height: 4px; border-radius: 2px; margin-left: 0.5rem;
    background: linear-gradient(90deg, #059669, #34d399);
    vertical-align: middle;
  }
  .typing { display: flex; gap: 5px; align-items: center; padding: 0.8rem 1rem; }
  .typing span {
    width: 7px; height: 7px;
    background: var(--primary-light); border-radius: 50%;
    animation: bounce 1.1s infinite;
  }
  .typing span:nth-child(2) { animation-delay: 0.2s; }
  .typing span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes bounce {
    0%,60%,100% { transform: translateY(0); }
    30% { transform: translateY(-7px); }
  }
  .input-bar {
    padding: 0.9rem 1.5rem; border-top: 1px solid var(--border);
    background: var(--surface); display: flex; gap: 0.65rem; align-items: flex-end;
    flex-shrink: 0;
  }
  textarea {
    flex: 1; background: var(--surface2); border: 1px solid var(--border);
    border-radius: 10px; color: var(--text); padding: 0.7rem 0.9rem;
    font-size: 0.875rem; font-family: inherit; resize: none; outline: none;
    max-height: 110px; transition: border-color 0.2s;
  }
  textarea:focus { border-color: var(--primary); }
  textarea::placeholder { color: var(--muted); }
  .send-btn {
    width: 42px; height: 42px; border-radius: 10px; border: none;
    background: linear-gradient(135deg, #059669, #0891b2);
    color: white; font-size: 1rem; cursor: pointer;
    transition: transform 0.2s, opacity 0.2s;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
  }
  .send-btn:hover { transform: scale(1.05); }
  .send-btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
  .welcome { text-align: center; padding: 3rem 2rem; color: var(--muted); }
  .welcome h2 {
    font-size: 1.4rem;
    background: linear-gradient(135deg, var(--primary-light), var(--secondary));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
  }
  .welcome p { font-size: 0.85rem; line-height: 1.7; }
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 100px; }
</style>
</head>
<body>

<div class="header">
  <div class="header-icon">🧠</div>
  <div class="header-info">
    <h1>Pathu Pattu AI — Custom Local Model</h1>
    <p id="modelInfo">Loading model...</p>
  </div>
  <div class="badge">🔒 100% Offline · No API · Your Data</div>
</div>

<div class="main">
  <div class="sidebar">
    <div class="offline-badge">🟢 Fully Offline Model<br>No internet needed</div>

    <h3 style="margin-top:0.4rem">Quick Test Questions</h3>
    <button class="quick-btn" onclick="ask('What is Pathu Pattu?')">What is Pathu Pattu?</button>
    <button class="quick-btn" onclick="ask('திருமுருகாற்றுப்படை')">திருமுருகாற்றுப்படை</button>
    <button class="quick-btn" onclick="ask('நக்கீரர் யார்?')">நக்கீரர் யார்?</button>
    <button class="quick-btn" onclick="ask('மதுரைக்காஞ்சி')">மதுரைக்காஞ்சி</button>
    <button class="quick-btn" onclick="ask('Karikal Chola')">Karikal Chola</button>
    <button class="quick-btn" onclick="ask('குறிஞ்சிப்பாட்டு மலர்கள்')">குறிஞ்சிப்பாட்டு மலர்கள்</button>
    <button class="quick-btn" onclick="ask('பட்டினப்பாலை புகார் நகர்')">பட்டினப்பாலை புகார்</button>
    <button class="quick-btn" onclick="ask('U.V. Swaminatha Iyer')">U.V. Swaminatha Iyer</button>
    <button class="quick-btn" onclick="ask('முல்லைப்பாட்டு')">முல்லைப்பாட்டு</button>
    <button class="quick-btn" onclick="ask('sangam era history')">Sangam Era History</button>

    <h3 style="margin-top:0.4rem">Model Info</h3>
    <div class="info-card" id="statsBox">Loading...</div>
  </div>

  <div class="chat-area">
    <div class="messages" id="messages">
      <div class="welcome">
        <h2>🧠 Custom AI · Trained on YOUR Data</h2>
        <p>This model was built entirely from the OCR-scanned pages<br>
        of <strong>பத்துப்பாட்டு.pdf</strong>.<br><br>
        No Gemini. No OpenAI. No internet.<br>
        Every answer comes directly from the book.</p>
      </div>
    </div>
    <div class="input-bar">
      <textarea id="input" rows="1"
        placeholder="கேள்வி கேளுங்கள் | Ask a question... (Enter to send)"
        onkeydown="handleKey(event)" oninput="autoResize(this)"></textarea>
      <button class="send-btn" id="sendBtn" onclick="sendMessage()">➤</button>
    </div>
  </div>
</div>

<script>
let isLoading = false;

fetch('/stats').then(r => r.json()).then(d => {
  document.getElementById('modelInfo').textContent =
    d.chunks + ' chunks · ' + d.pages + ' pages · offline';
  document.getElementById('statsBox').innerHTML =
    'Chunks: <span>' + d.chunks + '</span><br>' +
    'Pages:  <span>' + d.pages + '</span><br>' +
    'Dim:    <span>' + d.dim + '</span><br>' +
    'Built:  <span>' + d.built + '</span>';
});

function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
}
function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 110) + 'px';
}
function ask(q) { document.getElementById('input').value = q; sendMessage(); }

function addMsg(text, type) {
  const msgs = document.getElementById('messages');
  const w = msgs.querySelector('.welcome');
  if (w) w.remove();
  const d = document.createElement('div');
  d.className = 'message ' + type;
  d.innerHTML = '<div class="avatar">' + (type==='user'?'👤':'🧠') + '</div>' +
    '<div class="bubble">' + esc(text) + '</div>';
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
}

function addBotMsg(text, pages, confidence) {
  const msgs = document.getElementById('messages');
  const d = document.createElement('div');
  d.className = 'message bot';
  const confPct = Math.round(confidence * 100);
  const barW = Math.round(confPct * 1.2);
  d.innerHTML = '<div class="avatar">🧠</div><div>' +
    '<div class="bubble">' + esc(text) + '</div>' +
    '<div class="source-tag">📖 From pages: ' +
    pages.map(p => '<span>' + p + '</span>').join(' ') +
    ' · Confidence: ' + confPct + '%' +
    '<span class="confidence-bar" style="width:' + barW + 'px"></span></div>' +
    '</div>';
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
}

function showTyping() {
  const msgs = document.getElementById('messages');
  const d = document.createElement('div');
  d.className = 'message bot'; d.id = 'typing';
  d.innerHTML = '<div class="avatar">🧠</div><div class="bubble typing"><span></span><span></span><span></span></div>';
  msgs.appendChild(d); msgs.scrollTop = msgs.scrollHeight;
}
function hideTyping() { const t=document.getElementById('typing'); if(t) t.remove(); }

function esc(t) {
  return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

async function sendMessage() {
  if (isLoading) return;
  const inp = document.getElementById('input');
  const q = inp.value.trim(); if (!q) return;
  inp.value = ''; inp.style.height = 'auto';
  isLoading = true; document.getElementById('sendBtn').disabled = true;
  addMsg(q, 'user'); showTyping();
  try {
    const res = await fetch('/ask', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({question: q})
    });
    const d = await res.json();
    hideTyping();
    addBotMsg(d.answer, d.pages || [], d.confidence || 0);
  } catch(e) {
    hideTyping(); addMsg('⚠️ Server error: ' + e.message, 'bot');
  }
  isLoading = false; document.getElementById('sendBtn').disabled = false;
  inp.focus();
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/stats")
def stats():
    return jsonify({
        "chunks": model.meta.get("total_chunks", 0),
        "pages": model.meta.get("total_pages", 0),
        "dim": model.meta.get("dimension", 0),
        "built": model.meta.get("built_at", "not yet")
    })

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question"}), 400

    answer, pages, confidence = model.answer(question, top_k=8, verbose=True)
    return jsonify({
        "answer": answer,
        "pages": pages,
        "confidence": confidence
    })

if __name__ == "__main__":
    if ok:
        print("\n" + "="*50)
        print("  🧠 PATHU PATTU LOCAL MODEL SERVER")
        print("  Open: http://localhost:5000")
        print("  100% Offline — No Gemini — Your Data")
        print("="*50 + "\n")
        app.run(port=5000, debug=False)
    else:
        print("\n❌ First build the model: python build_model.py")
