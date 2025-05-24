"""
Sider AI 提供商实现
负责验证用户凭据的有效性
"""
from typing import Any
import logging

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from utils.sider_api import SiderAPIClient

logger = logging.getLogger(__name__)

class SiderChatProvider(ToolProvider):
    """Sider AI工具提供商"""
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        验证提供商凭据
        
        Args:
            credentials: 包含sider_token和sider_cookie的凭据字典
            
        Raises:
            ToolProviderCredentialValidationError: 当凭据验证失败时抛出
        """
        try:
            # 获取凭据
            token = credentials.get("sider_token")
            cookie = credentials.get("sider_cookie")
            
            # 检查必需的凭据
            if not token:
                raise ToolProviderCredentialValidationError("Sider Token is required")
            
            if not cookie:
                raise ToolProviderCredentialValidationError("Sider Cookie is required")
            
            # 创建API客户端并验证凭据
            logger.info("开始验证Sider AI凭据...")
            client = SiderAPIClient(token=token, cookie=cookie)
            
            # 执行凭据验证
            if not client.validate_credentials():
                raise ToolProviderCredentialValidationError(
                    "Invalid Sider credentials. Please check your token and cookie."
                )
            
            logger.info("Sider AI凭据验证成功")
            
        except ToolProviderCredentialValidationError:
            # 重新抛出已知的验证错误
            raise
        except Exception as e:
            logger.error(f"凭据验证过程中发生错误: {e}")
            raise ToolProviderCredentialValidationError(
                f"Failed to validate Sider credentials: {str(e)}"
            )
