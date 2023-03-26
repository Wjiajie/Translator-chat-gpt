# Translator-chat-gpt
一个python脚本，允许你将.vtt字幕格式从源语言翻译为另外一门目标语言，基于 gpt-3.5-turbo实现。



### 参数说明

```python

SRC_LANG = "英文"

DST_LANG = "中文"

skip_len = 3 # vtt 文件相同内容的重复次数，在我下载的vtt文件中，出现重复行数是3.

sleep_time = 3.0 # 普通的openai api key一分钟最多调用20次，所以设置一个安全休眠时间

next_response_index = 0 # 如果你的程序由于api调用超时了，根据程序抛出的错误重新设置该值，并重新运行程序，可以从中断的地方开始翻译。（注意，这个情况仅仅适合翻译单个文件的情况，如果你的文件夹中有多个.vtt文件，程序没有处理该情况）

vtt_dir_src = os.path.join("D:/Learn/datasets/cherno-game-engine/vtt-en") if next_response_index == 0 else os.path.join("D:/Learn/datasets/cherno-game-engine/vtt-zh") # 源文件夹

vtt_dir_dst = os.path.join("D:/Learn/datasets/cherno-game-engine/vtt-zh") #目标文件夹

```

### 运行说明

0. 建议新建一个conda虚拟环境
1. 将你的OPENAI_API_KEY填写在.env文件中
2. 在translate.py中填写具体的输入输出信息
3. `python translate.py`
