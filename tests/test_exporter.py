from dataprepkit.exporter import export_file_list


def test_export_relative_paths(tmp_path):
    folder = tmp_path / "images"
    folder.mkdir()
    first = folder / "one.jpg"
    nested = folder / "set" / "two.png"
    nested.parent.mkdir()
    first.write_bytes(b"1")
    nested.write_bytes(b"2")

    output = tmp_path / "files.txt"
    export_file_list([first, nested], output, folder)

    assert output.read_text() == "one.jpg\nset/two.png\n"
