import os
import random
import schedule
import time
import logging
from pathlib import Path
from instagrapi import Client
from instagrapi.story import StoryBuilder
from instagrapi.exceptions import LoginRequired, ChallengeRequired, PleaseWaitFewMinutes
from dotenv import load_dotenv

load_dotenv()
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class InstagramStoryBot:
    """
    Simple Instagram Story bot using instagrapi.
    Posts random videos and images to stories on schedule.
    
    WARNING: This uses an unofficial API and may violate Instagram's TOS.
    Use at your own risk. Accounts may be flagged or banned.
    """
    
    def __init__(self):
        self.username = os.getenv("IG_USERNAME")
        self.password = os.getenv("IG_PASSWORD")
        self.session_file = "session.json"

        # Media folders
        self.video_folder = Path("videos")
        self.pic_folder = Path("pics")
        
        # Create folders if they don't exist
        self.video_folder.mkdir(exist_ok=True)
        self.pic_folder.mkdir(exist_ok=True)
        
        if not self.username or not self.password:
            raise ValueError("IG_USERNAME and IG_PASSWORD must be set in environment")
        
        self.client = Client()
        self.setup_client()
    
    def setup_client(self):
        """Configure client settings for better reliability"""
        # Set delay between requests to appear more human
        self.client.delay_range = [1, 3]
        
        # Load session if exists (avoids repeated logins)
        if os.path.exists(self.session_file):
            try:
                logger.info("Loading existing session...")
                self.client.load_settings(self.session_file)
                self.client.login(self.username, self.password)
                logger.info("✅ Logged in using saved session")
                return
            except Exception as e:
                logger.warning(f"Failed to load session: {e}")
                logger.info("Will create new session...")
    
    def login(self):
        """
        Login to Instagram with error handling
        """
        try:
            logger.info(f"Logging in as {self.username}...")
            self.client.login(self.username, self.password)
            
            # Save session for future use
            self.client.dump_settings(self.session_file)
            logger.info("✅ Successfully logged in and saved session")
            return True
            
        except ChallengeRequired as e:
            logger.error("❌ Instagram security challenge required!")
            logger.error("You need to verify your account through the Instagram app")
            logger.error("Tip: Login manually on your phone, then try again")
            raise
            
        except PleaseWaitFewMinutes as e:
            logger.error("❌ Rate limited by Instagram")
            logger.error("Please wait a few minutes before trying again")
            raise
            
        except LoginRequired as e:
            logger.error("❌ Login failed - check username/password")
            raise
            
        except Exception as e:
            print(e)
            logger.error(f"❌ Unexpected login error: {e}")
            raise
    
    def get_random_media(self, folder, extensions):
        """Get random media file from folder"""
        files = [f for f in folder.iterdir() if f.suffix.lower() in extensions]
        if not files:
            return None
        return random.choice(files)
    
    def post_video_story(self):
        """Upload random video to story"""
        video_extensions = ['.mp4', '.mov', '.avi']
        video_path = self.get_random_media(self.video_folder, video_extensions)
        
        if not video_path:
            logger.warning("⚠️ No videos found in videos/ folder")
            return False
        
        try:
            logger.info(f"Uploading video: {video_path.name}")
            self.client.video_upload_to_story(video_path, caption="testing")
            logger.info(f"✅ Video uploaded successfully: {video_path.name}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to upload video: {e}")
            return False
    
    def post_image_story(self):
        """Upload random image to story"""
        image_extensions = ['.jpg', '.jpeg', '.png']
        image_path = self.get_random_media(self.pic_folder, image_extensions)
        
        if not image_path:
            logger.warning("⚠️ No images found in pics/ folder")
            return False
        
        try:
            logger.info(f"Uploading image: {image_path.name}")
            res = self.client.photo_upload_to_story(str(image_path), caption="testing image" )
            print(res, res.id)
            logger.info(f"✅ Image uploaded successfully: {image_path.name}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to upload image: {e}")
            return False
    
    def post_story(self):
        """Main function to post stories (video and/or image)"""
        logger.info("=" * 60)
        logger.info("🎬 Starting story posting job...")
        logger.info("=" * 60)
        
        try:
            # Ensure we're logged in
            if not self.client.user_id:
                logger.info("Session expired, re-logging in...")
                self.login()
            
            # Post video
            video_success = self.post_video_story()
            
            # Wait between posts to appear more human
            if video_success:
                wait_time = random.randint(5, 15)
                logger.info(f"⏳ Waiting {wait_time}s before posting image...")
                time.sleep(wait_time)
            
            # Post image
            image_success = self.post_image_story()
            
            # Summary
            logger.info("-" * 60)
            if video_success or image_success:
                logger.info("✅ Story posting completed successfully!")
            else:
                logger.warning("⚠️ No stories were posted (check media folders)")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"❌ Error during story posting: {e}")
            logger.info("Will retry at next scheduled time...")
    
    def check_media_folders(self):
        """Check if media folders have content"""
        videos = list(self.video_folder.glob('*.[mM][pP]4')) + \
                 list(self.video_folder.glob('*.[mM][oO][vV]'))
        images = list(self.pic_folder.glob('*.[jJ][pP][gG]')) + \
                 list(self.pic_folder.glob('*.[jJ][pP][eE][gG]')) + \
                 list(self.pic_folder.glob('*.[pP][nN][gG]'))
        
        logger.info(f"📊 Media inventory: {len(videos)} videos, {len(images)} images")
        
        if not videos and not images:
            logger.warning("⚠️ WARNING: No media files found!")
            logger.warning("Add .mp4/.mov files to videos/ folder")
            logger.warning("Add .jpg/.png files to pics/ folder")
            return False
        return True
    
    def run(self):
        """Start the bot with scheduled posting"""
        logger.info("🤖 Instagram Story Bot Started (instagrapi)")
        logger.info("=" * 60)
        
        # Initial login
        try:
            self.login()
        except Exception as e:
            logger.error("Failed to login. Exiting...")
            return
        
        # Check media folders
        self.check_media_folders()
        
        # Schedule configuration
        post_time = os.getenv("POST_TIME", "07:53")
        logger.info(f"📅 Scheduled to post daily at {post_time}")
        logger.info("=" * 60)
        
        # Schedule daily posting
        schedule.every().day.at(post_time).do(self.post_story)
        
        # Optional: Post immediately on startup (for testing)
        # Uncomment the line below to post right away
        # self.post_story()
        
        # Keep bot running
        logger.info("✅ Bot is now running... Press Ctrl+C to stop")
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("👋 Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                logger.info("Continuing to run...")
                time.sleep(300)  # Wait 5 minutes on error

def main():
    """Entry point"""
    try:
        bot = InstagramStoryBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()