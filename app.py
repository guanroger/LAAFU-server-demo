from flask import Flask, request, jsonify
from logging import FileHandler, WARNING
import json
import localization
import get_altered_AP
import get_altered_AP_list

app = Flask(__name__)

file_handler = FileHandler('error_log.txt')
file_handler.setLevel(WARNING)

app.logger.addHandler(file_handler)
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
        floor, changed_RP, location, unchanged_RP = get_altered_AP.get_altered_AP(address)
        #print(changed_RP) 
        #print(location)
        #print(unchanged_RP)
        return jsonify({"data": {"floor": floor , "altered_rp": changed_RP, "ap_position": location, "normal_rp" : unchanged_RP}})
    else:
        data=request.get_json()
        altered_ap_list = get_altered_AP_list.get_altered_AP_mac()
        return jsonify({"altered AP": altered_ap_list})

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5020)
    #app.run(host='143.89.36.109', port=5020)