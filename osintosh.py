import os
import json
import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.box import ROUNDED

console = Console()

REPO_OWNER = 'ogtirth'
REPO_NAME = 'osintosh'
BRANCH = 'main'

def clear_screen():
    console.clear()

def load_data():
    with open('osint_data.json', 'r') as file:
        return json.load(file)

def display_table(items, title):
    table = Table(title=title, style="bold green", box=ROUNDED, border_style="bright_green")
    table.add_column("No", justify="center", style="bold cyan", header_style="bold yellow")
    table.add_column("Name", justify="left", style="bold red", header_style="bold yellow")
    table.add_column("Type", justify="left", style="bold green", header_style="bold yellow")

    folder_icon = "📁"
    url_icon = "🔗"

    for i, item in enumerate(items, 1):
        icon = folder_icon if item['type'] == 'folder' else url_icon
        table.add_row(str(i), item['name'], f"{icon} {item['type']}")

    console.print(table)

def display_info_table(description, credits, update_status):
    info_table = Table(style="bold yellow", box=ROUNDED, border_style="bright_blue")
    info_table.add_column("Description", justify="left")
    info_table.add_column("Credits", justify="left")
    info_table.add_column("Update Status", justify="left")

    info_table.add_row(description, credits, update_status)
    console.print(info_table)

def check_for_updates():
    try:
        url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits/{BRANCH}'
        response = requests.get(url)
        response.raise_for_status()
        latest_commit = response.json()['sha']

        if os.path.exists('last_checked_commit.txt'):
            with open('last_checked_commit.txt', 'r') as f:
                last_checked_commit = f.read().strip()
        else:
            last_checked_commit = ''

        if latest_commit != last_checked_commit:
            return "[bold yellow]Hey, A new update is available! Please update the code.[/bold yellow]"
        else:
            return "[bold green]You are using the latest version of the tool! :)[/bold green]"

    except requests.exceptions.RequestException:
        return "[bold red]Failed to check for updates. Please check your internet connection.[/bold red]"

def navigate(data):
    while True:
        clear_screen()

        description = (
            "[bold green]OSINTOSH is an OSINT framework for exploring various categories and gathering information.[/bold green]\n"
            "[bold green]It utilizes the OSINT data provided by @lockfale's framework to help you navigate and explore resources.[/bold green]"
        )
        credits = (
            "Developed by [bold green]Tirth Parmar.[/bold green]\n"
            "Special thanks to [bold green]@lockfale[/bold green] for creating the OSINT framework and providing the data.\n"
            "Libraries used: [bold green]rich, requests.[/bold green]"
        )
        update_status = check_for_updates()

        display_info_table(description, credits, update_status)

        console.print(f"[bold cyan]{data['name']}[/bold cyan]", style="bold blue")

        if 'children' in data:
            display_table(data['children'], f"Contents of {data['name']}")

            choices = [str(i) for i in range(1, len(data['children']) + 1)]
            choices.append("b")
            choice = Prompt.ask(
                "\n[bold yellow]Enter the number of your choice or 'b' to go back[/bold yellow]",
                choices=choices
            )

            if choice == "b":
                return
            else:
                selected_item = data['children'][int(choice) - 1]
                if selected_item['type'] == 'folder':
                    navigate(selected_item)
                elif selected_item['type'] == 'url':
                    console.print(Panel(
                        f"[bold green]URL Name:[/bold green] {selected_item['name']}\n[bold green]URL:[/bold green] {selected_item['url']}",
                        style="bold blue",
                        border_style="bright_green"
                    ))
                    input("\nPress Enter to go back...")
        else:
            console.print(f"[bold red]No further items in {data['name']}[/bold red]")
            input("\nPress Enter to go back...")
            return

def start_tool():
    clear_screen()

    data = load_data()

    navigate(data)

if __name__ == "__main__":
    start_tool()
