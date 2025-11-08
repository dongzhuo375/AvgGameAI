import os

_stories_path : str = None
_end_text : str = None

def get_stories(newest_first=True):
    stories_path = _stories_path
    filenames = []

    if not os.path.exists(stories_path):
        print(f"错误：目录 '{stories_path}' 不存在")
        return filenames

    file_info = []
    for filename in os.listdir(stories_path):
        file_path = os.path.join(stories_path, filename)
        if (os.path.isfile(file_path) and
                (filename.endswith('.yaml') or filename.endswith('.yml'))):
            name_without_extension = os.path.splitext(filename)[0]
            mtime = os.path.getmtime(file_path)
            file_info.append((name_without_extension, mtime, filename))

    file_info.sort(key=lambda x: x[1], reverse=newest_first)
    filenames = [name for name, mtime, filename in file_info]

    return filenames

def set_storise_path(file: str):
    global _stories_path
    _stories_path = file

def get_stories_path():
    return  _stories_path

def set_end_text(text: str):
    global _end_text
    _end_text = text

def get_end_text():
    return  _end_text