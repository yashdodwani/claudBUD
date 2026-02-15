"""
WhatsApp Chat Parser

Cleans WhatsApp chat exports for signal extraction.
PRIVACY-FIRST: No raw chat storage, only processes in-memory.
"""

import re
from typing import List


def parse_whatsapp_chat(input_text: str) -> str:
    """
    Parse WhatsApp chat export and clean it for analysis.

    This function:
    - Removes timestamps
    - Removes phone numbers
    - Merges multi-line messages
    - Returns clean conversation text

    IMPORTANT: Does NOT store to disk. Only processes in memory.
    Raw chat is discarded after signal extraction.

    Args:
        input_text: Raw WhatsApp chat export text

    Returns:
        Clean conversation text ready for analyze_social_context()

    Example:
        >>> chat = '''
        ... 12/01/2024, 10:30 - +91 98765 43210: Hey boss, can we talk?
        ... 12/01/2024, 10:35 - Manager: What is it?
        ... 12/01/2024, 10:36 - +91 98765 43210: I'm feeling overwhelmed
        ... with all these tasks
        ... '''
        >>> clean = parse_whatsapp_chat(chat)
        >>> print(clean)
        Hey boss, can we talk?
        What is it?
        I'm feeling overwhelmed with all these tasks
    """

    if not input_text or not input_text.strip():
        return ""

    lines = input_text.strip().split('\n')
    cleaned_messages = []
    current_message = []

    # WhatsApp message pattern:
    # Formats supported:
    # - 12/01/2024, 10:30 - Contact Name: Message (Android)
    # - [1/12/24, 10:30:45 AM] Contact: Message (iOS)

    # Try to match message lines with flexible pattern
    message_pattern = re.compile(
        r'^\[?'  # Optional opening bracket
        r'(?P<date>\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})'  # Date
        r'[,\s]+'  # Separator
        r'(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)'  # Time
        r'\]?'  # Optional closing bracket
        r'\s*-?\s*'  # Optional dash with spaces (Android) or just spaces (iOS)
        r'(?P<sender>[^\]:]+?)'  # Sender name/number (non-greedy, stop at : or ])
        r':\s*'  # Colon after sender
        r'(?P<message>.*)$',  # Message content
        re.IGNORECASE
    )

    for line in lines:
        line = line.strip()

        if not line:
            continue

        match = message_pattern.match(line)

        if match:
            # New message detected
            # Save previous message if exists
            if current_message:
                cleaned_messages.append(' '.join(current_message))
                current_message = []

            # Extract sender and message using named groups
            sender = match.group('sender').strip()
            message = match.group('message').strip()

            # Remove phone numbers from sender
            sender_clean = re.sub(r'\+?\d[\d\s\-]{8,}', 'User', sender)

            # Store message (without timestamp and cleaned sender)
            if message:  # Only add non-empty messages
                current_message.append(message)

        else:
            # Continuation of previous message (multi-line)
            if current_message:
                current_message.append(line)

    # Add last message
    if current_message:
        cleaned_messages.append(' '.join(current_message))

    # Join all messages with newlines
    clean_text = '\n'.join(cleaned_messages)

    # Additional cleanup
    # Remove system messages
    system_messages = [
        'Messages and calls are end-to-end encrypted',
        'created group',
        'added',
        'left',
        'changed the subject',
        'changed this group',
        'image omitted',
        'video omitted',
        'audio omitted',
        'sticker omitted',
        'document omitted',
        'GIF omitted',
        'Contact card omitted',
        'Location omitted',
    ]

    lines = clean_text.split('\n')
    filtered_lines = []

    for line in lines:
        # Skip if line contains system message keywords
        is_system = any(keyword in line.lower() for keyword in system_messages)
        if not is_system and line.strip():
            filtered_lines.append(line)

    return '\n'.join(filtered_lines)


def extract_last_n_messages(input_text: str, n: int = 10) -> str:
    """
    Extract last N messages from WhatsApp chat.

    Useful for analyzing recent conversation context without processing
    entire chat history.

    Args:
        input_text: Raw WhatsApp chat export
        n: Number of recent messages to extract (default: 10)

    Returns:
        Clean text of last N messages
    """
    clean_text = parse_whatsapp_chat(input_text)

    if not clean_text:
        return ""

    messages = clean_text.split('\n')
    last_messages = messages[-n:] if len(messages) > n else messages

    return '\n'.join(last_messages)

