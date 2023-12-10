import pytest

from fxrates.fx_rate_database import FxRateDatabase, CurrencyNotFoundException, DateNotFoundException


def test_fx_rate_data():
    data = {"CURR1": {"2024-01-01": 1, "2024-01-02": 2},
            "CURR2": {"2024-01-01": 2, "2024-01-02": 4},
            }
    fx_rate_database = FxRateDatabase(data)

    assert fx_rate_database.get_fx_rate("CURR1", "2024-01-01") == 1
    assert fx_rate_database.get_fx_rate("CURR1") == {"2024-01-01": 1, "2024-01-02": 2}

    with pytest.raises(CurrencyNotFoundException):
        fx_rate_database.get_fx_rate("SAJT", "2024-01-01")

    with pytest.raises(DateNotFoundException):
        fx_rate_database.get_fx_rate("CURR1", "2024-01-03")
