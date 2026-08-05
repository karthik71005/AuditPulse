# ⚡ GEO Auditor (AuditPulse)

> **Generative Engine Optimization (GEO) & AI Search Visibility Auditor**
>
> Measure, diagnose, and optimize your business's presence inside ChatGPT, Perplexity, Claude, and Google AI Overviews.

---

## 🌐 Live Deployments

* **Frontend (Vite + React)**: [https://audit-pulse-taupe.vercel.app/](https://audit-pulse-taupe.vercel.app/)
* **Backend API (FastAPI)**: [https://auditpulse-xwxz.onrender.com/](https://auditpulse-xwxz.onrender.com/docs)

---

## 📖 Table of Contents

- [The Problem](#-the-problem)
- [System Architecture](#-system-architecture)
- [Key Features](#-key-features)
- [Deep Dive: What We Measure & Defense of Each Check](#-deep-dive-what-we-measure--defense-of-each-check)
- [What Is Real vs. Mocked](#-what-is-real-vs-mocked)
- [Product Tradeoffs & Scope Decisions](#-product-tradeoffs--scope-decisions)
- [Local Setup & Development](#-local-setup--development)
- [Environment Variables](#-environment-variables)
- [Future Roadmap (If Given Another Week)](#-future-roadmap-if-given-another-week)

---

## 🎯 The Problem

Search is fundamentally shifting from keyword-based Google queries to conversational AI engines (**ChatGPT**, **Perplexity**, **Claude**, **Google AI Overviews**).

When potential buyers ask an AI assistant *"What are the best tools for X?"* or *"Who provides service Y in city Z?"*, the AI synthesizes an answer directly and cites a handful of web sources. 

A business can rank **#1 on Google Search** and remain **completely invisible inside AI-generated answers** because generative engines evaluate sources by a fundamentally different set of rules:
1. **Crawlability & AI Access**: Can LLM bots (GPTBot, PerplexityBot) access your content?
2. **Entity Clarity**: Is your brand explicitly defined in JSON-LD schema so LLMs understand who you are?
3. **Answer Density**: Is your page formatted so LLMs can extract direct facts (Q&A headers, concise definitions, comparison tables)?
4. **Third-Party Citation Presence**: Does your brand show up across web sources cited by search-augmented LLMs?

**GEO Auditor** solves this gap by giving business owners a transparent, actionable diagnostic report with exact copy-paste code fixes to execute immediately.

---

## 🏗️ System Architecture

```
                                  +------------------------------------+
                                  |    Target Website (Target Domain)   |
                                  +------------------------------------+
                                                    |
                                                    v
                                  +------------------------------------+
                                  |    Crawler Layer (httpx + bs4)     |
                                  |   • Browser User-Agent Rotation    |
                                  |   • 403 Retry / Partial Fallback   |
                                  +------------------------------------+
                                                    |
                                                    v
                 +---------------------------------------------------------------------+
                 |                      Modular Evaluation Engine                      |
                 +---------------------------------------------------------------------+
                 | 1. Crawlability: robots.txt (GPTBot/PerplexityBot) & /llms.txt      |
                 | 2. Schema: JSON-LD (@type Organization, Product, FAQPage)           |
                 | 3. Content Structure: Question Headings & Answer Paragraph Density |
                 | 4. Live Search Citations: DuckDuckGo live buyer query evaluation    |
                 +---------------------------------------------------------------------+
                                                    |
                                                    v
                                  +------------------------------------+
                                  |   Groq AI Analyst (Llama 3.3 70B)  |
                                  |   • Tailored Buyer Intent Queries  |
                                  |   • Plain-English Executive Summary|
                                  |   • Site-Specific Finding Insights |
                                  +------------------------------------+
                                                    |
                                                    v
                                  +------------------------------------+
                                  |    Transparent Scoring Model       |
                                  |   • 100-Point Formula (No Magic)   |
                                  |   • High-Authority Platform Bypass |
                                  +------------------------------------+
                                                    |
                                                    v
                                  +------------------------------------+
                                  |   React + Tailwind SPA Frontend    |
                                  |   • Clean Light Mode Interface     |
                                  |   • LocalStorage Report Cache      |
                                  |   • PDF & Raw JSON Export          |
                                  +------------------------------------+
```

---

## ✨ Key Features

* **Transparent 100-Point Scoring**: No hidden "magic" numbers. Every point deducted corresponds to a specific technical or citation gap visible in the breakdown.
* **Groq-Powered AI Intelligence (`llama-3.3-70b-versatile`)**:
  * **Dynamic Buyer Query Generation**: Generates 3 realistic buyer queries specific to the target company (not hardcoded templates).
  * **Executive Summary**: Synthesizes complex technical findings into 2 plain-English paragraphs written for business owners.
  * **Contextualized Insights**: Explains *why* a specific issue matters for *this specific company*.
* **Copy-Paste Fixes**: Provides ready-to-use `<script type="application/ld+json">`, `robots.txt`, and `llms.txt` code blocks for every failing check.
* **High-Authority Domain Defense**: Automatically detects established platforms (e.g., Reddit, Wikipedia, StackOverflow) and adjusts scoring so intentional bot-blocking isn't penalized as a bug.
* **Client-Side Persistence**: Saves the last audit in `localStorage` so refreshing the browser retains the complete report state.
* **One-Click PDF & JSON Export**: Download a high-res PDF printout or full JSON report payload directly from the browser.

---

## 🔍 Deep Dive: What We Measure & Defense of Each Check

Rather than measuring generic SEO metrics (like page speed or meta tag length), GEO Auditor focuses on **the 4 pillars of AI search engine visibility**:

### Pillar 1: Crawlability & AI Access (Max 30 Points)
* **GPTBot & PerplexityBot Access (`robots.txt`)**: 
  * *Why it matters*: If your `robots.txt` explicitly disallows `GPTBot` or `PerplexityBot`, search-augmented LLMs cannot crawl or index your latest content.
* **`/llms.txt` Context File Presence**:
  * *Why it matters*: `/llms.txt` is an emerging open standard (analogous to `robots.txt` or `sitemap.xml`) that provides LLMs with a curated, markdown-formatted overview of a website's core facts, pricing, and documentation.

### Pillar 2: Structured Schema Markup (Max 30 Points)
* **Organization / Brand JSON-LD**:
  * *Why it matters*: LLMs require unambiguous entity disambiguation. Without `@type: Organization` schema containing official brand names and URLs, AI engines may misattribute brand claims or hallucinate company details.
* **Product / Service JSON-LD**:
  * *Why it matters*: Helps LLMs understand software features, pricing models, and service categories when answering buyer intent questions.
* **FAQPage Schema**:
  * *Why it matters*: Structured Q&A blocks are directly parsed by AI search engines to populate direct answer cards.

### Pillar 3: Content Answer Density & Format (Max 10 Points)
* **Question-Style Headings (`H1`/`H2`/`H3`)**:
  * *Why it matters*: Natural language processing models match user queries directly to question-formatted headings (`What is...`, `How does...`).
* **Answer Paragraph Density**:
  * *Why it matters*: LLMs prefer concise (< 250 character) direct-answer paragraphs immediately following question headings.

### Pillar 4: Live AI Citation Share (Max 30 Points)
* **DuckDuckGo Search Evaluation**:
  * *Why it matters*: Search-augmented LLMs (ChatGPT Search, Perplexity, AI Overviews) rely on live web retrieval. We evaluate whether your domain surfaces in top results when high-intent buyer queries are executed live.

> **High-Authority Platform Defense**: Established platforms like Reddit, Wikipedia, or GitHub frequently block AI bots in `robots.txt` as a business policy, yet they are already deeply embedded in LLM base training data. GEO Auditor detects high-authority domains, flags bot blocking as informational rather than critical, awards partial citation credit, and explains the rationale transparently in the audit notes.

---

## 🧪 What Is Real vs. Mocked

* **Live Web Scraping**: **REAL** (Uses `httpx` with randomized browser User-Agents and fallback retry logic).
* **Live Search Citations**: **REAL** (Executes live search queries via `duckduckgo-search` / `DDGS`).
* **AI Analysis & Query Generation**: **REAL** (Powered by live Groq API using `llama-3.3-70b-versatile`).
* **JSON-LD & Content Parsing**: **REAL** (Parsed dynamically using `BeautifulSoup4` and `json`).
* **Mocked Data**: **0%** — No dummy fallbacks or fake scores are presented. If a site restricts scrapers, the system handles it with a transparent partial audit notice.

---

## ✂️ Product Tradeoffs & Scope Decisions

In accordance with product developer guidelines, we aggressively cut non-essential features to focus on report quality and user experience:

| Feature Cut | Why It Was Cut | How It Is Addressed Instead |
|---|---|---|
| **User Authentication / Accounts** | Zero-friction requirement. Business owners want instant reports without creating an account. | Reports are instant; state persists via browser `localStorage`. |
| **Database (PostgreSQL / MongoDB)** | Unnecessary server state overhead for a client-driven diagnostic tool. | API returns lightweight JSON; reports can be saved/exported as PDF or JSON. |
| **Payment / Billing Gateway** | Out of scope for audit generation. | Focused 100% on delivery of immediate value. |

---

## 🛠️ Local Setup & Development

You can run the entire stack locally in **under 3 minutes**.

### Prerequisites
* **Python 3.10+**
* **Node.js 18+** & `npm`
* A free **Groq API Key** from [console.groq.com](https://console.groq.com)

---

### 1. Clone the Repository
```bash
git clone https://github.com/karthik71005/AuditPulse.git
cd GEO_AUDITOR
```

---

### 2. Backend Setup (FastAPI)
```bash
# Navigate to backend directory or use virtual environment
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp ../.env.example .env
# Edit .env and set your GROQ_API_KEY
```

**Start Backend Server:**
```bash
python -m uvicorn main:app --reload --port 8000
```
*Backend API will run at `http://localhost:8000` (API Docs: `http://localhost:8000/docs`)*

---

### 3. Frontend Setup (React + Vite)
Open a new terminal tab:

```bash
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
*Frontend app will run at `http://localhost:5173`*

---

## 🔑 Environment Variables

### Backend (`.env` or Render Environment)
```env
PORT=8000
ENVIRONMENT=development
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### Frontend (`frontend/.env` or Vercel Environment)
```env
VITE_API_URL=http://localhost:8000
```
*(In production, set `VITE_API_URL` to your live backend domain, e.g. `https://auditpulse-xwxz.onrender.com`)*

---

## 🚀 Future Roadmap (If Given Another Week)

1. **Multi-Page Site Crawling**: Expand beyond homepage analysis to automatically crawl subpages (`/pricing`, `/docs`, `/blog`) and aggregate a site-wide GEO score.
2. **Per-Engine Visibility Matrix**: Break down citation rates specifically across **ChatGPT Search**, **Perplexity Pro**, **Claude with Search**, and **Google AI Overviews**.
3. **Automated Fix PR Generator**: Integrate with GitHub API to automatically open a Pull Request adding `llms.txt` and missing `JSON-LD` schema directly to the user's repository.
4. **Competitor GEO Benchmarking**: Compare a business's score side-by-side against 3 key industry competitors.
