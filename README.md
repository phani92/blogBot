# blogBot
* Ai Agent to generate blogs
* This project uses Github actions to automatically run the program and generate a blog post.

## How to use
* Install the dependencies using `pip install -r requirements.txt`
* In `generate_blog.py`, change the values of
    * `api_key`
    * `model`
    * `prompt`
* For this project i have used Gemini API, therefore i used the sdk from the google genai.
* Store the API key in github actions secrets.
