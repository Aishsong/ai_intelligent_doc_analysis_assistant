# 智能文档分析助手（增强版RAG）

## 项目简介
本项目实现了一个智能文档分析助手，支持上传 PDF/Word 文档后，对文档中的文本与表格数据进行解析，并通过向量化检索和大模型问答，实现多轮对话与表格数据查询。  
技术栈：
- **文档解析**：使用 [Unstructured](https://github.com/Unstructured-IO/unstructured) 处理图文混合内容
- **向量数据库**：使用 [Chroma](https://github.com/chroma-core/chroma) 存储文档向量（也可以结合 FAISS 加速本地检索）
- **大模型**：使用 Llama 3-8B（可通过 Ollama 本地运行，或切换免费 API 如 Groq）
- **前端框架**：使用 [Streamlit](https://streamlit.io/) 构建交互界面
- **对话管理**：使用 [LangChain](https://github.com/hwchase17/langchain) 进行多轮对话链封装
- **统一接口**：使用 [LiteLLM](https://github.com/...) 统一不同模型的 API 调用

此外，项目还使用 Pandas 对表格数据进行预处理，并用 SQLite 存储表格数据，支持后续查询。

## 环境要求
- Windows 环境
- Python 3.8+

## 安装步骤

1. **克隆项目代码**

   ```bash
   git clone https://github.com/Aishsong/ai_intelligent_doc_analysis_assistant
   cd ai_intelligent_doc_analysis_assistant
   ```

2. **创建虚拟环境**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

4. **配置大模型接口**  
   - 如果使用 Ollama 运行 Llama 3-8B，请确保已经安装并启动 Ollama，本示例在 `qa_chain.py` 中默认采用 `litellm.create_llm("ollama", model="llama-3-8b")` 进行配置。  
   - 也可以自行修改 `qa_chain.py` 调用其它大模型或 API。

## 运行项目

启动 Streamlit 前端：

```bash
streamlit run app.py
```

运行后，在浏览器中即可看到上传文档、构建向量库、存储表格数据，以及与文档数据进行多轮对话查询的界面。

## 项目流程
1. 上传 PDF/Word 文档  
2. 系统使用 `doc_parser.py` 解析文档内容，提取普通文本和表格（HTML 格式）  
3. 使用 LangChain 与大模型构建对话链，其中：
   - 普通文本经过 BAID/bge-small-en 模型生成向量后存入 Chroma 向量数据库
   - 表格数据经过 Pandas 解析后存入 SQLite
4. 通过 Streamlit 前端实现多轮对话，并支持对表格与文本的联合查询。

## 注意
- 解析pdf文档需要配置poppler工具
- 问答模型使用的是ollama，本地运行需要配置ollama服务，此部分功能暂未进行测试完善
