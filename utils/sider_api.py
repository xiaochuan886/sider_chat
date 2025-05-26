"""
Sider AI API核心逻辑
复用现有项目的API调用、错误处理和重试机制
"""
import logging
from typing import Generator, Optional, Dict, Any
from dataclasses import dataclass

# 导入内部的Session实现
from .sider_session import Session

logger = logging.getLogger(__name__)

@dataclass
class ChatOptions:
    """聊天选项配置"""
    output_lang: Optional[str] = None
    thinking_mode: bool = False
    data_analysis: bool = True
    search: bool = False
    text_to_image: bool = False
    artifact: bool = True

@dataclass
class ChatRequest:
    """聊天请求数据结构"""
    prompt: str
    model: str = "gpt-4o-mini"
    context_id: str = ""
    options: ChatOptions = None
    
    def __post_init__(self):
        if self.options is None:
            self.options = ChatOptions()

@dataclass
class ChatResponse:
    """聊天响应数据结构"""
    response: str
    context_id: str
    model: str
    success: bool = True
    error: Optional[str] = None

class SiderAPIClient:
    """Sider AI API客户端"""
    
    def __init__(self, token: str, cookie: str):
        """
        初始化API客户端
        
        Args:
            token: Sider认证令牌
            cookie: Sider认证Cookie
        """
        self.token = token
        self.cookie = cookie
        self._last_session: Optional[Session] = None
    
    def _create_session(self, context_id: str = "") -> Session:
        """
        创建新的会话实例
        
        Args:
            context_id: 对话上下文ID
            
        Returns:
            Session: 会话实例
        """
        try:
            session = Session(
                token=self.token,
                cookie=self.cookie,
                context_id=context_id,
                update_info_at_init=False
            )
            logger.debug(f"创建会话: context_id='{context_id}'")
            return session
        except Exception as e:
            logger.error(f"创建会话失败: {e}")
            raise
    
    def _is_error_message(self, chunk: str) -> bool:
        """
        检查响应块是否为错误消息
        
        Args:
            chunk: 响应文本块
            
        Returns:
            bool: 是否为错误消息
        """
        error_patterns = [
            "<Message:",
            "Code:",
            "invalid conversation id",
            "Error:",
            "Failed to",
            "Unable to"
        ]
        return any(pattern in chunk for pattern in error_patterns)
    
    def chat(self, request: ChatRequest, streaming: bool = True) -> Generator[str, None, ChatResponse]:
        """
        执行聊天请求
        
        Args:
            request: 聊天请求对象
            streaming: 是否启用流式输出
            
        Yields:
            str: 响应文本块
            
        Returns:
            ChatResponse: 最终响应对象
        """
        # 创建会话实例
        session = self._create_session(request.context_id or "")
        self._last_session = session
        
        try:
            # 构建API调用参数
            api_params = {
                'prompt': request.prompt,
                'model': request.model,
                'stream': streaming,  # 根据参数决定是否使用流式输出
                'output_lang': request.options.output_lang,
                'thinking_mode': request.options.thinking_mode,
                'data_analysis': request.options.data_analysis,
                'search': request.options.search,
                'text_to_image': request.options.text_to_image,
                'artifact': request.options.artifact
            }
            
            logger.info(f"调用Sider API: model={request.model}, prompt长度={len(request.prompt)}, context_id='{session.context_id}', streaming={streaming}")
            
            # 调用API并生成响应
            response_chunks = []
            error_detected = False
            
            # 如果是非流式模式，先收集所有响应
            if not streaming:
                for chunk in session.chat(**api_params):
                    # 检查是否为错误消息
                    if self._is_error_message(chunk):
                        logger.warning(f"检测到错误消息: {chunk}")
                        error_detected = True
                        
                        # 如果是对话ID错误，创建新会话并重试
                        if "invalid conversation id" in chunk or "Code: 605" in chunk:
                            logger.info("检测到无效对话ID，创建新会话并重试...")
                            # 创建新的会话实例，开始新对话
                            session = self._create_session("")
                            self._last_session = session
                            
                            # 重新调用API
                            logger.info("重新调用Sider API...")
                            response_chunks = []  # 清空之前的响应
                            for retry_chunk in session.chat(**api_params):
                                if not self._is_error_message(retry_chunk):
                                    response_chunks.append(retry_chunk)
                                else:
                                    logger.error(f"重试后仍然出现错误: {retry_chunk}")
                                    raise Exception(f"Sider API错误: {retry_chunk}")
                            break
                        else:
                            # 其他错误直接抛出异常
                            raise Exception(f"Sider API错误: {chunk}")
                    else:
                        # 正常的响应内容
                        response_chunks.append(chunk)
                
                # 非流式模式：一次性yield完整响应
                if response_chunks:
                    full_response = "".join(response_chunks)
                    yield full_response
            else:
                # 流式模式：逐块yield响应
                for chunk in session.chat(**api_params):
                    # 检查是否为错误消息
                    if self._is_error_message(chunk):
                        logger.warning(f"检测到错误消息: {chunk}")
                        error_detected = True
                        
                        # 如果是对话ID错误，创建新会话并重试
                        if "invalid conversation id" in chunk or "Code: 605" in chunk:
                            logger.info("检测到无效对话ID，创建新会话并重试...")
                            # 创建新的会话实例，开始新对话
                            session = self._create_session("")
                            self._last_session = session
                            
                            # 重新调用API
                            logger.info("重新调用Sider API...")
                            for retry_chunk in session.chat(**api_params):
                                if not self._is_error_message(retry_chunk):
                                    response_chunks.append(retry_chunk)
                                    yield retry_chunk
                                else:
                                    logger.error(f"重试后仍然出现错误: {retry_chunk}")
                                    raise Exception(f"Sider API错误: {retry_chunk}")
                            break
                        else:
                            # 其他错误直接抛出异常
                            raise Exception(f"Sider API错误: {chunk}")
                    else:
                        # 正常的响应内容
                        response_chunks.append(chunk)
                        yield chunk
            
            if not response_chunks and not error_detected:
                raise Exception("未收到任何响应内容")
            
            # 返回最终响应
            full_response = "".join(response_chunks)
            return ChatResponse(
                response=full_response,
                context_id=session.context_id,
                model=request.model,
                success=True
            )
                
        except Exception as e:
            logger.error(f"Sider API调用失败: {e}")
            return ChatResponse(
                response="",
                context_id=session.context_id if session else "",
                model=request.model,
                success=False,
                error=str(e)
            )
    
    def get_last_context_id(self) -> str:
        """
        获取最后使用的上下文ID
        
        Returns:
            str: 上下文ID
        """
        if self._last_session:
            return self._last_session.context_id
        return ""
    
    def validate_credentials(self) -> bool:
        """
        验证凭据有效性
        
        Returns:
            bool: 凭据是否有效
        """
        try:
            # 创建测试会话
            test_session = self._create_session("")
            
            # 执行简单的测试请求
            test_request = ChatRequest(
                prompt="Hello",
                model="gpt-4o-mini",
                options=ChatOptions()
            )
            
            # 尝试获取第一个响应块
            for chunk in self.chat(test_request):
                if chunk and not self._is_error_message(chunk):
                    logger.info("凭据验证成功")
                    return True
                break
            
            logger.warning("凭据验证失败：未收到有效响应")
            return False
            
        except Exception as e:
            logger.error(f"凭据验证失败: {e}")
            return False 