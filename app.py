import os
from flask import Flask, request
from openai import OpenAI

app = Flask(__name__)


def ask_openai(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return "OPENAI_API_KEY is missing. Start the container with -e OPENAI_API_KEY=..."

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    return response.output_text


@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    prompt = ""

    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        if prompt:
            try:
                answer = ask_openai(prompt)
            except Exception as exc:
                answer = f"OpenAI request failed: {exc}"

    return f"""
<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>OpenAI Docker Demo</title>
  <style>
    body {{ font-family: Segoe UI, sans-serif; margin: 2rem; background: #f7f7fb; }}
    main {{ max-width: 760px; margin: auto; background: #fff; padding: 1rem 1.25rem; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,.08); }}
    textarea {{ width: 100%; min-height: 120px; padding: .75rem; }}
    button {{ margin-top: .75rem; padding: .6rem 1rem; cursor: pointer; }}
    pre {{ white-space: pre-wrap; background: #f2f4f8; padding: .75rem; border-radius: 8px; }}
  </style>
</head>
<body>
  <main>
    <h1>OpenAI from Docker</h1>
    <form method=\"post\">
      <textarea name=\"prompt\" placeholder=\"Ask something...\">{prompt}</textarea>
      <br/>
      <button type=\"submit\">Send</button>
    </form>
    <h3>Response</h3>
    <pre>{answer}</pre>
  </main>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
