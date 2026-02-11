import feedparser
from typing import List, Dict

class BloggerFeedParser:
    """RSS Parser مخصص لبلوجر"""
    
    def __init__(self, feed_url: str):
        self.feed_url = feed_url
        
    def get_recent_posts(self, max_results: int = 25) -> List[Dict]:
        """قراءة آخر المقالات من RSS"""
        feed = feedparser.parse(self.feed_url)
        posts = []
        
        for entry in feed.entries[:max_results]:
            # استخراج الرابط الصحيح
            link = entry.link if hasattr(entry, 'link') else entry.get('id', '')
            
            posts.append({
                'url': link,
                'title': entry.title,
                'published': entry.get('published', '')
            })
            
        return posts
