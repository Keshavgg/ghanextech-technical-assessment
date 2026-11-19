"""
Task 2: Autonomous AI Agent with Dynamic Tool Calling
Author: Keshav Jindal
"""

import json
import re
from typing import List, Dict, Any, Optional
try:
    from task_2_agent.tools.weather_tool import get_current_weather
    from task_2_agent.tools.calculator_tool import calculate_expression
    from task_2_agent.tools.knowledge_tool import search_knowledge
except ImportError:
    from tools.weather_tool import get_current_weather
    from tools.calculator_tool import calculate_expression
    from tools.knowledge_tool import search_knowledge

AVAILABLE_TOOLS = {
    "get_current_weather": {
        "function": get_current_weather,
        "description": "Fetches current real-time weather information (temperature, condition, wind) for a given city.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or locality (e.g., 'New Delhi', 'Tokyo', 'London', 'San Francisco')"
                }
            },
            "required": ["location"]
        }
    },
    "calculate_expression": {
        "function": calculate_expression,
        "description": "Safely evaluates mathematical expressions (arithmetic, powers, trigonometry, sqrt, logs).",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical formula to evaluate (e.g., '(45 * 12) + sqrt(144)', '2 ** 10')"
                }
            },
            "required": ["expression"]
        }
    },
    "search_knowledge": {
        "function": search_knowledge,
        "description": "Searches Wikipedia and online knowledge bases for facts, history, or technical concepts.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The topic or question to look up (e.g., 'Guido van Rossum', 'What is Quantum Computing')"
                }
            },
            "required": ["query"]
        }
    }
}

class AutonomousAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.conversation_history: List[Dict[str, str]] = []

    def set_api_key(self, api_key: Optional[str]):
        self.api_key = api_key

    def reset_conversation(self):
        self.conversation_history = []

    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in AVAILABLE_TOOLS:
            return {"error": f"Tool '{tool_name}' is not recognized."}

        func = AVAILABLE_TOOLS[tool_name]["function"]
        try:
            return func(**arguments)
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}

    def _detect_intent_locally(self, user_input: str) -> Optional[tuple]:
        """
        Deterministic intent detector when running without an external LLM API key.
        Detects weather queries, math expressions, and search lookups.
        """
        text = user_input.strip()

        # Check for Math / Calculation
        math_match = re.search(r'(?:calculate|what is|compute|solve)?\s*([0-9\.\+\-\*\/\^\(\)\s\%\*\*|sqrt|sin|cos|tan|log|pi|e]{4,})', text, re.IGNORECASE)
        if any(op in text for op in ["+", "-", "*", "/", "^", "sqrt", "sin", "cos", "log", "calculate", "power"]):
            # Extract expression
            expr = text
            for prefix in ["calculate", "compute", "solve", "what is", "evaluate"]:
                if expr.lower().startswith(prefix):
                    expr = expr[len(prefix):].strip()
            expr = expr.rstrip("?=")
            if re.search(r'\d', expr):
                return ("calculate_expression", {"expression": expr})

        # Check for Weather
        weather_match = re.search(r'(?:weather|temperature|forecast|climate|rain)\s+(?:in|at|for)?\s*([A-Za-z\s]+)', text, re.IGNORECASE)
        if weather_match or any(w in text.lower() for w in ["weather", "temperature", "forecast"]):
            city = ""
            if weather_match:
                city = weather_match.group(1).strip()
            else:
                words = text.split()
                city = words[-1].strip("?.,")
            # remove trigger words
            for tw in ["weather", "temperature", "forecast", "in", "at", "for", "what", "is", "the", "like"]:
                city = re.sub(rf'\b{tw}\b', '', city, flags=re.IGNORECASE).strip()
            if city:
                return ("get_current_weather", {"location": city})

        # Check for Knowledge Search
        search_match = re.search(r'(?:who is|who was|what is|tell me about|search for|lookup)\s+([A-Za-z0-9\s]+)', text, re.IGNORECASE)
        if search_match and not any(m in text.lower() for m in ["calculate", "weather", "temperature"]):
            query = search_match.group(1).strip("?., ")
            if query and len(query) > 2:
                return ("search_knowledge", {"query": query})

        return None

    def run(self, user_message: str) -> Dict[str, Any]:
        """
        Executes the agent reasoning loop:
        1. Analyzes user message within conversation context.
        2. Decides if tool invocation is necessary.
        3. Executes tool(s) if called and captures trace.
        4. Synthesizes final response for the user.
        """
        trace = []
        
        # Add to history
        self.conversation_history.append({"role": "user", "content": user_message})

        # Path A: Gemini API tool calling (if API key available)
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                
                # Format tools for Gemini API
                tool_declarations = []
                for name, meta in AVAILABLE_TOOLS.items():
                    tool_declarations.append(meta["function"])

                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    tools=tool_declarations,
                    system_instruction=(
                        "You are a capable, friendly AI Agent. You have access to tools for weather lookup, "
                        "safe mathematical calculations, and knowledge search. Use tools ONLY when necessary "
                        "for real-time data or precise computation. For general conversational chit-chat, answer directly. "
                        "After receiving tool outputs, synthesize a clear, helpful, and grounded final answer."
                    )
                )

                # Convert history
                chat = model.start_chat(enable_automatic_function_calling=True)
                response = chat.send_message(user_message)

                # Check if functions were called
                if hasattr(response, "candidates") and response.candidates:
                    first_cand = response.candidates[0]
                    for part in first_cand.content.parts:
                        if hasattr(part, "function_call") and part.function_call:
                            fn_call = part.function_call
                            trace.append({
                                "tool_name": fn_call.name,
                                "arguments": dict(fn_call.args),
                                "status": "executed via Gemini function calling"
                            })

                final_text = response.text if response and response.text else "Task completed successfully."
                self.conversation_history.append({"role": "assistant", "content": final_text})
                return {
                    "response": final_text,
                    "tool_calls": trace,
                    "model_used": "gemini-1.5-flash"
                }
            except Exception as e:
                # Fallback to local deterministic agent on error
                trace.append({"note": f"Gemini API unavailable ({str(e)}), fell back to local agent routing."})

        # Path B: Local ReAct Autonomous Routing
        detected = self._detect_intent_locally(user_message)
        
        if detected:
            tool_name, tool_args = detected
            trace.append({
                "tool_name": tool_name,
                "arguments": tool_args,
                "status": "invoked"
            })
            
            tool_output = self._execute_tool(tool_name, tool_args)
            trace[-1]["result"] = tool_output

            # Synthesize answer
            if tool_name == "get_current_weather":
                if tool_output.get("success"):
                    ans = (
                        f"🌤️ **Current Weather for {tool_output['location']}:**\n\n"
                        f"• **Condition:** {tool_output['condition']}\n"
                        f"• **Temperature:** {tool_output['temperature_celsius']}°C ({tool_output['temperature_fahrenheit']}°F)\n"
                        f"• **Wind Speed:** {tool_output['wind_speed_kmh']} km/h\n\n"
                        f"*Data retrieved live via Open-Meteo REST API.*"
                    )
                else:
                    ans = f"⚠️ Could not retrieve weather details: {tool_output.get('error')}"

            elif tool_name == "calculate_expression":
                if tool_output.get("success"):
                    ans = (
                        f"🔢 **Calculation Result:**\n\n"
                        f"$$\\text{{{tool_output['expression']}}} = \\mathbf{{{tool_output['result']}}}$$\n\n"
                        f"*Evaluated securely using AST parser.*"
                    )
                else:
                    ans = f"⚠️ Mathematical evaluation error: {tool_output.get('error')}"

            elif tool_name == "search_knowledge":
                if tool_output.get("success"):
                    ans = (
                        f"📖 **{tool_output.get('title', 'Information')}** (Source: {tool_output.get('source')}):\n\n"
                        f"{tool_output['summary']}"
                    )
                    if tool_output.get("url"):
                        ans += f"\n\n🔗 [Read More on {tool_output.get('source')}]({tool_output['url']})"
                else:
                    ans = tool_output.get("message", "No conclusive knowledge summary found.")
            else:
                ans = json.dumps(tool_output, indent=2)

        else:
            # Direct conversational reply
            lower = user_message.lower().strip()
            if any(greeting in lower for greeting in ["hi", "hello", "hey", "good morning", "good evening"]):
                ans = "Hello! I am your AI Agent equipped with real-time tool calling. I can fetch live weather, evaluate complex math expressions, or search knowledge topics. How can I help you today?"
            elif "who are you" in lower or "what can you do" in lower:
                ans = (
                    "I am an Autonomous AI Agent designed for practical tool execution! My capabilities include:\n"
                    "1. 🌤️ **Live Weather:** Check current temperatures, conditions, and wind in any city worldwide via Open-Meteo.\n"
                    "2. 🧮 **Safe Calculator:** Safely parse and calculate math expressions via AST.\n"
                    "3. 🔍 **Knowledge Search:** Query live Wikipedia and DuckDuckGo summaries."
                )
            else:
                ans = f"I understood your request: '{user_message}'. If you would like to look up live weather, compute mathematical calculations, or search for concepts, feel free to ask!"

        self.conversation_history.append({"role": "assistant", "content": ans})
        return {
            "response": ans,
            "tool_calls": trace,
            "model_used": "local-react-router"
        }
