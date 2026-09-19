from dataprepkit.scanner import scan_images


def test_scan_images_recursively(tmp_path):
    (tmp_path / "nested").mkdir()
    (tmp_path / "a.JPG").write_bytes(b"image")
    (tmp_path / "nested" / "b.png").write_bytes(b"image")
    (tmp_path / "notes.txt").write_text("ignore")

    names = [path.name for path in scan_images(tmp_path)]
    assert names == ["a.JPG", "b.png"]
