from PIL import Image


def validate_image(path):
    """Check that Pillow can read the image file without decoding errors."""
    try:
        with Image.open(path) as image:
            image.verify()
        return True, ""
    except Exception as exc:
        return False, str(exc)


def image_info(path):
    """Return the basic properties used by the dataset report."""
    with Image.open(path) as image:
        return {
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "mode": image.mode,
        }
