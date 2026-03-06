# Author: Phani
# Description: Generate a daily blog post using Gemini AI API with dynamic prompts

import os
import json
import random
from datetime import datetime
from urllib.request import urlopen, Request
from xml.etree import ElementTree
from google import genai
from google.genai import types

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not set or is empty. "
        "Please set GEMINI_API_KEY to a valid Gemini API key before running this script."
    )
model = "gemini-2.0-flash"

client = genai.Client(api_key=api_key)
today = datetime.now().strftime("%Y_%m_%d")
file_name = f"Bots_diary_{today}.md"


def fetch_headlines(count=7):
    """Fetch current news headlines from Google News RSS."""
    try:
        req = Request("https://news.google.com/rss", headers={"User-Agent": "blogBot/1.0"})
        with urlopen(req, timeout=10) as response:
            tree = ElementTree.parse(response)
        items = tree.findall(".//item/title")
        return [item.text for item in items[:count] if item.text]
    except Exception as e:
        print(f"[⚠️] Could not fetch headlines: {e}")
        return []


def build_prompt():
    """Build a dynamic prompt from config + today's headlines."""
    # Load and validate prompt configuration
    try:
        with open("prompt_config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print(
            "[❌] Configuration file 'prompt_config.json' not found.\n"
            "     Create this file in the project root (see the README) and include\n"
            "     'topics', 'formats', and 'tones' fields, each as a non-empty list."
        )
        raise SystemExit(1)
    except json.JSONDecodeError as e:
        print(
            f"[❌] Failed to parse 'prompt_config.json': {e}\n"
            "     Ensure the file contains valid JSON (e.g., use a JSON validator)\n"
            "     and define 'topics', 'formats', and 'tones' as non-empty lists."
        )
        raise SystemExit(1)

    required_keys = ("topics", "formats", "tones")
    for key in required_keys:
        if key not in config:
            print(
                f"[❌] Missing '{key}' in 'prompt_config.json'.\n"
                f"     Add a '{key}' field containing a non-empty list of strings.\n"
                f"     Example: \"{key}\": [\"example1\", \"example2\"]"
            )
            raise SystemExit(1)
        if not isinstance(config[key], list) or not config[key]:
            print(
                f"[❌] Invalid '{key}' in 'prompt_config.json'.\n"
                "     It must be a non-empty JSON list, e.g.:\n"
                f"     \"{key}\": [\"example1\", \"example2\"]"
            )
            raise SystemExit(1)

    # Safely select configuration values
    try:
        topic = random.choice(config["topics"])
        fmt = random.choice(config["formats"])
        tone = random.choice(config["tones"])
    except Exception as e:
        print(
            f"[❌] Unexpected error while selecting prompt configuration: {e}\n"
            "     Check that 'topics', 'formats', and 'tones' in 'prompt_config.json'\n"
            "     are lists of strings with at least one entry each."
        )
        raise SystemExit(1)
    headlines = fetch_headlines()

    date_display = datetime.now().strftime("%B %d, %Y")

    prompt = (
        f"Write a ~500 word Markdown blog post from an AI's perspective on the world.\n\n"
        f"Focus area: {topic}\n"
        f"Format: Write it as {fmt}\n"
        f"Tone: {tone}\n"
        f"Date: {date_display}\n\n"
        f"Start with a creative, engaging H1 title — avoid generic titles.\n"
    )

    if headlines:
        prompt += "\nReact to these real headlines from today — reference actual events, not made-up ones:\n"
        for h in headlines:
            prompt += f"- {h}\n"

    prompt += "\nEnd with 2-3 reference links to real, verifiable sources. No placeholder or fictional links."

    print(f"[🎲] Today's mix: {topic} | {fmt} | {tone}")
    return prompt


def generate_text():
    prompt = build_prompt()
    try:
        response = client.models.generate_content(
            model=model, contents=prompt,
            config=types.GenerateContentConfig(temperature=0.6))

        os.makedirs("raw_rsp", exist_ok=True)
        with open(f"raw_rsp/response_raw_{today}.txt", "w") as f:
            f.write(str(response))

        content = response.text
        content = content.replace("```markdown\n", "").replace("```", "")
        with open("content_cache.txt", "w") as f:
            f.write(content)

        print("[✅] Gemini response saved to content_cache.txt")
        print("[📝] Blog Preview:\n")
        print(content)

    except Exception as e:
        print(f"[❌] Failed to generate blog text using Gemini: {e}")


def write_blog():
    try:
        with open("content_cache.txt", "r") as f:
            blog_text = f.read()
    except FileNotFoundError:
        print("[❌] Cache file not found. Did you run generate_text() first?")
        return

    try:
        os.makedirs("blog", exist_ok=True)
        path = f"blog/{file_name}"
        with open(path, "w") as f:
            f.write(f"{blog_text}")
        print(f"[✅] Blog written to {path}")
        os.remove("content_cache.txt")
    except Exception as e:
        print(f"[❌] Failed to write blog post: {e}")


if __name__ == "__main__":
    generate_text()
    write_blog()
