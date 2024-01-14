import argparse
import yt_dlp
import os


def download_video(url, output_dir, audio_only=False,
                   bypass_postprocessors=True # False면 webm -> mp4 로 변환. (오래걸림)
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


def main():
    args = parse_arguments()
    # input_links를 쉼표로 구분하여 리스트로 변환합니다.
    input_links = args.input_links.split(',')
    # 리스트의 각 링크에 대해 download_video 함수를 호출합니다.
    for link in input_links:
        download_video(link, args.output_dir, audio_only=(args.mode == 'audio_only'))


if __name__ == '__main__':
    main()