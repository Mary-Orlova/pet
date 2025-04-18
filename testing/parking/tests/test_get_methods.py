import pytest


@pytest.mark.parametrize(
    "url_template,expected_code", [("/clients", 200), ("/clients/{client_id}", 200)]
)
def test_get_methods(client, test_client, url_template, expected_code):
    """Тест на работу get-методов"""
    url = (
        url_template.format(client_id=test_client.id)
        if "{client_id}" in url_template
        else url_template
    )

    response = client.get(url)
    assert response.status_code == expected_code

    if "clients/{client_id}" in url_template:
        assert response.json["id"] == test_client.id
        assert response.json["car_number"] == test_client.car_number
        assert response.json["credit_card"] == test_client.credit_card
