import argparse
import os
import re
from datetime import datetime
import requests


def current_date(args_date=None):
    if args_date:
        return args_date

    datetime_now = datetime.now()
    return datetime_now.strftime("%Y-%m-%d")


def current_folder():
    return os.path.dirname(os.path.realpath(__file__))


def parse_arguments():
    parser = argparse.ArgumentParser('Download videos')
    parser.add_argument('type', choices=['tagesschau', 'tagesschau20', 'tagesthemen', 'tagesthemengebaerden'])
    parser.add_argument('quality', choices=['mobil_h264', 'klein_h264', 'mittel_h264',
                                            'mittel_webm', 'gross_h264', 'gross_webm', 'hd_h264'])
    parser.add_argument('-d', '--date', default=current_date(), help='provide the date for video, format: YYYY-MM-DD')
    parser.add_argument('-f', '--file', help='name of the file after download')
    parser.add_argument('-p', '--path', default=current_folder(), help='path to the download-directory')

    return parser.parse_args()


def get_existing_urls(date_string):
    request = requests.get('http://www.tagesschau.de/multimedia/video/videoarchiv2~_date-{}.html'
                           .format(date_string.replace('-', '')))

    return re.findall('<h4 class="headline"><a href="([^"]+)">([^<]+)</a></h4>', request.text)


def get_video_page_url(link_name_list, link_type):
    for link_name in link_name_list:
        if link_type == 'tagesschau' and link_name[1] == 'tagesschau':
            return 'http://www.tagesschau.de' + link_name[0]
        if link_type == 'tagesschau20' and link_name[1] == 'tagesschau vor 20 Jahren':
            return 'http://www.tagesschau.de'+link_name[0]
        if link_type == 'tagesthemen' and link_name[1] == 'tagesthemen':
            return 'http://www.tagesschau.de'+link_name[0]
        if link_type == 'tagesthemengebaerden' and link_name[1] == u'tagesschau (mit Geb\xe4rdensprache)':
            return 'http://www.tagesschau.de'+link_name[0]


def get_video_qualities(video_page_url):
    request = requests.get(video_page_url)
    return re.findall('<a href="(http://download[^"]+)">([^<]+)', request.text)


def get_video(video_qualities_urls, quality):
    for video_quality_url in video_qualities_urls:
        if quality == 'mobil_h264' and video_quality_url[1] == 'Mobil (h264)':
            return video_quality_url[0]
        if quality == 'klein_h264' and video_quality_url[1] == 'Klein (h264)':
            return video_quality_url[0]
        if quality == 'mittel_h264' and video_quality_url[1] == 'Mittel (h264)':
            return video_quality_url[0]
        if quality == 'mittel_webm' and video_quality_url[1] == 'Mittel (WebM)':
            return video_quality_url[0]
        if quality == 'gross_h264' and video_quality_url[1] == 'Gro&szlig; (h264)':
            return video_quality_url[0]
        if quality == 'gross_webm' and video_quality_url[1] == 'Gro&szlig; (WebM)':
            return video_quality_url[0]
        if quality == 'hd_h264' and video_quality_url[1] == 'HD (h264)':
            return video_quality_url[0]


def download_object(url, path):
    request = requests.get(url, stream=True)

    with open(path, 'wb') as download_file:
        for chunk in request.iter_content(chunk_size=1024):
            if chunk:
                download_file.write(chunk)


def generate_file_name(args, video_url):
    if args.file is not None:
        return os.path.join(args.path, args.file)

    return os.path.join(args.path, '{}_{}_{}{}'.format(current_date(args.date),
                                                       args.type,
                                                       args.quality,
                                                       os.path.splitext(video_url)[1]))


def main():
    args = parse_arguments()
    all_urls = (get_existing_urls(args.date))
    video_page_url = get_video_page_url(all_urls, args.type)

    video_qualities_urls = get_video_qualities(video_page_url)
    video_url = (get_video(video_qualities_urls, args.quality))

    download_object(video_url, generate_file_name(args, video_url))


if __name__ == "__main__":
    main()
