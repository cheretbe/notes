### ollama
* Browse models: https://ollama.com/library
* https://github.com/ollama/ollama/blob/main/docs/api.md
* Difference between between /api/generate and /api/chat: https://github.com/ollama/ollama/issues/2774
```shell
# as root 😅
# [!!] check if it causes duplicate deb entries in /etc/apt/sources.list.d/contrib.list
#      https://github.com/ollama/ollama/issues/6923
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

# Benchmarking CPU usage
# View the number of cores available
nproc
# gpt-oss:20b always uses thinking mode
# https://github.com/ollama/ollama/issues/11751
# Compare response time by changing "num_thread" option
curl http://192.168.1.100:11434/api/generate -d '
{  
"model": "deepseek-r1:1.5b",  
"prompt": "Why is the blue sky blue?",  
"stream": false,
"think": false,
"keep_alive": 0,
"options":{
  "temperature": 0,
  "system": "You are a bored assistant. Provide short answers.",
  "num_thread": 20
}
}' | jq 'del(.context)'
```
### Continue plugin
Minimal working config for VSCode (~/.continue/config.yaml)
```yaml
name: Local Agent
version: 1.0.0
schema: v1
models:
  - name: Autodetect
    provider: ollama
    apiBase: "http://192.168.1.100:11434"
    model: AUTODETECT
roles:
  - chat
  - edit
  - apply

context:
  - provider: code
  - provider: docs
  - provider: diff
  - provider: terminal
  - provider: problems
  - provider: folder
  - provider: codebase
```
### Deepseek
* API: https://api-docs.deepseek.com/
* https://platform.deepseek.com/api_keys
