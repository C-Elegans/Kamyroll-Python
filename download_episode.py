import kamyroll
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('season_id')
parser.add_argument('--resolution', '-r', default='1920x1080', help='The resolution to download at')
args = parser.parse_args()

kamyroll.dl_root = "anime"


def filter_resolution(video_formats):
    return args.resolution in video_formats[1]

def filter_hardsub(video_formats):
    return not "hardsub" in video_formats[0]

def filter_locale(sub_formats):
    return "en" in sub_formats[1]

def select_formats(sub_info, vid_info):
    vid_info = filter(filter_resolution, vid_info)
    vid_info = filter(filter_hardsub, vid_info)
    vid_info = list(vid_info)
    if not vid_info:
        print(f"No video formats available for {episode_title}")
        return None, None
    vid_format = vid_info[0][0]
    print(f"using video format {vid_format}")

    sub_info = list(filter(filter_locale, sub_info))
    if not vid_info:
        print(f"No sub formats available for {episode_title}")
        return None, None
    sub_format = sub_info[0][0]
    print(f"using sub format {sub_format}")
    return sub_format, vid_format 


def download_episode(episode_id, episode_idx, episode_title):
    print(f"Downloading episode {episode_idx} {episode_id} {episode_title}")
    sub_info, vid_info = kamyroll.get_formats(episode_id)
    sub_format, vid_format = select_formats(sub_info, vid_info)
    kamyroll.download(episode_id, sub_format)
    kamyroll.download(episode_id, vid_format)
    

def download_all_episodes(season_id):

    episode_list = kamyroll.get_episodes(args.season_id)

    for episode_id, episode_idx, _, episode_title in episode_list:
        download_episode(episode_id, episode_idx, episode_title)


download_all_episodes(args.season_id)
