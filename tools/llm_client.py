from __future__ import annotations

import json
import os
import re

import requests
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def _get_secret(key: str) -> str:
    """Read from Streamlit secrets first, then env vars."""
    try:
        import streamlit as st
        val = st.secrets.get(key, "")
        if val:
            return val
    except Exception:
        pass
    return os.getenv(key, "")


GROQ_API_KEY = _get_secret("GROQ_API_KEY")
GEMINI_API_KEY = _get_secret("GEMINI_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"


def call_groq(prompt: str, temperature: float = 0.7) -> str | None:
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        return None
    try:
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": 2048,
            },
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        return None


def call_gemini(prompt: str) -> str | None:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return None
    try:
        resp = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
            json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": 2048}},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return None


def call_llm(prompt: str) -> str | None:
    result = call_groq(prompt)
    if result:
        return result
    return call_gemini(prompt)


def parse_json(text: str) -> dict | None:
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        pass
    try:
        match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text)
        if match:
            return json.loads(match.group(1))
    except Exception:
        pass
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except Exception:
        pass
    return None


def has_llm() -> bool:
    groq = _get_secret("GROQ_API_KEY")
    gemini = _get_secret("GEMINI_API_KEY")
    return bool(
        (groq and groq != "your_groq_api_key_here")
        or (gemini and gemini != "your_gemini_api_key_here")
    )
