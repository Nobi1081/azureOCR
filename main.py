import json
import os
import call_read_api
import make_pdf_pages

# Computer Visionリソースのサブスクリプションキー、エンドポイント設定
# サブスクリプションキーとエンドポイントは、リソースグループ作成時に控えておいたキー1,エンドポイントを入力します。
SUBSCRIPTION_KEY = "d3ec92aab5654eab9e99fa4c744f4b1c"
ENDPOINT ="https://kohara-ocr-visoin.cognitiveservices.azure.com/"

# ホストを設定
HOST = ENDPOINT.split("/")[2]

# vision-v3.2のread機能のURLを設定
TEXT_RECOGNITION_URL = (ENDPOINT + "vision/v3.2/read/analyze")

READ_HEADERS = {
    "Content-Type": "application/octet-stream",
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
}
RESULT_HEADERS = {
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
}
FILE_NAME = r"C:/progs/python/ocr/env/img/不定時.pdf"
OUTPUT_JSON_FILE = r"C:/progs/python/ocr/env/img/result.json"
OUTPUT_PDF_FILE = r"C:/progs/python/ocr/env/img/ocr_result.pdf"
FONT_NAME = "HeiseiKakuGo-W5"

# OCR結果を取得
result_dict = call_read_api.process_ocr(HOST, TEXT_RECOGNITION_URL, FILE_NAME, READ_HEADERS, RESULT_HEADERS)

# OCR結果を保存
with open(OUTPUT_JSON_FILE, "w", encoding='utf-8') as f:
    json.dump(result_dict, f, indent=3, ensure_ascii=False)

# OCR結果を元にPDFを作成
make_pdf_pages.create_pdf_with_ocr(FILE_NAME, OUTPUT_JSON_FILE, OUTPUT_PDF_FILE, FONT_NAME, encoding='utf-8')

# 作成したPDFを表示
os.startfile(OUTPUT_PDF_FILE)
