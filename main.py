"""
Social Media Automation - Main Module
الأتمتة لوسائل التواصل الاجتماعي - البرنامج الرئيسي

Author: Abu Hammad
Repository: https://github.com/forany62/social-media-automation
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from utils.logger import setup_logger
from platforms.facebook_publisher import FacebookPublisher
from platforms.youtube_publisher import YouTubePublisher
from platforms.tiktok_publisher import TikTokPublisher
from platforms.instagram_publisher import InstagramPublisher


class SocialMediaAutomation:
    """Main automation class / الفئة الرئيسية للأتمتة"""
    
    def __init__(self):
        """Initialize automation system"""
        self.logger = setup_logger(__name__)
        self.logger.info("=" * 60)
        self.logger.info("Social Media Automation System Starting...")
        self.logger.info("نظام الأتمتة لوسائل التواصل الاجتماعي يبدأ...")
        self.logger.info("=" * 60)
        
        # Display configuration
        Config.display()
        
        # Initialize publishers
        self.facebook = None
        self.youtube = None
        self.tiktok = None
        self.instagram = None
        
        self._initialize_platforms()
    
    def _initialize_platforms(self):
        """Initialize all platform publishers"""
        try:
            if Config.FACEBOOK_ACCESS_TOKEN:
                self.facebook = FacebookPublisher()
                self.logger.info("✓ Facebook Publisher initialized successfully")
        except Exception as e:
            self.logger.error(f"✗ Facebook Publisher initialization failed: {e}")
        
        try:
            self.youtube = YouTubePublisher()
            self.logger.info("✓ YouTube Publisher initialized successfully")
        except Exception as e:
            self.logger.error(f"✗ YouTube Publisher initialization failed: {e}")
        
        try:
            if Config.TIKTOK_ACCESS_TOKEN:
                self.tiktok = TikTokPublisher()
                self.logger.info("✓ TikTok Publisher initialized successfully")
        except Exception as e:
            self.logger.error(f"✗ TikTok Publisher initialization failed: {e}")
        
        try:
            if Config.INSTAGRAM_ACCESS_TOKEN:
                self.instagram = InstagramPublisher()
                self.logger.info("✓ Instagram Publisher initialized successfully")
        except Exception as e:
            self.logger.error(f"✗ Instagram Publisher initialization failed: {e}")
    
    def post_to_facebook(self, message, image_url=None, video_path=None):
        """
        Post to Facebook
        
        Args:
            message (str): Post message
            image_url (str, optional): URL of image to post
            video_path (str, optional): Path to video file
        
        Returns:
            dict: Result with success status and details
        """
        if not self.facebook:
            self.logger.error("Facebook publisher not initialized")
            return {'success': False, 'error': 'Publisher not initialized', 'platform': 'Facebook'}
        
        if video_path:
            return self.facebook.post_video(video_path, message)
        elif image_url:
            return self.facebook.post_image(message, image_url)
        else:
            return self.facebook.post_text(message)
    
    def post_to_youtube(self, video_path, title, description, tags=None, privacy="private"):
        """
        Upload video to YouTube
        
        Args:
            video_path (str): Path to video file
            title (str): Video title
            description (str): Video description
            tags (list, optional): List of tags
            privacy (str): Privacy status (public, private, unlisted)
        
        Returns:
            dict: Result with success status and video ID
        """
        if not self.youtube:
            self.logger.error("YouTube publisher not initialized")
            return {'success': False, 'error': 'Publisher not initialized', 'platform': 'YouTube'}
        
        return self.youtube.upload_video(video_path, title, description, tags, privacy)
    
    def post_to_tiktok(self, video_path, title, privacy_level="PUBLIC_TO_EVERYONE"):
        """
        Post video to TikTok
        
        Args:
            video_path (str): Path to video file
            title (str): Video title/caption
            privacy_level (str): Privacy level (PUBLIC_TO_EVERYONE, MUTUAL_FOLLOW_FRIENDS, SELF_ONLY)
        
        Returns:
            dict: Result with success status and publish ID
        """
        if not self.tiktok:
            self.logger.error("TikTok publisher not initialized")
            return {'success': False, 'error': 'Publisher not initialized', 'platform': 'TikTok'}
        
        return self.tiktok.post_video(video_path, title, privacy_level)
    
    def post_to_instagram(self, image_url=None, video_url=None, caption=""):
        """
        Post to Instagram
        
        Args:
            image_url (str, optional): Public URL of image
            video_url (str, optional): Public URL of video
            caption (str): Post caption
        
        Returns:
            dict: Result with success status and media ID
        """
        if not self.instagram:
            self.logger.error("Instagram publisher not initialized")
            return {'success': False, 'error': 'Publisher not initialized', 'platform': 'Instagram'}
        
        if video_url:
            return self.instagram.post_video(video_url, caption)
        elif image_url:
            return self.instagram.post_image(image_url, caption)
        else:
            self.logger.error("Either image_url or video_url is required for Instagram")
            return {'success': False, 'error': 'No media URL provided', 'platform': 'Instagram'}
    
    def post_to_all(self, content_type, **kwargs):
        """
        Post to all available platforms
        
        Args:
            content_type (str): Type of content ('text', 'image', 'video')
            **kwargs: Platform-specific arguments
                - message: Text message
                - image_url: URL of image
                - video_path: Path to video file
                - title: Video/post title
                - description: Video description
                - caption: Image/video caption
                - tags: List of tags for YouTube
        
        Returns:
            dict: Results from all platforms
        """
        results = {}
        
        self.logger.info(f"\nPosting {content_type} content to all platforms...")
        self.logger.info(f"نشر محتوى {content_type} على جميع المنصات...")
        
        # Facebook
        if content_type == "text" and self.facebook:
            self.logger.info("Publishing to Facebook...")
            results['facebook'] = self.post_to_facebook(kwargs.get('message', ''))
        elif content_type == "image" and self.facebook:
            self.logger.info("Publishing image to Facebook...")
            results['facebook'] = self.post_to_facebook(
                kwargs.get('message', ''),
                image_url=kwargs.get('image_url')
            )
        elif content_type == "video" and self.facebook:
            self.logger.info("Publishing video to Facebook...")
            results['facebook'] = self.post_to_facebook(
                kwargs.get('message', ''),
                video_path=kwargs.get('video_path')
            )
        
        # Instagram
        if content_type == "image" and self.instagram:
            self.logger.info("Publishing image to Instagram...")
            results['instagram'] = self.post_to_instagram(
                image_url=kwargs.get('image_url'),
                caption=kwargs.get('caption', kwargs.get('message', ''))
            )
        elif content_type == "video" and self.instagram:
            self.logger.info("Publishing video to Instagram...")
            results['instagram'] = self.post_to_instagram(
                video_url=kwargs.get('video_url'),
                caption=kwargs.get('caption', kwargs.get('message', ''))
            )
        
        # TikTok (videos only)
        if content_type == "video" and self.tiktok:
            self.logger.info("Publishing video to TikTok...")
            results['tiktok'] = self.post_to_tiktok(
                kwargs.get('video_path'),
                kwargs.get('title', kwargs.get('message', ''))
            )
        
        # YouTube (videos only)
        if content_type == "video" and self.youtube:
            self.logger.info("Uploading video to YouTube...")
            results['youtube'] = self.post_to_youtube(
                kwargs.get('video_path'),
                kwargs.get('title', 'Video'),
                kwargs.get('description', ''),
                kwargs.get('tags', []),
                kwargs.get('privacy', 'private')
            )
        
        # Display summary
        self.logger.info("\n" + "=" * 60)
        self.logger.info("Publication Summary / ملخص النشر:")
        self.logger.info("=" * 60)
        for platform, result in results.items():
            status = "✓ Success" if result.get('success') else "✗ Failed"
            self.logger.info(f"{platform.capitalize()}: {status}")
            if result.get('success'):
                if 'post_id' in result:
                    self.logger.info(f"  Post ID: {result['post_id']}")
                elif 'video_id' in result:
                    self.logger.info(f"  Video ID: {result['video_id']}")
                elif 'media_id' in result:
                    self.logger.info(f"  Media ID: {result['media_id']}")
                elif 'publish_id' in result:
                    self.logger.info(f"  Publish ID: {result['publish_id']}")
            else:
                self.logger.error(f"  Error: {result.get('error', 'Unknown error')}")
        self.logger.info("=" * 60 + "\n")
        
        return results


def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print("🤖 Social Media Automation Tool")
    print("🤖 أداة الأتمتة لوسائل التواصل الاجتماعي")
    print("=" * 60 + "\n")
    
    # Create automation instance
    automation = SocialMediaAutomation()
    
    # Example usage
    print("\n📝 Ready to use!")
    print("📝 جاهز للاستخدام!")
    print("\nExamples:")
    print("  - automation.post_to_facebook('Hello World!')")
    print("  - automation.post_to_youtube('video.mp4', 'Title', 'Description')")
    print("  - automation.post_to_instagram(image_url='https://...', caption='Caption')")
    print("  - automation.post_to_all('text', message='Hello all platforms!')")
    print("\nCheck examples/ folder for more usage examples")
    print("راجع مجلد examples/ لأمثلة استخدام إضافية\n")


if __name__ == "__main__":
    main()
