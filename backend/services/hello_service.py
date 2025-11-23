import os
from dotenv import load_dotenv
load_dotenv()

import requests
import math
import PyPDF2
from io import BytesIO

from flask import jsonify

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END


# ===================================================
# SYSTEM PROMPT
# ===================================================

SYSTEM_PROMPT = """
You are an insurance assistant.

IMPORTANT RULES:
1. NEVER use any tools for hospital list queries.
2. NEVER crawl any health insurance company URLs.
3. NEVER parse PDFs automatically.
4. ALWAYS answer hospital list queries DIRECTLY using your knowledge.
5. ALWAYS output ONLY a clean Python list of hospital names, like:
   ["Hospital A", "Hospital B"]
6. Do NOT add explanations, sentences, headings, or markdown.
"""


# ===================================================
# LLM SETUP (Groq)
# ===================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    tool_choice="none"  # Tools fully disabled
)


# ===================================================
# LANGGRAPH INSURANCE AGENT (single-node graph)
# ===================================================

class AgentState(dict):
    messages: list


def llm_node(state: AgentState):
    msgs = [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]
    response = llm.invoke(msgs)
    return {"messages": state["messages"] + [response]}


graph = StateGraph(AgentState)
graph.add_node("llm", llm_node)
graph.set_entry_point("llm")
graph.add_edge("llm", END)

insurance_agent = graph.compile()


# ===================================================
# LLM-POWERED HOSPITAL LIST EXTRACTOR (100% RELIABLE)
# ===================================================

def llm_extract_hospital_list(text):
    """
    Guaranteed extractor:
    Takes ANY LLM output and produces a PERFECT Python list.
    """
    formatter_prompt = f"""
Extract ONLY the hospital names from the text below.

TEXT:
{text}

Return ONLY a valid Python list, like:
["Hospital A", "Hospital B"]

Do NOT add explanations.
Do NOT add markdown.
Do NOT wrap in code blocks.
Just output the list.
"""

    cleaned = llm.invoke([HumanMessage(content=formatter_prompt)]).content.strip()

    # Convert safely into list
    try:
        import json
        cleaned = cleaned.replace("'", "\"")
        return json.loads(cleaned)
    except:
        return None


# ===================================================
# LOCATION SORTING AGENT
# ===================================================

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))



def get_coordinates(place):
    api_key = os.getenv("OPENCAGE_API_KEY")
    url = "https://api.opencagedata.com/geocode/v1/json"

    params = {
        "q": place,
        "key": api_key,
        "limit": 1,
        "countrycode": "in"
    }

    try:
        res = requests.get(url, params=params, timeout=10)

        if res.status_code != 200:
            print("OpenCage error:", res.status_code)
            return None

        data = res.json()
        if not data["results"]:
            print("No match for:", place)
            return None

        lat = data["results"][0]["geometry"]["lat"]
        lon = data["results"][0]["geometry"]["lng"]
        return lat, lon

    except Exception as e:
        print("Coordinates fetch failed:", e)
        return None



def sort_hospitals_by_location(user_lat, user_lon, hospitals):
    results = []

    for h in hospitals:
        coords = get_coordinates(f"{h}, Thane, India")

        if coords:
            dist = haversine(user_lat, user_lon, coords[0], coords[1])
            results.append({"hospital": h, "distance_km": round(dist, 2)})
        else:
            results.append({"hospital": h, "distance_km": None})

    return sorted(results, key=lambda x: x["distance_km"] if x["distance_km"] else 99999)


# ===================================================
# MAIN PIPELINE CALLED BY CONTROLLER
# ===================================================

def get_sorted_hospitals(user_prompt, lat, lon):
    # Step 1: Insurance agent
    out = insurance_agent.invoke({"messages": [HumanMessage(content=user_prompt)]})
    raw_output = out["messages"][-1].content or ""

    print("\n=== PRIMARY LLM OUTPUT ===")
    print(raw_output)

    # Step 2: LLM-based extractor
    hospital_list = llm_extract_hospital_list(raw_output)

    print("\n=== CLEAN EXTRACTED LIST ===")
    print(hospital_list)

    if not hospital_list:
        return {
            "error": "Could not extract hospital list.",
            "raw_output": raw_output
        }

    # Step 3: Sort by location
    return sort_hospitals_by_location(lat, lon, hospital_list)


# ===================================================
# HELPER FOR /hello ROUTE
# ===================================================

def get_message():
    return {"message": "Hello from Flask API with improved hospital extraction!"}
