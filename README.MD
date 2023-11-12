# 番剧批量改名工具
## Abstract
在网上下载绝大多数的、压制组而非字幕组制作的番剧时，
它们不带字幕。我们在其他网站，如某某网站和某某某某某网站下载字幕，
但是它们的文件名和视频文件名不一致，我们需要手动改名。

这个工具可以自动将字幕文件名改为视频文件名，方便我这种重度补番用户观看。

## 实现原理
1. 读取视频文件名，获取**集数**信息，这之前要过滤分辨率等影响集数的信息。
2. 如果文件名中有其他数字，比如如下番剧：
> [VCB-Studio] 86 -Eighty Six- [01][Ma10p_1080p][x265_flac_aac].mkv
  这种会在`reduce_name`中处理。

3. 读取字幕文件名，获取**集数**信息，这之前要过滤分辨率等影响集数的信息。
4. 改名。

## 编译方式
目前只提供Windows下，使用nuitka，基于CPython3.9编译的exe文件。

本软件亦提供源码，可以自行编译或直接运行。

## 开源协议
本软件使用3-Clause BSD License开源协议。使用前请认真阅读协议内容。

## 使用方法
目前没加拖拽功能，需要手动复制路径。