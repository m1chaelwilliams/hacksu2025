# Journey of the Ninja King

### Introduction

Journey of the Ninja king is a SU 2025 Hackathon game submission where the player, controlled by a reinforcement learning model,
fights in a top-down arena game agains hordes of various enemies.

<image src="images/ReadMeImage.png" width=900>

### Technical Details

The Game is written in ```Python``` with ```PyGame``` for windowing, graphics, and audio.

### AI

The AI player is power by [stable_baselines3](https://stable-baselines3.readthedocs.io/en/master/) and [Gymnasium](https://gymnasium.farama.org/)  libraries, which were used for the Reinforcement Learning.

TEAMWORK

## Install

### Mac/Linux

```bash
git clone https://github.com/m1chaelwilliams/hacksu2025.git --branch ai
cd hacksu2025
python3 venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 -m main
```

### Windows

```bash
git clone https://github.com/m1chaelwilliams/hacksu2025.git --branch ai
cd hacksu2025
python venv .venv
.venv/Scripts/Activate.ps1
pip install -r requirements.txt
python -m main
```
