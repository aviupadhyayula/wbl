from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST'])
def test_webhook():
    print("hi")

def create_response(message, number=0):
    response = {
    }
    return(jsonify(response))

if __name__ == '__main__':
    app.run(debug=True)
