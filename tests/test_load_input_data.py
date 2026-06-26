"""
テスト: load_input_data モジュール

検証項目：
  1. 正常なテキストファイルが正しくリスト化されること
  2. 空行や空白のみの行が適切に除外されること
  3. 末尾の改行コード（\n）が除去されていること
  4. 存在しないパスを指定した際に FileNotFoundError が送出されること
  5. ファイルが空の場合は [] を返すこと
"""

from src.my_library.load_input_data import load


def test_load():

    result = load(
        "tests/sample.txt"
    )

    assert len(result) > 0

    assert result["我慢"] == "n"

    assert (
        result["我慢しきれない"]
        == "n"
    )

    assert result["餓える"] == "n"

    assert result["延命"] == "e"

    assert result["怨み"] == "n"