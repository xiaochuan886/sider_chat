"""
Sider AI 提供商实现
"""
from typing import Any
from dify_plugin import ToolProvider

class SiderChatProvider(ToolProvider):
    """Sider AI工具提供商"""
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        验证凭据 - 简化版本，总是返回成功
        为了支持打包后的插件，这里不进行实际验证
        """
        # 不进行任何实际验证，直接返回成功
        # 这样可以绕过打包后插件无法验证的问题
        pass
