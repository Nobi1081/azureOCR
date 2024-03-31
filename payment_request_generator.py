import json
from pdfrw import PdfReader, PdfWriter
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from pdfrw import PdfReader, PdfWriter
from pdfrw import PdfWriter, PdfReader
from make_pdf_page import make_page
from typing import Dict, Any

# OCR結果を元にPDFを作成する関数
# input_pdf_file: OCR対象のPDFファイル
# ocr_result_file: OCR結果のjsonファイル
# output_pdf_file: 作成するPDFファイル
# font_name: 使用するフォント名
# encoding: jsonファイルのエンコーディング
def create_pdf_with_ocr(input_pdf_file: str, ocr_result_file: str, 
                        output_pdf_file: str, encoding: str = 'utf-8') -> None:
    
    # OCR結果のjsonファイルを読み込む
    with open(ocr_result_file, "r", encoding=encoding) as f:
        data_dict: Dict[str, Any] = json.load(f)

    # Define PdfWriter
    pdf_writer: PdfWriter = PdfWriter("img/ocr_result.pdf")

    # OCR対象となったPDFファイルを読み込む
    input_pdf = PdfReader(input_pdf_file, decompress=False)
    input_pdf_pages = input_pdf.pages

    # ファイルのページ分処理を回す
    for page_num, data_page in enumerate(data_dict["readResults"]):
        # OCR結果のjsonデータからページサイズを取得
        pdf_page = input_pdf_pages[page_num]

        # OCR結果を元に1ページ分のPDFを作成
        make_page(pdf_writer, pdf_page, data_page) 

# 1ページ分のPDFを作成する関数
# writer: PdfWriterオブジェクト
# pdf_page: 元のPDFの1ページ
# data_page: OCR結果の1ページ
def make_page(writer: PdfWriter, pdf_page: Any, data_page: Dict[str, Any]) -> None:
    # 中間生成物ファイル名
    tmp_file = r"img/work.pdf"

    # OCR結果のjsonデータからページサイズを取得
    page_width = data_page["width"]
    page_height = data_page["height"]
    pagesize = (page_width * inch, page_height * inch)

    # ここで定義したpdfにOCR結果を重畳して、tmp_fileに保存する
    pdf = canvas.Canvas(tmp_file, pagesize = pagesize)

    # 既存のPDFページをオブジェクト化
    pp = pagexobj(pdf_page)
    # 既存のPDFページを描画
    pdf.doForm(makerl(pdf,pp))

     # テキスト書き込み
    for line_num, line in enumerate(data_page["lines"]):
        # テキスト始点座標
        (pos_x,pos_y) = (line["boundingBox"][6], line["boundingBox"][7])

        # テキストボックスサイズ
        box_width = line["boundingBox"][2]-line["boundingBox"][0]
        box_height = line["boundingBox"][7]-line["boundingBox"][1]

        # テキスト
        text = line["text"]
        # フォント設定
        pdfmetrics.registerFont(UnicodeCIDFont(line["fontFamily"]))
        pdf.setFont(line["fontFamily"], line["fontSize"])
        # 色指定(黒色）
        pdf.setFillColorRGB(0, 0, 0)  # 黒色
        # テキストを描画する
        pdf.drawString(
            pos_x * inch,  # ここでx方向の位置を調整する
            (page_height - pos_y) * inch, # ここでy方向の位置を調整する
            text
        )

    pdf.showPage()
    pdf.save()

    # 中間生成のPDFファイルを読み込む
    with open(tmp_file, mode="rb") as f:
        pdf_reader = PdfReader(f)

    # 中間生成PDFをwriterに取り込む
    writer.addPage(pdf_reader.pages[0])

# メイン処理
FILE_NAME = r"img/不定時_Template.pdf"
OUTPUT_JSON_FILE = r"img/pdf_setting.json"
OUTPUT_PDF_FILE = r"img/ocr_result.pdf"

# OCR結果を元にPDFを作成
create_pdf_with_ocr(FILE_NAME, OUTPUT_JSON_FILE, OUTPUT_PDF_FILE, encoding='utf-8')