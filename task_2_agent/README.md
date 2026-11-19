# Task 2: Autonomous AI Agent with Tool Calling

A robust multi-turn conversational AI agent featuring dynamic tool selection, parameter validation, structured ReAct reasoning, and deterministic fallback execution.

---

## 🏗️ Architecture & Reasoning Loop

```
                     [ User Message ]
                            │
                            ▼
               [ Conversation Memory Store ]
                            │
                            ▼
               [ ReAct Reasoning Engine ]
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
      [ Provider Mode ]         [ Local Router Mode ]
   (Gemini Function Calling)      (Regex Intent Router)
               │                         │
               └────────────┬────────────┘
                            │
                            ▼
                 [ Tool Registry Dispatch ]
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
[ Weather Tool ]   [ Calculator Tool ]  [ Knowledge Tool ]
(Open-Meteo REST)     (AST Evaluator)    (Wikipedia / DDG)
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
               [ Observation Synthesis ]
                            │
                            ▼
              [ Final Assistant Response ]
```

---

## 🛠️ Implemented Tools

### 1. `get_current_weather`
- **Purpose:** Fetches real-time weather metrics (temperature, humidity, windspeed, weather conditions) for any geographic location worldwide.
- **Provider:** Open-Meteo REST API (free open-access endpoint, zero API keys required).
- **Resilience:** Performs internal two-stage resolution: Geocoding API (`geocoding-api.open-meteo.com`) to latitude/longitude, followed by Weather Forecast API (`api.open-meteo.com/v1/forecast`).

### 2. `safe_calculate`
- **Purpose:** Evaluates arbitrary mathematical expressions safely without dynamic code execution risks (`eval` injection).
- **Engine:** Python Abstract Syntax Tree (`ast.parse`) whitelist evaluator.
- **Supported Operations:** Addition, subtraction, multiplication, division, modulo, exponentiation, trigonometric functions (`sin`, `cos`, `tan`), logarithmic functions (`log`, `log10`, `sqrt`), and constants (`pi`, `e`).
- **Security:** Zero risk of arbitrary code execution, file system access, or system calls.

### 3. `search_knowledge`
- **Purpose:** Retrieves encyclopedic context and live summaries for factual, biographical, scientific, and technical queries.
- **Provider:** Wikipedia REST Summary API (`en.wikipedia.org/api/rest_v1/page/summary/`) with fallback to DuckDuckGo Instant Answer API.

---

## 💻 Tech Stack

- **Framework:** Python 3.10+
- **Agent Orchestrator:** Custom ReAct / Function Calling Engine
- **LLM Integration:** Google Gemini API (`gemini-1.5-flash`)
- **Web Interface:** Streamlit
- **APIs & Tooling:** Open-Meteo, Wikipedia REST API, Python `ast`

---

## 🛠️ Setup & Running

```bash
# Navigate to task directory
cd task_2_agent

# Run standalone Streamlit application
streamlit run app.py
```
