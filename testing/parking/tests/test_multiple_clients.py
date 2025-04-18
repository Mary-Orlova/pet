import pytest


@pytest.mark.parametrize("client_fixture", ["test_client", "second_client"])
def test_multiple_clients(client, client_fixture, request):
    """Тест get-запроса клиентов по client_id"""
    client_obj = request.getfixturevalue(client_fixture)
    response = client.get(f"/clients/{client_obj.id}")
    assert response.json["id"] == client_obj.id
