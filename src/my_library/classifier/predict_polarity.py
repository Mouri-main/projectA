"""
ソース：predict_polarity_v2.py
極性判定アルゴリズム
トークン列と辞書を用いた感情極性の判定
  - アルゴリズムはまかせた
  - 戻り値は厳密に "p", "n", "e" のいずれか
  - トークンリストが空、全極性が None、スコア拮抗時は安全に "e" を返す
"""
from .polarity_dictionary import PolarityDictionary


def predict(tokens: list[str], dictionary: PolarityDictionary) -> str:
    """


    判定方法は「最長一致」→「単純な多数決」。

    最長一致：
    現在位置のトークンから始め、後続のトークンを1つずつ連結していく。
    連結した文字列に対してget_polarityを呼び、Noneでない限り、
    その結果をスタックに積みながら連結を続ける。
    Noneが返ってきたら連結を打ち切り、スタックの最後の極性ラベルを
    その区間全体の結果として採用する。
    例えば「我慢」「する」「きれる」「ない」「ので」というトークン列で、
    「我慢するきれるない」までは辞書にあり「我慢するきれるないので」で
    初めてNoneになった場合、「我慢するきれるない」の極性ラベルを採用し、
    次の区間は「ので」から再開する。
    辞書に1単語も一致しない場合は、その1トークンは無視(None扱い)して次へ進む。

    単純な多数決：
    各区間の極性ラベルについて、
    "p" であればpositiveカウントを、"n" であればnegativeカウントを増やす。
    "e" やNoneの場合(中立、または辞書に存在しない場合)はカウントしない。

    最後にpositiveカウントとnegativeカウントを比較し、
    多い方を結果として返す。同数の場合(両方0件の場合を含む)は "e" を返す。
 

    議論：
    ・空白を引数に取った場合、現在は"e"を返すことにしているが、Noneを返した方が良い?
        ・アウトプット担当と認識のすり合わせが必要⇩
        ・eがどういうことを意味するのか。「中立的な文章」なのか、それとも「この文章からは感情は分からない」なのか
        ・それによって"e"を返すべきかNoneを返すべきかが変わると思う
    """
    if not tokens:
        return "e"
        # TODO: Noneか"e"か

    positive_count = 0
    negative_count = 0

    i = 0
    n = len(tokens)

    while i < n:
        stack = []
        current = tokens[i]
        polarity_label = dictionary.get_polarity(current)

        j = i
        while polarity_label is not None:
            stack.append(polarity_label)
            j += 1
            if j >= n:
                break
            current = current + tokens[j]
            polarity_label = dictionary.get_polarity(current)

        if stack:
            matched_label = stack[-1]
            if matched_label == "p":
                positive_count += 1
            elif matched_label == "n":
                negative_count += 1
            # 一致した分だけ進める
            i += len(stack)
        else:
            # 1トークン単体でも辞書になかった場合
            i += 1

    if positive_count > negative_count:
        return "p"
    elif negative_count > positive_count:
        return "n"
    else:
        return "e"
