# 网页云音乐爬虫

## 实现
### 获取playlistid
- 访问 url 
    - 以爬取摇滚风格的歌曲为例, 对应**曲风url**为https://music.163.com/#/discover/playlist/?cat=%E6%91%87%E6%BB%9A.
- 通过 url 获取 html
    - 直接用 requests.get 即可 
- 通过 html 获取 playlistid
    - html 中的歌曲列表信息格式 ``` <a title="[摇滚唱片行] 欢迎光临摇滚万岁经典唱片行" href="/playlist?id=5217150082" ```
    - 通过正则表达式解析 ``` r'playlist\?id=(\d+?)"'```

### 根据playlistid获取songid
- 访问 url
    - [playlistid]对应url为https://music.163.com/#/playlist?id=[playlistid]
- 通过 url 获取 html
    - 直接用 requests.get 即可 
- 通过 html 获取 songid
    - html 中的歌曲信息格式 ```<a href="/song?id=3950546">```
    - 通过正则表达式解析 ``` r'<a href="/song\?id=(\d+?)">'```

### 下载歌曲id对应的mp3音乐
- 歌曲id 24953439
- 歌曲url http://music.163.com/song/media/outer/url?id=24953439
- 直接用 youtube-dl 可以下载歌曲, ```youtube-dl --quiet --extract-audio 'http://music.163.com/song/media/outer/url?id=24953439' -o '24953439.%(ext)s'``` 下载到 ```24953439.mp3```
- 通过 parallel 可以实现并行下载



## 环境
- centos
- python3
- 配置
    sh env.sh
    ```bash
    #!/bin/bash
    pip install tqdm==4.48.2
    pip install urllib3==1.25.10
    pip install requests==2.24.0
    cd rpms && yum install parallel-20150522-1.el7.cern.noarch.rpm
    ```

## 运行
```bash
# 歌曲id写入txts
python3 netease.py
# 根据txts下载音乐到mp3s
sh get_mp3.sh
```
