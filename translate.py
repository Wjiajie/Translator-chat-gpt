import os
import openai
import time
import pycaption
from tqdm import tqdm

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

SRC_LANG = "英文"
DST_LANG = "中文"
skip_len = 3
sleep_time = 3.0
next_response_index = 0
vtt_dir_src = os.path.join("D:/Learn/datasets/cherno-game-engine/vtt-en") if next_response_index == 0 else os.path.join("D:/Learn/datasets/cherno-game-engine/vtt-zh")
vtt_dir_dst = os.path.join("D:/Learn/datasets/cherno-game-engine/vtt-zh")

def translate_text(text):
    prompt = f"假设你是一个出色的翻译家，给你一段{SRC_LANG}文本，你需要将它翻译为{DST_LANG}，注意你只需要翻译文本即可, 除了翻译内容, 不要回复多余的词。即使文本不是一个完整的句子，(比如只是一个词)，也请你尝试给出翻译。请将以下{SRC_LANG}文本翻译为{DST_LANG}: \n{text}"
    response = get_response(prompt)
    return response.strip().replace(f"{prompt}","")

def get_response(prompt):
    prompt = f"{prompt}\n"
    completions = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"你是一位资深的翻译家，能熟练地将{SRC_LANG}翻译为{DST_LANG}."},
        {"role": "user", "content": prompt},
    ],
    temperature=0.0
    )
    message = completions['choices'][0]['message']['content']
    # openai 普通账户限制每分钟调用次数为20次
    time.sleep(sleep_time)
    return message

def is_contain_chinese(str):
    for ch in str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def translate_vtt_file(src_path, dst_path):
    # Read the source subtitle file
    with open(src_path, 'r', encoding='utf-8') as f:
        subs = pycaption.WebVTTReader().read(f.read())
    
    # Translate the subtitle text here
    dirty_flag = 0
    global translated_text
    translated_text = ""
    sub_lists = subs.get_captions(subs.get_languages()[0])
    start_idx = next_response_index
    for idx, sub in zip(tqdm(range(len(sub_lists))), sub_lists):
        if idx < start_idx:
            continue
        print("idx, start_idx: ", idx, start_idx)
        print(" raw sub.nodes: ", sub.nodes)
        for node in sub.nodes:
            if('\xa0' == node.content or '' == node.content or None == node.content or is_contain_chinese(node.content)):
                continue 
            src_content = node.content
            # print("dirty_flag / kip_len: ", dirty_flag%skip_len)
            print("src_content: ", src_content)
            if dirty_flag % skip_len == 0:
                try:
                    # Start the timeout function in a separate thread
                    translated_text = translate_text(src_content)
                    # translated_text = src_content
                    node.content = translated_text

                except Exception as e:
                    print("翻译出错：", e)
                    print(f"\x1b[31m请将next_response_index 设置为 {idx} 并重试程序!\x1b[0m")
                    # Write the translated subtitle file
                    with open(dst_path, 'w', encoding='utf-8') as f:
                        f.write(pycaption.WebVTTWriter().write(subs))
                    exit()
            else:
                node.content = translated_text
            print("translated_text: ", translated_text)
            dirty_flag += 1
            
    # Write the translated subtitle file
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write(pycaption.WebVTTWriter().write(subs))

def main(): 
    if not os.path.exists(vtt_dir_dst):
        os.makedirs(vtt_dir_dst)

    list_files = os.listdir(vtt_dir_src)
    for idx, file_name in zip(tqdm(range(len(list_files))), list_files):
        if file_name.endswith(".vtt"):
            src_path = os.path.join(vtt_dir_src, file_name)
            dst_path = os.path.join(vtt_dir_dst, file_name.replace('.en', '.zh'))
            print("src_path: ", src_path)
            print("dst_path: ", dst_path)
            translate_vtt_file(src_path, dst_path)
            print(f"已翻译文件 {file_name}")
            
if __name__ == "__main__":
    main()