# utils/logger.py
import os
from datetime import datetime

def log(message):
    """Prints a timestamped log message."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def display_scoreboard(scoreboard_data):
    """Clears the console and displays the live scoreboard."""
    os.system('cls' if os.name == 'nt' else 'clear')
    log("Refreshing live scoreboard...")
    
    header = "🏆 LIVE SCOREBOARD"
    print("\n" + header)
    print("=" * (len(header) + 20))

    if not scoreboard_data:
        print("No results yet...")
    else:
        for model_name, tasks in scoreboard_data.items():
            print(f"📊 {model_name}:")
            if not tasks:
                print("  (No tasks completed yet)")
            else:
                for task_display, score in tasks.items():
                    print(f"  • {task_display:<30}: {score}")
            print("-" * (len(header) + 20))
    
    print("=" * (len(header) + 20) + "\n")