# app/chatbot_service.py
# The AI brain that understands natural language and calls the right Oracle API

import os
import json
from groq import Groq
from dotenv import load_dotenv
from app.mock_oracle_api import (
    get_employees,
    get_purchase_orders,
    get_invoices,
    get_department_summary
)

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ─── TOOL DEFINITIONS ─────────────────────────────────────────────────────────
# These tell the LLM what functions it can call and what parameters they take
# This is called "Function Calling" or "Tool Use"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_employees",
            "description": "Get employee data from Oracle HCM. Use when user asks about employees, staff, workers, HR data, headcount, or people in the organization.",
            "parameters": {
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "description": "Filter by department name e.g. Finance, HR, IT, SCM"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter by status: Active or Inactive"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_purchase_orders",
            "description": "Get purchase order data from Oracle SCM. Use when user asks about POs, purchase orders, procurement, vendors, or buying.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter by status: Open, Approved, or Closed"
                    },
                    "department": {
                        "type": "string",
                        "description": "Filter by department: Finance, HR, IT, SCM"
                    },
                    "min_amount": {
                        "type": "number",
                        "description": "Minimum amount filter in dollars"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_invoices",
            "description": "Get invoice data from Oracle Finance. Use when user asks about invoices, bills, payments, overdue amounts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter by status: Pending, Paid, or Overdue"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_department_summary",
            "description": "Get summary statistics for all departments. Use when user asks about department overview, headcount summary, or organizational stats.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

# ─── FUNCTION DISPATCHER ──────────────────────────────────────────────────────

def call_function(name: str, arguments: dict) -> str:
    """
    Execute the function the LLM decided to call.
    Returns the result as a JSON string.
    """
    print(f"🔧 Calling function: {name} with args: {arguments}")

    if name == "get_employees":
        result = get_employees(**arguments)
    elif name == "get_purchase_orders":
        result = get_purchase_orders(**arguments)
    elif name == "get_invoices":
        result = get_invoices(**arguments)
    elif name == "get_department_summary":
        result = get_department_summary()
    else:
        result = {"error": f"Unknown function: {name}"}

    return json.dumps(result)


# ─── MAIN CHAT FUNCTION ───────────────────────────────────────────────────────

def chat_with_erp(user_message: str, conversation_history: list) -> dict:
    """
    Main chatbot function that:
    1. Sends user message to LLM with tool definitions
    2. LLM decides which Oracle API to call
    3. We call that API and get real data
    4. Send data back to LLM for natural language response
    5. Return the final answer

    This is called an "Agentic Loop" - the LLM acts as an agent
    that decides what actions to take.
    """

    # System prompt — tells LLM its role and context
    system_prompt = """You are an intelligent Oracle Fusion ERP assistant for an enterprise company.
You have access to Oracle HCM (HR), Oracle SCM (Supply Chain), and Oracle Finance data.

When users ask questions:
- Always use the available tools to fetch real data
- Present data in a clear, business-friendly format
- Use tables or bullet points when showing multiple records
- Always mention the count of records found
- Format currency with $ and commas (e.g. $45,000)
- Be concise but complete

You represent an enterprise AI assistant integrated with Oracle Fusion Applications."""

    # Build messages array with full conversation history
    messages = [
        {"role": "system", "content": system_prompt},
        *conversation_history,
        {"role": "user", "content": user_message}
    ]

    # Step 1: First LLM call — LLM decides which tool to call
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",  # LLM decides whether to use a tool
        max_tokens=1000
    )

    assistant_message = response.choices[0].message
    tool_calls = assistant_message.tool_calls

    # Step 2: If LLM wants to call a tool, execute it
    if tool_calls:
        # Add assistant's tool call decision to messages
        messages.append({
            "role": "assistant",
            "content": assistant_message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in tool_calls
            ]
        })

        # Execute each tool call and add results to messages
        function_called = None
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            function_called = function_name

            # Call the actual function
            function_result = call_function(function_name, function_args)

            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": function_result
            })

        # Step 3: Second LLM call — generate natural language response from data
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1000
        )

        final_answer = final_response.choices[0].message.content

        return {
            "answer": final_answer,
            "function_called": function_called,
            "raw_data_fetched": True
        }

    else:
        # LLM answered directly without needing a tool
        return {
            "answer": assistant_message.content,
            "function_called": None,
            "raw_data_fetched": False
        }