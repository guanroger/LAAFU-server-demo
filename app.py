from flask import Flask, request, jsonify
app = Flask(__name__)
app.debug=True

@app.route("/", methods=['GET', 'POST'])
def index():
    #value = request.json['V'][1]
    value_A =request.json['A']
    value_V =request.json['V']
    location=[123, 456]
    floor="G"
    return jsonify({"x":location[0], "y": location[1], "floor": floor})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)