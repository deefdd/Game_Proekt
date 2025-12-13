# Game_Proekt

Optimize your PC for a smoother and more stable gaming experience.

## About the Project
Game_Proekt is a Python-based optimization tool created as part of the 30 Day Coding Challenge.  
It helps low- and mid-range computers run games more smoothly by removing unnecessary load and stabilizing system performance.

## Features

### System Optimization
- Detects system hardware and live resource usage
- Adjusts system performance for specific games and hardware setups

### FPS Stabilization
- Closes unnecessary background processes
- Frees RAM dynamically
- Reduces micro-stutters and frame drops

### Deep Cleaning Tools
- Clears temporary files
- Cleans Windows Temp directory
- Cleans Chrome browser cache
- Removes NVIDIA / AMD shader cache
- Cleans Windows Update cache

### Logging System
- Detailed logging for all modules
- Automatic error logging
- Auto-cleanup of old logs

## Technologies Used
- Python 3
- Libraries: `psutil`, `subprocess`, `ctypes`, `GPUtil`

## Installation
```bash
git clone https://github.com/<your-username>/Game_Proekt.git
cd Game_Proekt
pip install -r requirements.txt
