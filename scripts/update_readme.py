import os
import re
import random
import requests
from datetime import datetime, timezone

# Fallback developer quotes in case API is down or rate-limited
FALLBACK_QUOTES = [
    {"quote": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
    {"quote": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "author": "Martin Fowler"},
    {"quote": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House"},
    {"quote": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
    {"quote": "Before software can be reusable it first has to be usable.", "author": "Ralph Johnson"},
    {"quote": "Make it work, make it right, make it fast.", "author": "Kent Beck"},
    {"quote": "Programming is not about what you know; it's about what you can figure out.", "author": "Chris Pine"},
    {"quote": "Talk is cheap. Show me the code.", "author": "Linus Torvalds"},
    {"quote": "Simplicity is the soul of efficiency.", "author": "Austin Freeman"},
    {"quote": "The best error message is the one that never shows up.", "author": "Thomas Fuchs"},
    {"quote": "Walking on water and developing software from a specification are easy if both are frozen.", "author": "Edward V. Berard"}
]

def fetch_programming_joke():
    """Tries to fetch a random programming joke from JokeAPI."""
    try:
        url = "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if not data.get("error", False):
                if data.get("type") == "single":
                    joke_text = data.get("joke")
                    return f'> "{joke_text}"\n>\n> — *Programming Joke*'
                elif data.get("type") == "twopart":
                    setup = data.get("setup")
                    delivery = data.get("delivery")
                    return f'> **Setup:** {setup}\n>\n> **Punchline:** *{delivery}*'
    except Exception as e:
        print(f"Error fetching joke: {e}")
    return None

def fetch_tech_quote():
    """Tries to fetch a random tech quote from ZenQuotes."""
    try:
        url = "https://zenquotes.io/api/random"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                quote_text = data[0].get("q")
                quote_author = data[0].get("a")
                return f'> "{quote_text}"\n>\n> — **{quote_author}**'
    except Exception as e:
        print(f"Error fetching quote: {e}")
    return None

def get_content():
    """Decides whether to fetch a joke or a quote, with fallback mechanism."""
    # 50% chance of a joke, 50% chance of a quote
    if random.choice([True, False]):
        content = fetch_programming_joke()
        if not content:
            content = fetch_tech_quote()
    else:
        content = fetch_tech_quote()
        if not content:
            content = fetch_programming_joke()
            
    # Fallback if both APIs failed
    if not content:
        print("APIs failed. Selecting a fallback quote...")
        fallback = random.choice(FALLBACK_QUOTES)
        content = f'> "{fallback["quote"]}"\n>\n> — **{fallback["author"]}**'
        
    return content

def update_readme():
    # Define file paths
    # We want to support running both locally and inside GitHub Actions (workspace root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(os.path.dirname(script_dir), "README.md")
    
    if not os.path.exists(readme_path):
        print(f"README.md not found at {readme_path}!")
        return

    # Read existing README
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Get new dynamic content
    new_quote = get_content()
    
    formatted_block = f"<!-- START_DAILY_QUOTE -->\n{new_quote}\n<!-- END_DAILY_QUOTE -->"

    # Regex search and replace
    pattern = r"<!-- START_DAILY_QUOTE -->.*?<!-- END_DAILY_QUOTE -->"
    updated_content, count = re.subn(pattern, formatted_block, readme_content, flags=re.DOTALL)

    if count > 0:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("README.md updated successfully!")
    else:
        print("Could not find the <!-- START_DAILY_QUOTE --> tags in README.md!")

if __name__ == "__main__":
    update_readme()
