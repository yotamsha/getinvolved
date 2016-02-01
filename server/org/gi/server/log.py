import logging


FORMAT = '%(asctime)-15s  %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())
