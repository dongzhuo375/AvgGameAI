import os

def get_stories(stories_path ):
    print(stories_path)
    filenames = []

    # 检查目录是否存在
    if not os.path.exists(stories_path):
        print(f"错误：目录 '{stories_path}' 不存在")
        return filenames

    for filename in os.listdir(stories_path):
        # 确保是文件而不是目录
        file_path = os.path.join(stories_path, filename)
        if os.path.isfile(file_path):
            # 分割文件名和扩展名，只取文件名部分
            name_without_extension = os.path.splitext(filename)[0]
            filenames.append(name_without_extension)

    return filenames
