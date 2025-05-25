# Sider AI Chat Plugin

**Author:** xiaochuan886
**Version:** 0.0.1
**Type:** Tool Plugin  

## Description

Sider AI Chat Plugin 是一个强大的AI聊天工具插件，为Dify平台提供流式AI对话功能。该插件支持多种主流AI模型，包括GPT、Claude、Gemini等，并具备上下文管理、流式响应等高级功能。

## Features

### 🤖 多模型支持
- **GPT系列**: GPT-4.1, GPT-4.1 Mini
- **Claude系列**: Claude 4 Sonnet, Claude 4 Opus, Claude 3.5 Haiku
- **Gemini系列**: Gemini 2.5 Flash, Gemini 2.5 Pro
- **O系列**: O3, O4 Mini
- **DeepSeek系列**: DeepSeek Chat, DeepSeek Reasoner, DeepSeek R1 Distill Llama 70B

### 💬 智能对话功能
- **流式响应**: 实时显示AI生成的内容
- **上下文管理**: 支持多轮对话，保持对话连续性
- **思考模式**: 启用AI深度思考模式，获得更详细的推理过程
- **多语言支持**: 支持中文、英文、日文等多种语言输出

### 🔧 高级功能
- **数据分析**: 内置数据分析能力
- **网络搜索**: 可选择启用网络搜索获取最新信息
- **错误处理**: 完善的错误处理和重试机制
- **安全认证**: 支持Token和Cookie双重认证

## Installation

### 1. 获取认证信息
在使用插件前，您需要从 [sider.ai](https://sider.ai) 获取以下认证信息：
- **Sider Token**: 从账户设置中获取
- **Sider Cookie**: 从浏览器开发者工具中获取（登录状态下）

### 2. 安装插件
1. 下载 `sider_chat.difypkg` 插件包
2. 在Dify管理界面进入"插件管理"页面
3. 点击"上传插件"并选择插件包文件
4. 配置认证信息（Sider Token 和 Sider Cookie）

### 3. 使用插件
在Dify应用中添加"Sider AI Chat"工具节点，配置以下参数：
- **prompt** (必需): 发送给AI的消息或问题
- **context_id** (可选): 用于保持对话连续性的上下文ID
- **model** (可选): 选择使用的AI模型，默认为"sider"
- **output_lang** (可选): 输出语言偏好，默认为"auto"
- **thinking_mode** (可选): 是否启用思考模式，默认为false
- **data_analysis** (可选): 是否启用数据分析，默认为true
- **search** (可选): 是否启用网络搜索，默认为false

## Usage Examples

### 基础对话
```yaml
prompt: "请介绍一下人工智能的发展历史"
model: "gpt-4.1"
output_lang: "zh-CN"
```

### 持续对话
```yaml
prompt: "那么AI在未来会如何发展？"
context_id: "previous_conversation_context_id"
model: "claude-4-sonnet"
thinking_mode: true
```

### 数据分析任务
```yaml
prompt: "分析这组销售数据的趋势"
model: "deepseek-reasoner"
data_analysis: true
search: false
```

## Output Variables

插件执行后会返回以下变量，可在后续节点中使用：

- **context_id**: 新的上下文ID，用于继续对话
- **model**: 使用的AI模型名称
- **response**: AI的完整响应内容
- **success**: 执行是否成功
- **prompt_length**: 输入提示词长度
- **response_length**: 响应内容长度

## Configuration

### 环境变量
如需本地调试，请配置以下环境变量：
```bash
DIFY_API_HOST=https://your-dify-host.com
DIFY_API_KEY=your-api-key
```

### 认证配置
在Dify插件管理界面配置：
- **Sider Token**: 您的Sider API令牌
- **Sider Cookie**: 您的Sider会话Cookie

## Troubleshooting

### 常见问题

**Q: 插件安装失败，提示签名验证错误？**  
A: 请确保manifest.yaml和provider配置中的author字段设置为您的GitHub ID，或在Dify的.env文件中添加 `FORCE_VERIFYING_SIGNATURE=false`

**Q: 认证失败？**  
A: 请检查Sider Token和Cookie是否正确，确保在sider.ai网站上处于登录状态

**Q: 响应为空或出错？**  
A: 请检查网络连接，确认Sider服务可用，并查看插件日志获取详细错误信息

## Development

### 本地开发
```bash
# 克隆项目
git clone https://github.com/xiaochuan886/sider_chat.git
cd sider_chat

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（mac/lunix）
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件填入配置

# 启动调试
python -m main
```

### 打包插件
```bash
dify plugin package ./sider_chat
```

## License

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## Contributing

欢迎提交Issue和Pull Request来改进这个插件！

## Support

如有问题或建议，请通过以下方式联系：
- GitHub Issues: [https://github.com/xiaochuan886/sider_chat/issues](https://github.com/xiaochuan886/sider_chat/issues)
- Email: 通过GitHub联系

---

**注意**: 使用本插件需要有效的Sider AI账户和相应的API访问权限。请遵守Sider AI的服务条款和使用政策。



