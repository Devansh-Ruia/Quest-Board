# Quest Board ⚔️

Turn your real-life tasks, calendar events, and GitHub commits into an epic RPG adventure. Quest Board is an OpenClaw skill that gamifies productivity with XP, leveling, class assignment, and boss fights—all narrated in D&D dungeon master style.

Built for the SF OpenClaw Hackathon, Feb 15 2026.

## 🎯 Features

- **Daily Quest Generation**: Automatically scans Google Calendar and creates RPG-style quests
- **XP & Leveling System**: Complete tasks to gain XP, level up, and unlock new abilities
- **Class Assignment**: Auto-assign classes (Artificer, Bard, Scribe, Barbarian, Wizard, Ranger) based on your work patterns
- **Boss Fights**: Major deadlines become multi-phase boss encounters with dramatic narration
- **Persistent Character Sheet**: Track stats, achievements, and quest history
- **Discord Integration**: Post quest boards and narrations to your messaging channel
- **Multi-Model AI**: Uses Claude Sonnet for creative narration and Haiku for data processing

## 🚀 Quick Setup

### Prerequisites
- OpenClaw installed and running locally
- Google Calendar API access (for quest generation)
- Discord/Telegram/Slack bot setup (for messaging)
- OpenRouter API key (optional, for multi-model routing)

### Installation

1. **Clone to OpenClaw Skills Directory**
```bash
cp -r quest-board ~/.openclaw/workspace/skills/
```

2. **Configure OpenClaw**
Add to your `~/.openclaw/openclaw.json`:
```json
{
  "skills": ["quest-board"],
  "discord": {
    "token": "YOUR_DISCORD_BOT_TOKEN",
    "channel_id": "YOUR_CHANNEL_ID"
  }
}
```

3. **Set Environment Variables**
```bash
export OPENROUTER_API_KEY="your_openrouter_key_here"
export GOOGLE_CALENDAR_CREDENTIALS="path/to/credentials.json"
```

4. **Restart OpenClaw**
```bash
openclaw restart
```

## 🎮 How to Use

### Basic Commands
- `/quests` — Show today's quest board
- `/complete <quest-name>` — Mark quest complete, get XP + narration
- `/stats` — Display your character sheet
- `/boss` — Trigger boss fight for next big deadline
- `/history` — Show recent quest completions

### Example Workflow

1. **Morning**: OpenClaw automatically posts your daily quest board:
```
⚔️ QUEST BOARD — Feb 15, 2026

🟢 [Easy] The Morning Missive — Reply to 3 emails (25 XP)
🟡 [Medium] The Council of Stakeholders — Team sync meeting (50 XP)  
🔴 [Hard] The Siege of Sprint Planning — Sprint planning (100 XP)
💀 [BOSS] The Dragon of Quarterly Reports — Q1 report due EOD (250 XP)

Your Level: 3 | XP: 150/300 | Class: Artificer
```

2. **Complete Tasks**: After finishing a meeting:
```
/user: /complete "The Council of Stakeholders"

Quest Board: Through skill and determination, you have emerged victorious from this challenge. The townsfolk nod in approval. +50 XP.
```

3. **Level Up**: When you hit XP thresholds:
```
Quest Board: A golden light envelops you as raw power surges through your being. You have ascended to Level 4! New title unlocked: Expert.
```

## 📁 File Structure

```
quest-board/
├── SKILL.md                    # Core skill definition (REQUIRED)
├── scripts/
│   ├── generate_quests.py      # Calendar → quest generation
│   ├── resolve_quest.py        # XP calculation, level-ups
│   └── boss_fight.py           # Multi-phase boss encounters
├── references/
│   ├── rpg_system.md           # XP thresholds, class definitions
│   └── narration_examples.md   # DM style guide
├── data/                       # Persistent state (created at runtime)
│   ├── character_sheet.md      # Your RPG character
│   ├── quest_log.json          # Active/completed quests
│   └── config.json             # Skill settings
└── README.md                   # This file
```

## 🎭 RPG System

### Classes
- **Artificer**: Coding/engineering tasks (INT)
- **Bard**: Meetings, social tasks (CHA)
- **Scribe**: Writing, documentation (WIS)
- **Barbarian**: Exercise, physical tasks (STR)
- **Wizard**: Research, learning (INT)
- **Ranger**: Errands, travel (DEX)

### XP Rewards
| Difficulty | Duration | XP  |
|-----------|----------|-----|
| Easy      | < 30min  | 25  |
| Medium    | 30min-1hr| 50  |
| Hard      | 1hr-2hr  | 100 |
| Boss      | 2hr+     | 250 |

### Boss Fights
Major deadlines become 3-phase encounters:
1. **The Approach** — Setup and initial challenge
2. **The Twist** — Complication mid-battle  
3. **The Resolution** — Final confrontation

## 🛠️ Technical Details

### Dependencies
- Python 3.8+
- OpenClaw core
- Google Calendar API
- OpenRouter API (optional)
- Discord.py or equivalent messaging library

### Script Usage

**Generate Quests from Calendar:**
```bash
python3 scripts/generate_quests.py < calendar_events.json
```

**Resolve Quest Completion:**
```bash
echo '{"quest": {...}, "character_sheet": {...}}' | python3 scripts/resolve_quest.py
```

**Generate Boss Fight:**
```bash
echo '{"quest": {...}, "character_sheet": {...}}' | python3 scripts/boss_fight.py
```

### Model Routing
When OpenRouter is available:
- **Claude Sonnet** (`anthropic/claude-sonnet-4-5`) for creative narration
- **Claude Haiku** (`anthropic/claude-haiku-4-5`) for data processing

## 🎨 Demo Scenario

Pre-populated calendar for testing:
```json
{
  "items": [
    {
      "title": "Team Standup",
      "start": {"dateTime": "2026-02-15T09:00:00Z"},
      "end": {"dateTime": "2026-02-15T09:30:00Z"}
    },
    {
      "title": "Code Review Session", 
      "start": {"dateTime": "2026-02-15T14:00:00Z"},
      "end": {"dateTime": "2026-02-15T15:30:00Z"}
    },
    {
      "title": "Q1 Report - FINAL DEADLINE",
      "start": {"dateTime": "2026-02-15T16:00:00Z"},
      "end": {"dateTime": "2026-02-15T19:00:00Z"}
    }
  ]
}
```

## 🤝 Contributing

Built during a 5-hour hackathon—contributions welcome! Focus areas:
- Additional integrations (GitHub, Jira, Notion)
- More class types and abilities
- Multiplayer/party features
- Mobile app interface
- Advanced achievement system

## 📜 License

MIT License - feel free to use, modify, and distribute.

## 👥 Team

Built by [Your Name] for the SF OpenClaw Hackathon 2026.

---

**Remember**: Every email sent, every meeting attended, every line of code written is part of your epic adventure. Will you answer the call to quest? ⚔️
