from geoindex import GeoGridIndex, GeoPoint
from pyrebase import pyrebase
import geohash
from geoindex import utils
from geoindex.geo_grid_index import GEO_HASH_GRID_SIZE
import requests

# GeoFire for Python - By Guanjiu Zhang
class GeoFire(GeoGridIndex):
    def __init__(self,
                 lat,
                 lon,
                 radius,
                 unit='km'
                 ):
        GeoGridIndex.__init__(self,precision=3)
        self.center_point = GeoPoint(
            latitude=float(lat),
            longitude=float(lon)
        )
        self.radius = radius
        self.unit = unit
        self._config = None

    @property
    def __config(self):
        return self._config

    @__config.setter
    def __config(self, value):
        self._config = value

    def config_firebase(self,
                        api_key,
                        auth_domain,
                        database_URL,
                        storage_bucket):
        self.__config = {
            "apiKey": api_key,
            "authDomain": auth_domain,
            "databaseURL": database_URL,
            "storageBucket": storage_bucket
        }
        return self

    # Get all nearest regions geohashes to form a search circle
    def __get_search_region_geohashes(self):
        if self.unit == 'mi':
            self.radius = utils.mi_to_km(self.radius)
        grid_size = GEO_HASH_GRID_SIZE[self.precision]
        if self.radius > grid_size / 2:
            # radius is too big for current grid, we cannot use 9 neighbors
            # to cover all possible points
            suggested_precision = 0
            for precision, max_size in GEO_HASH_GRID_SIZE.items():
                if self.radius > max_size / 2:
                    suggested_precision = precision - 1
                    break
            raise ValueError(
                'Too large radius, please rebuild GeoHashGrid with '
                'precision={0}'.format(suggested_precision)
            )
        search_region_geohashes = geohash.expand(self.get_point_hash(self.center_point))
        return search_region_geohashes

    def query_nearby_objects(self, query_ref, geohash_ref, token_id = None):
        search_region_hashes = self.__get_search_region_geohashes()
        all_nearby_objects = {}
        for search_region_hash in search_region_hashes:
            try:
                firebase = pyrebase.initialize_app(self.__config)
                db = firebase.database()
                test_node = db.child(str(query_ref))
                nearby_objects = test_node.order_by_child(str(geohash_ref)). \
                    start_at(search_region_hash).end_at(search_region_hash + '\uf8ff').get(token=token_id).val()
                all_nearby_objects.update(nearby_objects)
            except requests.HTTPError as error:
                raise error
            except:
                continue
        return all_nearby_objects