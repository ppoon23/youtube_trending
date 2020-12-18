import sys
import pandas as pd
from googleapiclient.discovery import build

DEVELOPER_KEY = sys.argv[1]

region_code = ['US', 'GB', 'CA', 'JP', 'MX', 'ES'] # https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2


def build_service():
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

def get_response(region_code):
    youtube = build_service()
    search_response = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=50
    ).execute()
    return search_response


# print(search_response['items'][0]['snippet'].keys())    # ['publishedAt', 'channelId', 'title', 'description', 'thumbnails', 'channelTitle', 'categoryId',
                                                          # 'liveBroadcastContent', 'defaultLanguage', 'localized', 'defaultAudioLanguage'])
def get_video_data(response):
    vid_compile = []
    for vid in response['items']:
        vid_dict = {'video_id': vid['id'],
                    'publish_at': vid['snippet']['publishedAt'],
                    'title': vid['snippet']['title'],
                    'channel_id': vid['snippet']['channelId'],
                    'description': vid['snippet']['description'],
                    'view_count': vid['statistics']['viewCount'],
                    'trending': 1 # 1 is trending; 0 is not trending.
                    }
        if 'likeCount' in vid['statistics']:
            vid_dict['like_count'] = vid['statistics']['likeCount']
            vid_dict['ratings_disabled'] = False
        else:
            vid_dict['like_count'] = 0
            vid_dict['ratings_disabled'] = True

        if 'dislikeCount' in vid['statistics']:
            vid_dict['dislike_count'] = vid['statistics']['dislikeCount']
            vid_dict['ratings_disabled'] = False
        else:
            vid_dict['dislike_count'] = 0
            vid_dict['ratings_disabled'] = True

        if 'commentCount' in vid['statistics']:
            vid_dict['comment_count'] = vid['statistics']['commentCount']
            vid_dict['comments_disabled'] = False
        else:
            vid_dict['comment_count'] = 0
            vid_dict['comments_disabled'] = True

        vid_compile.append(vid_dict)
    return vid_compile


if __name__ == '__main__':
    for country in region_code:
        response = get_response(country)
        df = pd.DataFrame(get_video_data(response))
        df.to_csv(f'data_export/{country}.csv')
