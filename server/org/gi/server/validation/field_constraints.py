__author__ = 'avishayb'

LENGTH_CONSTRAINTS = {
    'user': {'password': (8, 12), 'first_name': (2, 22), 'last_name': (2, 22),'user_name': (2, 22)},
    'task': {'description': (8, 50), 'title': (2, 22)},
    'case': {'description': (8, 50), 'title': (2, 22)},
    'address': {'street_name': (3, 25), 'street_number': (1, 6), 'city': (3, 25), 'country': (2, 22), 'floor': (1, 4),
                'zip_code': (3, 7), 'entrance': (2, 10), 'apartment_number': (2, 8)}
}

