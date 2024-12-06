# xmlrpc_handler/tools/config.py
import os
from dotenv import load_dotenv


class XMLRPCConfig:
    def __init__(self):
        # Load .env file
        load_dotenv()

        # Get credentials from environment
        self.url = os.getenv('ODOO_URL', '').rstrip('/')
        self.db = os.getenv('ODOO_DB')
        self.username = os.getenv('ODOO_USERNAME')
        self.api_key = os.getenv('ODOO_API_KEY')

    def get_connection_params(self):
        return {
            'url': self.url,
            'db': self.db,
            'username': self.username,
            'api_key': self.api_key
        }

    def validate_config(self):
        """Validate that all required credentials are present"""
        missing = []
        if not self.url:
            missing.append('ODOO_URL')
        if not self.db:
            missing.append('ODOO_DB')
        if not self.username:
            missing.append('ODOO_USERNAME')
        if not self.api_key:
            missing.append('ODOO_API_KEY')

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")