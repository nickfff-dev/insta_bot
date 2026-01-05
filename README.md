# 🤖 Instagram Story Bot

Automated Instagram story posting bot that uploads videos and images on a schedule using Python and instagrapi.

## ⚠️ Disclaimer

This bot uses an unofficial Instagram API and may violate Instagram's Terms of Service. Use at your own risk. Your account may be flagged, rate-limited, or banned.

## ✨ Features

- 📹 Posts random videos from `videos/` folder
- 🖼️ Posts random images from `pics/` folder
- ⏰ Scheduled daily posting at a specific time
- 🔄 Session persistence to avoid repeated logins
- 🚀 Easy deployment to Railway
- 📝 Detailed logging

## 🏗️ Project Structure

```
instagram-story-bot/
├── main.py              # Main bot script
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
├── .dockerignore       # Files to exclude from Docker
├── railway.json        # Railway deployment config
├── README.md           # This file
├── videos/             # Add your video files here (.mp4, .mov)
├── pics/               # Add your image files here (.jpg, .png)
└── temp/               # Temporary files (auto-created)
```

## 🚀 Quick Start (Local)

### Prerequisites

- Python 3.11+
- Instagram account

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd instagram-story-bot
   ```

2. **Create virtual environment**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**

   ```bash
   IG_USERNAME=your_instagram_username
   IG_PASSWORD=your_instagram_password
   POST_TIME=09:00
   ```

5. **Add media files**
   - Place videos in `videos/` folder
   - Place images in `pics/` folder

6. **Run the bot**

   ```bash
   python main.py
   ```

## ☁️ Deploy to Railway

### Step 1: Prepare Repository

1. Create a GitHub repository
2. Upload all project files
3. Add at least one video to `videos/` folder
4. Add at least one image to `pics/` folder
5. Commit and push

### Step 2: Deploy on Railway

1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository
6. Wait for build to complete (2-3 minutes)

### Step 3: Configure Environment Variables

In Railway dashboard, add these variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `IG_USERNAME` | your_username | Instagram username |
| `IG_PASSWORD` | your_password | Instagram password |
| `POST_TIME` | 09:00 | Daily posting time (24h format) |

### Step 4: Verify Deployment

1. Go to **"Deployments"** tab
2. Wait for green checkmark ✅
3. Click **"View Logs"**
4. Look for: `✅ Bot is now running...`

## 🔧 Configuration

### Posting Schedule

Change the `POST_TIME` environment variable to set when stories are posted daily:

```
POST_TIME=09:00    # 9:00 AM
POST_TIME=14:30    # 2:30 PM
POST_TIME=21:00    # 9:00 PM
```

### Test Posting Immediately

To test without waiting for scheduled time, uncomment this line in `main.py`:

```python
# In the run() method, around line 170
self.post_story()  # Uncomment this line
```

Then redeploy. **Remember to comment it back** to avoid posting on every restart.

## 📝 How It Works

1. **Bot starts** and logs into Instagram
2. **Saves session** to avoid repeated logins
3. **Waits** for scheduled time (e.g., 09:00)
4. **Posts random video** from `videos/` folder
5. **Waits 5-15 seconds** (human-like behavior)
6. **Posts random image** from `pics/` folder
7. **Repeats** daily at scheduled time

## 🔍 Monitoring

### View Logs (Railway)

```bash
# In Railway dashboard:
Your Service → Logs tab
```

### Expected Log Output

```
🤖 Instagram Story Bot Started (instagrapi)
✅ Logged in using saved session
📊 Media inventory: 1 videos, 1 images
📅 Scheduled to post daily at 09:00
✅ Bot is now running... Press Ctrl+C to stop
```

### When It Posts

```
🎬 Starting story posting job...
Uploading video: video.mp4
✅ Video uploaded successfully: video.mp4
⏳ Waiting 12s before posting image...
Uploading image: image.jpg
✅ Image uploaded successfully: image.jpg
✅ Story posting completed successfully!
```

## 🐛 Troubleshooting

### Login Failed

- ✅ Verify username and password are correct
- ✅ Try logging into Instagram manually on your phone first
- ✅ Check if Instagram sent a security alert
- ✅ Wait a few hours if rate-limited

### No Media Found

- ✅ Ensure `videos/` folder has .mp4 or .mov files
- ✅ Ensure `pics/` folder has .jpg or .png files
- ✅ Check file extensions are lowercase

### Session Expired Errors

- ✅ This is normal - bot will re-login automatically
- ✅ If it happens frequently, Instagram may be flagging your account
- ✅ Consider using a dedicated account for the bot

### Railway Build Failed

- ✅ Ensure `Dockerfile` is named exactly (capital D, no extension)
- ✅ Check all files are in repository root
- ✅ Verify `requirements.txt` exists

## 🛡️ Security Best Practices

- 🔒 **Never commit `.env` file** to Git
- 🔒 Use Railway's environment variables for credentials
- 🔒 Consider using a separate Instagram account for automation
- 🔒 Don't share your `session.json` file
- 🔒 Keep your repository private if it contains credentials

## 📦 Dependencies

- `instagrapi` - Instagram API wrapper
- `schedule` - Job scheduling
- `python-dotenv` - Environment variable management
- `pillow` - Image processing
- `requests` - HTTP library

## 🔄 Updating Media

To change the video/image being posted:

1. Replace files in `videos/` and `pics/` folders
2. Commit and push to GitHub
3. Railway will auto-deploy the new version
4. New media will be posted at next scheduled time

## 📄 License

This project is provided as-is for educational purposes. Use responsibly.

## ⚠️ Important Notes

- Instagram may detect and ban automated activity
- Use at your own risk
- Consider Instagram's rate limits
- Test with a non-primary account first
- Stories posted by bot may be flagged by Instagram

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section
2. Review Railway logs
3. Verify environment variables
4. Check Instagram account status

---

**Built with ❤️ using Python and instagrapi**
