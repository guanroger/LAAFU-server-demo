from flask import Flask, request, jsonify
app = Flask(__name__)
app.debug=True

@app.route("/", methods=['GET', 'POST'])
def index():
    #value = request.json['V'][1]
    data=request.get_json()
    if data !=None:
        A=data['A']
        V=data['V']
    location=[123, 456]
    floor="G"
    return jsonify({"x":location[0], "y": location[1], "floor": floor})
    #return jsonify({"return":data})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)