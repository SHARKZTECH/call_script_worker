import logging
from tools.call_script_generator import generate_call_script
from tools.logger import setup_logger


logger = setup_logger(__name__)


class CallScriptService:
    """Service to generate call scripts using tools.call_script_generator"""

    @staticmethod
    def get_call_script(user_name, call_reason, user_company, job_title, tone="Formal", language="english"):
        """Wrapper method to fetch the call script from the generator."""
        logger.info("📝 Generating call script via service layer...")
        return generate_call_script(user_name=user_name, call_reason=call_reason, user_company=user_company, job_title=job_title, tone=tone, language=language)
