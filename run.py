from app import app
from sys import argv

deb = 'debug' in argv
app.run(host='0.0.0.0', port=8880, debug=deb)
