"""
Configuration Module for Social Media Automation
مودول الإعدادات لأتمتة وسائل التواصل الاجتماعي
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables / تحميل المتغيرات البيئية
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Main configuration class"""
    
    # Facebook Configuration
    FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
    FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')
    
    # YouTube Configuration
    YOUTUBE_CLIENT_SECRETS_FILE = os.getenv('YOUTUBE_CLIENT_SECRETS_FILE', 'client_secrets.json')
    YOUTUBE_CREDENTIALS_PICKLE = os.getenv('YOUTUBE_CREDENTIALS_PICKLE', 'youtube_credentials.pickle')
    
    # TikTok Configuration
    TIKTOK_ACCESS_TOKEN = os.getenv('TIKTOK_ACCESS_TOKEN')
    
    # Instagram Configuration
    INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    INSTAGRAM_ACCOUNT_ID = os.getenv('INSTAGRAM_ACCOUNT_ID')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/automation.log')
    
    # Scheduler Configuration
    ENABLE_SCHEDULER = os.getenv('ENABLE_SCHEDULER', 'False').lower() == 'true'
    TIMEZONE = os.getenv('TIMEZONE', 'Africa/Cairo')
    
    @classmethod
    def validate(cls):
        """Validate configuration / التحقق من صحة الإعدادات"""
        errors = []
        
        if not cls.FACEBOOK_ACCESS_TOKEN:
            errors.append("Facebook Access Token is missing")
        if not cls.FACEBOOK_PAGE_ID:
            errors.append("Facebook Page ID is missing")
        if not cls.TIKTOK_ACCESS_TOKEN:
            errors.append("TikTok Access Token is missing")
        if not cls.INSTAGRAM_ACCESS_TOKEN:
            errors.append("Instagram Access Token is missing")
        if not cls.INSTAGRAM_ACCOUNT_ID:
            errors.append("Instagram Account ID is missing")
            
        if errors:
            print("⚠️  Configuration Warnings:")
            for error in errors:
                print(f"   - {error}")
        
        return len(errors) == 0
    
    @classmethod
    def display(cls):
        """Display current configuration (safely) / عرض الإعدادات الحالية"""
        print("\n🔧 Current Configuration:")
        print(f"   Facebook: {'✓ Configured' if cls.FACEBOOK_ACCESS_TOKEN else '✗ Missing'}")
        print(f"   YouTube: {'✓ Configured' if os.path.exists(cls.YOUTUBE_CLIENT_SECRETS_FILE) else '✗ Missing'}")
        print(f"   TikTok: {'✓ Configured' if cls.TIKTOK_ACCESS_TOKEN else '✗ Missing'}")
        print(f"   Instagram: {'✓ Configured' if cls.INSTAGRAM_ACCESS_TOKEN else '✗ Missing'}")
        print(f"   Scheduler: {'✓ Enabled' if cls.ENABLE_SCHEDULER else '✗ Disabled'}")
        print(f"   Timezone: {cls.TIMEZONE}")
        print()
