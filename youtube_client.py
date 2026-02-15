import json
import httpx
import os
from config import YOUTUBE_API_KEY, YOUTUBE_PLAYLIST_ID
from logger import log_error, log_info

class YouTubeClient:
    def __init__(self, metadata_path="video_metadata.json"):
        self.metadata_path = metadata_path
        self.videos = self._load_metadata()
        self.api_key = YOUTUBE_API_KEY
        self.playlist_id = YOUTUBE_PLAYLIST_ID

    def _load_metadata(self):
        try:
            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            log_error(f"Error loading video metadata: {e}")
            return []

    def get_videos_by_level(self, level):
        """Filter videos by level: Beginner, Intermediate, Advanced"""
        return [v for v in self.videos if v['level'].lower() == level.lower()]

    def find_relevant_video(self, query, language=None):
        """Find the most relevant video based on tags and query text"""
        query_lower = query.lower()
        best_match = None
        highest_score = 0

        # Filter by language if specified
        target_videos = self.videos
        if language:
            target_videos = [v for v in self.videos if v.get('language') == language]

        for video in target_videos:
            score = 0
            # Check tags
            for tag in video.get('tags', []):
                if tag in query_lower:
                    score += 10
            
            # Check title
            if any(word in video['title'].lower() for word in query_lower.split() if len(word) > 3):
                score += 5

            if score > highest_score:
                highest_score = score
                best_match = video

        # Return only if we have a decent level of confidence
        if highest_score >= 10:
            return best_match
        return None

    async def sync_playlist(self):
        """Optional: Sync with YouTube API to update titles/IDs (requires API key)"""
        if not self.api_key:
            log_info("YouTube API Key missing, skipping sync. Using local metadata.")
            return False

        try:
            url = f"https://www.googleapis.com/robot/v1/metadata/x509/youtube.googleapis.com" # Placeholder for actual sync logic if needed
            # In a real implementation, we'd call the playlistItems endpoint
            # Since we have a curated list in JSON for categorization, 
            # we'll stick to the JSON as the source of truth for labels/tags.
            return True
        except Exception as e:
            log_error(f"YouTube Sync Error: {e}")
            return False
