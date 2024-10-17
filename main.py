import time
import requests
from bs4 import BeautifulSoup
from pypresence import Presence

# SoundCloudのトラック情報を取得する関数
def get_track_info(track_url):
    try:
        response = requests.get(track_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # タイトルを取得
        title = soup.find('title').text.replace(' - SoundCloud', '').strip()
        
        # アーティスト名を取得
        user_info = soup.find('a', class_='sc-link-primary sc-font-light')
        artist = user_info.text.strip() if user_info else "Unknown Artist"
        
        # カバー画像を取得
        cover_image = soup.find('meta', property='og:image')
        cover_image_url = cover_image['content'] if cover_image else None
        
        return {
            'title': title,
            'artist': artist,
            'cover_image': cover_image_url
        }
    except Exception as e:
        print("Error retrieving track info:", e)
        return None

# Discordのリッチプレゼンスを更新する関数
def update_discord_presence(track_info, rpc):
    if track_info is not None:
        rpc.update(
            state=track_info['title'],  # トラックのタイトル
            details=track_info['artist'],  # アーティスト名
            large_image=track_info['cover_image'] if track_info['cover_image'] else None,
            large_text=track_info['title']  # トラックのタイトル
        )
    else:
        print("No track info available to update.")

# メイン処理
if __name__ == "__main__":
    track_url = "https://soundcloud.com/n0gejhpoqrgc/sets/6sd6xclihus5"  # ここにトラックのURLを指定

    rpc = Presence("1296381230346010696")  # DiscordのアプリケーションIDを指定
    rpc.connect()

    while True:
        track_info = get_track_info(track_url)
        update_discord_presence(track_info, rpc)
        time.sleep(1)  # 1秒ごとにチェック
