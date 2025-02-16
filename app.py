import os
import streamlit as st
from doc_parser import parse_document
from db_handler import store_tables_in_sqlite
from qa_chain import create_chat_chain
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb

st.title("智能文档分析助手（增强版RAG）")

# 文件上传
uploaded_file = st.file_uploader("上传 PDF 或 DOCX 文档", type=["pdf", "docx"])
if uploaded_file is not None:
    file_path = uploaded_file.name
    # 保存上传文件到本地
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.info("文件已保存，开始解析文档...")
    try:
        texts, tables = parse_document(file_path)
        st.success(f"解析完成：文本条数 = {len(texts)}，表格数量 = {len(tables)}")

        # 构建文本向量库（Chroma）
        if st.button("构建文本向量库"):
            try:
                # 使用 BAIA/bge-small-en 生成 Embedding
                embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
                client = chromadb.Client()
                collection = client.create_collection(name="documents")
                for idx, text in enumerate(texts):
                    emb = embeddings.embed_query(text)
                    collection.add(documents=[text], embeddings=[emb], ids=[str(idx)])
                st.success("文本向量库已构建成功！")
            except Exception as e:
                st.error(f"构建向量库失败：{e}")

        # 存储表格数据到 SQLite
        if st.button("存储表格数据到 SQLite"):
            try:
                store_tables_in_sqlite(tables)
                st.success("表格数据已成功存入 SQLite 数据库！")
            except Exception as e:
                st.error(f"存入表格数据失败：{e}")

        st.markdown("---")
        st.header("对话问答")
        question = st.text_input("请输入你的问题：")
        
        if st.button("发送问题"):
            if question:
                chat_chain = create_chat_chain(tables)
                answer = chat_chain(question)
                st.write("回答：", answer)
            else:
                st.warning("请输入问题")
    except Exception as e:
        st.error(f"解析文档失败：{e}")
else:
    st.info("请先上传一个文档")