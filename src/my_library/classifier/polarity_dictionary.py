"""
極性辞書データアクセス
  極性辞書データを管理する
  - 複数の辞書ファイルをディレクトリから読み込み
  - load_input_data.load_data を使用してファイルを読む
  - 
  - 単語を受け取ったら極性ラベルを返す
  - 未登録単語や空文字へのgetはKeyErrorを送出せずNoneを返す
"""

from pathlib import Path

from ..load_input_data import load


class PolarityDictionary:
    """
    極性辞書管理クラス
    """

    def __init__(
        self,
        dictionary_dir: str
    ):

        self._dictionary: dict[str, str] = {}

        path = Path(dictionary_dir)

        if not path.exists():
            return

        for file_path in path.glob("*.txt"):

            try:

                data = load(
                    str(file_path)
                )

                self._dictionary.update(
                    data
                )

            except Exception:
                continue

    def get_polarity(
        self,
        word: str
    ) -> str | None:
        """
        単語の極性取得

        Returns
        -------
        "p"
        "e"
        "n"
        None
        """

        if not word:
            return None

        return self._dictionary.get(
            word
        )