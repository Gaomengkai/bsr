'''

The 3-Clause BSD License

Copyright 2023, merky (github.com/Gaomengkai)

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form or with modification must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the merky nor the names of its contributors may be used to endorse or promote products derived

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

from typing import Dict, List
import shutil
import re
import pathlib
import os
from functools import reduce
VIDEO_SUFFIX = ['mp4', 'mkv']
SUBTITLE_SUFFIX = ['ass', 'srt']
RESOLUTION_STR = ['1080p', '720p', '2160p', '1920',
                  '1080', '1280', '720', '2560', '1440', '3840', '2160']
ENCODING_STR = ['h264', 'H264', 'x264', 'X264', 'h265', 'H265', 'x265', 'X265',
                'h.264', 'H.264', 'x.264', 'X.264', 'h.265', 'H.265', 'x.265', 'X.265']
BIT_STR = ['10bit', '8bit', '10p']

__author__ = 'Merky'
__description__ = 'A tool to rename video files\' subtitles.'


a1 = r'''
F:\Downloads\a4k.net_1598323283
'''.strip().strip('"').strip("'").strip()

v1 = r'''
Y:\Downloads\[异域-11番小队][妄想代理人 Paranoia Agent][1-13+SP][BDRIP][X264-10bit_AAC][720P]
'''.strip().strip('"').strip("'").strip()

VIDEO_PATH = pathlib.Path(
    v1
)

ASS_PATH = pathlib.Path(
    a1
)


def match_numbers(s: str) -> List[str]:
    # 中括号的窄匹配,例子：
    # [XKsub&SweetSub&VCB-Studio] Sonny Boy [01][Ma10p_1080p][x265_flac].chs
    pattern_test = re.compile(r'\[(SP\d*|OVA\d*|OAD\d*|\d{2,3}V*\d*)\]')
    if reres := re.findall(pattern_test, s):
        # 窄匹配
        return reres
    # 减号+空格+两个数字+空格模式，例子：
    #【推しの子】 Kimi wa Houkago Insomnia - 02 (Sentai 1920x1080 AVC AAC MKV) [AD9EEC62]
    elif reres:= re.findall(re.compile(r'- ([0-9]{2}) '),s):
        return reres
    else:
        # 不要匹配CRC32
        neg_pattern = re.compile(r'[0-9a-fA-F]{8}')
        s = re.sub(neg_pattern, '', s)
        # 宽匹配
        pattern = re.compile(r'SP\d*|OVA\d*|OAD\d*|[0-9]{2}\.?[5]?')
        filename_clear = reduce(lambda x, y: x.replace(
            y, ''), RESOLUTION_STR+ENCODING_STR+BIT_STR, s)
        # 去掉末尾的点
        res = re.findall(pattern, filename_clear)
        return list(map(lambda x: x.strip('.'), res))


# match_numbers("[XKsub][Oshi no Ko][01][CHS][1080P][WEBrip][MP4]")


def find_videos(path: pathlib.Path) -> Dict[str, pathlib.Path]:
    _v_files: List[pathlib.Path] = []
    # 不处理子文件夹
    for _v_file in path.iterdir():
        if _v_file.is_file() and _v_file.suffix[1:] in VIDEO_SUFFIX:
            _v_files.append(_v_file)
    matched = []
    for f in _v_files:
        matched.append(match_numbers(f.stem))
    if len(matched[0]) == 0:
        exception = 'No matched numbers found in file names.'
        raise FileNotFoundError(exception)
    reduced_numbers = reduce_name(matched)
    res = {}
    for i in range(len(reduced_numbers)):
        res[reduced_numbers[i]] = _v_files[i]
    return res


def find_subtitles(path: pathlib.Path) -> Dict[str, List[pathlib.Path]]:
    _s_files: List[pathlib.Path] = []
    # 不处理子文件夹
    for _s_file in path.iterdir():
        if _s_file.is_file() and _s_file.suffix[1:].lower() in SUBTITLE_SUFFIX:
            _s_files.append(_s_file)
    matched = []
    for f in _s_files:
        if nums := match_numbers(f.stem):
            matched.append(nums)
    if len(matched[0]) == 0:
        exception = 'No matched numbers found in file names.'
        raise FileNotFoundError(exception)
    reduced_numbers = reduce_name(matched)
    res = {}
    for i in range(len(reduced_numbers)):
        if res.get(reduced_numbers[i]) is None:
            res[reduced_numbers[i]] = []
        res[reduced_numbers[i]].append(_s_files[i])
    return res


def reduce_name(terms: List[List[str]]) -> List[str]:
    if not terms:
        return []
    if len(terms[0]) == 1:
        return [x[0] for x in terms]
    minlen = min([len(x) for x in terms])
    accu = [0 for _ in range(minlen)]
    for j in range(minlen):
        for i in range(len(terms)):
            for k in range(i+1, len(terms)):
                if terms[i][j] == terms[k][j]:
                    accu[j] += 1
    # 找出最小值的index
    min_index = accu.index(min(accu))
    # print(accu)
    res = []
    for i in range(len(terms)):
        res.append(terms[i][min_index])
    return res

def name_reducer(names:list[str]) -> list[str]:
    nums = [match_numbers(x) for x in names]
    return reduce_name(nums)

def gaiming(videopath: pathlib.Path, subtitlepath: pathlib.Path, willcopy: bool = True) -> List[pathlib.Path]:
    vres = find_videos(videopath)
    sres = find_subtitles(subtitlepath)
    succeed_files = []
    for k, v in vres.items():
        if d := sres.get(k):
            for s in d:
                s_suffixs = s.name.split('.')[1:]
                s_suffixs = filter(lambda x: len(
                    x) <= 4 or re.findall("[SsTt][Cc]", x), s_suffixs)
                s_suffix = '.'.join(s_suffixs)
                new_file_name = v.stem + '.' + s_suffix

                new_path = s.parent.absolute() / new_file_name
                try:
                    shutil.copy(s, new_path)
                except shutil.SameFileError:
                    pass
                if willcopy:
                    new_path = v.parent.absolute() / new_file_name
                    try:
                        shutil.copy(s, new_path)
                    except shutil.SameFileError:
                        pass
                succeed_files.append(new_path)
    return succeed_files


if __name__ == '__main__':
    debug = True
    if not debug:
        videopath = pathlib.Path(input("视频：").strip('"').strip("'").strip())
        vres = find_videos(videopath)
        print(f"找到视频：{len(vres)}")

        subtitlepath = pathlib.Path(input("字幕：").strip('"').strip("'").strip())
        sres = find_subtitles(subtitlepath)
        print(f"找到字幕：{len(sres)}")
        willCopy = input("是否复制字幕？(y/n)")
        willCopy = willCopy.lower() == 'y'
    else:
        vres = find_videos(VIDEO_PATH)
        sres = find_subtitles(ASS_PATH)
        willCopy = True
    for k, v in vres.items():
        print('\n', k, v.name)
        # 重命名字幕文件
        if sres.get(k) is not None:

            for s in sres[k]:
                s_suffixs = s.name.split('.')[1:]
                s_suffixs = filter(lambda x: len(
                    x) <= 4 or re.findall("[SsTt][Cc]", x), s_suffixs)
                s_suffix = '.'.join(s_suffixs)
                new_file_name = v.stem + '.' + s_suffix
                os.rename(s, s.parent.absolute() / new_file_name)
                print('rename', s.name, 'to', new_file_name)
                if willCopy:
                    shutil.copy(s.parent.absolute() / new_file_name,
                                v.parent.absolute() / new_file_name)
