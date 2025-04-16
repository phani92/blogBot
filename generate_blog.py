# Author: Phani
# Description: Generate a blog post using Gemini AI API

import os
from datetime import datetime
from google import genai

api_key = os.getenv("GEMINI_API_KEY") # Change your API key here
model = "gemini-2.0-flash" # Change your model here

client = genai.Client(api_key=api_key)
today = datetime.now().strftime("%Y_%m_%d")
title = f"NVIDIA Stock Performance: {today}"
file_name = f"stock_NVIDIA_{today}.md"

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
            f.write(f"---\ntitle: \"{title}\"\ndate: {today}\n---\n\n{blog_text}")
        print(f"[✅] Blog written to {path}")
        os.remove("content_cache.txt")
    except Exception as e:
        print(f"[❌] Failed to write blog post: {e}")

def generate_text():
    prompt = f"Generate Markdown blog post (~300-500 words) titled '{title}' about Nvidia stock performance {today}, with reference links."
    try:
        response = client.models.generate_content(model=model, contents=prompt)

        # Save raw Gemini response to a file for debugging
        os.makedirs("raw_rsp", exist_ok=True)
        with open(f"raw_rsp/response_raw_{today}.txt", "w") as f:
            f.write(str(response))

        # Save only the blog content as plain text
        content = response.text
        with open("content_cache.txt", "w") as f:
            f.write(content)

        print("[✅] Gemini response saved to content_cache.txt")
        print("[📝] Blog Preview:\n")
        print(content)

    except Exception as e:
        print(f"[❌] Failed to generate blog text using Gemini: {e}")

if __name__ == "__main__":
    generate_text()
    write_blog()
