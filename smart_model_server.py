"""
PATHU PATTU — SMART HYBRID MODEL SERVER (V3 - OpenAI Integrated)
================================================================
Architecture:
  1. FAISS vector search finds the most relevant pages from YOUR OCR data (local, offline)
  2. Those pages are sent as context to a generative model to compose a proper answer
  3. Generative backend (tries in order):
       a) OpenAI (GPT-4o-mini - Primary, high quality)
       b) Gemini (1.0 Pro - Backup)
       c) Smart formatter (Local extraction)

Run: python smart_model_server.py
Open: http://localhost:5000
"""

from flask import Flask, request, jsonify, render_template_string
from local_model import LocalPathuPattuModel
import urllib.request
import json
import os
import re
import time
from openai import OpenAI

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

app = Flask(__name__)

# Load local knowledge base
print("⚙️  Loading local vector model...")
model = LocalPathuPattuModel()
ok = model.load()

# Config
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

# Simple Response Cache to speed up repeated questions
response_cache = {}

openai_client = None
if OPENAI_KEY:
    openai_client = OpenAI(api_key=OPENAI_KEY)
    print("✅ OpenAI client initialized!")

def try_openai(question, context):
    """Use OpenAI GPT-4o-mini for very high quality synthesis."""
    if not openai_client:
        return None
    
    prompt = f"""You are a world-class Tamil historian and literary scholar of Pathu Pattu (பத்துப்பாட்டு).
Your goal is to provide a masterfully written, accurate, and deeply informative answer based on the provided scans of the original book.

=== ORIGINAL BOOK SCANS (OCR) ===
{context[:8000]}
=== END OF SCANS ===

USER QUESTION: {question}

INSTRUCTIONS:
1. Synthesize a professional, smooth answer. DO NOT just list chunks.
2. If in Tamil, use modern literary Tamil that is easy to understand but retains scholarly depth.
3. Use the scans as the primary evidence. If they refer to specific page numbers, respect those contexts.
4. Format with bold terms and bullet points where helpful.
5. If the question is in English, answer in English. If in Tamil, answer in Tamil.

MASTERFUL RESPONSE:"""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=600 # Faster generation
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = f"OpenAI Error: {str(e)}"
        print(error_msg)
        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}\n")
        return None

def try_gemini(question, context, api_key):
    """Try Gemini 1.0 Pro as a backup."""
    model_name = "gemini-1.0-pro"
    
    prompt = f"""You are an elite Tamil scholar specializing in Pathu Pattu (பத்துப்பாட்டு).
Provide a high-quality, detailed answer based on the following book scans.

BOOK SCANS:
{context[:6000]}

USER QUESTION: {question}

INSTRUCTIONS:
1. Synthesize a professional answer from the scans.
2. If in Tamil, use modern literary Tamil.
3. Be professional and detailed.

ANSWER:"""

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode()

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        if "candidates" in result and result["candidates"]:
            return result["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"Gemini Error: {e}")
    return None

def smart_format(question, results):
    """Excellent fallback extraction."""
    if not results:
        return "மன்னிக்கவும், இந்தப் புத்தகத்தில் உங்கள் கேள்விக்கான தகவல்கள் கிடைக்கவில்லை."

    from collections import defaultdict
    pages_map = defaultdict(list)
    for r in results:
        pages_map[r['page']].append(r['text'])

    ans = ["### 📚 தரவு திரட்டு (Extracted Data)\n"]
    ans.append(f"உங்கள் கேள்வி: **{question}**\n")
    ans.append("தற்போது நேரடித் தகவல்கள் மட்டும் காட்டப்படுகின்றன (AI Synthesis Unavailable):\n")
    
    for page in sorted(pages_map.keys()):
        ans.append(f"#### 📄 பக்கம் {page}")
        for txt in pages_map[page]:
            ans.append(f"> {txt.strip()}")
        ans.append("")
    return "\n".join(ans)

# ---- UI ----
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pathu Pattu AI — OpenAI Powered</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Serif+Tamil:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0d1117; --surface: #161b22; --surface2: #21262d;
    --border: rgba(48,54,61,0.7);
    --primary: #2f81f7; --accent: #79c0ff; --green: #3fb950;
    --text: #c9d1d9; --muted: #8b949e; --radius: 12px;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);height:100vh;display:flex;flex-direction:column;overflow:hidden}
  .header{padding:1rem 1.5rem;background:var(--surface);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:1rem;flex-shrink:0}
  .title h1{font-size:1rem;font-weight:700;color:var(--accent)}
  .title p{font-size:.75rem;color:var(--muted)}
  .engine-badge{margin-left:auto;padding:.3rem .9rem;border-radius:100px;font-size:.72rem;font-weight:600;background:rgba(47,129,247,0.1);color:var(--primary);border:1px solid var(--primary)}
  .main{display:flex;flex:1;overflow:hidden}
  .sidebar{width:260px;flex-shrink:0;background:var(--surface);border-right:1px solid var(--border);padding:1.2rem;overflow-y:auto;display:flex;flex-direction:column;gap:.7rem}
  .sidebar h3{font-size:.68rem;text-transform:uppercase;color:var(--muted);margin-bottom:.2rem}
  .qbtn{width:100%;text-align:left;padding:.6rem .8rem;background:var(--surface2);border:1px solid var(--border);border-radius:10px;color:var(--text);font-size:.8rem;cursor:pointer;transition:all .2s}
  .qbtn:hover{background:rgba(47,129,247,0.15);border-color:var(--primary)}
  .chat-area{flex:1;display:flex;flex-direction:column;overflow:hidden}
  .msgs{flex:1;padding:1.5rem;overflow-y:auto;display:flex;flex-direction:column;gap:1.2rem}
  .msg{display:flex;gap:.8rem;max-width:90%}
  .msg.user{align-self:flex-end;flex-direction:row-reverse}
  .bub{padding:.9rem 1.1rem;border-radius:var(--radius);font-size:.9rem;line-height:1.75}
  .user .bub{background:var(--primary);color:#fff;border-bottom-right-radius:2px}
  .bot .bub{background:var(--surface2);border:1px solid var(--border);color:var(--text);border-bottom-left-radius:2px;white-space:pre-wrap;font-family:'Noto Serif Tamil','Inter',sans-serif}
  .meta{font-size:.7rem;color:var(--muted);margin-top:.4rem;display:flex;gap:.5rem;align-items:center}
  .page-tag{background:rgba(121,192,255,0.1);border:1px solid rgba(121,192,255,0.2);border-radius:4px;padding:1px 6px;color:var(--accent)}
  .input-bar{padding:1.25rem 1.5rem;border-top:1px solid var(--border);background:var(--surface);display:flex;gap:.8rem;align-items:flex-end}
  textarea{flex:1;background:var(--surface2);border:1px solid var(--border);border-radius:10px;color:var(--text);padding:.75rem 1rem;font-size:.9rem;resize:none;outline:none;max-height:120px}
  button.sbtn{background:var(--primary);color:#fff;border:none;padding:.75rem 1.5rem;border-radius:10px;font-weight:600;cursor:pointer}
  .welcome{text-align:center;padding:3rem 1.5rem;color:var(--muted)}
  .welcome h2{color:var(--accent);margin-bottom:.5rem}
</style>
</head>
<body>
<div class="header">
  <div class="logo">🧬</div>
  <div class="title">
    <h1>Pathu Pattu AI — OpenAI Enhanced</h1>
    <p>Semantic Vector Retrieval + GPT-4o-mini Synthesis</p>
  </div>
  <div class="engine-badge" id="badge">Initializing...</div>
</div>
<div class="main">
  <div class="sidebar">
    <h3>Classic Questions</h3>
    <button class="qbtn" onclick="ask('What is Pathu Pattu?')">What is Pathu Pattu?</button>
    <button class="qbtn" onclick="ask('பத்துப்பாட்டு நூல்கள் யாவை?')">பத்துப்பாட்டு நூல்கள்</button>
    <button class="qbtn" onclick="ask('Who is the author of Thirumurugaatruppadai?')">Author of Thirumurug...</button>
    <button class="qbtn" onclick="ask('நக்கீரரைப் பற்றி கூறு')">நக்கீரர் யார்?</button>
    <button class="qbtn" onclick="ask('Tell me about Karikal Chola')">Karikal Chola</button>
    <button class="qbtn" onclick="ask('Shortest book in Pathu Pattu?')">Shortest book?</button>
    <button class="qbtn" onclick="ask('மதுரைக்காஞ்சியின் சிறப்புகள்')">மதுரைக்காஞ்சி</button>
  </div>
  <div class="chat-area">
    <div class="msgs" id="msgs">
      <div class="welcome">
        <h2>📚 Master the 10 Sangam Classics</h2>
        <p>Ask anything about Pathu Pattu. Your query will be matched against 814 pages of original scans and synthesized by GPT-4o-mini.</p>
      </div>
    </div>
    <div class="input-bar">
      <textarea id="inp" rows="1" placeholder="Type your scholarly question here..."></textarea>
      <button class="sbtn" onclick="send()">Ask</button>
    </div>
  </div>
</div>
<script>
let busy=false;
let engineName = "Local Extractor";

fetch('/info').then(r=>r.json()).then(d=>{
  document.getElementById('badge').textContent = "Engine: " + d.engine;
  engineName = d.engine;
});

function ask(q){document.getElementById('inp').value=q;send();}
function esc(t){return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function addMsg(t,type,meta=""){
  const m=document.getElementById('msgs');
  m.querySelector('.welcome')?.remove();
  const d=document.createElement('div');d.className=`msg ${type}`;
  d.innerHTML=`<div class="bub">${esc(t)}</div>` + (meta?`<div class="meta">${meta}</div>`:"");
  m.appendChild(d);m.scrollTop=m.scrollHeight;
}
async function send(){
  if(busy)return;
  const i=document.getElementById('inp');
  const q=i.value.trim();if(!q)return;
  i.value='';busy=true;
  addMsg(q,'user');
  const d=document.createElement('div');d.className='msg bot';d.innerHTML='<div class="bub">Synthesizing response...</div>';
  document.getElementById('msgs').appendChild(d);
  try{
    const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
    const res=await r.json();
    const pgTags=res.pages.map(p=>`<span class="page-tag">p.${p}</span>`).join(' ');
    d.innerHTML=`<div class="bub">${esc(res.answer)}</div><div class="meta">📖 ${pgTags} | ✨ ${res.engine}</div>`;
  }catch(e){d.innerHTML='<div class="bub">Error connecting to server.</div>';}
  busy=false;document.getElementById('msgs').scrollTop=document.getElementById('msgs').scrollHeight;
}
</script>
</body>
</html>
"""

@app.route("/")
def index(): return render_template_string(HTML)

@app.route("/info")
def info():
    e = "Local Extractor"
    if OPENAI_KEY: e = "GPT-4o-mini"
    elif GEMINI_KEY: e = "Gemini-Pro"
    return jsonify({"chunks": model.meta.get("total_chunks", 0), "pages": model.meta.get("total_pages", 0), "engine": e})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    q = data.get("question", "").strip()
    
    # Check cache first (for exact matches)
    if q in response_cache:
        print(f"⚡ Cache Hit for: {q[:30]}...")
        return jsonify(response_cache[q])

    results = model.search(q, top_k=5) # Reduced from 8 for speed
    pages = sorted(set(r["page"] for r in results))
    context = "\n".join([f"[Page {r['page']}] {r['text']}" for r in results])
    context = context[:4000] # Cap context for faster processing
    
    # Priority 1: OpenAI
    ans = try_openai(q, context)
    engine = "GPT-4o-mini"
    
    # Priority 2: Gemini
    if not ans and GEMINI_KEY:
        ans = try_gemini(q, context, GEMINI_KEY)
        engine = "Gemini-Pro"
    
    # Fallback: Smart Formatter
    if not ans:
        ans = smart_format(q, results)
        engine = "Local Extractor"
    
    # Store in cache
    response_cache[q] = {"answer": ans, "pages": pages, "engine": engine}
    
    return jsonify(response_cache[q])

if __name__ == "__main__":
    app.run(port=5000)
