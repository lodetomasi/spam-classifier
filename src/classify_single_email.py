#!/usr/bin/env python3
"""
Single Email Multi-Agent Spam Classifier
Classifies a single email using the multi-agent system
"""

import json
import sys
from real_agent_classifier import load_pattern_catalog, format_pattern_context, create_agent_prompt, parse_agent_response


def classify_email(email_text: str, email_id: int = None, actual_label: str = None, detected_patterns: list = None):
    """Classify a single email using multi-agent system."""

    # Load pattern catalog
    catalog = load_pattern_catalog('data/pattern_catalog.json')
    pattern_context = format_pattern_context(catalog)

    print("\n" + "="*70)
    print("MULTI-AGENT SPAM CLASSIFICATION")
    print("="*70)
    print(f"\nEmail ID: {email_id}")
    print(f"Actual Label: {actual_label}")
    print(f"Detected Patterns: {', '.join(detected_patterns) if detected_patterns else 'None'}")
    print("\nEmail Content:")
    print("-"*70)
    print(email_text[:500] + ("..." if len(email_text) > 500 else ""))
    print("-"*70)

    # Step 1: Content Analyzer
    print("\n[AGENT 1] Content Analyzer")
    print("-"*70)
    content_prompt = create_agent_prompt("content_analyzer", email_text, pattern_context)
    print("Prompt generated. Awaiting Task invocation...")
    print("\nCONTENT ANALYZER PROMPT:")
    print(content_prompt)

    # Step 2: Pattern Recognizer
    print("\n\n[AGENT 2] Pattern Recognizer")
    print("-"*70)
    pattern_prompt = create_agent_prompt("pattern_recognizer", email_text, pattern_context)
    print("Prompt generated. Awaiting Task invocation...")
    print("\nPATTERN RECOGNIZER PROMPT:")
    print(pattern_prompt)

    # Note: In actual execution, these results would come from Task tool invocations
    # For now, we'll show the structure
    print("\n\n[AGENT 3] Intent Analyzer")
    print("-"*70)
    intent_prompt = create_agent_prompt("intent_analyzer", email_text, pattern_context, {})
    print("Prompt generated. Awaiting Task invocation...")
    print("\nINTENT ANALYZER PROMPT:")
    print(intent_prompt)

    print("\n\n[AGENT 4] Consensus Agent")
    print("-"*70)
    print("Consensus agent will synthesize all results after agents 1-3 complete.")

    print("\n" + "="*70)
    print("Next Steps:")
    print("="*70)
    print("1. Execute Content Analyzer prompt using Task tool")
    print("2. Execute Pattern Recognizer prompt using Task tool")
    print("3. Execute Intent Analyzer prompt using Task tool")
    print("4. Execute Consensus Agent prompt with all results")
    print("5. Format final JSON response")


if __name__ == '__main__':
    # The email from the user
    email_text = """Subject: neon retreat
ho ho ho, we're around to that most wonderful time of the year --- neon leaders retreat time!
i know that this time of year is extremely hectic, and that it's tough to think about anything past the holidays, but life does go on past the week of december 25 through january 1, and that's what i'd like you to think about for a minute.
on the calendar that i handed out at the beginning of the fall semester, the retreat was scheduled for the weekend of january 5-6..."""

    email_id = 12
    actual_label = "ham"
    detected_patterns = ["business correspondence", "internal communication"]

    classify_email(email_text, email_id, actual_label, detected_patterns)
