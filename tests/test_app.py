from app.main import create_app


def test_index():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["status"] == "running"


def test_health():
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_normalise_rule():
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/normalise",
        json={"rule": "  CUSTOMER   RECORDS must be retained  "},
    )

    assert response.status_code == 200
    assert (
        response.get_json()["normalised"]
        == "customer records must be retained"
    )


def test_missing_rule():
    app = create_app()
    client = app.test_client()

    response = client.post("/normalise", json={})

    assert response.status_code == 400
    assert response.get_json()["error"] == "A rule is required"