from unstructured.partition.pdf import partition_pdf
from unstructured.partition.docx import partition_docx

def parse_document(file_path):
    """
    根据文件后缀解析 PDF 或 Word 文档，并提取文本和表格数据。
    """
    if file_path.lower().endswith('.pdf'):
        elements = partition_pdf(file_path, strategy="auto")
    elif file_path.lower().endswith('.docx'):
        elements = partition_docx(file_path, strategy="auto")
    else:
        raise ValueError("暂不支持该文件格式，请上传 PDF 或 DOCX 文件。")
    
    texts = [el.text for el in elements if el.category == "UncategorizedText"]
    tables = [el.metadata.text_as_html for el in elements if el.category == "Table"]
    return texts, tables

# 测试代码（仅用于本地调试时使用）
if __name__ == "__main__":
    texts, tables = parse_document("doc.pdf")
    print("文本条数：", len(texts))
    print("表格条数：", len(tables))