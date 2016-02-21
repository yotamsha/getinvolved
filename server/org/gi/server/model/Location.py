from org.gi.server.service import location as location_service


class Location:
    def __init__(self):
        pass

    @staticmethod
    def retrieve_all_location_data(location):
        if location.get('address'):
            geo = location_service.get_lat_lng(location.get('address'))
            location['geo_location'] = geo
        elif location.get('geo_location'):
            geo = location.get('geo_location')
            address = location_service.get_address(geo.get('lat'), geo.get('lng'))
            location['address'] = address

    # Mongodb documentation: Always list coordinates in longitude, latitude order.
    @staticmethod
    def change_geo_location_to_db_format(location):
        geo_location = location.get('geo_location')
        db_geo_location = {
            'type': 'Point',
            'coordinates': [geo_location.get('lng'), geo_location.get('lat')]
        }
        location['geo_location'] = db_geo_location

    @staticmethod
    def change_geo_location_to_client_format(location):
        if not location:
            return

        coordinates = location.get('geo_location')['coordinates']
        client_geo_location = {
            'lng': coordinates[0],
            'lat': coordinates[1]
        }
        location['geo_location'] = client_geo_location
