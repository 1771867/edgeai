from waitress import serve
from app import main as app

serve(app.app, host='0.0.0.0', port=9007)