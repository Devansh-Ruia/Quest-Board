#!/usr/bin/env python3
"""
Resolve quest completion, calculate XP, level-ups, and stat changes.
Accepts quest ID and character sheet data as input.
Outputs JSON with resolution results and narration prompts.
"""

import json
import sys
import datetime
import hashlib
from typing import Dict, Any, List, Tuple

# XP thresholds from RPG system
XP_THRESHOLDS = {
    1: 0, 2: 100, 3: 300, 4: 600, 5: 1000,
    6: 1500, 7: 2100, 8: 2800, 9: 3600, 10: 4500
}

def get_level_from_xp(xp: int) -> int:
    """Calculate level from total XP."""
    level = 1
    for lvl, threshold in XP_THRESHOLDS.items():
        if xp >= threshold:
            level = lvl
        else:
            break
    return level

def get_xp_to_next_level(current_level: int, current_xp: int) -> int:
    """Calculate XP needed to reach next level."""
    if current_level >= 10:
        # Level 11+ needs 1000 XP per level
        next_level_threshold = XP_THRESHOLDS[10] + (current_level - 10) * 1000
    else:
        next_level_threshold = XP_THRESHOLDS.get(current_level + 1, 1000)
    return next_level_threshold - current_xp

def get_stat_from_category(category: str) -> str:
    """Map quest category to primary stat."""
    stat_map = {
        'coding': 'INT',
        'meeting': 'CHA',
        'writing': 'WIS',
        'exercise': 'STR',
        'research': 'WIS',
        'misc': 'CON'
    }
    return stat_map.get(category, 'CON')

def get_class_from_category(category: str) -> str:
    """Map quest category to class."""
    class_map = {
        'coding': 'Artificer',
        'meeting': 'Bard',
        'writing': 'Scribe',
        'exercise': 'Barbarian',
        'research': 'Wizard',
        'misc': 'Ranger'
    }
    return class_map.get(category, 'Ranger')

def calculate_stat_bonuses(completed_quests: List[Dict[str, Any]]) -> Dict[str, int]:
    """Calculate stat bonuses based on quest completion history."""
    stat_counts = {
        'STR': 0, 'DEX': 0, 'CON': 0,
        'INT': 0, 'WIS': 0, 'CHA': 0
    }
    
    for quest in completed_quests:
        category = quest.get('category', 'misc')
        stat = get_stat_from_category(category)
        stat_counts[stat] += 1
    
    # +1 for every 5 completions in that category
    bonuses = {}
    for stat, count in stat_counts.items():
        bonuses[stat] = count // 5
    
    return bonuses

def determine_class(completed_quests: List[Dict[str, Any]]) -> str:
    """Determine class based on most-completed quest category."""
    category_counts = {
        'coding': 0, 'meeting': 0, 'writing': 0,
        'exercise': 0, 'research': 0, 'misc': 0
    }
    
    for quest in completed_quests:
        category = quest.get('category', 'misc')
        category_counts[category] += 1
    
    # Find category with most completions
    max_category = max(category_counts, key=category_counts.get)
    return get_class_from_category(max_category)

def get_level_title(level: int, character_class: str = "Unclassed") -> str:
    """Get title based on level and class."""
    if character_class == "Unclassed":
        titles = {
            1: "Novice Questgiver",
            2: "Apprentice Adventurer",
            3: "Journeyman Hero"
        }
    else:
        titles = {
            1: "Novice",
            2: "Apprentice", 
            3: "Journeyman",
            4: "Expert",
            5: "Master",
            6: "Adept",
            7: "Veteran",
            8: "Elite",
            9: "Legendary",
            10: "Paragon"
        }
    
    return titles.get(level, "Legendary")

def generate_narration_prompt(quest: Dict[str, Any], xp_gained: int, leveled_up: bool, new_level: int = None) -> Dict[str, str]:
    """Generate narration prompts for the agent."""
    difficulty = quest.get('difficulty', 'easy')
    category = quest.get('category', 'misc')
    quest_name = quest.get('name', 'Unknown Quest')
    
    # Victory narration templates
    victory_templates = {
        'easy': [
            "The scroll has been delivered. A minor task, perhaps, but even the mightiest adventurer began by clearing rats from a cellar. +{xp} XP.",
            "A small victory, but victory nonetheless. The path to greatness is paved with such moments. +{xp} XP.",
            "Task completed with practiced efficiency. You grow stronger with each challenge overcome. +{xp} XP."
        ],
        'medium': [
            "Through skill and determination, you have emerged victorious from this challenge. The townsfolk nod in approval. +{xp} XP.",
            "The obstacle has been overcome. Your reputation grows with each successful endeavor. +{xp} XP.",
            "Well done, adventurer. This quest tested your mettle, and you did not disappoint. +{xp} XP."
        ],
        'hard': [
            "Through sheer force of will, you have conquered this formidable challenge. The bards will sing of this day! +{xp} XP.",
            "A true test of your abilities, and you have risen to the occasion. Legends are built on such victories. +{xp} XP.",
            "The odds were against you, but you persevered. This triumph will be remembered. +{xp} XP."
        ],
        'boss': [
            "THE BEAST HAS FALLEN! Where lesser adventurers would have fled, you stood firm and emerged victorious. The realm is safe... for now. +{xp} XP.",
            "LEGENDARY! You have accomplished what many thought impossible. Your name will be whispered in awe throughout the land. +{xp} XP.",
            "VICTORY! The great challenge has been overcome. You have proven yourself a true hero of epic proportions. +{xp} XP."
        ]
    }
    
    # Level up narration
    level_up_narration = ""
    if leveled_up:
        level_up_narration = f"A golden light envelops you as raw power surges through your being. You have ascended to Level {new_level}! New title unlocked: {get_level_title(new_level)}. The road ahead grows darker, but so does your resolve."
    
    # Select appropriate template
    templates = victory_templates.get(difficulty, victory_templates['easy'])
    base_narration = templates[hash(quest_name) % len(templates)]
    victory_narration = base_narration.format(xp=xp_gained)
    
    return {
        "victory": victory_narration,
        "level_up": level_up_narration,
        "quest_name": quest_name,
        "difficulty": difficulty,
        "category": category
    }

def resolve_quest_completion(quest: Dict[str, Any], character_sheet: Dict[str, Any], all_completed_quests: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Main function to resolve quest completion."""
    
    # Extract current stats
    current_xp = character_sheet.get('xp', 0)
    current_level = character_sheet.get('level', 1)
    quest_xp = quest.get('xp_reward', 25)
    
    # Calculate new XP
    new_xp = current_xp + quest_xp
    new_level = get_level_from_xp(new_xp)
    leveled_up = new_level > current_level
    
    # Calculate XP to next level
    xp_to_next = get_xp_to_next_level(new_level, new_xp)
    
    # Update quest completion
    quest['completed_at'] = datetime.datetime.now().isoformat() + "Z"
    quest['status'] = 'completed'
    
    # Add to completed quests list
    updated_completed = all_completed_quests + [quest]
    
    # Calculate stat bonuses
    stat_bonuses = calculate_stat_bonuses(updated_completed)
    
    # Determine class (at level 3+)
    character_class = character_sheet.get('class', 'Unclassed')
    if new_level >= 3 and character_class == 'Unclassed':
        character_class = determine_class(updated_completed)
    
    # Update stats
    base_stats = character_sheet.get('stats', {
        'STR': 10, 'DEX': 10, 'CON': 10,
        'INT': 10, 'WIS': 10, 'CHA': 10
    })
    
    updated_stats = {}
    for stat, base_value in base_stats.items():
        bonus = stat_bonuses.get(stat, 0)
        updated_stats[stat] = base_value + bonus
    
    # Generate narration prompts
    narration = generate_narration_prompt(quest, quest_xp, leveled_up, new_level)
    
    # Prepare result
    result = {
        "quest_completed": quest,
        "xp_gained": quest_xp,
        "new_total_xp": new_xp,
        "previous_level": current_level,
        "new_level": new_level,
        "leveled_up": leveled_up,
        "xp_to_next_level": xp_to_next,
        "class": character_class,
        "title": get_level_title(new_level, character_class),
        "updated_stats": updated_stats,
        "stat_changes": stat_bonuses,
        "total_quests_completed": len(updated_completed),
        "narration_prompts": narration
    }
    
    return result

def main():
    """Main function to process input and resolve quest."""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
        
        quest = input_data.get('quest', {})
        character_sheet = input_data.get('character_sheet', {})
        completed_quests = input_data.get('completed_quests', [])
        
        # Resolve quest completion
        result = resolve_quest_completion(quest, character_sheet, completed_quests)
        
        # Output result
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
