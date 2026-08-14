"""
Gemini AI Service

Handles AI-powered insights generation using Google's Gemini API.
Provides empathetic, supportive responses for emotion reports.

TODO: Add retry logic for API failures
TODO: Add response caching for similar queries
TODO: Add fallback to simpler templates if API fails
"""
import logging
import os
import google.generativeai as genai

from app.core.config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)

# Configure Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
else:
    logger.warning("GEMINI_API_KEY not set. AI insights will use fallback responses.")
    model = None


def generate_daily_insight(summary: str) -> str:
    """
    Generate daily emotion insight using Gemini AI.
    
    Args:
        summary: Summary of today's emotions
        
    Returns:
        AI-generated insight text
    """
    if not model:
        logger.warning("Gemini model not available, using fallback")
        return "Your emotions today show meaningful patterns. Take a few moments to reflect and care for yourself."
    
    try:
        prompt = f"""
You are a supportive mental health assistant.

Based on today's emotional summary:
1. Write a short INSIGHT (2–3 lines)
2. Write a gentle SUGGESTION (1–2 lines)

Rules:
- Do NOT diagnose
- Be calm, supportive, non-judgmental
- Avoid medical terms
- Keep responses concise and empathetic

Summary:
{summary}

Respond ONLY in this format:

Insight:
<text>

Suggestion:
<text>
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating daily insight: {str(e)}")
        raise


def generate_weekly_insight(summary: str) -> str:
    """
    Generate weekly emotion insight using Gemini AI.
    
    Args:
        summary: Summary of weekly emotions and trends
        
    Returns:
        AI-generated insight text
    """
    if not model:
        logger.warning("Gemini model not available, using fallback")
        return "Your emotions this week show repeating patterns. Maintain routines that support emotional balance."
    
    try:
        prompt = f"""
You are a supportive mental health assistant.

Based on the WEEKLY emotional summary:
1. Write a short INSIGHT (3–4 lines)
2. Write a gentle SUGGESTION (2–3 lines)

Rules:
- Do NOT diagnose
- Be calm, supportive, non-judgmental
- Avoid medical terms
- Focus on habits and routines
- Identify patterns and trends

Weekly Summary:
{summary}

Respond ONLY in this format:

Insight:
<text>

Suggestion:
<text>
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating weekly insight: {str(e)}")
        raise




