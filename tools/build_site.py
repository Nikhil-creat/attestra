"""Static site generator. Edit content here, then run: python tools/build_site.py
Designed and developed by NIKHIL CHARY SRIRAMOJU."""
import os, json
BASE = "https://nikhil-creat.github.io/questionnaire-ai/"
BRAND = "Attestra"
EMAIL = "sriramojunikhil66@gmail.com"
GH = "https://github.com/Nikhil-creat"
LI = "https://in.linkedin.com/in/nikhil-chary-sriramoju-95041b38a"
REPO = GH + "/questionnaire-ai"
UPDATED = "October 11, 2026"
OUT = os.path.join(os.path.dirname(__file__), "..", "site")
SYMBOL = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="lg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs><path d="M32 4 56 18v28L32 60 8 46V18Z" fill="none" stroke="url(#g)" stroke-width="3" stroke-linejoin="round"/><path d="M32 13 48.5 22.5v19L32 51 15.5 41.5v-19Z" fill="url(#g)" opacity=".16"/><path d="M20 33.5l8.5 8.5L45 22" fill="none" stroke="url(#g)" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round"/><circle cx="32" cy="4" r="2.6" fill="#22d3ee"/><circle cx="56" cy="46" r="2.6" fill="#8b5cf6"/><circle cx="8" cy="46" r="2.6" fill="#22d3ee"/><circle cx="45" cy="22" r="2.2" fill="#fff"/></symbol></svg>'
EXTRA = ""
if os.path.exists(os.path.join(OUT, "og.png")):
    EXTRA = f'<meta property="og:image" content="{BASE}og.png"><link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="icon-192.png">'
NAV = [("Product", "index.html#how"), ("Pricing", "pricing.html"), ("Docs", "docs.html"), ("Security", "security.html"),
       ("About", "about.html"), ("Contact", "contact.html")]

CSS = """:root{--bg:#0b0e14;--bg2:#121722;--fg:#e9ecf3;--mut:#9aa3b5;--line:#ffffff1f;--acc:#6ea8fe;--acc2:#4cc3a0;--btn:#6ea8fe;--btnfg:#07101f}
@media(prefers-color-scheme:light){:root{--bg:#f7f8fb;--bg2:#fff;--fg:#10131a;--mut:#555d70;--line:#0000001a;--btn:#2457d6;--btnfg:#fff;--acc:#2457d6;--acc2:#0a8f6a}}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:72px}
body{margin:0;font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--fg);padding-bottom:env(safe-area-inset-bottom,0)}
a{color:var(--acc)}img,svg{max-width:100%}.w{max-width:1080px;margin:auto;padding:0 18px}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:var(--bg2);padding:8px;z-index:99}
.hd{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);padding-top:env(safe-area-inset-top,0)}
.hd .w{display:flex;align-items:center;gap:16px;height:60px}.brand{font-weight:800;color:var(--fg);text-decoration:none;font-size:18px;display:flex;gap:8px;align-items:center}
.logo{width:26px;height:26px;border-radius:7px;background:linear-gradient(135deg,var(--acc),var(--acc2))}
nav{margin-left:auto;display:flex;gap:18px;align-items:center}nav a{color:var(--mut);text-decoration:none;font-size:15px}nav a:hover,nav a[aria-current]{color:var(--fg)}
.btn{display:inline-block;background:var(--btn);color:var(--btnfg)!important;padding:10px 16px;border-radius:10px;font-weight:600;text-decoration:none;border:0;cursor:pointer}
.btn.o{background:transparent;color:var(--fg)!important;border:1px solid var(--line)}#mb{display:none;background:none;border:1px solid var(--line);color:var(--fg);border-radius:8px;padding:6px 10px;font-size:18px;margin-left:auto}
@media(max-width:820px){#mb{display:block}nav{display:none;position:absolute;top:60px;left:0;right:0;flex-direction:column;align-items:stretch;background:var(--bg2);padding:14px 18px;border-bottom:1px solid var(--line);gap:12px}nav.open{display:flex}.hd .btn.hide{display:none}}
.hero{padding:64px 0 40px;text-align:center}.hero h1{font-size:clamp(32px,6vw,56px);line-height:1.1;margin:0 0 16px;letter-spacing:-.02em}
.hero p{color:var(--mut);font-size:18px;max-width:640px;margin:0 auto 24px}.cta{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.pill{display:inline-block;border:1px solid var(--line);color:var(--mut);padding:4px 12px;border-radius:99px;font-size:13px;margin-bottom:16px}
section{padding:44px 0}h2{font-size:clamp(24px,4vw,34px);margin:0 0 8px;letter-spacing:-.01em}.sub{color:var(--mut);margin:0 0 24px}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}.card{background:var(--bg2);border:1px solid var(--line);border-radius:14px;padding:18px}
.card h3{margin:0 0 6px;font-size:17px}.card p{margin:0;color:var(--mut);font-size:15px}.num{color:var(--acc);font-weight:800}
.price{font-size:32px;font-weight:800}.price small{font-size:14px;color:var(--mut);font-weight:400}.card ul{padding-left:18px;color:var(--mut);margin:10px 0}
.band{background:var(--bg2);border-block:1px solid var(--line);text-align:center}.tbl{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:15px}
td,th{text-align:left;padding:10px;border-bottom:1px solid var(--line);vertical-align:top}th{color:var(--mut);font-weight:600}
details{background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:8px 0}summary{cursor:pointer;font-weight:600}details p{color:var(--mut);margin:8px 0 0}
.page{padding:40px 0}.page h1{font-size:clamp(28px,5vw,42px);margin:0 0 8px}.page h2{font-size:22px;margin:28px 0 6px}.page p,.page li{color:var(--mut)}
footer{border-top:1px solid var(--line);background:var(--bg2);margin-top:30px;padding:36px 0 calc(24px + env(safe-area-inset-bottom,0))}
.fg{display:grid;gap:24px;grid-template-columns:2fr 1fr 1fr 1fr}@media(max-width:820px){.fg{grid-template-columns:1fr 1fr}}
footer h4{margin:0 0 10px;font-size:14px}footer a{display:block;color:var(--mut);text-decoration:none;margin:6px 0;font-size:14px}footer a:hover{color:var(--fg)}
.cr{border-top:1px solid var(--line);margin-top:24px;padding-top:16px;color:var(--mut);font-size:13px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
label{display:block;margin:12px 0 4px;font-size:14px;color:var(--mut)}input,textarea,select{width:100%;padding:10px;border-radius:10px;border:1px solid var(--line);background:var(--bg2);color:var(--fg);font:inherit}textarea{min-height:120px}pre{background:var(--bg2);border:1px solid var(--line);border-radius:10px;padding:12px;overflow-x:auto;font-size:13px}code{font-family:ui-monospace,monospace}.big{font-size:22px;color:var(--fg)}
:root{--acc:#22d3ee;--acc2:#8b5cf6;--btn:linear-gradient(135deg,#22d3ee,#8b5cf6);--btnfg:#05101c}
@media(prefers-color-scheme:light){:root{--acc:#0e7490;--acc2:#6d28d9;--btn:linear-gradient(135deg,#0e7490,#6d28d9);--btnfg:#fff}}
.logo{width:28px;height:28px;filter:drop-shadow(0 0 6px #22d3ee66)}
.btn{transition:transform .15s,box-shadow .15s}.btn:hover{transform:translateY(-1px);box-shadow:0 6px 24px #22d3ee40}
.card{transition:transform .2s,border-color .2s;backdrop-filter:blur(6px)}.card:hover{transform:translateY(-3px);border-color:var(--acc)}
.grad{background:linear-gradient(90deg,var(--acc),var(--acc2));-webkit-background-clip:text;background-clip:text;color:transparent}
.hero{position:relative;overflow:hidden;padding:72px 0 28px;background:radial-gradient(60% 50% at 50% 0,#22d3ee22,transparent),radial-gradient(40% 40% at 85% 20%,#8b5cf622,transparent)}
.hero:before{content:"";position:absolute;inset:0;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:44px 44px;-webkit-mask-image:radial-gradient(70% 70% at 50% 30%,#000,transparent);mask-image:radial-gradient(70% 70% at 50% 30%,#000,transparent)}
#fx{position:absolute;inset:0;width:100%;height:100%}.hero-in{position:relative}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--acc2);margin-right:6px;box-shadow:0 0 10px var(--acc);animation:pl 2s infinite}
@keyframes pl{50%{opacity:.35}}
.term{max-width:620px;margin:32px auto 0;text-align:left;background:#05080dd9;color:#cfe9f1;border:1px solid var(--line);border-radius:14px;padding:0 16px 14px;font:13px/1.9 ui-monospace,Menlo,monospace;box-shadow:0 0 40px #22d3ee22}
.term .bar{display:flex;gap:6px;align-items:center;padding:10px 0;color:#7c8aa0;font-size:12px}.term .bar i{width:10px;height:10px;border-radius:50%;background:#ffffff30}.term .bar span{margin-left:auto}
.ln{opacity:0;transform:translateY(4px);animation:rv .4s forwards;animation-delay:var(--d)}.ln b{color:var(--acc)}.ln.ok{color:#7ee0b5}.ln.wn{color:#f0b429}
@keyframes rv{to{opacity:1;transform:none}}
.built{font-size:13px;margin-top:18px}.pipe{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.chip{padding:8px 14px;border:1px solid var(--line);border-radius:99px;background:var(--bg2);font-size:14px;animation:gl 4.8s infinite;animation-delay:calc(var(--i)*.8s)}
@keyframes gl{0%,16%,100%{border-color:var(--line);box-shadow:none}6%{border-color:var(--acc);box-shadow:0 0 16px #22d3ee55}}
@media(prefers-reduced-motion:reduce){.ln{opacity:1;transform:none;animation:none}.chip,.dot{animation:none}html{scroll-behavior:auto}}
:focus-visible{outline:2px solid var(--acc);outline-offset:2px}"""

def head(fn, title, desc):
    url = BASE + ("" if fn == "index.html" else fn)
    ld = {"@context": "https://schema.org", "@type": "Organization", "name": BRAND, "url": BASE,
          "founder": {"@type": "Person", "name": "Nikhil Chary Sriramoju", "sameAs": [GH, LI]}, "email": EMAIL}
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}"><meta name="author" content="Nikhil Chary Sriramoju">
<meta name="theme-color" content="#0b0e14"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">{EXTRA}<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css"><script defer src="fx.js"></script><script type="application/ld+json">{json.dumps(ld)}</script></head>"""

def header(fn):
    links = "".join(f'<a href="{h}"' + (' aria-current="page"' if h == fn else "") + f">{n}</a>" for n, h in NAV)
    return f"""<body>{SYMBOL}<a class="skip" href="#main">Skip to content</a>
<header class="hd"><div class="w"><a class="brand" href="index.html"><svg class="logo" width="28" height="28" aria-hidden="true"><use href="#lg"/></svg>{BRAND}</a>
<nav id="nav" aria-label="Main">{links}<a class="btn" href="demo.html">Try the demo</a></nav>
<button id="mb" aria-label="Menu" aria-expanded="false" onclick="var n=document.getElementById('nav');var o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)">&#9776;</button></div></header><main id="main">"""

FOOT = f"""</main><footer><div class="w"><div class="fg">
<div><a class="brand" href="index.html" style="margin:0 0 8px"><svg class="logo" width="28" height="28" aria-hidden="true"><use href="#lg"/></svg>{BRAND}</a>
<p style="color:var(--mut);font-size:14px;margin:0;max-width:300px">AI agents that draft cited answers to customer security questionnaires from your own policies.</p></div>
<div><h4>Product</h4><a href="index.html#how">How it works</a><a href="pricing.html">Pricing</a><a href="docs.html">Documentation</a><a href="roi.html">ROI calculator</a><a href="demo.html">Live demo</a><a href="{REPO}">Source code</a></div>
<div><h4>Company</h4><a href="about.html">About</a><a href="security.html">Security</a><a href="contact.html">Contact</a></div>
<div><h4>Legal &amp; connect</h4><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms of Service</a><a href="{GH}" rel="noopener">GitHub</a><a href="{LI}" rel="noopener">LinkedIn</a></div></div>
<div class="cr"><span>&copy; 2026 {BRAND}. All rights reserved.</span>
<span>Designed and developed by <b>NIKHIL CHARY SRIRAMOJU</b>, Founder</span></div></div></footer></body></html>"""

def write(fn, title, desc, body):
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(head(fn, title, desc) + header(fn) + body + FOOT)

def card(t, p): return f'<div class="card"><h3>{t}</h3><p>{p}</p></div>'

HOME = f"""<div class="hero"><canvas id="fx" aria-hidden="true"></canvas><div class="w hero-in"><span class="pill"><i class="dot"></i>Early access &middot; agentic compliance AI</span>
<h1>Answer security questionnaires with <span class="grad">evidence, not guesswork.</span></h1>
<p>Attestra's AI agents draft answers from your own policies, a critic verifies every claim against its source, and your team approves. Export straight back into the buyer's spreadsheet.</p>
<div class="cta"><a class="btn" href="demo.html">Try the live demo</a><a class="btn o" href="contact.html">Get early access</a></div>
<div class="term" role="img" aria-label="Illustrative terminal output"><div class="bar"><i></i><i></i><i></i><span>illustrative output</span></div>
<div class="ln" style="--d:.2s"><b>$</b> attestra draft vendor-questionnaire.xlsx</div>
<div class="ln ok" style="--d:1.1s">&#10003; parsed questions from the spreadsheet</div>
<div class="ln ok" style="--d:1.9s">&#10003; searched your policies and evidence</div>
<div class="ln ok" style="--d:2.7s">&#10003; drafted answers with citations</div>
<div class="ln wn" style="--d:3.5s">! weak or sensitive answers escalated to a human</div>
<div class="ln ok" style="--d:4.3s">&#10003; exported answers.xlsx</div></div>
<p class="built">Stack: FastAPI &middot; pgvector &middot; LangGraph &middot; Claude API &middot; Docker</p></div></div>
<section><div class="w"><div class="pipe"><span class="chip" style="--i:0">Ingest</span><span class="chip" style="--i:1">Plan</span><span class="chip" style="--i:2">Draft</span><span class="chip" style="--i:3">Critic</span><span class="chip" style="--i:4">Human approval</span><span class="chip" style="--i:5">Export</span></div></div></section>
<section id="how"><div class="w"><h2>How it works</h2><p class="sub">From a buyer's spreadsheet to a reviewed, export-ready answer set.</p><div class="grid">
{card('<span class="num">1</span> Upload your policies','Add PDFs, Word docs, or text. We split them into searchable, citable passages.')}
{card('<span class="num">2</span> Upload the questionnaire','Drop in the buyer\'s XLSX. Questions are detected automatically.')}
{card('<span class="num">3</span> Agents draft and verify','A drafter answers only from your evidence. A critic rejects anything unsupported.')}
{card('<span class="num">4</span> Review and export','Approve or edit, then export answers with citations back into the original file.')}</div></div></section>
<section class="band"><div class="w"><h2>Built so a wrong answer never ships</h2><p class="sub">Security answers are commitments. The product is designed around that.</p><div class="grid" style="text-align:left">
{card('Every answer is cited','Each draft points to the exact passage it came from, or says "Insufficient evidence".')}
{card('Critic and escalation','Weak support, missing citations, and sensitive topics (breaches, certifications, legal) go to a human.')}
{card('Human approval','Nothing is final until a reviewer approves it. Approvals are logged.')}
{card('Answer library','Approved answers are reused for repeat questions, so each questionnaire gets faster.')}
{card('Privacy by design','Emails, phone numbers and IPs are masked before any language-model call.')}
{card('Gap and freshness insights','See which questions keep escalating and which policies are out of date.')}</div></div></section>
<section><div class="w"><h2>Frequently asked questions</h2><p class="sub">Straight answers.</p>
<details><summary>Will it make things up?</summary><p>It is built not to. Drafts must cite retrieved passages, and a critic blocks uncited or unsupported claims. When evidence is missing, the answer says so and a human decides.</p></details>
<details><summary>Which formats do you support?</summary><p>Policies: PDF, DOCX, TXT, Markdown. Questionnaires: XLSX today. Portal and Word/PDF export are on the roadmap.</p></details>
<details><summary>Where does my data go?</summary><p>The live demo runs entirely in your browser. The full product sends text to a language model only after masking personal data, and is designed for zero-retention provider settings. See the <a href="security.html">Security</a> page for what exists today and what is planned.</p></details>
<details><summary>Are you SOC 2 certified?</summary><p>No. We are an early-stage company and will publish our certification status honestly as it changes.</p></details>
<details><summary>How do I get started?</summary><p>Try the <a href="demo.html">live demo</a>, then <a href="contact.html">contact us</a> about an early-access pilot.</p></details></div></section>
<section><div class="w"><h2>On the roadmap</h2><p class="sub">Not built yet. Listed so you know where we are going.</p><div class="grid">
{card('Agentic portal filling','A browser agent that fills buyer portals, always with human sign-off.')}
{card('Chat approvals','Approve or edit escalated answers from Slack or Teams.')}
{card('Verifiable audit trail','Tamper-evident approval history you can hand to auditors.')}
{card('Evidence integrations','Sync policies and controls from Drata, Vanta, Drive and Notion.')}</div></div></section>
<section class="band"><div class="w"><h2>See it on your own questionnaire</h2><p class="sub">Send one redacted questionnaire and we will return cited drafts for you to judge.</p>
<a class="btn" href="contact.html">Request a pilot</a></div></section>"""

write("index.html", f"{BRAND}: Cited AI answers for security questionnaires",
      "AI agents draft cited answers to customer security questionnaires from your own policies. Critic-checked, human-approved, XLSX in and out.", HOME)

def tier(n, pr, items, feat=False):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'<div class="card"{" style=border-color:var(--acc)" if feat else ""}><h3>{n}</h3><div class="price">{pr}<small>/month</small></div><ul>{li}</ul><a class="btn{"" if feat else " o"}" href="contact.html">Request access</a></div>'
write("pricing.html", f"Pricing | {BRAND}", "Early-access pricing for Attestra, based on completed questionnaires.",
 f"""<div class="w page"><h1>Pricing</h1><p>Early-access pricing, charged per completed questionnaire because value scales with volume, not seats. Prices are indicative while we run pilots.</p>
<div class="grid" style="margin-top:20px">
{tier("Starter","$199",["5 questionnaires / month","1 workspace","Answer library","Email support"])}
{tier("Growth","$499",["20 questionnaires / month","Up to 5 reviewers","Gap analysis and audit log","Priority support"],True)}
{tier("Scale","$1,200+",["60+ questionnaires / month","SSO and advanced audit (planned)","Custom retention","Dedicated support"])}</div>
<p style="margin-top:20px">Extra questionnaires: $15-25 each. <b>Pilot offer:</b> design partners get a free first questionnaire and discounted early pricing in exchange for feedback. <a href="contact.html">Ask about the pilot</a>.</p></div>""")

write("security.html", f"Security | {BRAND}", "How Attestra handles data, what exists today, and what is planned.",
 f"""<div class="w page"><h1>Security</h1><p>You are trusting us with security answers, so we are specific about what is built today and what is not. Last updated {UPDATED}.</p>
<div class="tbl"><table><tr><th>Area</th><th>Status</th><th>Detail</th></tr>
<tr><td>Cited, critic-checked answers</td><td>Built</td><td>No citation means escalation to a human.</td></tr>
<tr><td>PII masking before LLM calls</td><td>Built</td><td>Emails, phone numbers and IP addresses are masked.</td></tr>
<tr><td>Audit log of approvals</td><td>Built</td><td>Uploads, runs and approvals are timestamped.</td></tr>
<tr><td>Tenant isolation (Postgres row-level security)</td><td>Designed</td><td>Schema is written; wiring to the API is in progress.</td></tr>
<tr><td>Authentication and SSO</td><td>Planned</td><td>Required before any production customer data.</td></tr>
<tr><td>Zero-retention LLM settings</td><td>Planned</td><td>Contractual and configuration controls with the model provider.</td></tr>
<tr><td>SOC 2</td><td>Not started</td><td>We will begin once paying customers justify it, and publish status honestly.</td></tr></table></div>
<h2>Live demo</h2><p>The demo on this site runs in your browser. Text you enter is not sent to our servers.</p>
<h2>Report a vulnerability</h2><p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> or use <a href="{REPO}/security/advisories">GitHub Security Advisories</a>. Please do not disclose publicly before we respond.</p></div>""")

write("about.html", f"About | {BRAND}", "About Attestra and its founder, Nikhil Chary Sriramoju.",
 f"""<div class="w page"><h1>About</h1><p>Enterprise deals stall in security review. Teams spend hours re-answering the same questions from scattered documents. We are building agents that do the first draft with evidence attached, so people only review.</p>
<h2>Our principles</h2><ul><li>Evidence first: no source, no claim.</li><li>Humans decide: automation drafts, people approve.</li><li>Honest about maturity: we publish what exists and what does not.</li></ul>
<h2>Founder</h2><div class="card"><h3>Nikhil Chary Sriramoju</h3><p>Founder, designer and developer. Final-year B.Tech Computer Science student building agentic AI, RAG and security-focused systems.</p>
<p style="margin-top:10px"><a href="{GH}" rel="noopener">GitHub</a> &middot; <a href="{LI}" rel="noopener">LinkedIn</a></p></div></div>""")

write("contact.html", f"Contact | {BRAND}", "Contact Attestra for early access, pilots and security reports.",
 f"""<div class="w page"><h1>Contact</h1><p>Request early access, ask about a pilot, or share feedback. We reply by email.</p>
<div class="grid" style="margin-top:20px">{card("Early access and pilots",f'<a href="mailto:{EMAIL}?subject=Questionnaire%20AI%20pilot">{EMAIL}</a>')}
{card("Security reports",f'<a href="mailto:{EMAIL}?subject=Security%20report">{EMAIL}</a>')}
{card("Code and issues",f'<a href="{REPO}/issues" rel="noopener">GitHub issues</a>')}
{card("Founder",f'<a href="{LI}" rel="noopener">LinkedIn</a> &middot; <a href="{GH}" rel="noopener">GitHub</a>')}</div></div>""")

write("privacy.html", f"Privacy Policy | {BRAND}", "Privacy Policy for the Attestra website and demo.",
 f"""<div class="w page"><h1>Privacy Policy</h1><p>Last updated {UPDATED}.</p>
<h2>What this site collects</h2><p>This website is static. It does not use cookies, advertising trackers or analytics. Hosting is provided by GitHub Pages, which may process standard server logs such as IP addresses under its own policy.</p>
<h2>Live demo</h2><p>Text you enter into the demo is processed in your browser and is not transmitted to us.</p>
<h2>Email</h2><p>If you email us, we use your message and address only to respond and will not sell or share them.</p>
<h2>Product data</h2><p>Terms for customer data in the hosted product will be provided in a data processing agreement before any pilot involving real documents.</p>
<h2>Your rights and contact</h2><p>To ask about or delete anything you sent us, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>""")

write("terms.html", f"Terms of Service | {BRAND}", "Terms of Service for the Attestra website and demo.",
 f"""<div class="w page"><h1>Terms of Service</h1><p>Last updated {UPDATED}.</p>
<h2>Use of the site and demo</h2><p>The site and demo are provided for evaluation. Do not enter confidential or regulated data into the demo.</p>
<h2>No guarantee of accuracy</h2><p>Drafted answers are suggestions generated from the material you supply. You are responsible for reviewing and approving every answer before sharing it with a third party.</p>
<h2>No warranty and liability</h2><p>The service is provided "as is", without warranties of any kind, and to the extent permitted by law we are not liable for losses arising from its use.</p>
<h2>Open-source code</h2><p>The source code is available under the MIT License in the <a href="{REPO}">repository</a>.</p>
<h2>Changes and contact</h2><p>We may update these terms; the date above shows the latest version. Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>""")

write("404.html", f"Page not found | {BRAND}", "Page not found.",
 '<div class="w page" style="text-align:center"><h1>404</h1><p>That page does not exist.</p><a class="btn" href="index.html">Back to home</a></div>')


write("contact.html", f"Contact | {BRAND}", "Contact Attestra for early access, pilots and security reports.", """<div class="w page"><h1>Contact</h1>
<p>Request early access, ask about a pilot, or share feedback. Submitting opens your email app with the message filled in.</p>
<div class="grid" style="margin-top:16px"><form id="cf" class="card"><label for="nm">Name</label><input id="nm" required autocomplete="name">
<label for="em">Your email</label><input id="em" type="email" required autocomplete="email"><label for="co">Company</label><input id="co" autocomplete="organization">
<label for="topic">Topic</label><select id="topic"><option>Early access</option><option>Pilot</option><option>Pricing</option><option>Security report</option><option>Other</option></select>
<label for="msg">Message</label><textarea id="msg" required></textarea><p><button class="btn" type="submit">Compose email</button></p></form>
<div><div class="card"><h3>Email</h3><p><a href="mailto:@EMAIL@">@EMAIL@</a></p></div><div class="card" style="margin-top:14px"><h3>Elsewhere</h3><p><a href="@GH@/issues" rel="noopener">GitHub issues</a><br><a href="@LI@" rel="noopener">LinkedIn</a><br><a href="@GH@" rel="noopener">GitHub</a></p></div></div></div>
<script>document.getElementById('cf').onsubmit=function(e){e.preventDefault();var g=function(i){return document.getElementById(i).value};
var b='Name: '+g('nm')+'\\nCompany: '+g('co')+'\\nEmail: '+g('em')+'\\n\\n'+g('msg');
location.href='mailto:@EMAIL@?subject='+encodeURIComponent('Attestra: '+g('topic'))+'&body='+encodeURIComponent(b)}</script></div>""".replace("@EMAIL@", EMAIL).replace("@GH@", GH).replace("@LI@", LI))

write("roi.html", f"ROI Calculator | {BRAND}", "Estimate hours and money saved by automating security questionnaires.", """<div class="w page"><h1>ROI calculator</h1>
<p>A rough estimate. Change the numbers to match your team. The default time saved is an assumption to test in a pilot, not a guarantee.</p>
<div class="grid" style="margin-top:16px"><div class="card"><label for="n">Questionnaires per month</label><input id="n" type="number" value="10" min="0">
<label for="h">Hours per questionnaire today</label><input id="h" type="number" value="8" min="0">
<label for="r">Loaded cost per hour (USD)</label><input id="r" type="number" value="60" min="0">
<label for="p">Time saved by automation (%)</label><input id="p" type="number" value="60" min="0" max="100"></div>
<div class="card"><h3>Estimated savings</h3><p id="o" class="big"></p><p style="margin-top:12px">Compare with the Growth plan at $499/month on the <a href="pricing.html">pricing page</a>.</p><p style="margin-top:12px"><a class="btn" href="contact.html">Request a pilot</a></p></div></div>
<script>var $=function(i){return document.getElementById(i)};function calc(){var n=+$('n').value,h=+$('h').value,r=+$('r').value,p=+$('p').value/100,s=n*h*p;
$('o').innerHTML='<b>'+s.toFixed(0)+'</b> hours saved / month<br><b>$'+(s*r).toFixed(0).replace(/\\B(?=(\\d{3})+(?!\\d))/g,',')+'</b> estimated value / month'}
document.querySelectorAll('input').forEach(function(e){e.oninput=calc});calc()</script></div>""")

write("docs.html", f"Documentation | {BRAND}", "Quickstart, API reference and configuration for Attestra.", """<div class="w page"><h1>Documentation</h1>
<p>Run the API locally, upload policies, process a questionnaire, and export answers.</p>
<h2>Quickstart</h2><pre><code>git clone @REPO@.git
cd questionnaire-ai/apps/api
pip install -r requirements.txt
uvicorn main:app --reload     # http://localhost:8000</code></pre>
<h2>Example</h2><pre><code>curl -F file=@policy.md http://localhost:8000/api/documents
curl -F file=@questionnaire.xlsx http://localhost:8000/api/questionnaires
curl -OJ http://localhost:8000/api/questionnaires/&lt;id&gt;/export</code></pre>
<h2>API reference</h2><div class="tbl"><table><tr><th>Method and path</th><th>Purpose</th></tr>
<tr><td><code>POST /api/documents</code></td><td>Upload a policy (pdf, docx, txt, md)</td></tr>
<tr><td><code>POST /api/questionnaires</code></td><td>Upload XLSX; returns drafted, cited answers</td></tr>
<tr><td><code>GET /api/questionnaires/{id}</code></td><td>Fetch a run</td></tr>
<tr><td><code>POST /api/questionnaires/{id}/items/{n}/approve</code></td><td>Approve (optionally edit) an answer; adds it to the library</td></tr>
<tr><td><code>GET /api/questionnaires/{id}/export</code></td><td>Download the answered XLSX</td></tr>
<tr><td><code>GET /api/questionnaires/{id}/gaps</code></td><td>Why answers were escalated</td></tr>
<tr><td><code>GET /api/stale-documents</code></td><td>Policies past their review date</td></tr>
<tr><td><code>GET /api/audit</code></td><td>Audit log</td></tr><tr><td><code>GET /health</code></td><td>Health check</td></tr></table></div>
<h2>Configuration</h2><div class="tbl"><table><tr><th>Variable</th><th>Meaning</th></tr>
<tr><td><code>ANTHROPIC_API_KEY</code></td><td>Enables LLM drafting. Without it, offline extractive mode is used.</td></tr>
<tr><td><code>ANTHROPIC_MODEL</code></td><td>Model name for drafting</td></tr>
<tr><td><code>API_KEY</code></td><td>If set, every <code>/api</code> request must send <code>X-API-Key</code></td></tr>
<tr><td><code>RATE_LIMIT</code></td><td>Max <code>/api</code> requests per minute per client (default 60)</td></tr></table></div>
<p>Send <code>X-Tenant</code> to separate workspaces in the demo build. Production tenancy will come from authenticated tokens.</p>
<h2>Limits</h2><p>The current build stores data in memory and is for evaluation. See the <a href="security.html">Security</a> page.</p></div>""".replace("@REPO@", REPO))

open(os.path.join(OUT, "style.css"), "w").write(CSS)
open(os.path.join(OUT, "fx.js"), "w").write("(function(){var c=document.getElementById('fx');if(!c||matchMedia('(prefers-reduced-motion:reduce)').matches)return;\nvar x=c.getContext('2d'),P=[],W,H,N=42;function rs(){W=c.width=c.offsetWidth;H=c.height=c.offsetHeight}rs();addEventListener('resize',rs);\nfor(var i=0;i<N;i++)P.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.35,vy:(Math.random()-.5)*.35});\n(function f(){x.clearRect(0,0,W,H);P.forEach(function(p,i){p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;\nx.fillStyle='rgba(34,211,238,.8)';x.fillRect(p.x,p.y,2,2);for(var j=i+1;j<N;j++){var q=P[j],d=Math.hypot(p.x-q.x,p.y-q.y);\nif(d<120){x.strokeStyle='rgba(139,92,246,'+(1-d/120)*.3+')';x.beginPath();x.moveTo(p.x,p.y);x.lineTo(q.x,q.y);x.stroke()}}});requestAnimationFrame(f)})()})();")
pages = ["index.html", "pricing.html", "security.html", "about.html", "contact.html", "privacy.html", "terms.html", "docs.html", "roi.html", "demo.html"]
open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
    "".join(f"<url><loc>{BASE}{'' if p == 'index.html' else p}</loc></url>" for p in pages) + "</urlset>")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
print("built", len(pages) + 1, "pages")
