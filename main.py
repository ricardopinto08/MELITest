from MELIdb import *
from dotenv import load_dotenv
from controller import app


if __name__ == "__main__":
    create_tables()
    populate_tables()
    load_dotenv()
    app.run(host = '0.0.0.0', port = 5000, debug = False)