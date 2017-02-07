# GeoFire-Python
GeoFire for Python (v0.3)
====================
A Firebase geo-query library: GeoFire for Python

Contributors
------------
* Guanjiu Zhang

Installation
------------

~~~~
    pip install GeoFire-Python
~~~~

Module Import
------------

~~~~
    from GeoFire.geofire import GeoFire
~~~~

Usage Example
------------
>   * Put following code into a python file (eg. example.py) and run on local server

~~~~
    from GeoFire.geofire import GeoFire

    app = Flask(__name__)

    @app.route('/')
    def example():
        geofire = GeoFire(lat = 42.26853470728501,
                       lon = -83.7487,
                       radius = 25,
                       unit = 'km').config_firebase(
            api_key='AIzaSyDk7YcWydJ66LNNP05KaSb2lkaZH5HGNIc',
            auth_domain='geofire-python-example.firebaseapp.com',
            database_URL='https://geofire-python-example.firebaseio.com',
            storage_bucket='geofire-python-example.appspot.com'
        )
        nearby_people_details = geofire.query_nearby_objects(query_ref='Locations',
                                            geohash_ref='geohash')
        nearby_info = []
        for nearby_person_detail in nearby_people_details.values():
            nearby_info.append(" {0} is at {1}.".format(nearby_person_detail['name'], nearby_person_detail['place_name']))
        return jsonify({'nearby_people': nearby_info})


    if __name__ == '__main__':
        app.run(debug=True)

~~~~

>   * Type following address in your browser to see example database structure:

~~~~
    https://geofire-python-example.firebaseio.com/.json?print=pretty
~~~~