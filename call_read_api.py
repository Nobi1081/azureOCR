from ast import Dict
from typing import Any
import urllib
import time
import urllib.parse
from read_api import call_read_api, call_get_read_result_api
from typing import Dict, Any

# OCR結果を取得する関数
# api_host: APIのホスト名
# api_url: APIのURL
# file_name: OCR対象のファイル名
# read_headers: リクエストヘッダ
# result_headers: 結果取得ヘッダ
# return: OCR結果の辞書
def process_ocr(api_host: str, api_url: str, file_name: str, read_headers: Dict[str, Any], result_headers: Dict[str, Any]) -> Dict[str, Any]:
    # OCR対象のファイルをバイナリで読み込む
    body = open(file_name,"rb").read()

    # パラメータの指定
    # 自然な読み取り順序で出力できるオプションを追加
    params = urllib.parse.urlencode({
        # Request parameters
        'readingOrder': 'natural',
    })

    # readAPIを呼んでOperation Location URLを取得
    operation_location_url = call_read_api(api_host, api_url, body, params, read_headers)

    print(operation_location_url)

    # 処理待ち10秒
    time.sleep(10)

    # Read結果取得
    result_dict = call_get_read_result_api(api_host, file_name, operation_location_url, result_headers)
    return result_dict

