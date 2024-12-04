"""
Automatic Ripping Machine - User Interface (UI)
Provided for free and hosted on GitHub under the MIT License
https://github.com/automatic-ripping-machine/automatic-ripping-machine
"""
from waitress import serve

from ui import create_app

if __name__ == '__main__':
    app = create_app()

    # Serve ARM using Waitress
    serve(app,
          host=app.config["SERVER_HOST"],
          port=app.config["SERVER_PORT"],
          threads=40)
