import os
import time
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from feed_parser import BloggerFeedParser

# إعدادات
SCOPES = ['https://www.googleapis.com/auth/indexing']
BLOG_URL = os.environ['BLOG_URL']
RSS_FEED = os.environ['BLOGGER_RSS_FEED']
MAX_REQUESTS = int(os.environ.get('MAX_REQUESTS_PER_DAY', 200))

def get_authenticated_service():
    """تسجيل الدخول لـ Google Indexing API"""
    credentials_json = os.environ['GOOGLE_SERVICE_ACCOUNT_KEY']
    creds_dict = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=SCOPES)
    return build('indexing', 'v3', credentials=credentials)

def send_url_to_google(service, url):
    """إرسال رابط واحد إلى Indexing API"""
    body = {
        'url': url,
        'type': 'URL_UPDATED'
    }
    try:
        response = service.urlNotifications().publish(body=body).execute()
        print(f'✅ تم الإرسال: {url}')
        return True
    except Exception as e:
        print(f'❌ فشل الإرسال {url}: {e}')
        return False

def main():
    print('🚀 بدأ تشغيل سكربت فهرسة بلوجر...')
    
    # قراءة المقالات من RSS
    parser = BloggerFeedParser(RSS_FEED)
    posts = parser.get_recent_posts(max_results=25)
    
    print(f'📄 تم العثور على {len(posts)} مقالة جديدة')
    
    if not posts:
        print('⚠️ لا توجد مقالات جديدة')
        return
    
    # الاتصال بـ Google API
    service = get_authenticated_service()
    
    # إرسال الروابط
    success_count = 0
    for i, post in enumerate(posts):
        if i >= MAX_REQUESTS:
            print(f'🛑 تخطيت حد {MAX_REQUESTS} طلب في اليوم')
            break
            
        if send_url_to_google(service, post['url']):
            success_count += 1
        time.sleep(1)  # مهلة ثانية بين الطلبات
    
    print(f'✅ تم بنجاح: {success_count} من {len(posts)}')

if __name__ == '__main__':
    main()
