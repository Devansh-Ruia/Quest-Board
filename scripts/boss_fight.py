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
            f"The air grows cold as you approach the {boss_name.lower()}. Its scales shimmer with the urgency of impending due dates. You grip your weapon tightly—this will be a battle against time itself.",
            f"The mountain lair of the {boss_name.lower()} looms before you. Smoke billows from its nostrils, each puff representing another hour slipping away. The final deadline approaches.",
            f"You stand at the gates of the {boss_name.lower()}'s domain. The ground trembles with each step of the great beast. Your quest: {quest_name} begins now."
        ],
        'code_lich': [
            f"The crypt of the {boss_name.lower()} beckons, filled with the skeletons of forgotten functions and variables. Your torchlight reveals ancient code that should not be. The quest {quest_name} demands your expertise.",
            f"Deep in the digital underworld, the {boss_name.lower()} awaits. Lines of cursed code twist like writhing serpents. Only a brave programmer can cleanse this corruption.",
            f"The {boss_name.lower()} rises from the repository of the damned. Its eyes glow with the light of a thousand syntax errors. Your quest {quest_name} has led you to this moment."
        ],
        'presentation_phoenix': [
            f"The boardroom transforms into an arena where the {boss_name.lower()} awaits. Stakeholders sit like ancient judges, their gazes piercing. Your quest {quest_name} requires more than slides—it demands courage.",
            f"The {boss_name.lower()} spreads its wings of expectation and judgment. PowerPoint slides become your shield, your words your sword. The quest {quest_name} begins.",
            f"In the hallowed halls of commerce, the {boss_name.lower()} circles overhead. Each beat of its wings represents another question from the executive team. Face your destiny in {quest_name}."
        ]
    }
    
    # Get appropriate template or use generic
    templates = phase_1_templates.get(boss_type, [
        f"The {boss_name.lower()} stands before you, a formidable obstacle to your quest {quest_name}. The air crackles with tension as you prepare for the confrontation ahead.",
        f"Your journey has led you to the lair of the {boss_name.lower()}. The quest {quest_name} will test your limits and push you beyond what you thought possible.",
        f"The path to completing {quest_name} is blocked by the mighty {boss_name.lower()}. Steel your resolve—this battle will be legendary."
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
            f"The {boss_name.lower()} roars and the deadline suddenly moves up! Unexpected complications arise as the beast unleashes its time-warping breath. You must adapt quickly or be consumed by the temporal storm.",
            f"Mid-battle, the {boss_name.lower()} reveals a hidden phase—additional requirements materialize out of thin air. The scope creeps like shadows at dusk, threatening to overwhelm your progress.",
            f"The {boss_name.lower()} summons its minions: meetings, interruptions, and urgent emails. You must fight through these distractions to maintain focus on {quest_name}."
        ],
        'code_lich': [
            f"The {boss_name.lower()} laughs as the codebase suddenly shifts! Dependencies break, APIs change, and the ground beneath your feet becomes unstable. Your debugging skills are put to the ultimate test.",
            f"Unexpectedly, the {boss_name.lower()} reveals that the real problem lies deeper than you thought. The surface issues were merely symptoms of a much darker architectural corruption.",
            f"The {boss_name.lower()} casts a spell of confusion! Your IDE crashes, documentation becomes contradictory, and your usual tools fail you. You must rely on pure programming instinct."
        ],
        'presentation_phoenix': [
            f"The {boss_name.lower()} rises from the ashes of your first points with challenging questions! Stakeholders reveal hidden concerns and objections you never anticipated. Think fast!",
            f"Mid-presentation, the {boss_name.lower()} transforms the meeting dynamics. Key decision-makers change their minds, new requirements emerge, and your carefully crafted narrative must adapt.",
            f"The {boss_name.lower()} tests your resolve with technical difficulties! The projector fails, slides won't advance, and your demo environment crashes. The show must go on!"
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
            f"The final confrontation! The {boss_display_name.lower()} unleashes its ultimate attack—the last-minute rush. With adrenaline surging, you channel all your skill and experience into this final push. Victory is within reach!",
            f"This is it—the moment of truth! The {boss_display_name.lower()} stands cornered, its power waning. One final effort will determine the fate of {quest_name}. Give it everything you've got!",
            f"The {boss_display_name.lower()} roars its defiance, but you can see the fatigue in its movements. The quest {quest_name} reaches its climax. This final battle will decide everything!"
        ],
        'code_lich': [
            f"The {boss_display_name.lower()} faces its final compilation! One last push of debugging, refactoring, and testing will determine whether the codebase is saved or doomed to eternal legacy status.",
            f"The {boss_display_name.lower()} gathers its remaining dark energy for a final assault. Your fingers fly across the keyboard as you race against the forces of technical debt. The fate of {quest_name} hangs in the balance!",
            f"The final merge conflict! The {boss_display_name.lower()} makes its last stand amidst conflicting branches and merge conflicts. Your git-fu will be tested as never before in {quest_name}."
        ],
        'presentation_phoenix': [
            f"The {boss_display_name.lower()} prepares for its final rebirth! Your closing arguments, summary slides, and call to action will determine whether you emerge victorious or face the ashes of defeat.",
            f"The Q&A from hell! The {boss_display_name.lower()} unleashes its most challenging questions yet. Your knowledge, confidence, and communication skills will be put to the ultimate test in {quest_name}.",
            f"The final decision point! The {boss_display_name.lower()} awaits the judgment of the stakeholders. Your performance in {quest_name} reaches its dramatic conclusion."
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
        "victory_message": f"BOSS DEFEATED! The {boss_display_name.lower()} has fallen! +{xp_reward} XP and eternal glory!"
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
