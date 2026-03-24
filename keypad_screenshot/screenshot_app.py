#!/usr/bin/env python3
"""
Keypad Screenshot App
Takes a screenshot whenever an arrow key is pressed.
Useful for capturing long documents page by page.
"""

import os
import time
import threading
from datetime import datetime
from pathlib import Path

from pynput import keyboard
import mss
import mss.tools


# --- Config ---
SCREENSHOT_DIR = Path.home() / "screenshots"
DELAY = 0.4       # seconds to wait after keypress (let page finish scrolling)
DEBOUNCE = 0.5    # minimum seconds between captures (prevents hold-key spam)

ARROW_KEYS = {
    keyboard.Key.up,
    keyboard.Key.down,
    keyboard.Key.left,
    keyboard.Key.right,
}

# --- State ---
last_screenshot_time = 0
session_count = 0
session_dir = None
lock = threading.Lock()


def get_session_dir() -> Path:
    global session_dir
    if session_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = SCREENSHOT_DIR / f"session_{timestamp}"
        session_dir.mkdir(parents=True, exist_ok=True)
        print(f"  Saving to: {session_dir}\n")
    return session_dir


def take_screenshot():
    global last_screenshot_time, session_count

    with lock:
        now = time.time()
        if now - last_screenshot_time < DEBOUNCE:
            return
        last_screenshot_time = now

    # Wait for scroll to settle
    time.sleep(DELAY)

    with lock:
        session_count += 1
        count = session_count

    filename = get_session_dir() / f"screenshot_{count:04d}.png"

    with mss.mss() as sct:
        sct.shot(output=str(filename))

    print(f"  [{count:04d}] {filename.name}")


def on_press(key):
    if key in ARROW_KEYS:
        threading.Thread(target=take_screenshot, daemon=True).start()


def main():
    print("=" * 40)
    print("  Keypad Screenshot App")
    print("=" * 40)
    print("  Arrow keys  → capture screenshot")
    print("  Ctrl+C      → stop\n")

    get_session_dir()  # create session folder immediately

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            pass

    print(f"\n  Done! Captured {session_count} screenshots.")
    if session_dir:
        print(f"  Folder: {session_dir}")


if __name__ == "__main__":
    main()
