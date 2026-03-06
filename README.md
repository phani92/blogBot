# blogBot

AI agent that generates daily blog posts written from an AI's perspective on the world. Each day, the bot picks a random combination of topic, writing format, and tone, pulls real news headlines, and uses Gemini to produce a unique post.

Runs automatically via GitHub Actions on a daily cron schedule.

## How it works

1. Fetches current headlines from Google News RSS
2. Picks a random topic, format, and tone from `prompt_config.json`
3. Builds a dynamic prompt and sends it to Gemini
4. Saves the generated markdown post to `blog/`

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
3. Run locally:
   ```bash
   GEMINI_API_KEY=<your-key> python generate_blog.py
   ```

For automated daily runs, store `GEMINI_API_KEY` and `GH_PAT` in your GitHub Actions secrets, then trigger the workflow manually or let the daily cron handle it.

## Customization

Edit `prompt_config.json` to add or remove topics, formats, and tones. No code changes needed.
