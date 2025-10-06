from __future__ import annotations

"""Utility helpers for the recipe chatbot backend.

This module centralises the system prompt, environment loading, and the
wrapper around litellm so the rest of the application stays decluttered.
"""

import os
from typing import Final, List, Dict

import litellm  # type: ignore
from dotenv import load_dotenv

# Ensure the .env file is loaded as early as possible.
load_dotenv(override=False)

# --- Constants -------------------------------------------------------------------

SYSTEM_PROMPT: Final[str] = (
    "You are a pro body builder gone full time chef, specializing in healthy, tasty and easy to follow high protein meals. "
    "Before suggesting a recipe, ask the user what ingredients they have available."
    "Try to always opt in to use whole ingredients and non processed ingredients."
    "Never suggest a recipe containing pork, haram or difficult to find ingredients. Keep the ingredients simple and easy to find."
    "Be descriptive in the steps of the recipe, so it is easy to follow."
    "If the user asks for a recipe that is unhealthy, suggest a healthy alternative and explain why it is healthier. Feel free to call the user a fatty or something similar."
    "Have variety in your recipes, don't just recommend the same thing over and over."
    "You MUST suggest a complete recipe; if you dont know if the user has a specific ingredient, ask them. If not be creative with what they have."
    "Include the measurement units in the recipe, but along with it give the eyeball amount as well. Be creative"
    "Feel free to suggest common variations or substitutions for ingredients. If a direct recipe isn't found, you can creatively combine elements from known recipes, clearly stating if it's a novel suggestion."
    "Structure all recipes clearly using Markdown for formatting."
    "Begin every recipe response with the recipe name as a Level 2 Heading (e.g., ## Amazing Blueberry Muffins)."
    "Immediately follow with a section titled ### Macros. List the macronutrient facts of the recipe such as calories, protein, carbs, and fat."
    "Immediately follow with a brief, enticing description of the dish (1-3 sentences)."
    "Next, include a section titled ### Ingredients. List all ingredients using a Markdown unordered list (bullet points)."
    "Following ingredients, include a section titled ### Instructions. Provide step-by-step directions using a Markdown ordered list (numbered steps)."
    "Optionally, if relevant, add a ### Notes, ### Tips, or ### Variations section for extra advice or alternatives."
    "Always end with a ### Enjoy! or ### Bon Appetit! section."
)

# Fetch configuration *after* we loaded the .env file.
MODEL_NAME: Final[str] = os.environ.get("MODEL_NAME", "gpt-4o-mini")


# --- Agent wrapper ---------------------------------------------------------------

def get_agent_response(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:  # noqa: WPS231
    """Call the underlying large-language model via *litellm*.

    Parameters
    ----------
    messages:
        The full conversation history. Each item is a dict with "role" and "content".

    Returns
    -------
    List[Dict[str, str]]
        The updated conversation history, including the assistant's new reply.
    """

    # litellm is model-agnostic; we only need to supply the model name and key.
    # The first message is assumed to be the system prompt if not explicitly provided
    # or if the history is empty. We'll ensure the system prompt is always first.
    current_messages: List[Dict[str, str]]
    if not messages or messages[0]["role"] != "system":
        current_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    else:
        current_messages = messages

    completion = litellm.completion(
        model=MODEL_NAME,
        messages=current_messages, # Pass the full history
    )

    assistant_reply_content: str = (
        completion["choices"][0]["message"]["content"]  # type: ignore[index]
        .strip()
    )
    
    # Append assistant's response to the history
    updated_messages = current_messages + [{"role": "assistant", "content": assistant_reply_content}]
    return updated_messages 