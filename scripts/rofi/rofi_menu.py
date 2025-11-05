#!/usr/bin/env python3
"""
Rofi Menu Wrapper - Load menu options from YAML file and display via Rofi
"""

import os
import sys
import yaml
import subprocess
import argparse
from pathlib import Path


def parse_args():
    """Parse command line arguments."""
    # Get the config directory from user's home
    config_dir = os.path.expanduser("~/.config/rofi_menu")
    default_config = os.path.join(config_dir, "menu.yaml")

    parser = argparse.ArgumentParser(description="Rofi menu wrapper that reads from YAML file")
    parser.add_argument(
        "-c", "--config", type=str, default=default_config, help="Path to YAML configuration file"
    )
    parser.add_argument(
        "-p", "--prompt", type=str, default="Select an option", help="Custom prompt for Rofi"
    )
    return parser.parse_args()


def load_menu_config(config_file):
    """Load menu configuration from YAML file."""
    try:
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
            return config if config else {}
    except FileNotFoundError:
        # Return empty config if file doesn't exist
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)


def get_subdirectories(directory):
    """Get all subdirectories in the given directory."""
    try:
        path = Path(directory)
        if not path.exists():
            return []
        return [d.name for d in path.iterdir() if d.is_dir()]
    except Exception as e:
        print(f"Error reading directory {directory}: {e}")
        return []


def load_dynamic_menu(directory):
    """Check for and execute dynamic menu generator, return config from stdout."""
    generator_path = os.path.join(directory, "generate_menu")

    if not os.path.exists(generator_path):
        return None

    if not os.access(generator_path, os.X_OK):
        print(f"Warning: {generator_path} exists but is not executable")
        return None

    try:
        result = subprocess.run([generator_path], cwd=directory, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            print(f"Warning: {generator_path} exited with code {result.returncode}")
            if result.stderr:
                print(f"Error output: {result.stderr}")
            return None

        # Parse YAML from stdout
        config = yaml.safe_load(result.stdout)
        return config if config else {}

    except subprocess.TimeoutExpired:
        print(f"Warning: {generator_path} timed out after 30 seconds")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML from {generator_path}: {e}")
        return None
    except Exception as e:
        print(f"Error executing {generator_path}: {e}")
        return None


def run_rofi(menu_items, prompt, show_back=False):
    """Run rofi with the provided menu items and return the selected option."""
    # Create a list of menu item labels
    labels = []
    if show_back:
        labels.append("← Back")
    labels.extend([item["label"] for item in menu_items])

    # Join labels with newlines for rofi input
    menu_str = "\n".join(labels)

    # Run rofi as a subprocess
    try:
        process = subprocess.Popen(
            ["rofi", "-dmenu", "-p", prompt, "-i"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        stdout, stderr = process.communicate(input=menu_str)

        # Return the selected option (strip whitespace)
        selected = stdout.strip()
        return selected if selected else None

    except subprocess.SubprocessError as e:
        print(f"Error running rofi: {e}")
        sys.exit(1)


def get_clipboard_content():
    """Get clipboard content using xclip."""
    try:
        result = subprocess.run(
            ["xclip", "-selection", "clipboard", "-o"], capture_output=True, text=True, check=True
        )
        return result.stdout
    except FileNotFoundError:
        print("Error: xclip is not installed. Install it with: sudo apt install xclip")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error getting clipboard content: {e}")
        return None


def load_history():
    """Load history from ~/.cache/rofi_menu/history.yml."""
    history_file = os.path.expanduser("~/.cache/rofi_menu/history.yml")
    try:
        with open(history_file, "r") as file:
            history = yaml.safe_load(file)
            return history if history else []
    except FileNotFoundError:
        return []
    except yaml.YAMLError as e:
        print(f"Error parsing history file: {e}")
        return []


def save_history(history):
    """Save history to ~/.cache/rofi_menu/history.yml."""
    history_file = os.path.expanduser("~/.cache/rofi_menu/history.yml")
    history_dir = os.path.dirname(history_file)

    # Ensure cache directory exists
    os.makedirs(history_dir, exist_ok=True)

    try:
        with open(history_file, "w") as file:
            yaml.dump(history, file, default_flow_style=False)
    except Exception as e:
        print(f"Error saving history: {e}")


def update_history(item):
    """Update history with the selected item, keeping only last 20 items."""
    # Load current history
    history = load_history()

    # Remove item if it already exists in history
    history = [
        h for h in history if h.get("label") != item.get("label") or h.get("text") != item.get("text")
    ]

    # Add item to the beginning
    history.insert(0, item)

    # Keep only last 20 items
    history = history[:20]

    # Save updated history
    save_history(history)


def insert_text(text):
    """Insert text into the currently focused X11 window using xdotool."""
    try:
        subprocess.run(["xdotool", "type", "--", text], check=True)
    except FileNotFoundError:
        print("Error: xdotool is not installed. Install it with: sudo apt install xdotool")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error inserting text with xdotool: {e}")


def show_history_menu(prompt):
    """Display a history submenu with all history items."""
    history = load_history()

    if not history:
        print("No history items found")
        return False

    # Create menu items from history
    history_menu_items = []
    for item in history:
        history_menu_items.append({"label": item["label"], "type": "history", "original_item": item})

    # Run rofi and get selection
    selected = run_rofi(history_menu_items, prompt, show_back=True)

    # Handle selection
    if not selected:
        return False

    if selected == "← Back":
        return True  # Signal to go back

    # Find the selected item
    for item in history_menu_items:
        if item["label"] == selected:
            original_item = item["original_item"]
            # Update history before inserting text
            update_history(original_item)
            # Insert text into focused window
            insert_text(original_item["text"])
            return False

    return False


def show_menu(config_dir, menu_path, prompt, is_submenu=False):
    """Display a menu and handle selection, recursively handling submenus."""
    # Get current directory
    current_dir = os.path.join(config_dir, menu_path) if menu_path else config_dir

    # Try to load dynamic menu first
    config = load_dynamic_menu(current_dir)

    # If no dynamic menu, fall back to static menu.yaml
    if config is None:
        full_menu_path = os.path.join(current_dir, "menu.yaml")
        config = load_menu_config(full_menu_path)

    # Config should be a flat array of menu items
    menu_items = config if isinstance(config, list) else []

    # Get subdirectories to create submenu entries
    subdirs = get_subdirectories(current_dir)

    # Create submenu items from subdirectories
    submenu_items = [
        {"label": f"📁 {subdir}", "type": "submenu", "path": subdir} for subdir in sorted(subdirs)
    ]

    # Add clipboard option and history items only at the top level
    clipboard_items = []
    history_items = []
    last_used_item = []

    if not menu_path:  # Only show at top level
        clipboard_items = [{"label": "📋 Type clipboard content", "type": "clipboard"}]

        # Load history and create history items
        history = load_history()
        if history:
            # Add the last used item first
            last_used_item = [
                {"label": f"🕐 {history[0]['label']}", "type": "history", "original_item": history[0]}
            ]

            # Add history submenu if there are more than 1 items
            if len(history) > 1:
                history_items = [{"label": "📜 History", "type": "history_submenu"}]

    # Combine clipboard items, last used item, history submenu, submenu items and regular menu items
    all_items = clipboard_items + last_used_item + history_items + submenu_items + menu_items

    if not all_items:
        print(f"No menu items or subdirectories found in {current_dir}")
        return False

    # Run rofi and get selection
    selected = run_rofi(all_items, prompt, show_back=is_submenu)

    # Handle selection
    if not selected:
        return False

    if selected == "← Back":
        return True  # Signal to go back

    # Find the selected item
    for item in all_items:
        if item["label"] == selected:
            if item.get("type") == "clipboard":
                # Get clipboard content and type it
                clipboard_content = get_clipboard_content()
                if clipboard_content is not None:
                    insert_text(clipboard_content)
                return False
            elif item.get("type") == "history":
                # Handle history item selection
                original_item = item["original_item"]
                # Update history before inserting text
                update_history(original_item)
                # Insert text into focused window
                insert_text(original_item["text"])
                return False
            elif item.get("type") == "history_submenu":
                # Enter history submenu
                history_prompt = f"{prompt} > History"

                # Show history submenu in a loop to handle back navigation
                while True:
                    should_continue = show_history_menu(history_prompt)
                    if not should_continue:
                        # User cancelled or executed a command, exit completely
                        return False
                    else:
                        # User pressed back, return to current menu
                        break

                # After returning from history submenu, show current menu again
                return show_menu(config_dir, menu_path, prompt, is_submenu)
            elif item.get("type") == "submenu":
                # Enter submenu
                subdir_name = item["path"]
                new_menu_path = os.path.join(menu_path, subdir_name) if menu_path else subdir_name
                submenu_prompt = f"{prompt} > {subdir_name}"

                # Show submenu in a loop to handle back navigation
                while True:
                    should_continue = show_menu(config_dir, new_menu_path, submenu_prompt, is_submenu=True)
                    if not should_continue:
                        # User cancelled or executed a command, exit completely
                        return False
                    else:
                        # User pressed back, return to current menu
                        break

                # After returning from submenu, show current menu again
                return show_menu(config_dir, menu_path, prompt, is_submenu)
            else:
                # Regular menu item - update history before inserting text
                update_history(item)
                # Insert text into focused window
                insert_text(item["text"])
                return False

    return False


def main():
    """Main function to run the rofi menu wrapper."""
    args = parse_args()

    # Get config directory (extract directory from config path if custom path provided)
    if args.config != os.path.join(os.path.expanduser("~/.config/rofi_menu"), "menu.yaml"):
        # Custom config path provided, use its directory
        config_dir = os.path.dirname(args.config)
    else:
        # Use default config directory
        config_dir = os.path.expanduser("~/.config/rofi_menu")

    # Ensure config directory exists
    os.makedirs(config_dir, exist_ok=True)

    # Start with the root menu
    show_menu(config_dir, "", args.prompt, is_submenu=False)


if __name__ == "__main__":
    main()
