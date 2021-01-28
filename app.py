from flask import Flask, request, jsonify
from json import dumps
import localization

app = Flask(__name__)
app.debug=True

@app.route("/", methods=['GET', 'POST'])
def index():
    #value = request.json['V'][1]
    data=request.get_json()
    if data !=None:
        floor=data['floor']
        data_string=dumps(data)
        location, altered_ap =localization.localization(data_string)


    else:
        floor="A"
        location=[123, 456]
    return jsonify({"x":location[0], "y": location[1], "floor": floor})
    #return jsonify({"return":data})

@app.route("/altered_ap", methods=['GET', 'POST'])
def altered_ap():
    data=request.get_json()
    if data !=None:
        data_string=dumps(data)
        location, altered_ap =localization.localization(data_string)
    else:
        altered_ap="No input"

    return jsonify({"altered AP": altered_ap})

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)