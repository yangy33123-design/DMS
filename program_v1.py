

import subprocess
import pygame.mixer
import pygame.time
import threading

# 创建一个字典来跟踪各关键字符串的锁
lock_dict = {}


def play_mp3(file_path, keyword):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    # 释放锁
    lock_dict[keyword].release()


def monitor_program_a_output(process, keywords_to_mp3):
    for line in process.stdout:
        print(line, end="")  # 打印程序A的输出
        for keyword, mp3_path in keywords_to_mp3.items():
            if keyword in line and lock_dict[keyword].acquire(blocking=False):
                threading.Thread(target=play_mp3, args=(mp3_path, keyword)).start()


def run_program_a_and_monitor():
    # 定义关键字符串及其对应的MP3文件路径
    keywords_to_mp3 = {
        "phone-phone-phone": r'D:\YY\yolov5-7.0\MP3\打电话.mp3',
        "sleep-sleep-sleep": r'D:\YY\yolov5-7.0\MP3\睡觉.mp3',
        "smoke-smoke-smoke": r'D:\YY\yolov5-7.0\MP3\抽烟.mp3',
        "turn-turn-turn": r'D:\YY\yolov5-7.0\MP3\看前方.mp3',
        "yawn-yawn-yawn": r'D:\YY\yolov5-7.0\MP3\打起精神.mp3',
        # 可以添加更多的关键字符串及其对应的MP3文件
    }

    # 为每一个关键字符串初始化一个锁
    for keyword in keywords_to_mp3:
        lock_dict[keyword] = threading.Lock()

    # 启动programA.py并获取其输出
    process = subprocess.Popen(["python", "detect_v1.py"], stdout=subprocess.PIPE, text=True, encoding='utf-8',
                               bufsize=1, universal_newlines=True)

    # 使用一个线程监视程序A的输出，以便可以并行地播放MP3文件
    monitor_thread = threading.Thread(target=monitor_program_a_output, args=(process, keywords_to_mp3))
    monitor_thread.start()

    # 等待程序A完成
    process.wait()

    # 确保监视线程也已完成
    monitor_thread.join()


if __name__ == "__main__":
    run_program_a_and_monitor()
