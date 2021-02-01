from flask import Flask, request, jsonify
import json
import localization
import get_altered_AP

app = Flask(__name__)

app.debug=True

@app.route("/", methods=['GET', 'POST'])
def index():
    #value = request.json['V'][1]
    data=request.get_json()
    if data !=None:
        floor=data['floor']
        data_string=json.dumps(data)
        location, altered_ap =localization.localization(data_string)


    else:
        floor="A"
        location=[123, 456]
    return jsonify({"x":location[0], "y": location[1], "floor": floor})
    #return jsonify({"return":data})

@app.route("/altered_ap", methods=['GET', 'POST'])
def altered_ap():
    address = request.args.get('mac')
    if address != None:
        data=request.get_json()
        changed_RP, location, unchanged_RP = get_altered_AP.get_altered_AP(address)
    else:
        changed_RP = 'Not found' 
        location = 'Not found'
        unchanged_RP = 'Not found'
    return jsonify({"data": {"altered_rp": changed_RP, "ap_position": location, "normal_rp" : unchanged_RP}})

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)