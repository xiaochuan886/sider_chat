#!/usr/bin/env python3
"""
测试流式输出开关功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.sider_chat import SiderChatTool
from dify_plugin.entities.tool import ToolInvokeMessage

def test_streaming_functionality():
    """测试流式输出功能"""
    
    # 模拟工具参数
    test_params_streaming = {
        "prompt": "请简单介绍一下Python编程语言",
        "model": "sider",
        "streaming": True,  # 启用流式输出
        "sider_token": "test_token",
        "sider_cookie": "test_cookie"
    }
    
    test_params_non_streaming = {
        "prompt": "请简单介绍一下Python编程语言", 
        "model": "sider",
        "streaming": False,  # 禁用流式输出
        "sider_token": "test_token",
        "sider_cookie": "test_cookie"
    }
    
    tool = SiderChatTool()
    
    print("=== 测试流式输出模式 (streaming=True) ===")
    try:
        messages = list(tool._invoke(test_params_streaming))
        print(f"收到 {len(messages)} 条消息")
        for i, msg in enumerate(messages):
            print(f"消息 {i+1}: {type(msg).__name__}")
            if hasattr(msg, 'message'):
                print(f"  内容: {msg.message[:100]}...")
    except Exception as e:
        print(f"流式模式测试失败: {e}")
    
    print("\n=== 测试非流式输出模式 (streaming=False) ===")
    try:
        messages = list(tool._invoke(test_params_non_streaming))
        print(f"收到 {len(messages)} 条消息")
        for i, msg in enumerate(messages):
            print(f"消息 {i+1}: {type(msg).__name__}")
            if hasattr(msg, 'message'):
                print(f"  内容: {msg.message[:100]}...")
    except Exception as e:
        print(f"非流式模式测试失败: {e}")

if __name__ == "__main__":
    test_streaming_functionality() 