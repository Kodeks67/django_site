import pytest
from django.urls import reverse

from portfolio.models import ContactMessage


@pytest.mark.django_db
def test_contact_honeypot_blocks(client):
    assert ContactMessage.objects.count() == 0

    resp = client.post(
        reverse("contact"),
        {
            "name": "Bot",
            "email": "bot@example.com",
            "message": "spam",
            "website": "filled",
        },
    )

    assert resp.status_code == 200
    assert ContactMessage.objects.count() == 0


@pytest.mark.django_db
def test_contact_ok(client):
    assert ContactMessage.objects.count() == 0

    resp = client.post(
        reverse("contact"),
        {"name": "User", "email": "user@example.com", "message": "Hello!"},
        follow=True,
    )

    assert resp.status_code == 200
    assert ContactMessage.objects.count() == 1
