document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prompt-form');
    const input = document.getElementById('prompt-input');
    const responseBox = document.getElementById('response-box');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const prompt = input.value.trim();
        
        if (!prompt) return;
        
        // 清空输入框
        input.value = '';
        
        // 显示用户提问
        responseBox.innerHTML += `<div class="user-prompt">你: ${prompt}</div>`;
        
        // 显示AI正在思考
        const thinkingDiv = document.createElement('div');
        thinkingDiv.className = 'ai-response';
        thinkingDiv.innerHTML = 'AI: <span class="typing-cursor"></span>';
        responseBox.appendChild(thinkingDiv);
        
        // 滚动到底部
        responseBox.scrollTop = responseBox.scrollHeight;
        
        // 创建EventSource连接
        const eventSource = new EventSource(`/ask?prompt=${encodeURIComponent(prompt)}`);
        let aiResponse = '';
        
        eventSource.onmessage = function(e) {
            if (e.data === '[DONE]') {
                eventSource.close();
                // 移除打字光标
                thinkingDiv.querySelector('.typing-cursor').remove();
                return;
            }
            
            // 追加新内容
            aiResponse += e.data;
            thinkingDiv.innerHTML = `AI: ${aiResponse}<span class="typing-cursor"></span>`;
            
            // 滚动到底部
            responseBox.scrollTop = responseBox.scrollHeight;
        };
        
        eventSource.onerror = function() {
            eventSource.close();
            thinkingDiv.innerHTML = `AI: ${aiResponse}`;
        };
    });
});