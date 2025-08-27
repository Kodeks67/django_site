import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def image_file():
    # создаём маленькую png-картинку в памяти
    from PIL import Image

    buf = io.BytesIO()
    img = Image.new("RGB", (10, 10), color=(255, 0, 0))
    img.save(buf, format="PNG")
    buf.seek(0)
    return SimpleUploadedFile("test.png", buf.read(), content_type="image/png")
