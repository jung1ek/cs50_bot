import os
from dotenv import load_dotenv
load_dotenv(".env")

from flask import Flask, render_template, request, jsonify
import time

from agent import create_graph

app = Flask(__name__)
bot = create_graph()
chats = []

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get",methods=('GET','POST'))
def send_message():
    if request.method == "POST":
        data = request.get_json()
        query = data.get("message")
        chats.append({"role":"user","content":query})
        result = bot.invoke({"messages": chats})
        return {"response": result["messages"][-1].content}
    return "GET Method\n"


if __name__=="__main__":
    app.run(debug=True)