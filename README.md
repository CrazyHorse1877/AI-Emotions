# AI Emotions Simulator

*A living world where emotion shapes behaviour.*

---

## 🧠 Concept

This project is a visual simulation that explores how an artificial intelligence might *appear* to experience emotion. It uses internal states like hunger, energy, fear, and stimulation to determine behavioural responses, creating the illusion of a feeling, reactive agent.

The aim is not to claim that machines can truly feel, but rather to demonstrate how complex internal variables can produce human-like emotional behaviours.

---

## 🐢 The Agent

The player watches a single AI agent that:

- **Feels hunger**: rises over time, relieved by consuming prey.
- **Feels fear**: triggered by predators nearby.
- **Grows tired**: energy drains from action and stress.
- **Gets bored**: stimulation fades from repetition.
- **Can die**: from starvation, exhaustion, or attack.

From this, the agent transitions into emotional states:
- `Hungry`, `Fearful`, `Curious`, `Bored`, `Exhausted`, `Idle`, or `Dead`

Each emotion:
- **Changes the agent's colour** and **movement**
- Is displayed **above the agent** and at the **top of the screen**
- Triggers **subtle feedback** (e.g., thought bubbles, message hints)

---

## 🌍 The World

The world includes:

- **Prey**: passive creatures that reproduce and can be eaten.
- **Predators**: entities that hunt prey and attack the agent.

Entities move, interact, and reproduce inside a closed space. The simulation runs continuously, evolving with or without player input.

---

## 🎨 Interface & Visuals

- **Top-centre emotion display**: large colourised label with a soft backdrop, showing the agent's mood.
- **Progress bars**: smooth, rounded, and colour-coded for health, hunger, energy, and stimulation.
- **Thought bubbles**: occasional glyphs above the agent to imply reflective states like curiosity or fear.
- **Message log**: one-liner emotional summaries displayed at the bottom, enhancing narrative depth.
- **Clean background visuals**: subtle gradients or noise for a more immersive world.
- **Colour-coded emotion system**:
  - Red = fear, yellow = curiosity, grey = death, orange = hunger, etc.

---

## 🚀 Intent

This simulator encourages players to reflect on:

- What creates the appearance of emotion?
- Can reactivity and internal state give rise to believable personalities?
- How do we anthropomorphise systems that merely *appear* to feel?

It blends systems design, emergent behaviour, and emotional storytelling — making the invisible mind of the machine visible.

---

Built with Python and Pygame.


Build Instructions
________________

stuff here