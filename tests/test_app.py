import json
from unittest.mock import patch

from fxrates.app import create_app
from fxrates.fx_rate_database import FxRateDatabase


def mock_init_database():
    data = {"CURR1": {"2024-01-01": 1, "2024-01-02": 2},
            "CURR2": {"2024-01-01": 2, "2024-01-02": 4},
            "CURR3": {"2024-01-01": None, "2024-01-02": None},
            }
    return FxRateDatabase(data)


def test_app():
    with patch("fxrates.app._init_database", mock_init_database):
        app = create_app()
        client = app.test_client()

        # query single value
        response = client.get("/fxrates/CURR1?date=2024-01-01")
        assert response.status_code == 200
        assert response.text == "1"

        # query historical values for a currency
        response = client.get("/fxrates/CURR1")
        assert response.status_code == 200
        assert json.loads(response.text) == {"2024-01-01": 1, "2024-01-02": 2}

        # query N/A value
        response = client.get("/fxrates/CURR3?date=2024-01-01")
        assert response.status_code == 200
        assert response.text == "N/A"

        # query non-existent currency
        response = client.get("/fxrates/SAJT?date=2024-01-01")
        assert response.status_code == 404

        # query non-existent date
        response = client.get("/fxrates/SAJT?date=2024-01-01")
        assert response.status_code == 404


def test_database_setup_only_once():
    with patch("fxrates.app._init_database") as mocked_init_database:
        app = create_app()
        client = app.test_client()

        client.get("/fxrates/SKK?date=2023-12-08")
        client.get("/fxrates/SKK?date=2023-12-09")
        client.get("/fxrates/SKK?date=2023-12-10")

        mocked_init_database.assert_called_once()

