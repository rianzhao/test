# Feature Engineering Practice

# 如何选择特征 ： https://www.zhihu.com/question/28641663

# 如何清理数据： https://www.zhihu.com/question/22077960

# 数据清理练习1： 观察RESOURCE里的文件，按照几个原则，分别列出你所观察到的需要清理的数据

# 数据清理练习2： 用语音识别的库，模仿用户，录入10段左右的语音，尽可能模拟不同情况，并保存到数据库，分析一下录入结果可能出现的需要清理的内容

# 选择特征练习1： 为电影评分预测系统选择合适的特征，并说明这些特征是如何选择的

# 选择特真练习2： 通过搜索客户电话样本的分析，列出可能提取出的特征，并说明打算如何分析特征。

#1：无用数据：video release date and IMDb URL and timestamp
#   完整性: data that missing parts like user_id, item_id, rating, age or gender or occupation
#   唯一性：same data (same user_id item_id and rating)
#   合法性：data with unreasonable age, rating not in 1 to 5.

#2: 录入结果：无法对中文进行转换，英文转换不准确 （可能与音频中口音有关），暂时不知道如何解决

#3: rating, age , gender, occupation and genre
#   通过已有数据中，不同类型的电影的评分，打分人群的职业，性别，年龄分析计算出 新电影在某地区的评分预测
#   可能需要该地区的人群的性别，职业，年龄数据 例如男性多少 女性多少 不同年龄段多少人

#4: 以银行业客服电话为例，人工服务音频中客户的需求，分析此需求的需求量，判断有无将该需求加入到自动服务中。


import speech_recognition as sr
from os import path
import sys
from database import *


class SpeechRecognitionResult(BaseModel):
    __tablename__ = "speech_recognition_result"
    msg_id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    file_name = Column(String(255))
    msg = Column(String(255))


class SpeechRecognitionResultDBExecutor(CommonDBExecutor):
    def __init__(self, db_url=""):
        if not db_url:
            db_url = get_db_uri()
        super(SpeechRecognitionResultDBExecutor, self).__init__(
            db_url=db_url, table=SpeechRecognitionResult)


def process_audio(audio, r, lan):
    ret = False
    msg = ""
    if audio is None:
        print(f"Failed to read audio.")

    try:
        msg = r.recognize_sphinx(audio, language=lan)
        print(
            f"Spinx thinks you said: {msg}.")
        ret = True
    except sr.UnknownValueError:
        print("Spinx could not understand audio.")
    except sr.RequestError as e:
        print(f"Spinx error {e}")
    return ret, msg


def process_audio_from_file(filepath, lan):
    ret = False
    print(f"Begin to do speech recognition with {filepath}...")
    r = sr.Recognizer()
    audio = None
    with sr.AudioFile(filepath) as source:
        audio = r.record(source)
        ret, msg = process_audio(audio, r, lan)
    return ret, msg


def process_audio_from_microphone(lan):
    ret = False
    print(f"Begin to do speech recognition with microphone...")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say:")
        audio = r.listen(source)
        ret, msg = process_audio(audio, r, lan)
    return ret, msg


if __name__ == '__main__':
    chinese_audio_list = ["中文1到10_1.wav",
                          "中文1到10_2.wav", "中文是不是_1.wav", "中文是不是_2.wav", "混合中文1.wav"]
    english_audio_list = ["英文1到10_1.wav",
                          "英文1到10_2.wav", "英文是不是_1.wav", "英文是不是_2.wav", "混合英文1.wav"]
    db = SpeechRecognitionResultDBExecutor()
    for caudio in chinese_audio_list:
        ret, msg = process_audio_from_file(path.join(path.dirname(
            path.realpath(__file__)), "res", caudio), "zh-CN")
        if ret:
            db.insert(file_name=caudio, msg=msg)
        else:
            print(f"Failed to get message with audio {caudio}")
    for eaudio in english_audio_list:
        ret, msg = process_audio_from_file(path.join(path.dirname(
            path.realpath(__file__)), "res", eaudio), "en-US")
        if ret:
            db.insert(file_name=eaudio, msg=msg)
        else:
            print(f"Failed to get message with audio {eaudio}")







