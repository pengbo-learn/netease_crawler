# 网页云音乐爬虫

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
