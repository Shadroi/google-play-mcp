
import os
import sys
import subprocess
import webbrowser
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def install_package(package_name):
    """Install a package using the current python executable."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

import json

def load_messages():
    """Load messages from locales.json file."""
    try:
        # Determine the directory where setup_key.py is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        locales_path = os.path.join(script_dir, "locales.json")
        
        with open(locales_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[bold red]Error loading locales.json: {e}[/bold red]")
        sys.exit(1)

MESSAGES = load_messages()

# Global language setting
LANG = "en"
TEXT = MESSAGES["en"]

def pause(msg=None):
    if msg is None:
        msg = TEXT["press_enter"]
    console.input(f"\n[bold yellow]{msg}[/bold yellow]")

def copy_to_clipboard(text):
    try:
        import pyperclip
    except ImportError:
        console.print(f"{TEXT['pyperclip_install']}")
        if install_package("pyperclip"):
            try:
                import pyperclip
            except ImportError:
                console.print(f"{TEXT['pyperclip_error']}")
                console.print(TEXT['copy_manual'].format(text=text))
                return
        else:
            console.print(f"{TEXT['copy_install_fail']}")
            console.print(TEXT['copy_manual'].format(text=text))
            return

    try:
        pyperclip.copy(text)
        console.print(TEXT['copy_success'].format(text=text))
    except Exception as e:
        console.print(TEXT['copy_fail'].format(e=e))
        console.print(TEXT['copy_manual'].format(text=text))

def perform_link_step(title, instructions, url):
    console.clear()
    console.print(Panel.fit(f"[bold blue]{title}[/bold blue]"))
    console.print(Markdown(instructions))
    
    if Prompt.ask(TEXT["open_browser"], choices=["y", "n", ""], default="y", show_choices=False) != "n":
        webbrowser.open(url)
    
    pause()

def perform_service_account_step():
    title = TEXT["step2_title"]
    instructions = TEXT["step2_desc"]
    
    url = "https://console.cloud.google.com/iam-admin/serviceaccounts"

    console.clear()
    console.print(Panel.fit(f"[bold blue]{title}[/bold blue]"))
    console.print(Markdown(instructions))

    # Define suggested values
    sa_name = "Google Play MCP Helper"
    sa_id = "google-play-mcp"
    sa_desc = "Automated management of Google Play Store releases and products via MCP."

    # Show suggested values - padded for easier selection
    console.print(Panel(f"""
{TEXT['sa_suggested_title']}

{TEXT['sa_name_label']}
[cyan]  {sa_name}  [/cyan]

{TEXT['sa_id_label']}
[cyan]  {sa_id}  [/cyan]

{TEXT['sa_desc_label']}
[cyan]  {sa_desc}  [/cyan]
    """, title=TEXT['sa_details_title'], border_style="green", padding=(1, 2)))

    if Prompt.ask(TEXT["open_browser"], choices=["y", "n", ""], default="y", show_choices=False) != "n":
        webbrowser.open(url)

    # Interactive copy loop
    console.print(TEXT['copy_menu_intro'])
    while True:
        choice = Prompt.ask(
            TEXT['copy_menu_prompt'],
            choices=["1", "2", ""],
            default=""
        )

        if choice == "1":
            # Copy Name and ID
            text = f"Name: {sa_name}\nID: {sa_id}"
            copy_to_clipboard(text)
        elif choice == "2":
            # Copy Description
            copy_to_clipboard(sa_desc)
        else:
            break

def main():
    global LANG, TEXT
    
    # Parse arguments for language
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", default="en", help="Language code (en or ko)")
    args = parser.parse_args()
    
    if args.lang in MESSAGES:
        LANG = args.lang
        TEXT = MESSAGES[LANG]

    # Attempt to install rich if missing, using valid pip call
    try:
        import rich
    except ImportError:
        install_package("rich")
        # Global import after install
        import rich
        pass
    
    # Step 1: Enable API
    perform_link_step(
        TEXT["step1_title"],
        TEXT["step1_desc"],
        "https://console.cloud.google.com/apis/library/androidpublisher.googleapis.com"
    )

    # Step 2: Service Account & Key (Custom step with copy functionality)
    perform_service_account_step()

    # Step 3: Link to Play Console
    perform_link_step(
        TEXT["step3_title"],
        TEXT["step3_desc"],
        "https://play.google.com/console/users-and-permissions"
    )

    # Final Configuration
    console.clear()
    console.print(Panel.fit(TEXT["final_config_title"]))
    
    while True:
        key_path = Prompt.ask(TEXT["key_path_prompt"]).strip()
        # Handle quotes from drag-and-drop
        if (key_path.startswith("'") and key_path.endswith("'")) or (key_path.startswith('"') and key_path.endswith('"')):
            key_path = key_path[1:-1]
        
        # Expand ~ to user home
        key_path = os.path.expanduser(key_path)

        if os.path.exists(key_path):
            break
        console.print(TEXT['key_file_error'].format(key_path=key_path))

    package_name = Prompt.ask(TEXT["package_name_prompt"]).strip()

    with open(".env", "w") as f:
        f.write(f"GOOGLE_PLAY_KEY_FILE={os.path.abspath(key_path)}\n")
        f.write(f"GOOGLE_PLAY_PACKAGE_NAME={package_name}\n")
    
    console.print(TEXT['success_msg'].format(key_path=key_path, package_name=package_name))

if __name__ == "__main__":
    # Ensure rich is installed before anything else requiring it
    try:
        import rich
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
        import rich
    
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.markdown import Markdown
    
    # Re-declare console to be sure
    console = Console()
        
    main()
