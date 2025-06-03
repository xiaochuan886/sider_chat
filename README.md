# Sider AI Chat Plugin

**Author:** xiaochuan886 
**Version:** 0.0.1 
**Type:** Tool Plugin

## Description

Sider AI Chat Plugin is a powerful AI chat tool plugin based on the sider_ai_api open-source project code, calling the Sider.ai Python API library. It provides a comprehensive solution for accessing ChatGPT, Gemini, Claude, Llama, and even O1 foreign large language models when unable to access international AI platforms like ChatGPT. It offers streaming AI dialogue functionality for the Dify platform, with features like context management and streaming responses.

## Features

### 🤖 Multi-Model Support
- **GPT Series:** 
  - GPT-4.1
  - GPT-4.1 Mini
- **Claude Series:**
  - Claude 4 Sonnet
  - Claude 4 Opus
- **Gemini Series:**
  - Gemini 2.5 Flash
  - Gemini 2.5 Pro
- **O Series:**
  - O3
  - O4 Mini
- **DeepSeek Series:**
  - DeepSeek Chat
  - DeepSeek Reasoner
  - DeepSeek R1 Distill Llama 70B

### 💬 Intelligent Dialogue Capabilities
- **Streaming Response:** Real-time display of AI-generated content (can be manually disabled)
- **Context Management:** Supports multi-turn conversations, maintaining dialogue continuity
- **Thinking Mode:** Enable AI deep thinking mode to obtain more detailed reasoning processes
- **Multi-Language Support:** Supports output in multiple languages including Chinese, English, Japanese, etc.

### 🔧 Advanced Features
- **Data Analysis:** Built-in data analysis capabilities
- **Web Search:** Optional web search to obtain the latest information
- **Error Handling:** Comprehensive error handling and retry mechanism
- **Secure Authentication:** Supports dual authentication with Token and Cookie

## Installation

### 1. Obtain Authentication Information
Before using the plugin, you need to obtain the following authentication information from sider.ai:
- **Sider Token:** Retrieved from browser developer tools (while logged in)
- **Sider Cookie:** Retrieved from browser developer tools (while logged in)

> **Note:** Token can be viewed in browser settings or developer tools. For Edge, cookies and tokens can be viewed at `edge://settings/cookies/detail?site=sider.ai`

### 2. Install Plugin
1. Download `sider_chat.difypkg` plugin package
2. Go to the "Plugin Management" page in the Dify management interface
3. Click "Upload Plugin" and select the plugin package file
4. Configure authentication information (Sider Token and Sider Cookie)

### 3. Use Plugin
Add "Sider AI Chat" tool node in Dify application, configure the following parameters:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Sider Token | Required | Sider Token | - |
| Sider Cookie | Required | Sider Cookie | - |
| prompt | Required | Message or question sent to AI | - |
| context_id | Optional | Context ID for maintaining conversation continuity | - |
| model | Optional | Select AI model | "sider" |
| output_lang | Optional | Output language preference | "auto" |
| thinking_mode | Optional | Whether to enable thinking mode | false |
| data_analysis | Optional | Whether to enable data analysis | true (currently unavailable) |
| search | Optional | Whether to enable web search | false |

## Usage Examples

### Basic Conversation
- **Prompt:** "Please introduce the development history of artificial intelligence"
- **Model:** "gpt-4.1"
- **Output Language:** "zh-CN"

### Continuous Conversation
- **Prompt:** "How will AI develop in the future?"
- **Context ID:** "previous_conversation_context_id"
- **Model:** "claude-4-sonnet"
- **Thinking Mode:** true

## Output Variables
The plugin will return the following variables:

| Variable | Description |
|----------|-------------|
| context_id | New context ID for continuing the conversation |
| model | Name of the AI model used |
| response | Complete AI response content |
| success | Whether execution was successful |
| prompt_length | Input prompt length |
| response_length | Response content length |

## Configuration

### Environment Variables
For local debugging, configure:
```
DIFY_API_HOST=https://your-dify-host.com
DIFY_API_KEY=your-api-key
```

### Authentication Configuration
Configure in the Dify plugin management interface:
- **Sider Token:** Your Sider API token
- **Sider Cookie:** Your Sider session cookie

## Troubleshooting

### Common Issues

1. **Q: Plugin installation fails with signature verification error?**
   - **A:** Ensure that the author field in `manifest.yaml` and provider configuration is set to your GitHub ID, or add `FORCE_VERIFYING_SIGNATURE=false` in Dify's `.env` file

2. **Q: Authentication failure?**
   - **A:** Check if Sider Token and Cookie are correct, ensure you are logged in on the sider.ai website

3. **Q: Empty or error response?**
   - **A:** Check network connection, confirm Sider service availability, and view plugin logs for detailed error information

## Development

### Local Development
```bash
# Clone project
git clone https://github.com/xiaochuan886/sider_chat.git
cd sider_chat

# Create virtual environment
python -m venv venv

# Activate virtual environment (mac/linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env file to fill in configuration

# Start debugging
python -m main
```

### Package Plugin
```bash
dify plugin package ./sider_chat
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Welcome to submit Issues and Pull Requests to improve this plugin!

## Support
For questions or suggestions, please contact via:
- **GitHub Issues:** https://github.com/xiaochuan886/sider_chat/issues
- **Email:** Contact through GitHub

> **Note:** Using this plugin requires a valid Sider AI account and corresponding API access rights. Please comply with Sider AI's terms of service and usage policies.
