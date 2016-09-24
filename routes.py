from flask import Flask

app = Flask("Eco")

@app.route('/')
def home_page():
    return "Hello World"


app.run()
