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

def try_openai(question, context, history=None):
    """Use OpenAI GPT-4o-mini for very high quality synthesis."""
    if not openai_client:
        return None
        
    history_str = ""
    if history:
        history_str = "\n=== RECENT CONVERSATION HISTORY (MEMORY) ===\n"
        for item in history:
            history_str += f"User: {item.get('question', '')}\nPattu LLM: {item.get('answer', '')}\n\n"
        history_str += "=== END OF MEMORY ===\n"
    
    prompt = f"""You are Pattu LLM, a world-class Tamil historian and literary scholar AI of Pathu Pattu (பத்துப்பாட்டு).
You were created and founded by Mohammed Saaqib and his team.

Your goal is to provide a masterfully written, highly simplified, and deeply informative answer based on the provided scans and texts. Focus on providing simplified meanings and data for better understanding, breaking down complex ancient Tamil concepts into easy-to-digest formats.

=== LOCAL DATA & BOOK SCANS ===
{context[:8000]}
=== END OF DATA ===
{history_str}
USER QUESTION: {question}

INSTRUCTIONS:
1. Identify yourself as Pattu LLM if asked about your identity or name.
2. Acknowledge your creators as "Mohammed Saaqib and his team" if asked about your founder, creator, or who made you.
3. Synthesize a professional, smooth answer. DO NOT just list chunks.
4. ALWAYS answer in Tamil (தமிழில்), even if the question is in English. This is a strict requirement.
5. If asked for the lines of a song (பாடல் வரிகள்), provide the full original lines found in the context. DO NOT summarize them unless specifically asked.
6. Use modern literary Tamil that is easy to understand but retains scholarly depth. Ensure archaic Tamil is explained with simplified meanings.
7. Provide a "Simplified Meaning" (எளிய விளக்கம்) section whenever the query involves understanding literature or poems.
8. Use the data as the primary evidence. If they refer to specific page numbers, respect those contexts.
9. Format with bold terms and bullet points where helpful.

MASTERFUL RESPONSE (IN TAMIL ONLY):"""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1000 # Increased generation tokens for full lines and simplified meanings
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = f"OpenAI Error: {str(e)}"
        print(error_msg)
        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}\n")
        return None

def try_gemini(question, context, api_key, history=None):
    """Try Gemini 1.0 Pro as a backup."""
    model_name = "gemini-1.0-pro"
    
    history_str = ""
    if history:
        history_str = "\nRECENT CONVERSATION HISTORY:\n"
        for item in history:
            history_str += f"User: {item.get('question', '')}\nPattu LLM: {item.get('answer', '')}\n\n"
    
    prompt = f"""You are Pattu LLM, an elite Tamil scholar AI specializing in Pathu Pattu (பத்துப்பாட்டு).
You were created by Mohammed Saaqib and his team.

Provide a high-quality, deeply simplified, and detailed answer based on the following book scans and texts.

LOCAL DATA:
{context[:6000]}
{history_str}
USER QUESTION: {question}

INSTRUCTIONS:
1. ALWAYS answer in Tamil (தமிழில்), even if the question is in English.
2. Identify yourself as Pattu LLM if asked.
3. Acknowledge your creators "Mohammed Saaqib and his team" if asked.
4. If asked for song lines, provide the original Tamil lines from the context.
5. Synthesize a professional answer from the scans. Connect archaic meanings with simple modern Tamil words.
6. Include a "Simplified Meaning" (எளிய விளக்கம்) section if explaining poems.
7. Be professional and detailed. Provide easy-to-understand explanations.

ANSWER (IN TAMIL ONLY):"""

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode("utf-8") # Explicitly use utf-8 for safety

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8")) # Explicitly use utf-8 for safety
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
<title>Pattu LLM — OpenAI Powered</title>
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
    <h1>Pattu LLM</h1>
    <p>Created by Mohammed Saaqib and his team</p>
  </div>
</div>
<div class="main">
  <div class="sidebar">
    <h3>Classic Questions</h3>
    <button class="qbtn" onclick="ask('Who created you?')">Who created you?</button>
    <button class="qbtn" onclick="ask('What is your name?')">What is your name?</button>
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
        <p>Ask anything about Pathu Pattu. Your query will be matched against original scans and texts and synthesized by Pattu LLM.</p>
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
    d.innerHTML=`<div class="bub">${esc(res.answer)}</div><div class="meta">📖 ${pgTags}</div>`;
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
    e = "Pattu Local Extractor"
    if OPENAI_KEY: e = "Pattu LLM (OpenAI)"
    elif GEMINI_KEY: e = "Pattu LLM (Gemini)"
    return jsonify({"chunks": model.meta.get("total_chunks", 0), "pages": model.meta.get("total_pages", 0), "engine": e})

@app.route("/ask", methods=["POST"])
def ask():
    """Main route for the AI Chatbot with synthesis and RAG."""
    try:
        data = request.json
        if not data or "question" not in data:
            return jsonify({"answer": "கேள்வி ஏதுமில்லை.", "pages": [], "engine": "Error"})
        
        q = data.get("question", "").strip()
        history = data.get("history", []) # Recent conversation for context
        
        # Check cache first for exact matches
        if q in response_cache:
            print(f"⚡ Cache Hit for: {q[:30]}...")
            return jsonify(response_cache[q])

        print(f"--- Question received: {q[:50]}... ---")
        
        # 1. RETRIEVE RELEVANT CONTEXT (RAG)
        # Increase top_k to 10 for better song line coverage
        results = model.search(q, top_k=10)
        pages = sorted(list(set(r["page"] for r in results)))
        
        context_parts = []
        for r in results:
            context_parts.append(f"[Page {r['page']}]: {r['text']}")
        
        context = "\n\n".join(context_parts)
        context = context[:8000] # Increased context window
        
        # 2. GENERATE ANSWER (Try OpenAI -> Gemini -> Fallback)
        ans = try_openai(q, context, history)
        engine = "Pattu LLM (OpenAI)"
        
        if not ans:
            # Try Gemini if OpenAI fails
            if GEMINI_KEY:
                ans = try_gemini(q, context, GEMINI_KEY, history)
                engine = "Pattu LLM (Gemini)"
        
        if not ans:
            # Last fallback: Local formatting
            ans = smart_format(q, results)
            engine = "Pattu Local Extractor"
        
        # Store in cache
        res_obj = {"answer": ans, "pages": pages, "engine": engine}
        response_cache[q] = res_obj
        
        # 3. SAVE INTERACTION FOR FINE-TUNING
        try:
            dataset_entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "question": q,
                "pages_retrieved": pages,
                "answer": ans,
                "engine": engine,
                "has_context": len(results) > 0
            }
            with open("qa_dataset.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(dataset_entry, ensure_ascii=False) + "\n")
        except Exception as log_e:
            print(f"Log Error: {log_e}")
            
        return jsonify(res_obj)
        
    except Exception as e:
        error_msg = f"Fatal Error in /ask: {str(e)}"
        print(error_msg)
        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {error_msg}\n")
        return jsonify({
            "answer": "மன்னிக்கவும், சர்வரில் பிழை ஏற்பட்டுள்ளது (Server Error). AI மூளை தற்போது பணிகளில் உள்ளது, சிறிது நேரம் கழித்து மீண்டும் முயலவும்.",
            "pages": [],
            "engine": "Error"
        })

if __name__ == "__main__":
    # Ensure dependencies are loaded
    model.load()
    print("✅ Pattu LLM Server is READY on port 5000")
    app.run(port=5000, host="0.0.0.0")
