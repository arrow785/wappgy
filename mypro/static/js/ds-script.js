document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('askForm');
    const chatHistory = document.getElementById('chat-history');
    const submitBtn = document.getElementById('submit-btn');

    // 初始化消息ID计数器
    let messageId = 0;

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const input = form.question;
        const question = input.value.trim();
        if (!question) return;

        // 生成唯一消息ID
        const currentMessageId = ++messageId;
        
        try {
            // 添加用户消息
            addMessage(question, 'user', currentMessageId);
            input.value = '';
            toggleSubmitState(true);
            
            // 显示加载状态
            const loadingElement = showLoading(currentMessageId);
            
            // 发送请求
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `question=${encodeURIComponent(question)}`
            });

            if (!response.ok) throw new Error(`HTTP错误! 状态码: ${response.status}`);
            
            const data = await response.json();
            removeLoading(loadingElement);

            if (data.error) {
                addMessage(`错误: ${data.error}`, 'ai', currentMessageId, true);
            } else {
                addMessage(formatResponse(data.answer), 'ai', currentMessageId);
            }
        } catch (error) {
            removeLoading(document.querySelector(`#msg-${currentMessageId} .loading`));
            addMessage(`请求失败: ${error.message}`, 'ai', currentMessageId, true);
        } finally {
            toggleSubmitState(false);
        }
    });

    function formatResponse(text) {
        // 增强的Markdown格式转换
        return text
            // 转义HTML特殊字符
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            // 代码块处理（支持语言标识）
            .replace(/```(\w*)\s*([\s\S]*?)```/g, (_, lang, code) => {
                return `<div class="code-block">${lang ? `<div class="code-lang">${lang}</div>` : ''}<pre><code>${code.trim()}</code></pre></div>`;
            })
            // 有序列表（支持多行）
            .replace(/(\d+\.\s+.*(?:\n\s+.*)*)/g, '<ol class="ai-list">$1</ol>')
            .replace(/(\d+\.)\s+(.*)/g, '<li>$2</li>')
            // 无序列表（支持多级）
            .replace(/(-\s+.*(?:\n\s+.*)*)/g, '<ul class="ai-list">$1</ul>')
            .replace(/-\s+(.*)/g, '<li>$1</li>')
            // 强调文本
            .replace(/\*\*(.*?)\*\*/g, '<strong class="em-text">$1</strong>')
            // 斜体文本
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            // 步骤说明
            .replace(/(步骤\s*\d+:)/g, '<div class="step-block">$1</div>')
            // 链接处理
            .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>')
            // 换行处理
            .replace(/\n/g, '<br>')
            // 清理多余标签
            .replace(/<\/?(ol|ul)>(?=\s*<\/?(ol|ul)>)/g, '');
    }

    function addMessage(content, type, id, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        messageDiv.id = `msg-${id}`;
        
        if (isError) {
            messageDiv.classList.add('error-message');
            messageDiv.innerHTML = `
                <i class="fas fa-exclamation-triangle"></i>
                <div class="error-content">${content}</div>
            `;
        } else {
            messageDiv.innerHTML = (type === 'ai') ? content : content.replace(/</g, '&lt;').replace(/>/g, '&gt;');
        }

        chatHistory.appendChild(messageDiv);
        messageDiv.scrollIntoView({ behavior: 'smooth' });
    }

    function showLoading(id) {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message loading';
        loadingDiv.id = `msg-${id}`;
        loadingDiv.innerHTML = `
            <div class="loading-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        `;
        chatHistory.appendChild(loadingDiv);
        return loadingDiv;
    }

    function removeLoading(element) {
        if (element && element.parentNode) {
            element.parentNode.removeChild(element);
        }
    }

    function toggleSubmitState(disabled) {
        submitBtn.disabled = disabled;
        submitBtn.innerHTML = disabled 
            ? '<i class="fas fa-spinner fa-spin"></i> 处理中...'
            : '<i class="fas fa-paper-plane"></i> 发送';
    }
});