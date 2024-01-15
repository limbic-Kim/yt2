import argparse
import yt_dlp
import os, re


def download_video(url, output_dir, audio_only=False,
                   bypass_postprocessors=True
                  ):
    try:
        output_directory = output_dir
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        if audio_only:
            format_option = "bestaudio/best"
            ext = "webm" if bypass_postprocessors else "mp3"
            postprocessors = [] if bypass_postprocessors else [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            format_option = "bestvideo+bestaudio/best"
            ext = "webm" if bypass_postprocessors else "mp4"
            postprocessors = [] if bypass_postprocessors else [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]

        ydl_opts = {
            "format": format_option,
            "outtmpl": f"{output_directory}/%(title)s.%(ext)s",
            "noplaylist": True,
            "postprocessors": postprocessors,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("Download completed.")

    except Exception as e:
        print("Error occurred while downloading:", e)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Youtube Download CLI')
    parser.add_argument('--mode', choices=['audio_only', 'audio_and_video'], required=True, help='Mode of operation: audio_only or audio_and_video')
    parser.add_argument('--output_dir', type=str, required=True, help='Path to output directory')
    parser.add_argument('--input_links', type=str, required=True, help='Comma-separated list of youtube links')
    return parser.parse_args()


def refine_url(url):
    pattern = r"https://(?:www\.youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)"
    video_id = 'hV5n74eMDoY'

    match = re.search(pattern, url)
    if match:
        video_id = match.group(1)

    return f'https://www.youtube.com/watch?v={video_id}'


def main():
    args = parse_arguments()
    input_links = args.input_links.split(',')
    for link in input_links:
        download_video(refine_url(link), args.output_dir, audio_only=(args.mode == 'audio_only'))


if __name__ == '__main__':
    main()