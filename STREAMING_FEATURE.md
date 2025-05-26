# Sider Chat 流式输出开关功能

## 功能概述

为 Sider Chat 工具添加了流式输出开关功能，允许用户控制是否启用实时流式响应显示。

## 新增参数

### `streaming` 参数

- **类型**: `boolean`
- **必需**: `false`
- **默认值**: `true`
- **描述**: 控制是否启用流式输出

#### 多语言标签
- **英文**: Streaming Output
- **中文**: 流式输出
- **葡萄牙语**: Saída em Streaming
- **日语**: ストリーミング出力

#### 多语言描述
- **英文**: Enable streaming output for real-time response display
- **中文**: 启用流式输出以实时显示响应
- **葡萄牙语**: Ativar saída em streaming para exibição de resposta em tempo real
- **日语**: リアルタイム応答表示のためのストリーミング出力を有効にする

## 功能行为

### 启用流式输出 (`streaming: true`)
- AI 响应会实时逐块显示
- 用户可以看到响应的生成过程
- 提供更好的交互体验
- 适合长文本响应

### 禁用流式输出 (`streaming: false`)
- AI 响应会在完全生成后一次性显示
- 减少网络请求频率
- 适合需要完整响应的场景
- 可能会有较长的等待时间

## 实现细节

### YAML 配置更新
- 在 `tools/sider_chat.yaml` 中添加了 `streaming` 参数定义
- 在输出变量中添加了 `streaming` 状态信息

### Python 实现更新
- 在 `tools/sider_chat.py` 中添加了流式输出控制逻辑
- 在 `utils/sider_api.py` 中更新了 API 调用方法以支持流式开关
- 根据 `streaming` 参数决定响应的输出方式

### 输出变量
新增输出变量 `streaming`，用于记录本次调用是否启用了流式输出。

## 使用示例

### 启用流式输出
```yaml
parameters:
  prompt: "请介绍一下人工智能的发展历史"
  model: "gpt-4.1"
  streaming: true
```

### 禁用流式输出
```yaml
parameters:
  prompt: "请介绍一下人工智能的发展历史"
  model: "gpt-4.1"
  streaming: false
```

## 兼容性

- 该功能向后兼容，默认启用流式输出
- 现有的工作流程无需修改即可继续使用
- 新的工作流程可以根据需要选择是否启用流式输出

## 测试

可以使用 `test_streaming.py` 脚本来测试流式输出开关功能：

```bash
python test_streaming.py
```

该脚本会分别测试启用和禁用流式输出的情况，并显示相应的输出行为差异。 