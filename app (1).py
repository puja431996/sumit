from flask import Flask
import geocoder
import geopy
from geopy.geocoders import Nominatim
from datetime import datetime
from flask import request
from flask import jsonify
from flask_cors import CORS
# from werkzeug.contrib.fixers import ProxyFix
# app.wsgi_app = ProxyFix(app.wsgi_app)



app = Flask(__name__)
CORS(app)


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    #print(request.environ['REMOTE_ADDR'])
    #request.remote_addr
    if not request.headers.getlist("X-Forwarded-For"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-For")[0]
    return {'ip': ip}, 200


@app.route('/get_location')
def get_location():
    ip,_ = get_my_ip()
    #print(ip["ip"])
    try:
        g = geocoder.ip(ip["ip"])
        lat_long=g.latlng
        coord=', '.join(list(map(str,lat_long)))
        geolocator = Nominatim(user_agent="test_project")
        location = geolocator.reverse(coord)

        return location.address ,ip["ip"]
    except:
        return "Sorry..! Could not determine location" ,ip["ip"]



@app.route('/get_shops')
def get_shops():
    return_data = dict()
    curr_address,ip = get_location()
    return_data["location"] = curr_address
    return_data["store_name"] = [{"shop_name":"Dummy_Shop1","category":"restaurant","rating":"5 star","description":"good store","contact":"987654321","timing":"9AM-5PM"},{"shop_name":"Dummy_Shop2","rating":"5 star","category":"grocery","description":"average store","contact":"987654321","timing":"9AM-5PM"},{"shop_name":"Dummy_Shop3","rating":"5 star","category":"salon","description":"bad store","contact":"987654321","timing":"9AM-5PM"},{"shop_name":"Dummy_Shop4","rating":"5 star","description":"decent store","category":"home_appliance ","contact":"987654321","timing":"9AM-5PM"},{"shop_name":"Dummy_Shop5","rating":"5 star","description":"good store","category":"restaurant","contact":"987654321","timing":"9AM-5PM"}]
    return_data["date_time"]=str(datetime.now())
    return_data["ip address"] = ip
    return return_data




if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")