import faiss
import numpy as np

def build_faiss_index(embeddings_list):
    """
    根据所有文本 Embedding 构建 FAISS 索引。
    embeddings_list: list，每个元素为对应文本的向量（list 或 numpy 数组）
    """
    if not embeddings_list:
        raise ValueError("embeddings_list 为空")
    
    dimension = len(embeddings_list[0])
    index = faiss.IndexFlatL2(dimension)
    xb = np.array(embeddings_list).astype("float32")
    index.add(xb)
    return index

def search_faiss_index(index, query_embedding, texts, top_k=5):
    """
    使用 FAISS 索引查询最接近的 top_k 个文本块。
    query_embedding: 待查询的向量
    texts: 原文本列表，与 embeddings_list 一一对应
    """
    query_vec = np.array([query_embedding]).astype("float32")
    distances, indices = index.search(query_vec, top_k)
    results = [texts[i] for i in indices[0] if i < len(texts)]
    return results

# 测试代码（仅用于本地调试时使用）
if __name__ == "__main__":
    # 构造假数据：3个随机向量和对应文本
    embeddings_list = [[0.1, 0.2, 0.3], [0.2, 0.1, 0.0], [0.3, 0.4, 0.5]]
    texts = ["文本1", "文本2", "文本3"]
    index = build_faiss_index(embeddings_list)
    # 查询向量
    query_embedding = [0.1, 0.2, 0.3]
    results = search_faiss_index(index, query_embedding, texts)
    print("检索结果：", results)