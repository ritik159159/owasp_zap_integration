def test_comments_filtered_by_post(session, base_url):
    r = session.get(f"{base_url}/comments", params={"postId": 1}, timeout=15)
    assert r.status_code == 200
    assert len(r.json()) > 0


def test_todos_completed_filter(session, base_url):
    r = session.get(f"{base_url}/todos", params={"completed": "true"}, timeout=15)
    assert r.status_code == 200
    assert all(t["completed"] is True for t in r.json())


def test_albums(session, base_url):
    r = session.get(f"{base_url}/albums", timeout=15)
    assert r.status_code == 200
    assert len(r.json()) == 100