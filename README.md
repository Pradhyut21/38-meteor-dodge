# Meteor Dodge Repair Lab

This project is a space survival obstacle-dodging game using **Pygame**. It introduces students to directional velocity vectors, radial collision math, starfield rendering, particle trails, and dynamic difficulty scaling within an object-oriented codebase.
---

## What's Provided

A working Meteor Dodge game with:

- A responsive player starship with engine trail effects and 4-directional movement (`WASD` / Arrow Keys)
- Procedurally generated starfield background
- Irregular polygonal meteors that rotate and tumble downwards at randomized speeds and angles
- Radius-based circular collision detection against the ship
- Dynamic spawn intervals that decrease as survival time increases
- Launch state, survival timer HUD, and a Game Over overlay with restart functionality

It has **one deliberate bug** and **three optional features** left as tasks to implement. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**
---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python main.py
```

**Controls:** Press SPACE to launch or restart. Use WASD or Arrow Keys to pilot the ship.
| Key | Action |
|-----|--------|
| W/A/S/D or Arrows | Move ship |
| SPACE | Start / Restart |

## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the laser firing / input state bug

Pressing SPACE launches the ship from the title screen, but pressing SPACE during active flight does nothing rather than firing a defensive laser projectile. Ensure the ship fires lasers to destroy incoming meteors while flying.

### Task 2: Implement Meteor Splitting on Impact

Destroying large meteors currently causes them to vanish completely from the screen. Make destroyed large meteors fracture into smaller child fragments that diverge outwards, while small meteors dissolve entirely.
 
### Task 3: Implement Collectible Shield Power-Up Orbs

The ship is instantly destroyed on any meteor contact. Introduce a drifting energy orb that the player can collect to gain a temporary shield barrier capable of absorbing one collision.

### Task 4: Implement Consecutive Survival Multipliers

Score currently increments at a flat rate over time. Introduce an escalating multiplier that boosts score gain for every 10 seconds of continuous survival without taking a hit.

---

## Expected Behavior

- Pressing SPACE begins flight from the title screen.
- Arrow keys or WASD steer the ship smoothly inside the window dimensions.   
- Meteors continuously spawn from the top and fall at varying trajectories and rotation speeds.
- Colliding with any meteor ends the run and displays the final survival time.
- Pressing SPACE on the Game Over screen resets all objects and timers for a new run.

## Folder Structure

```
meteor-dodge/
├── main.py
├── requirements.txt
├── game/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── ship.py
│   ├── meteor.py
│   ├── laser.py
│   └── shield_orb.py
└── README.md
```

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
