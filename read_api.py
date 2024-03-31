import time
import http.client, urllib.request, urllib.parse
import urllib.error, base64
import ast

# Read APIを呼ぶ関数
# host: APIのホスト名
# text_recognition_url: APIのURL
# body: リクエストボディ
# params: パラメータ
# read_headers: リクエストヘッダ
# return: Operation-Location URL
def call_read_api(host, text_recognition_url, body, params, read_headers):
    # Read APIの呼び出し
    try:
        conn = http.client.HTTPSConnection(host)
        # 読み取りリクエスト
        conn.request(
            method = "POST",
            url = text_recognition_url + "?%s" % params,
            body = body,
            headers = read_headers,
        )

        # 読み取りレスポンス
        read_response = conn.getresponse()
        print(read_response.status)

        # レスポンスの中から読み取りのOperation-Location URLを取得
        OL_url = read_response.headers["Operation-Location"]

        conn.close()
        print("read_request:SUCCESS")

    except Exception as e:
        if hasattr(e, 'errno'):
            print("[ErrNo {0}]{1}".format(e.errno, e.strerror))
        else:
            print(str(e))
            OL_url = None

    return OL_url

# OCR結果を取得する関数
# host: APIのホスト名
# file_name: OCR対象のファイル名
# OL_url: Operation-Location URL
# result_headers: 結果取得ヘッダ
# return: OCR結果の辞書
def call_get_read_result_api(host, file_name, OL_url, result_headers):
    result_dict = {}
    # Read結果取得
    try:
        conn = http.client.HTTPSConnection(host)

        # 読み取り完了/失敗時にFalseになるフラグ
        poll = True
        while(poll):
            # Operation-Location URLの値がNoneの場合は終了
            if (OL_url == None):
                print(file_name + ":None Operation-Location")
                break

            # 読み取り結果取得
            conn.request(
                method = "GET",
                url = OL_url,
                headers = result_headers,
            )
            # 読み取り結果レスポンス
            result_response = conn.getresponse()
            # 読み取り結果の文字列を取得
            result_str = result_response.read().decode()
            # 読み取り結果の文字列を辞書に変換
            result_dict = ast.literal_eval(result_str)

            if ("analyzeResult" in result_dict):
                poll = False
                print("get_result:SUCCESS")
            elif ("status" in result_dict and 
                  result_dict["status"] == "failed"):
                poll = False
                print("get_result:FAILD")
            else:
                time.sleep(10)
        conn.close()

    except Exception as e:
        print("[ErrNo {0}] {1}".format(e.errno,e.strerror))

    return result_dict
