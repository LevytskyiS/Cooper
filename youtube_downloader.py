import os
from pathlib import Path

from pytube import YouTube

vid_url = "https://www.youtube.com/watch?v=r_0JjYUe5jo&ab_channel=LyricalLemonade"


async def get_youtube_video(url: str) -> str:
    download_folder = "./youtube"
    yt = YouTube(url)

    (
        yt.streams.filter(progressive=True, file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
        .download(output_path=download_folder)
    )
    video_path = [file for file in Path(download_folder).iterdir()][0]
    video_size = os.path.getsize(video_path)

    if video_size >= 49000000:
        await remove_downloaded_video(video_path)
        return

    return video_path


async def remove_downloaded_video(video_path: str) -> None:
    try:
        os.remove(video_path)
    except FileNotFoundError as e:
        print("File not found")
    print("Removed video")
