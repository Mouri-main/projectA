"""
ファイル入力処理モジュール
機能：
  指定されたパスのテキストファイルを読み込み、行ごとのリストに変換する。
仕様：
  - 入力：ファイルパス (str)
  - 出力：行のリスト (list[str])
  - 改行コード・前後の空白を除去
  - 空行（空白のみの行を含む）は除外
  - janome.tokenizer.Tokenizer を使用して単語を原型にする
  - janomeはtokenizerをインポートして使用する
  - 文節は分割するが、例えば、「我慢 し きる ない」は「我慢」「我慢 し」「我慢 し きる」「我慢 し きる ない」すべてが入ってる必要があるので、すべて登録する。
    - この登録するとき、例えば「我慢」が前に登録されていたら登録せずにスキップ。
  - 英字は半角にする
  - ファイルが存在しない場合は FileNotFoundError
  - ファイルが空の場合は [] を返す
"""

from . import tokenizer
from pathlib import Path
import unicodedata


def _normalize_text(text: str) -> str:
    """
    全角英数字を半角に統一
    """
    return unicodedata.normalize("NFKC", text)


def _generate_phrases(text: str) -> list[str]:
    """
    我慢 し きれ ない

    ↓

    [
        "我慢",
        "我慢し",
        "我慢しきれ",
        "我慢しきれない"
    ]
    """

    tokens = text.split()

    return [
        "".join(tokens[:i])
        for i in range(1, len(tokens) + 1)
    ]


def load_lines(file_path: str) -> list[str]:
    """
    ファイルを読み込み、
    空行除去＋正規化済みの行リストを返す
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    text = path.read_text(
        encoding="utf-8"
    )

    if text.strip() == "":
        return []

    result = []

    for raw_line in text.splitlines():

        line = _normalize_text(
            raw_line.strip()
        )

        if line:
            result.append(line)

    return result


def parse_polarity_data(
    lines: list[str]
) -> dict[str, str]:
    """
    行リストから
    単語→極性辞書を作成
    """

    result = {}

    for line in lines:

        parts = line.split("\t")

        # ネガ（経験） 我慢 し きれ ない

        if len(parts) == 2:

            category = parts[0]
            expression = parts[1]

            if "ネガ" in category:
                polarity = "n"
            elif "ポジ" in category:
                polarity = "p"
            else:
                polarity = "e"

            phrases = _generate_phrases(expression)

            for phrase in phrases[:-1]:

                if phrase not in result:
                    result[phrase] = "e"

            full_phrase = phrases[-1]

            if full_phrase not in result:
                result[full_phrase] = polarity

        # 延命 e ～する（行為）
        # 良い ～である p
        # 二度寝 ～する(行為) 客観 12345678910 n

        elif len(parts) >= 3:

            word = parts[0]

            polarity = None

            if parts[1] in {"p", "e", "n"}:
                polarity = parts[1]

            elif parts[-1] in {"p", "e", "n"}:
                polarity = parts[-1]

            if polarity is not None:
                result.setdefault(
                    word,
                    polarity
                )

    return result


def load(file_path: str) -> dict[str, str]:
    """
    極性辞書ファイル読込
    """

    lines = load_lines(file_path)

    return parse_polarity_data(lines)