"""
Facebook Publisher Module
مودول نشر المحتوى على فيسبوك

Uses Facebook Graph API to post content
"""

import requests
from config import Config
from utils.logger import setup_logger


class FacebookPublisher:
    """Facebook content publisher / ناشر محتوى فيسبوك"""
    
    def __init__(self):
        """Initialize Facebook publisher"""
        self.logger = setup_logger(__name__)
        self.access_token = Config.FACEBOOK_ACCESS_TOKEN
        self.page_id = Config.FACEBOOK_PAGE_ID
        self.graph_url = "https://graph.facebook.com/v18.0"
        
        if not self.access_token or not self.page_id:
            raise ValueError("Facebook credentials are missing in configuration")
        
        self.logger.info("Facebook Publisher initialized successfully")
    
    def post_text(self, message):
        """
        Post text message to Facebook page
        نشر رسالة نصية على صفحة فيسبوك
        
        Args:
            message (str): Text message to post
        
        Returns:
            dict: Response from Facebook API
        """
        self.logger.info(f"Posting text to Facebook: {message[:50]}...")
        
        url = f"{self.graph_url}/{self.page_id}/feed"
        payload = {
            'message': message,
            'access_token': self.access_token
        }
        
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            data = response.json()
            
            if 'id' in data:
                self.logger.info(f"✓ Facebook post created successfully: {data['id']}")
                return {'success': True, 'post_id': data['id'], 'platform': 'Facebook'}
            else:
                self.logger.error(f"✗ Facebook post failed: {data}")
                return {'success': False, 'error': data, 'platform': 'Facebook'}
        
        except requests.exceptions.RequestException as e:
            self.logger.error(f"✗ Facebook API request failed: {e}")
            return {'success': False, 'error': str(e), 'platform': 'Facebook'}
    
    def post_image(self, message, image_url):
        """
        Post image with caption to Facebook page
        نشر صورة مع نص على صفحة فيسبوك
        
        Args:
            message (str): Image caption
            image_url (str): URL of image to post
        
        Returns:
            dict: Response from Facebook API
        """
        self.logger.info(f"Posting image to Facebook: {image_url}")
        
        url = f"{self.graph_url}/{self.page_id}/photos"
        payload = {
            'message': message,
            'url': image_url,
            'access_token': self.access_token
        }
        
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            data = response.json()
            
            if 'id' in data:
                post_id = data.get('post_id', data['id'])
                self.logger.info(f"✓ Facebook image posted successfully: {post_id}")
                return {'success': True, 'post_id': post_id, 'platform': 'Facebook'}
            else:
                self.logger.error(f"✗ Facebook image post failed: {data}")
                return {'success': False, 'error': data, 'platform': 'Facebook'}
        
        except requests.exceptions.RequestException as e:
            self.logger.error(f"✗ Facebook API request failed: {e}")
            return {'success': False, 'error': str(e), 'platform': 'Facebook'}
    
    def post_video(self, video_path, description=""):
        """
        Post video to Facebook page
        نشر فيديو على صفحة فيسبوك
        
        Args:
            video_path (str): Path to video file
            description (str): Video description
        
        Returns:
            dict: Response from Facebook API
        """
        self.logger.info(f"Posting video to Facebook: {video_path}")
        
        url = f"{self.graph_url}/{self.page_id}/videos"
        
        try:
            with open(video_path, 'rb') as video_file:
                files = {'source': video_file}
                data = {
                    'description': description,
                    'access_token': self.access_token
                }
                
                response = requests.post(url, files=files, data=data)
                response.raise_for_status()
                result = response.json()
                
                if 'id' in result:
                    self.logger.info(f"✓ Facebook video uploaded successfully: {result['id']}")
                    return {'success': True, 'video_id': result['id'], 'platform': 'Facebook'}
                else:
                    self.logger.error(f"✗ Facebook video upload failed: {result}")
                    return {'success': False, 'error': result, 'platform': 'Facebook'}
        
        except FileNotFoundError:
            self.logger.error(f"✗ Video file not found: {video_path}")
            return {'success': False, 'error': 'File not found', 'platform': 'Facebook'}
        except requests.exceptions.RequestException as e:
            self.logger.error(f"✗ Facebook API request failed: {e}")
            return {'success': False, 'error': str(e), 'platform': 'Facebook'}
