#!/bin/bash
# 下载 txts 中记录的歌曲 id 对应的歌曲文件

get_clip() {
    echo $1 | while read ind tag id tag_folder; do 
        echo $ind", "$tag", "$id", "$tag_folder; 
        url="http://music.163.com/song/media/outer/url?id="$id".mp3"
        date;
        AUDIO_PATH=${tag_folder}"/"${id}".%(ext)s"
        if [ ! -f ${tag_folder}"/"${id}".mp3" ]; then
            youtube-dl --quiet --extract-audio ${url} -o "${AUDIO_PATH}";
        fi
    done
}
export -f get_clip;

TYPES="风格 情感"   # 待爬取的类型
PARA_NUM="32"       # 爬取并行进程数
MUSIC_NUM="1"       # 每个歌曲标签下载歌曲数
for TYPE in $TYPES; do
    AUDIO_FOLDER="mp3s/"$TYPE;
    TXT_FOLDER="txts/"$TYPE;
    for TXT_NAME in `ls ${TXT_FOLDER}`; do
        TXT_PATH=${TXT_FOLDER}/${TXT_NAME};
        TAG_NAME=${TXT_NAME%.txt};
        TAG_FOLDER=${AUDIO_FOLDER}"/"${TAG_NAME};
        mkdir -p $TAG_FOLDER;
        cat -n ${TXT_PATH} | head -${MUSIC_NUM} | while read line; do echo ${line}" "${TAG_FOLDER}; done | parallel -j ${PARA_NUM} -k get_clip
    done
done
