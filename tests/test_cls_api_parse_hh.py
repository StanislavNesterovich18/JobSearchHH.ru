from unittest.mock import patch

from src.cls_api_parse_hh import HH


def test_cls_api_parse_hh() -> None:
    with patch("requests.Session") as mock:
        mock.status_code = 200
        mock.json.return_value = {"items": []}

        hh = HH()
        assert hh.load_vacancies("") == []
