import csv
from collections import defaultdict


class CurrencyNotFoundException(RuntimeError):
    pass


class DateNotFoundException(RuntimeError):
    pass


class FxRateDatabase:
    """
    A simple database class for the Foreign Exchange rates.
    Stores the data in a nested dict structure keyed by the Currency, then the date.
    """

    def __init__(self, data: dict):
        self._data = data

    def get_fx_rate(self, currency: str, date: str = None):
        """
        Get the fx rate from the database
        :param currency: The queried currency as a string
        :param date: The queried date as a string (optional)
        :return: The specific fx rate or a dictionary of all historical data if `date` is None
        """

        if currency not in self._data:
            raise CurrencyNotFoundException(currency)

        currency_data = self._data[currency]
        if date is None:
            return currency_data

        if date not in currency_data:
            raise DateNotFoundException(date)

        return currency_data[date]

    @staticmethod
    def load_from_csv(csv_path: str) -> "FxRateDatabase":
        """
        Loads the data from a csv. The format of the csv file should be the following
        Date, Currency1, Currency2, ...
        Date1, ExchangeRate, ExchangeRate, ...
        Date2, ExchangeRate, ExchangeRate, ...
        ...

        :param csv_path: The path to the csv file
        :return: An FxRateDatabase instance with the values loaded from the csv
        """
        data = defaultdict(dict)

        with open(csv_path, newline='') as csv_file:
            reader = csv.DictReader(csv_file)

            currencies = reader.fieldnames[1:]
            for row in reader:
                date = row["Date"]
                for currency in currencies:
                    value = row[currency]
                    exchange_rate = float(value) if value and value != "N/A" else None
                    data[currency][date] = exchange_rate

        return FxRateDatabase(data)
