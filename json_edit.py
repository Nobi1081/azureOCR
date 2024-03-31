import json

# 書式設定用josonファイルの読み込み
with open('img/pdf_attr.json', 'r', encoding='utf-8') as f:
    attr = json.load(f)

# jsonファイルを読み込む
with open('img/result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# PDF設定ファイルの初期化
pdf_setting_data = {"readResults": []}

# 検索対象line番号
search_text = [30,41,53,85]

# analyzeResult -> readResults -> lines -> textの値が指定の文字列の場合、その要素を取り出す
for readResults in data['analyzeResult']['readResults']:
    # readResultsの属性をコピー
    page = {       
            "page": readResults['page'],
            "width": readResults['width'],
            "height": readResults['height'],
            "unit": readResults['unit'],
            "lines": []
            }
    # OCR結果のjsonデータから特定の結果を取得し、新たなjsonデータを作成
    for number, line in enumerate(readResults['lines']):
        # textの値が指定の文字列の場合、その要素を取り出す
        if number in search_text:
            # 書式設定ファイルの属性を追加
            attr_data = attr[f"line{number}"]
            # 追加するデータ
            page['lines'].append({
                "text": line['text'],
                "fontSize": attr_data['fontSize'],
                "fontFamily": attr_data['fontFamily'],
                "boundingBox": line['boundingBox']
            })

    # PDF設定ファイルに追加
    pdf_setting_data['readResults'].append(page)

# PDF設定ファイルに追加
with open('img/pdf_setting.json', 'w', encoding='utf-8') as f:
    json.dump(pdf_setting_data, f, ensure_ascii=False, indent=4)