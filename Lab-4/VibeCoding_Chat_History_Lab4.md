# Lab 4: VibeCoding — Meteor Dodge Report & Chat History

- **Course / Assignment:** Lab 4: VibeCoding
- **Student GitHub:** [Pradhyut21](https://github.com/Pradhyut21)
- **Forked Repository:** `https://github.com/Pradhyut21/38-meteor-dodge`
- **Tool Used:** Google Antigravity (Gemini 3.8 Flash Pair Programmer)
- **Date & Time:** October 7, 2026, 06:00 PM – 07:00 PM IST

---

## 1. Summary of Deliverables

| Deliverable | Location / Filename | Description |
| :--- | :--- | :--- |
| **Video: Before** | `Lab-4/before.mp4` / `before.mp4` | 10.0 seconds (300 frames, 30 FPS) showing gameplay before fixes, highlighting the bug where pressing SPACE during flight fails to fire defensive lasers. |
| **Video: After** | `Lab-4/after.mp4` / `after.mp4` | 10.0 seconds (300 frames, 30 FPS) showing gameplay with all 4 tasks implemented: laser firing, meteor splitting, shield pickup/absorption, and dynamic multiplier scaling. |
| **Updated Code** | `game/` package | All bug fixes and features implemented and tested. |
| **Git Commits** | Repository Commit History | Clean, individual commits corresponding to each task. |

---

## 2. Tasks & Bug Resolution Walkthrough

### Task 1: Fix the laser firing / input state bug
- **Identified Bug:** In `game/game_engine.py`, the `handle_events` method checked `if event.key == pygame.K_SPACE: if self.game_over: self.reset() else: self.started = True`. When flight was already active (`self.started == True`), pressing space did nothing instead of firing a defensive laser projectile.
- **Solution:** 
  1. Created `game/laser.py` with `Laser` class containing position, vertical velocity (`vy = -10`), collision check (`collides`), and glowing beam rendering.
  2. Added `fire()` method in `game/ship.py`.
  3. Updated `game/game_engine.py` to spawn laser projectiles on spacebar input during active flight, update projectile motion, and detect collisions with meteors.
- **Git Commit:** `Task 1: Fix laser firing and spacebar input state bug` (`e71960f`)

### Task 2: Implement Meteor Splitting on Impact
- **Requirement:** Destroying large meteors causes them to fracture into smaller child fragments diverging outwards, while small meteors dissolve completely.
- **Solution:**
  1. Updated `game/meteor.py` with `split()` method.
  2. Meteors with `radius > 16` fracture into two smaller fragments (`radius * 0.58`) with diverging horizontal velocities (`vx ± random.uniform(1.8, 3.2)`).
  3. Small meteors (`radius <= 16`) return empty lists and dissolve.
  4. Updated laser collision logic in `game/game_engine.py` to remove parent meteor and append child fragments.
- **Git Commit:** `Task 2: Implement meteor splitting on laser impact` (`fdcd4bb`)

### Task 3: Implement Collectible Shield Power-Up Orbs
- **Requirement:** Ship is destroyed on any contact. Introduce drifting energy orbs that the player can collect to gain a temporary shield barrier absorbing one collision.
- **Solution:**
  1. Created `game/shield_orb.py` with drifting sinusoidal wobble motion, pulsing outer ring, and collision detection.
  2. Added `has_shield` attribute and animated translucent glowing shield barrier in `game/ship.py`.
  3. In `game/game_engine.py`, periodically spawn shield orbs. When collected by the ship, activate `ship.has_shield`.
  4. When a meteor hits the ship while shield is active, absorb the hit, remove the meteor, and consume the shield without triggering game over.
- **Git Commit:** `Task 3: Implement collectible shield power-up orbs` (`fbf6027`)

### Task 4: Implement Consecutive Survival Multipliers
- **Requirement:** Introduce escalating multiplier boosting score gain for every 10 seconds of continuous survival without taking a hit.
- **Solution:**
  1. In `game/game_engine.py`, tracked `survival_frames` and continuous `streak_frames`.
  2. Multiplier calculated as `1 + (streak_frames // 600)` (every 600 frames at 60 FPS is 10 seconds).
  3. Score increments each frame by the active multiplier (`self.score += self.multiplier`).
  4. If a meteor is absorbed by the shield, streak resets to 0 and multiplier resets to 1x.
  5. Updated HUD in `draw()` to display elapsed time, total score, and active multiplier (`x1`, `x2`, etc.) in gold/accent colors.
- **Git Commit:** `Task 4: Implement consecutive survival score multipliers` (`04f4283`)

---

## 3. Commit History

```text
e34a4cc Docs: Update folder structure in README.md
04f4283 Task 4: Implement consecutive survival score multipliers
fbf6027 Task 3: Implement collectible shield power-up orbs
fdcd4bb Task 2: Implement meteor splitting on laser impact
e71960f Task 1: Fix laser firing and spacebar input state bug
b168286 Update README.md
49607ea Add files via upload
```

---

## 4. Video Recording Verification

Both videos were generated using headless Pygame frame capture with OpenCV VideoWriter (`mp4v` codec) at 30 FPS:
- `before.mp4`: 300 frames, 10.0s duration, 700x520 resolution. Demonstrates ship flight, falling meteors, and spacebar press failing to fire lasers.
- `after.mp4`: 300 frames, 10.0s duration, 700x520 resolution. Demonstrates laser fire, meteor splitting into fragments, shield orb collection, shield absorption, and score multiplier HUD scaling.
