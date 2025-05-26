"""
Sider AI 聊天工具实现
提供流式AI聊天功能，支持上下文管理和多种AI模型
"""
from collections.abc import Generator
from typing import Any
import logging
import json

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from utils.sider_api import SiderAPIClient, ChatRequest, ChatOptions

logger = logging.getLogger(__name__)

class SiderChatTool(Tool):
    """Sider AI聊天工具"""
    
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        """
        执行聊天工具调用
        
        Args:
            tool_parameters: 工具参数字典
            
        Yields:
            ToolInvokeMessage: 工具调用消息
        """
        try:
            # 获取工具参数
            prompt = tool_parameters.get("prompt", "")
            context_id = tool_parameters.get("context_id", "")
            model = tool_parameters.get("model", "sider")
            output_lang = tool_parameters.get("output_lang", "auto")
            thinking_mode = tool_parameters.get("thinking_mode", False)
            streaming = tool_parameters.get("streaming", True)
            data_analysis = tool_parameters.get("data_analysis", True)
            search = tool_parameters.get("search", False)
            
            # 验证必需参数
            if not prompt:
                yield self.create_text_message("错误：prompt参数不能为空")
                return
            
            # 从工具参数获取认证信息
            token = tool_parameters.get("sider_token")
            cookie = tool_parameters.get("sider_cookie")
            
            if not token or not cookie:
                yield self.create_text_message("错误：缺少Sider认证信息（token和cookie）")
                return
            
            # 创建API客户端
            client = SiderAPIClient(token=token, cookie=cookie)
            
            # 处理output_lang参数
            processed_output_lang = None if output_lang == "auto" else output_lang
            
            # 构建聊天选项
            options = ChatOptions(
                output_lang=processed_output_lang,
                thinking_mode=thinking_mode,
                data_analysis=data_analysis,
                search=search,
                text_to_image=False,  # 暂不支持图像生成
                artifact=True
            )
            
            # 构建聊天请求
            chat_request = ChatRequest(
                prompt=prompt,
                model=model,
                context_id=context_id,
                options=options
            )
            
            logger.info(f"开始Sider AI聊天: model={model}, prompt长度={len(prompt)}, context_id='{context_id}'")
            
            # 执行聊天并流式返回结果
            accumulated_response = ""
            final_context_id = ""
            
            # 获取聊天响应生成器
            chat_generator = client.chat(chat_request, streaming=streaming)
            
            try:
                # 流式处理响应
                for chunk in chat_generator:
                    if chunk:
                        accumulated_response += chunk
                        # 根据streaming参数决定是否发送流式文本消息
                        if streaming:
                            yield self.create_text_message(chunk)
                
                # 获取最终响应对象
                final_response = next(chat_generator, None)
                if final_response:
                    final_context_id = final_response.context_id
                    
                    # 如果有错误，报告错误
                    if not final_response.success:
                        error_msg = f"Sider API错误: {final_response.error}"
                        logger.error(error_msg)
                        yield self.create_text_message(f"\n\n{error_msg}")
                        return
                else:
                    # 如果没有最终响应对象，从客户端获取context_id
                    final_context_id = client.get_last_context_id()
                
            except StopIteration:
                # 生成器正常结束
                final_context_id = client.get_last_context_id()
            
            # 如果没有启用流式输出，在这里一次性输出完整响应
            if not streaming and accumulated_response:
                yield self.create_text_message(accumulated_response)
            
            # 发送完成提示
            yield self.create_text_message(f"\n\n")
            
            # 构建结果数据 - 使用标准的JSON格式输出
            result_data = {
                "context_id": final_context_id,
                "model": model,
                "response": accumulated_response,
                "success": True,
                "prompt_length": len(prompt),
                "response_length": len(accumulated_response),
                "output_lang": output_lang,
                "thinking_mode": thinking_mode,
                "streaming": streaming,
                "data_analysis": data_analysis,
                "search": search
            }
            
            # 发送JSON结果消息 - 这是标准的Dify输出方式
            yield self.create_json_message(result_data)
            
            logger.info(f"Sider AI聊天完成: 响应长度={len(accumulated_response)}, 新context_id='{final_context_id}'")
            
        except Exception as e:
            error_msg = f"Sider AI聊天工具执行失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            
            # 发送错误消息
            yield self.create_text_message(error_msg)
            
            # 发送错误结果
            error_data = {
                "success": False,
                "error": str(e),
                "context_id": context_id,  # 返回原始context_id
                "model": tool_parameters.get("model", "sider"),
                "response": "",
                "prompt_length": len(prompt) if prompt else 0,
                "response_length": 0
            }
            yield self.create_json_message(error_data)
