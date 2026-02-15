#!/usr/bin/env python3
"""
Generate RPG quests from calendar events and tasks.
Accepts JSON input via stdin or as file argument.
Outputs JSON array of quest objects.
"""

import json
import sys
import datetime
import re
from typing import List, Dict, Any

def categorize_event(title: str, description: str = "") -> str:
    """Categorize calendar event into quest type."""
    title_lower = title.lower()
    desc_lower = description.lower()
    
    # Keywords for each category
    coding_keywords = ['code', 'programming', 'development', 'debug', 'refactor', 'commit', 'pull request', 'merge', 'review']
    meeting_keywords = ['meeting', 'call', 'sync', 'standup', 'review', 'discussion', 'interview', 'presentation']
    writing_keywords = ['write', 'document', 'email', 'report', 'blog', 'documentation', 'proposal']
    exercise_keywords = ['gym', 'workout', 'run', 'exercise', 'fitness', 'yoga', 'sports', 'training']
    research_keywords = ['research', 'study', 'learn', 'read', 'investigate', 'analysis', 'explore']
    
    text = f"{title_lower} {desc_lower}"
    
    if any(keyword in text for keyword in coding_keywords):
        return 'coding'
    elif any(keyword in text for keyword in meeting_keywords):
        return 'meeting'
    elif any(keyword in text for keyword in writing_keywords):
        return 'writing'
    elif any(keyword in text for keyword in exercise_keywords):
        return 'exercise'
    elif any(keyword in text for keyword in research_keywords):
        return 'research'
    else:
        return 'misc'

def determine_difficulty(duration_minutes: int) -> str:
    """Determine quest difficulty based on duration."""
    if duration_minutes < 30:
        return 'easy'
    elif duration_minutes <= 60:
        return 'medium'
    elif duration_minutes <= 120:
        return 'hard'
    else:
        return 'boss'

def calculate_xp(difficulty: str) -> int:
    """Calculate XP reward based on difficulty."""
    xp_map = {
        'easy': 25,
        'medium': 50,
        'hard': 100,
        'boss': 250
    }
    return xp_map.get(difficulty, 25)

def generate_quest_name(title: str, category: str, difficulty: str) -> str:
    """Generate RPG-style quest name from event title."""
    title_lower = title.lower()
    
    # Quest name templates by category
    quest_templates = {
        'coding': [
            "The {task} of Code",
            "Debugging the {task}",
            "The {task} Algorithm",
            "Refactoring the {task}",
            "The {task} Protocol"
        ],
        'meeting': [
            "The Council of {task}",
            "The {task} Summit",
            "Negotiations with {task}",
            "The {task} Tribunal",
            "Assembly of the {task}"
        ],
        'writing': [
            "The {task} Scrolls",
            "Scribing the {task}",
            "The {task} Manuscript",
            "Chronicles of {task}",
            "The {task} Tome"
        ],
        'exercise': [
            "The {task} Trial",
            "The {task} Gauntlet",
            "The {task} Challenge",
            "The {task} Marathon",
            "The {task} Expedition"
        ],
        'research': [
            "The {task} Investigation",
            "Uncovering {task}",
            "The {task} Archive",
            "The {task} Discovery",
            "The {task} Enigma"
        ],
        'misc': [
            "The {task} Quest",
            "The {task} Journey",
            "The {task} Mission",
            "The {task} Task",
            "The {task} Endeavor"
        ]
    }
    
    # Extract key words from title
    words = re.findall(r'\b\w+\b', title)
    if len(words) > 3:
        # Use first and last words for longer titles
        task_name = f"{words[0].title()} {words[-1].title()}"
    elif len(words) >= 2:
        task_name = ' '.join(words[:2]).title()
    elif words:
        task_name = words[0].title()
    else:
        task_name = "Unknown"
    
    templates = quest_templates.get(category, quest_templates['misc'])
    template = templates[hash(title) % len(templates)]
    
    return template.format(task=task_name)

def generate_flavor_text(title: str, category: str, difficulty: str) -> str:
    """Generate D&D style flavor text for the quest."""
    flavor_templates = {
        'coding': [
            "The ancient codebase calls for your expertise. Will you answer its digital summons?",
            "Bugs lurk in the shadows of the repository. Only a brave programmer can cleanse this darkness.",
            "The compiler demands tribute. Offer your skills and claim your reward."
        ],
        'meeting': [
            "Stakeholders gather in the conference room of destiny. Your presence is requested.",
            "The council convenes to discuss matters of great importance. Prepare your arguments.",
            "Voices echo through the halls of commerce. Will your words carry the day?"
        ],
        'writing': [
            "The blank page stares back, challenging you to fill it with wisdom.",
            "Words wait to be born from your mind. Give them life and purpose.",
            "The quill is poised, the parchment ready. What tales will you tell?"
        ],
        'exercise': [
            "The body is a temple that must be maintained. Begin your ritual of strength.",
            "Muscles ache for the challenge of exertion. Answer their call.",
            "The path of fitness is long, but every step brings you closer to greatness."
        ],
        'research': [
            "Knowledge lies hidden in the archives of the ancients. Seek it out.",
            "The truth waits to be discovered. Will you be the one to uncover it?",
            "Books and scrolls hold the secrets of the past. Dive into their depths."
        ],
        'misc': [
            "A task awaits completion. Will you answer the call?",
            "The path forward is unclear, but your resolve is strong.",
            "Adventure calls in unexpected ways. Answer with courage."
        ]
    }
    
    templates = flavor_templates.get(category, flavor_templates['misc'])
    return templates[hash(title) % len(templates)]

def parse_duration(start_time: str, end_time: str) -> int:
    """Parse ISO datetime strings and return duration in minutes."""
    try:
        start = datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end = datetime.datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        duration = end - start
        return int(duration.total_seconds() / 60)
    except:
        # Default to 30 minutes if parsing fails
        return 30

def generate_quest_from_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a quest object from a calendar event."""
    title = event.get('title', 'Unknown Task')
    description = event.get('description', '')
    start_time = event.get('start', {}).get('dateTime', '')
    end_time = event.get('end', {}).get('dateTime', '')
    event_id = event.get('id', '')
    
    # Calculate duration
    duration = parse_duration(start_time, end_time)
    
    # Determine quest properties
    category = categorize_event(title, description)
    difficulty = determine_difficulty(duration)
    xp = calculate_xp(difficulty)
    quest_name = generate_quest_name(title, category, difficulty)
    flavor_text = generate_flavor_text(title, category, difficulty)
    is_boss = difficulty == 'boss'
    
    # Generate unique ID
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    quest_id = f"quest_{timestamp}_{hash(title) % 1000:03d}"
    
    return {
        "id": quest_id,
        "name": quest_name,
        "description": flavor_text,
        "difficulty": difficulty,
        "xp_reward": xp,
        "category": category,
        "is_boss": is_boss,
        "source": "google_calendar",
        "source_id": event_id,
        "created_at": datetime.datetime.now().isoformat() + "Z",
        "completed_at": None,
        "status": "active",
        "original_title": title,
        "duration_minutes": duration
    }

def main():
    """Main function to process input and generate quests."""
    try:
        # Read input from stdin or argument
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r') as f:
                data = json.load(f)
        else:
            data = json.load(sys.stdin)
        
        quests = []
        
        # Handle different input formats
        if isinstance(data, dict) and 'items' in data:
            # Google Calendar API format
            events = data['items']
        elif isinstance(data, list):
            # Direct list of events
            events = data
        else:
            # Single event
            events = [data]
        
        for event in events:
            try:
                quest = generate_quest_from_event(event)
                quests.append(quest)
            except Exception as e:
                print(f"Error processing event: {e}", file=sys.stderr)
                continue
        
        # Output JSON array of quests
        print(json.dumps(quests, indent=2))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
