# -*- coding: utf-8 -*-
""" 爬取指定标签(如流行)的热门播放列表, 将列表中的歌曲id写入txt文件. """

import os
import re

import tqdm
import urllib
import requests


class NeteaseCrawler:
    def __init__(self):
        self.playlist_url = "https://music.163.com/playlist?id="
        self.playlist_cat_url = (
            "https://music.163.com/discover/playlist/?order=hot&cat="
        )
        self.playlist_pattern = re.compile(r'playlist\?id=(\d+?)"')
        self.song_pattern = re.compile(r'<a href="/song\?id=(\d+?)">')
        self.headers = {
            "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": (
                "_iuqxldmzr_=32; _ntes_nnid=b9e9c8a460bfdbc1250ffc5908f95cad,1543554353478; "
                "_ntes_nuid=b9e9c8a460bfdbc1250ffc5908f95cad; __utma=94650624.345999225.1543"
                "554354.1543554354.1543554354.1; __utmc=94650624; __utmz=94650624.1543554354"
                ".1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; WM_TID=N3LQ47ihEYOKTieS1"
                "8tLGKdN8q6R0iyt; WM_NI=VJ7qPEylWXfPBYYl3aMJisRzvjArZ%2BpJ9ES13N1zv1m4f9Vnfi"
                "HOdDEdcZWOUY6xS9Gi27GgC4pLKvWki7aHQISPLz9y0Uo3kGEPO5874RygU9DtXL3P1LY1%2BiV"
                "xtw77UEk%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee8bd05d8a96ba85ef7af2bc8fa6c14f"
                "929b9e85f25cbbb5afa2d874bc96a2b8d12af0fea7c3b92a9696f992d34fbbb499b9e55c828"
                "7978db26b8f96a794d172b6b68f93d921b496f7a6d23bf192ff9bf53bafecaadad566a6b788"
                "b0e75087bcadbbd6459787fa99d23385b7fed8c66d81ecc0adca7e95b5a7d8e44493979db1c"
                "f72fba700b6ee39a9998bb1ce3ffce9fcb3fc6d97e78c95db48f190ffaddc3be9b79a99f77d"
                "f5e99ba6ea37e2a3; JSESSIONID-WYYY=pNCF%2B8xzB2jTGWW7r7JlavTaS0YVMSZBP9THDnX"
                "Zp86OQ3Aqo5WpW6dr3h6FR3hgevYdmOdO8N7aubiagD%2FhBrf%2BYd%2BcXtBehyUotNH%2BCs"
                "%5CqZXKRbf4Pyt6fU1tl7UCsXBvbe6b5%2BQwZ%5Cuth8Shm4fRFdkApHsDIEA9tuUYQYDB7BYu"
                "o%3A1543559635032; __utmb=94650624.51.10.1543554354"
            ),
            "Host": "music.163.com",
            "Referer": "https://music.163.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": ("Mozilla/5.0 (Windows NT 6.3; WOW64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/68.0.3440.106 Safari/537.36"),
        }

    def get_html(self, url=None):
        """ 获取 url 对应的 html 文本. """

        html_str = requests.get(url, headers=self.headers).text
        return html_str

    def get_playlistids(self, tag=None):
        """ 获取指定标签(tag)的所有播放列表id(playlistids). """

        tag = urllib.parse.quote(tag)
        url = f"{self.playlist_cat_url}{tag}"
        html_str = self.get_html(url=url)
        playlistids = self.playlist_pattern.findall(html_str)
        return playlistids[::2]

    def get_playlist_songids(self, playlistid=None):
        """ 获取指定播放列表id(playlistid)中所有歌曲id(songids). """

        url = f"{self.playlist_url}{playlistid}"
        html_str = self.get_html(url=url)
        songids = self.song_pattern.findall(html_str)
        return songids


if __name__ == "__main__":
    """ 获取每种标签的前10个播放列表, 并将播放列表中的歌曲id写入txt. """

    NC = NeteaseCrawler()
    type2tags = {
        "风格": [
            "流行",
            "摇滚",
            "民谣",
            "电子",
            "舞曲",
            "说唱",
            "轻音乐",
            "爵士",
            "乡村",
            "民族",
            "英伦",
            "金属",
            "朋克",
            "蓝调",
            "古风",
        ],
        "情感": ["怀旧", "清新", "浪漫", "伤感", "治愈", "放松", "孤独", "感动", "兴奋", "快乐", "安静", "思念"],
    }
    playlist_num = 10
    for tag_type, tags in type2tags.items():
        for tag in tags:
            playlistids = NC.get_playlistids(tag=tag)[:playlist_num]
            assert len(set(playlistids)) == playlist_num
            songids_set = set([])
            for playlistid in tqdm.tqdm(playlistids, desc=f"{tag_type}/{tag}"):
                songids = NC.get_playlist_songids(playlistid=playlistid)
                assert len(songids) == 10
                songids_set.update(songids)
            lines = [f"{tag} {x}" for x in songids_set]
            # write
            folder = f"txts/{tag_type}"
            if not os.path.exists(folder):
                os.mkdir(folder)
            txt_path = f"{folder}/{tag}.txt"
            with open(txt_path, "w") as fout:
                fout.write("\n".join(lines))
