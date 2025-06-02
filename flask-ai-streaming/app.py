from flask import Flask, render_template, request, Response
import time
import random

app = Flask(__name__)

# 模拟AI生成的回答
AI_RESPONSES = [
    "Flask是一个轻量级的Python Web框架，它简单易用但功能强大。",
    "要实现流式输出，可以使用Flask的Response对象结合生成器函数。",
    "SSE(Server-Sent Events)是一种服务器向客户端推送数据的技术。",
    "流式输出可以显著提升用户体验，特别是在处理长时间运行的任务时。",
    "Python的生成器函数非常适合用于实现流式内容输出。"
]

def simulate_ai_thinking(prompt):
    """模拟AI思考过程，生成流式响应"""
    # 随机选择一个回答
    full_response = random.choice(AI_RESPONSES)
    
    # 模拟AI思考延迟
    time.sleep(1)
    
    # 逐字输出回答
    for i in range(len(full_response)):
        chunk = full_response[i]
        
        # 随机添加一些延迟，模拟网络波动
        delay = random.uniform(0.02, 0.1)
        time.sleep(delay)
        
        # 返回当前块
        yield f"data: {chunk}\n\n"
    
    # 最后发送结束标记
    yield "data: [DONE]\n\n"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST','GET'])
def ask_ai():
    prompt = request.form.get('prompt', '')
    print(f"收到提问: {prompt}")
    
    # 返回流式响应
    return Response(
        simulate_ai_thinking(prompt),
        mimetype='text/event-stream'
    )

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5009)