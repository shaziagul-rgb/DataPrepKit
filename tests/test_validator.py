from PIL import Image

from dataprepkit.validator import image_info, validate_image


def test_validate_and_read_image_info(tmp_path):
    path = tmp_path / "sample.png"
    Image.new("RGB", (20, 10)).save(path)

    assert validate_image(path) == (True, "")
    assert image_info(path)["width"] == 20
    assert image_info(path)["height"] == 10


def test_invalid_image(tmp_path):
    path = tmp_path / "broken.png"
    path.write_bytes(b"not a real image")

    ok, error = validate_image(path)
    assert not ok
    assert error
