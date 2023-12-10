import os.path
import ssl
from io import BytesIO
from tempfile import TemporaryDirectory
from urllib.request import urlopen
from zipfile import ZipFile

import certifi
from flask import Flask, abort, current_app, request

from fxrates.fx_rate_database import FxRateDatabase, CurrencyNotFoundException, DateNotFoundException

FX_RATES_ZIP_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"


def create_app():
    app = Flask(__name__)

    @app.route('/fxrates/<currency>')
    def get_fx_rates(currency):
        fx_rate_database = current_app.database
        date = request.args.get('date')
        try:
            fx_rate = fx_rate_database.get_fx_rate(currency, date)
            if fx_rate is None:
                return "N/A"
            elif date is not None:  # single value returned
                return str(fx_rate)
            else:
                return fx_rate
        except CurrencyNotFoundException:
            abort(404, f"Currency {currency} not found")
        except DateNotFoundException:
            abort(404, f"Date {date} not found")

    with app.app_context():
        current_app.database = _init_database()
    return app


def _init_database():
    """
    Download the latest fx rate data and initialise the database
    :return: The initialised FxRateDatabase instance
    """
    with urlopen(FX_RATES_ZIP_URL, context=ssl.create_default_context(cafile=certifi.where())) as response:
        with ZipFile(BytesIO(response.read())) as zip_file:
            with TemporaryDirectory() as temp_dir:
                zip_file.extractall(temp_dir)
                csv_path = os.path.join(temp_dir, 'eurofxref-hist.csv')
                fx_rate_data = FxRateDatabase.load_from_csv(csv_path)
    return fx_rate_data


def main():
    app = create_app()
    app.run()


if __name__ == '__main__':
    main()
