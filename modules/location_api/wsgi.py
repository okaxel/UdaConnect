"""
UdaConnect App Microservice version
===================================

Service: LocationApi
"""

# restructured import according to pylint suggestions

import os

from app import create_app


app = create_app(os.getenv("FLASK_ENV") or "test")


if __name__ == "__main__":
    app.run(debug=True)
