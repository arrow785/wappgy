class Config:
    DEEPSEEK_API_KEY = "sk-709b1426f00d42c880e1db9b43b22a3c"
    DEEPSEEK_API_URL = r"https://api.deepseek.com/v1/chat/completions"


C = Config()
print(C.DEEPSEEK_API_KEY)
print(C.DEEPSEEK_API_URL)
