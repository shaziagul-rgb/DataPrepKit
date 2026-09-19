from dataprepkit.duplicates import find_duplicates


def test_duplicate_files(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    c = tmp_path / "c.txt"
    a.write_text("same")
    b.write_text("same")
    c.write_text("different")

    groups = find_duplicates([a, b, c])
    assert len(groups) == 1
    assert set(groups[next(iter(groups))]) == {a, b}
