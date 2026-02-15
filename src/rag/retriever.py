"""
Behavior Knowledge RAG Retrieval

Simple keyword-based matching to find relevant behavioral patterns
from the behavior_library.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional


def retrieve_behavior_knowledge(scenario: str) -> dict:
    """
    Retrieve behavior knowledge from behavior_library based on scenario.

    Uses simple keyword matching to find the best matching JSON file.
    Loads all JSON files and returns the one with the most keyword matches.

    Args:
        scenario: Scenario description or keywords (e.g., "office stress", "exam anxiety")

    Returns:
        Dict containing behavior patterns, or empty dict if no match found

    Example:
        >>> knowledge = retrieve_behavior_knowledge("boss yelled at me work")
        >>> print(knowledge.get('scenario'))  # 'office_stress'
        >>> print(knowledge.get('do'))  # List of helpful patterns
    """

    # Try multiple possible paths for behavior_library
    possible_paths = [
        Path(__file__).parent.parent.parent / "behavior_library",  # Development
        Path("/app/behavior_library"),  # Docker production
        Path.cwd() / "behavior_library",  # Alternative
    ]

    lib_path = None
    for path in possible_paths:
        if path.exists():
            lib_path = path
            break

    if lib_path is None:
        print(f"Warning: behavior_library not found. Tried: {[str(p) for p in possible_paths]}")
        return {}

    # Convert scenario to lowercase keywords
    scenario_keywords = set(scenario.lower().split())

    best_match = None
    best_score = 0

    # Scan all JSON files in behavior_library
    for json_file in lib_path.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle both array and single object formats
            if isinstance(data, list) and len(data) > 0:
                data = data[0]  # Take first entry if array

            # Extract scenario name from filename
            file_scenario = json_file.stem.replace('_enhanced', '').replace('_', ' ')

            # Calculate keyword match score
            file_keywords = set(file_scenario.split())

            # Also check the scenario field if it exists
            if 'scenario' in data:
                file_keywords.update(data['scenario'].replace('_', ' ').split())

            # Count matching keywords
            matches = len(scenario_keywords & file_keywords)

            # Boost score if filename closely matches
            if any(keyword in json_file.stem.lower() for keyword in scenario_keywords):
                matches += 2

            if matches > best_score:
                best_score = matches
                best_match = data

        except Exception as e:
            # Skip files that can't be parsed
            continue

    # Return best match or empty dict
    if best_match:
        return best_match
    else:
        return {}


def get_all_scenarios() -> List[str]:
    """
    Get list of all available scenarios in behavior_library.

    Returns:
        List of scenario names
    """
    lib_path = Path(__file__).parent.parent.parent / "behavior_library"

    if not lib_path.exists():
        return []

    scenarios = []
    for json_file in lib_path.glob("*.json"):
        scenario_name = json_file.stem.replace('_enhanced', '').replace('_', ' ')
        scenarios.append(scenario_name)

    return sorted(scenarios)


def find_relevant_knowledge(
    user_message: str,
    social_analysis: Optional[Dict] = None
) -> dict:
    """
    Find relevant behavior knowledge based on user message and social analysis.

    Combines keywords from both user message and detected signals for better matching.

    Args:
        user_message: The user's actual message
        social_analysis: Optional dict with emotion, relationship, etc.

    Returns:
        Dict containing relevant behavior patterns
    """

    # Build search query from message and signals
    search_terms = [user_message]

    if social_analysis:
        # Add emotion
        if 'primary_emotion' in social_analysis:
            search_terms.append(social_analysis['primary_emotion'])

        # Add relationship context
        if 'relationship' in social_analysis:
            search_terms.append(social_analysis['relationship'])

        # Add user need
        if 'user_need' in social_analysis:
            search_terms.append(social_analysis['user_need'])

    # Combine all search terms
    combined_query = ' '.join(search_terms)

    return retrieve_behavior_knowledge(combined_query)

