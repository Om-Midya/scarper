import os
import googleapiclient.discovery


def get_youtube_comments(video_id, api_key):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )

    while request:
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textOriginal']
            comments.append(comment)
        request = youtube.commentThreads().list_next(request, response)

    return comments


def save_comments_to_file(comments, filename='comments.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for comment in comments:
            f.write(comment + '\n')


# Replace with your own video ID and API key
video_id = 'EMGnzU2F9fk'
api_key = 'AIzaSyC65o_7yTyLXjQ9g4mtO0yUqHz6tZ4e2fo'

comments = get_youtube_comments(video_id, api_key)
save_comments_to_file(comments)
print(f"Saved {len(comments)} comments to comments.txt")
