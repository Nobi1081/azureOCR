from pdfrw import PdfWriter, PdfReader
import json
from make_pdf_page import make_page
from typing import List, Dict, Any

# OCR結果を元にPDFを作成する関数
# input_pdf_file: OCR対象のPDFファイル
# ocr_result_file: OCR結果のjsonファイル
# output_pdf_file: 作成するPDFファイル
# font_name: 使用するフォント名
# encoding: jsonファイルのエンコーディング
def create_pdf_with_ocr(input_pdf_file: str, ocr_result_file: str, 
                        output_pdf_file: str, font_name: str, encoding: str = 'utf-8') -> None:
    
    # OCR結果のjsonファイルを読み込む
    with open(ocr_result_file, "r", encoding=encoding) as f:
        data_dict: Dict[str, Any] = json.load(f)

    # Define PdfWriter
    pdf_writer: PdfWriter = PdfWriter()

    # OCR対象となったPDFファイルを読み込む
    input_pdf = PdfReader(input_pdf_file, decompress=False)
    input_pdf_pages = input_pdf.pages

    # ファイルのページ分処理を回す
    for page_num, data_page in enumerate(data_dict["analyzeResult"]["readResults"]):
        # OCR結果のjsonデータからページサイズを取得
        pdf_page = input_pdf_pages[page_num]

        # OCR結果を元に1ページ分のPDFを作成
        make_page(pdf_writer, font_name, pdf_page, data_page) 