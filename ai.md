### ollama
* Browse models: https://ollama.com/library
```shell
# as root 😅
curl -fsSL https://ollama.com/install.sh | sh

ollama pull deepseek-coder:1.3b-base
ollama list
# remotely
curl http://192.168.1.100:11434/api/tags | jq
ollama rm deepseek-coder:1.3b-base

# 1b 7b etc. is the number of (billions of) parameters in the model
# View this number for a downloaded model
ollama show deepseek-coder
curl http://192.168.1.100:11434/api/show -d '{
  "name": "deepseek-coder:latest"
}' | jq '.details'
```
