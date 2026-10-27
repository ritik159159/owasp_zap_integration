import pytest


def test_list_posts(session, base_url):
    r = session.get(f"{base_url}/posts", timeout=15)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list) and len(data) == 100


def test_filter_posts_by_user(session, base_url):
    r = session.get(f"{base_url}/posts", params={"userId": 1}, timeout=15)
    assert r.status_code == 200
    assert all(p["userId"] == 1 for p in r.json())


def test_get_single_post(session, base_url):
    r = session.get(f"{base_url}/posts/1", timeout=15)
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == 1
    assert {"userId", "title", "body"} <= body.keys()


def test_get_post_not_found(session, base_url):
    r = session.get(f"{base_url}/posts/9999", timeout=15)
    assert r.status_code == 404


def test_create_post(session, base_url):
    payload = {"title": "zap test title", "body": "zap test body", "userId": 1}
    r = session.post(f"{base_url}/posts", json=payload, timeout=15)
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == payload["title"]
    assert "id" in body  # jsonplaceholder fakes the write and returns id 101


def test_update_post_put(session, base_url):
    payload = {"id": 1, "title": "updated", "body": "updated body", "userId": 1}
    r = session.put(f"{base_url}/posts/1", json=payload, timeout=15)
    assert r.status_code == 200
    assert r.json()["title"] == "updated"


def test_update_post_patch(session, base_url):
    r = session.patch(f"{base_url}/posts/1", json={"title": "patched"}, timeout=15)
    assert r.status_code == 200
    assert r.json()["title"] == "patched"


def test_delete_post(session, base_url):
    r = session.delete(f"{base_url}/posts/1", timeout=15)
    assert r.status_code == 200


def test_post_comments(session, base_url):
    r = session.get(f"{base_url}/posts/1/comments", timeout=15)
    assert r.status_code == 200
    assert all(c["postId"] == 1 for c in r.json())