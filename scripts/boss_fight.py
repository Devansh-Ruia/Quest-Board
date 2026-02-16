#!/usr/bin/env python3
"""
Generate 3-phase boss fight encounters for major quests.
Accepts boss quest object and character sheet as input.
Outputs JSON with structured encounter phases.
"""

import json
import sys
import hashlib
from typing import Dict, Any, List

def roll_d20(seed: str = "") -> int:
    """Generate deterministic d20 roll based on seed."""
    if seed:
        hash_obj = hashlib.md5(seed.encode())
        return (int(hash_obj.hexdigest()[:8], 16) % 20) + 1
    else:
        import random
        return random.randint(1, 20)

def get_boss_type(quest: Dict[str, Any]) -> str:
    """Determine boss type based on quest category and content."""
    category = quest.get('category', 'misc')
    title = quest.get('name', '').lower()
    
    # Check for specific boss type keywords
    if 'dragon' in title or 'deadline' in title:
        return 'deadline_dragon'
    elif 'code' in title or 'refactor' in title or 'legacy' in title:
        return 'code_lich'
    elif 'bureaucracy' in title or 'admin' in title or 'compliance' in title:
        return 'bureaucracy_behemoth'
    elif 'presentation' in title or 'meeting' in title or 'review' in title:
        return 'presentation_phoenix'
    
    # Default by category
    boss_types = {
        'coding': 'code_lich',
        'meeting': 'presentation_phoenix',
        'writing': 'documentation_demon',
        'exercise': 'endurance_titan',
        'research': 'knowledge_devourer',
        'misc': 'chaos_entity'
    }
    
    return boss_types.get(category, 'chaos_entity')

def get_boss_name(boss_type: str) -> str:
    """Get boss name and title."""
    boss_names = {
        'deadline_dragon': "The Dragon of Deadlines",
        'code_lich': "The Lich of Legacy Code",
        'bureaucracy_behemoth': "The Behemoth of Bureaucracy",
        'presentation_phoenix': "The Phoenix of Presentations",
        'documentation_demon': "The Demon of Documentation",
        'endurance_titan': "The Titan of Endurance",
        'knowledge_devourer': "The Devourer of Knowledge",
        'chaos_entity': "The Entity of Chaos"
    }
    return boss_names.get(boss_type, "The Unknown Boss")

def generate_phase_1(boss_type: str, quest: Dict[str, Any], character_sheet: Dict[str, Any]) -> Dict[str, Any]:
    """Generate Phase 1: The Approach."""
    boss_name = get_boss_name(boss_type)
    quest_name = quest.get('name', 'Unknown Quest')
    player_level = character_sheet.get('level', 1)
    
    # Generate dice roll for flavor
    dice_seed = f"{quest_name}_phase1_{player_level}"
    dice_roll = roll_d20(dice_seed)
    
    # Phase 1 templates by boss type
    phase_1_templates = {
        'deadline_dragon': [
            f"okay so here's the thing about this {boss_name.lower()}. it's breathing down your neck and the deadline is way too close for comfort.",
            f"right so you're staring at the {boss_name.lower()} and thinking 'this is fine, i've got this'. you don't. but you will anyway.",
            f"time to face the {boss_name.lower()}. the quest {quest_name} begins now. godspeed."
        ],
        'code_lich': [
            f"the crypt of {boss_name.lower()} is calling your name. probably because something broke again. typical.",
            f"deep in the digital underworld, the {boss_name.lower()} awaits. your IDE is already open, isn't it. let's do this.",
            f"the {boss_name.lower()} rises from the repository of damned. at least this time you have coffee."
        ],
        'presentation_phoenix': [
            f"the boardroom transforms into an arena where the {boss_name.lower()} awaits. stakeholders looking judgy. fun.",
            f"the {boss_name.lower()} spreads its wings of powerpoint and judgment. your slides are your sword. good luck with that.",
            f"in the hallowed halls of commerce, the {boss_name.lower()} circles. each beat of its wings is another executive question. brace yourself."
        ]
    }
    
    # Get appropriate template or use generic
    templates = phase_1_templates.get(boss_type, [
        f"the {boss_name.lower()} stands before you. this is gonna be a problem. time to deal with it for {quest_name}.",
        f"so you're here to fight the {boss_name.lower()}. the quest {quest_name} led you to this mess. good luck.",
        f"the path to completing {quest_name} is blocked by the {boss_name.lower()}. steel yourself. this'll be rough."
    ])
    
    narration = templates[hash(quest_name) % len(templates)]
    
    # Add dice roll flavor
    if dice_roll >= 18:
        roll_flavor = "You feel a surge of confidence! The odds seem to be in your favor."
    elif dice_roll <= 3:
        roll_flavor = "A sense of dread washes over you. This will be more difficult than anticipated."
    else:
        roll_flavor = "You assess the situation carefully. The challenge ahead is significant but manageable."
    
    return {
        "phase": 1,
        "title": "The Approach",
        "narration": narration,
        "dice_roll": dice_roll,
        "roll_flavor": roll_flavor,
        "challenge": f"Begin the {quest_name} with determination and focus.",
        "progress_marker": "25%"
    }

def generate_phase_2(boss_type: str, quest: Dict[str, Any], character_sheet: Dict[str, Any]) -> Dict[str, Any]:
    """Generate Phase 2: The Twist."""
    boss_name = get_boss_name(boss_type)
    quest_name = quest.get('name', 'Unknown Quest')
    player_level = character_sheet.get('level', 1)
    
    # Generate dice roll for flavor
    dice_seed = f"{quest_name}_phase2_{player_level}"
    dice_roll = roll_d20(dice_seed)
    
    # Phase 2 templates by boss type
    phase_2_templates = {
        'deadline_dragon': [
            f"damn, the {boss_name.lower()} just got REAL angry. the deadline moved up. of course it did.",
            f"mid-battle, the {boss_name.lower()} reveals a hidden phase—additional requirements materialize out of thin air. this just got way harder than it needed to be.",
            f"the {boss_name.lower()} summons its minions: meetings, interruptions, and urgent emails. fight through the noise. stay focused on {quest_name}."
        ],
        'code_lich': [
            f"the {boss_name.lower()} laughs as the codebase suddenly shifts! dependencies break, APIs change, ground beneath your feet becomes unstable. classic.",
            f"unexpectedly, the {boss_name.lower()} reveals that the real problem lies deeper than you thought. the surface issues were just the appetizer.",
            f"the {boss_name.lower()} casts a spell of confusion! your IDE crashes, documentation becomes contradictory, and your usual tools fail you. improvise."
        ],
        'presentation_phoenix': [
            f"the {boss_name.lower()} rises from the ashes of your first points with challenging questions! stakeholders reveal hidden concerns you never saw coming.",
            f"mid-presentation, the {boss_name.lower()} transforms meeting dynamics. key decision-makers change their minds, new requirements emerge. adapt or die.",
            f"the {boss_name.lower()} tests your resolve with technical difficulties! the projector fails, slides won't advance, and your demo environment crashes. the show must go on!"
        ]
    }
    
    # Get appropriate template or use generic
    templates = phase_2_templates.get(boss_type, [
        f"The {boss_name.lower()} reveals its true power! A complication emerges that threatens to derail your progress on {quest_name}. You must think creatively to overcome this new challenge.",
        f"Just when you thought you had the upper hand, the {boss_name.lower()} unleashes an unexpected twist. The path to completing {quest_name} has suddenly become more complex.",
        f"The {boss_name.lower()} adapts to your strategy, forcing you to evolve your approach. This middle phase will determine whether you have the flexibility to succeed."
    ])
    
    narration = templates[hash(quest_name + "_twist") % len(templates)]
    
    # Add dice roll flavor
    if dice_roll >= 18:
        roll_flavor = "Critical insight! You spot a weakness in the boss's strategy."
    elif dice_roll <= 3:
        roll_flavor = "A setback! The boss's attack catches you off guard."
    else:
        roll_flavor = "You hold your ground, neither gaining nor losing advantage."
    
    return {
        "phase": 2,
        "title": "The Twist",
        "narration": narration,
        "dice_roll": dice_roll,
        "roll_flavor": roll_flavor,
        "challenge": f"Adapt your strategy to overcome the unexpected complications in {quest_name}.",
        "progress_marker": "50%"
    }

def generate_phase_3(boss_type: str, quest: Dict[str, Any], character_sheet: Dict[str, Any]) -> Dict[str, Any]:
    """Generate Phase 3: The Resolution."""
    boss_name = get_boss_type(quest)
    boss_display_name = get_boss_name(boss_type)
    quest_name = quest.get('name', 'Unknown Quest')
    player_level = character_sheet.get('level', 1)
    xp_reward = quest.get('xp_reward', 250)
    
    # Generate dice roll for flavor
    dice_seed = f"{quest_name}_phase3_{player_level}"
    dice_roll = roll_d20(dice_seed)
    
    # Phase 3 templates by boss type
    phase_3_templates = {
        'deadline_dragon': [
            f"IT'S HAPPENING. FINAL PUSH ON THE {boss_display_name.upper()}. everything you've got, right now.",
            f"this is it—the moment of truth! the {boss_display_name.lower()} is cornered, its power waning. one final effort will decide the fate of {quest_name}.",
            f"the {boss_display_name.lower()} roars its defiance, but you can see fatigue in its movements. the quest {quest_name} reaches its climax. this final battle will decide everything!"
        ],
        'code_lich': [
            f"the {boss_display_name.lower()} faces its final compilation! one last push of debugging, refactoring, and testing will determine whether the codebase is saved or doomed to eternal legacy status.",
            f"the {boss_display_name.lower()} gathers its remaining dark energy for a final assault. your fingers fly across the keyboard as you race against the forces of technical debt. the fate of {quest_name} hangs in the balance!",
            f"the final merge conflict! the {boss_display_name.lower()} makes its last stand amidst conflicting branches and merge conflicts. your git-fu will be tested like never before in {quest_name}."
        ],
        'presentation_phoenix': [
            f"the {boss_display_name.lower()} prepares for its final rebirth! your closing arguments, summary slides, and call to action will determine whether you emerge victorious or face the ashes of defeat.",
            f"the Q&A from hell! the {boss_display_name.lower()} unleashes its most challenging questions yet. your knowledge, confidence, and communication skills will be put to the ultimate test in {quest_name}.",
            f"the final decision point! the {boss_display_name.lower()} awaits the judgment of stakeholders. your performance in {quest_name} reaches its dramatic conclusion."
        ]
    }
    
    # Get appropriate template or use generic
    templates = phase_3_templates.get(boss_type, [
        f"The {boss_display_name.lower()} stands before you, weakened but defiant. This final phase of {quest_name} will require all your strength, wisdom, and courage. The battle reaches its climax!",
        f"The moment of arrival! The {boss_display_name.lower()} faces its final challenge. Everything you've worked for in {quest_name} comes down to this decisive moment.",
        f"Victory or defeat! The {boss_display_name.lower()} gathers its remaining power for one final confrontation. The quest {quest_name} reaches its epic conclusion."
    ])
    
    narration = templates[hash(quest_name + "_final") % len(templates)]
    
    # Add dice roll flavor
    if dice_roll >= 18:
        roll_flavor = "CRITICAL HIT! You've found the boss's weakness!"
    elif dice_roll <= 3:
        roll_flavor = "The boss lands a heavy blow, but you refuse to fall!"
    else:
        roll_flavor = "The battle reaches its dramatic conclusion!"
    
    return {
        "phase": 3,
        "title": "The Resolution",
        "narration": narration,
        "dice_roll": dice_roll,
        "roll_flavor": roll_flavor,
        "challenge": f"Complete {quest_name} with your full effort and claim your victory!",
        "progress_marker": "100%",
        "victory_xp": xp_reward,
        "victory_message": f"YOU DID IT AND I AM LOSING MY MIND. the {boss_display_name.lower()} is finally DEAD. +{xp_reward} XP and eternal glory."
    }

def generate_boss_encounter(quest: Dict[str, Any], character_sheet: Dict[str, Any]) -> Dict[str, Any]:
    """Generate complete 3-phase boss encounter."""
    boss_type = get_boss_type(quest)
    boss_name = get_boss_name(boss_type)
    
    # Generate all three phases
    phase_1 = generate_phase_1(boss_type, quest, character_sheet)
    phase_2 = generate_phase_2(boss_type, quest, character_sheet)
    phase_3 = generate_phase_3(boss_type, quest, character_sheet)
    
    # Create encounter summary
    encounter = {
        "boss_type": boss_type,
        "boss_name": boss_name,
        "quest_name": quest.get('name', 'Unknown Quest'),
        "quest_difficulty": quest.get('difficulty', 'boss'),
        "player_level": character_sheet.get('level', 1),
        "phases": [phase_1, phase_2, phase_3],
        "total_xp_reward": quest.get('xp_reward', 250),
        "estimated_duration": quest.get('duration_minutes', 120),
        "encounter_summary": f"Face the mighty {boss_name.lower()} in this epic {quest.get('difficulty', 'boss')} battle!"
    }
    
    return encounter

def main():
    """Main function to process input and generate boss encounter."""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
        
        quest = input_data.get('quest', {})
        character_sheet = input_data.get('character_sheet', {})
        
        # Generate boss encounter
        encounter = generate_boss_encounter(quest, character_sheet)
        
        # Output result
        print(json.dumps(encounter, indent=2))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
