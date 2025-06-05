from flask import Flask, request, jsonify
import openai
import os

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return "DrugGPT is alive."

# This is your /ask POST endpoint
@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("prompt")

    if not user_input:
        return jsonify({"error": "Missing prompt"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are DrugGPT, an expert on legal and illegal substances."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        answer = response['choices'][0]['message']['content']
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional: Run locally for testing
if __name__ == "__main__":
    app.run(debug=True)
