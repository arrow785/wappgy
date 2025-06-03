document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('askForm');
    const chatHistory = document.getElementById('chat-history');
    const submitBtn = document.getElementById('submit-btn');
    const saveSettingsBtn = document.getElementById('saveSettings_');
    const resetSettingsBtn = document.getElementById('resetSettings');
    const tips = document.getElementById('tips');
    const modelSelect = document.getElementById('modelSelect');
    const anwer = document.getElementById('answer');
    // 初始化消息ID计数器
    let messageId = 0;

    let DEEPSEEK_SYSTEM_INIT = `
    你是一个有趣的AI助手，擅长日常问题的回答
    
    `
    saveSettingsBtn.addEventListener('click', function () {
        const x = document.querySelector('#ai-persona').value
        if (!x) {
            tips.innerHTML = `<i class="fas fa-exclamation-triangle"></i> 请输入AI助手的个性化设定！`;
            return;
        }
        DEEPSEEK_SYSTEM_INIT = x;
        console.log(modelSelect.value);

        tips.innerHTML = `<i class="fas fa-check-circle"></i> 设置已保存！`;
    })
    resetSettingsBtn.addEventListener('click', function () {
        DEEPSEEK_SYSTEM_INIT = `你是一个有趣的AI助手，擅长日常问题的回答。`
        document.querySelector('#ai-persona').value = DEEPSEEK_SYSTEM_INIT;
        tips.innerHTML = `<i class="fas fa-check-circle"></i> 设置已重置！`;
    })

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const input = form.question;
        const question = input.value.trim();
        if (!question) return;
        let htmlx = ''
        // 生成唯一消息ID
        const currentMessageId = ++messageId;

        try {
            // 添加用户消息
            addMessage(question, 'user', currentMessageId);
            input.value = '';
            toggleSubmitState(true);

            // 显示加载状态
            const loadingElement = showLoading(currentMessageId);
            console.log(`用户设定为：${DEEPSEEK_SYSTEM_INIT}`);

            removeLoading(loadingElement);
            anwer.style.display = 'block';
            const event_s = new EventSource(`/ask?id=${currentMessageId}$sys_init=${encodeURIComponent(DEEPSEEK_SYSTEM_INIT)}&model=${encodeURIComponent(modelSelect.value)}&q=${encodeURIComponent(question)}`)
            event_s.onmessage = function (e) {
                if (e.data === '[END]') {
                    event_s.close()
                } else {
                    htmlx += e.data
                    addMessage(formatResponse(htmlx), 'ai', currentMessageId, false)
                }
            }
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