from langchain.schema import SystemMessage, HumanMessage
import litellm

def get_llm():
    """
    创建大模型 API 接口，目前使用 Ollama 执行 Llama 3-8B 模型。  
    可根据需求调整为其他模型或 API（例如 Groq）。
    """
    # 使用旧版 litellm 的 create_llm 接口
    return litellm.create_llm("ollama", model="llama-3-8b")

def create_chat_chain(tables):
    """
    根据当前文档包含的表格信息构造一个问答链，
    返回一个 chat_chain 函数用于处理输入问题。
    """
    llm = get_llm()
    
    def chat_chain(question):
        # 构造对话上下文，添加系统提示中包含表格信息
        system_msg = SystemMessage(
            content=f"你是一个文档助手，请根据上下文回答。当前文档包含表格：{tables}"
        )
        human_msg = HumanMessage(content=question)
        # 拼接对话内容（简单方式：合并消息内容，每行一条）
        prompt = f"{system_msg.content}\n{human_msg.content}"
        
        # 调用大模型生成回答（使用 litellm 的 generate 接口）
        response = llm.generate(text=prompt)
        return response.strip()
    
    return chat_chain

# 测试代码（仅用于本地调试时使用）
if __name__ == "__main__":
    # 假设当前文档解析后包含一个简单的表格信息
    tables = "<table><tr><td>示例数据</td></tr></table>"
    chat = create_chat_chain(tables)
    answer = chat("请介绍一下文档中的内容")
    print("回答：", answer)