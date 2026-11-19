"""
Task 2: AI Agent with Tool Calling Streamlit Application
Author: Keshav Jindal
"""

import os
import streamlit as st

try:
    from task_2_agent.agent import AutonomousAgent, AVAILABLE_TOOLS
except ImportError:
    from agent import AutonomousAgent, AVAILABLE_TOOLS

def render_task_2():
    # Custom Styling
    st.markdown("""
    <style>
        .agent-title { font-size: 2.2rem; font-weight: 700; color: #10B981; margin-bottom: 0.2rem; }
        .agent-sub { font-size: 1.05rem; color: #4B5563; margin-bottom: 1.5rem; }
        .tool-chip { background-color: #ECFDF5; border: 1px solid #10B981; border-radius: 6px; padding: 6px 10px; margin: 4px; display: inline-block; font-size: 0.85rem; font-weight: 600; color: #065F46; }
    </style>
    """, unsafe_allow_html=True)

    # Session State Initialization
    if "agent" not in st.session_state:
        st.session_state.agent = AutonomousAgent()
    if "agent_chat_history" not in st.session_state:
        st.session_state.agent_chat_history = []

    # Main Interface Header
    st.markdown('<div class="agent-title">🤖 AgentFlow: Autonomous Tool-Calling Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="agent-sub">Multi-turn conversational AI capable of reasoning, selecting, and invoking external APIs in real-time.</div>', unsafe_allow_html=True)

    # Active Tools Banner
    st.markdown("""
    <div style="margin-bottom: 15px;">
        <span class="tool-chip">🌤️ Live Weather (Open-Meteo REST API)</span>
        <span class="tool-chip">🧮 Safe Math Evaluator (AST Parser)</span>
        <span class="tool-chip">🔍 Live Knowledge Search (Wikipedia / DDG)</span>
    </div>
    """, unsafe_allow_html=True)

    # Configuration & Tools Expander
    with st.expander("🛠️ Tool Inspection & Model Settings", expanded=False):
        c1, c2 = st.columns([1, 1])
        with c1:
            api_key = st.text_input(
                "Gemini API Key (Optional)",
                value=os.environ.get("GEMINI_API_KEY", ""),
                type="password",
                help="Optional: Free tier Gemini API key for native function calling. If omitted, local autonomous ReAct router is used."
            )
            if api_key != st.session_state.agent.api_key:
                st.session_state.agent.set_api_key(api_key.strip() if api_key else None)
        with c2:
            st.caption("Registered System Tools:")
            for name, tool in AVAILABLE_TOOLS.items():
                st.markdown(f"• **`{name}`**: {tool['description']}")

    # Quick Prompts & Controls
    c_p1, c_p2, c_p3, c_p4 = st.columns(4)
    with c_p1:
        if st.button("🌦️ Tokyo Weather", use_container_width=True):
            st.session_state.agent_prefill = "What is the current weather in Tokyo?"
    with c_p2:
        if st.button("🧮 Math Calculation", use_container_width=True):
            st.session_state.agent_prefill = "Calculate (150 * 4) + sqrt(1024) - 2 ** 6"
    with c_p3:
        if st.button("🔍 Knowledge Search", use_container_width=True):
            st.session_state.agent_prefill = "Tell me about Alan Turing and his legacy"
    with c_p4:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.agent.reset_conversation()
            st.session_state.agent_chat_history = []
            st.rerun()

    st.markdown("---")

    # Display Chat History
    for msg in st.session_state.agent_chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("tool_calls"):
                with st.expander(f"⚡ Inspect Tool Execution Trace ({len(msg['tool_calls'])} action)"):
                    for t in msg["tool_calls"]:
                        st.json(t)

    # Prompt Input
    prefill = st.session_state.pop("agent_prefill", None)
    user_prompt = st.chat_input("Ask a question, request weather, or compute a calculation...") or prefill

    if user_prompt:
        with st.chat_message("user"):
            st.write(user_prompt)
        
        st.session_state.agent_chat_history.append({"role": "user", "content": user_prompt})

        with st.chat_message("assistant"):
            with st.spinner("Agent is reasoning and deciding tool actions..."):
                result = st.session_state.agent.run(user_prompt)
                st.markdown(result["response"])
                
                if result.get("tool_calls"):
                    with st.expander(f"⚡ Inspect Tool Execution Trace ({len(result['tool_calls'])} action)"):
                        for t in result["tool_calls"]:
                            st.json(t)
                
                st.session_state.agent_chat_history.append({
                    "role": "assistant",
                    "content": result["response"],
                    "tool_calls": result.get("tool_calls", [])
                })

if __name__ == "__main__":
    st.set_page_config(
        page_title="AgentFlow - Tool Calling AI Agent",
        page_icon="🤖",
        layout="wide"
    )
    render_task_2()
