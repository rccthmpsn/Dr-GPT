from flask import Flask, request, jsonify
from druggpt_core import generate_response

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    reply = generate_response(message)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
