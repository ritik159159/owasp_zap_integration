def test_list_users(session, base_url):
    r = session.get(f"{base_url}/users", timeout=15)
    assert r.status_code == 200
    assert len(r.json()) == 10


def test_get_user(session, base_url):
    r = session.get(f"{base_url}/users/1", timeout=15)
    assert r.status_code == 200
    user = r.json()
    assert user["id"] == 1
    assert "@" in user["email"]


def test_user_not_found(session, base_url):
    r = session.get(f"{base_url}/users/9999", timeout=15)
    assert r.status_code == 404