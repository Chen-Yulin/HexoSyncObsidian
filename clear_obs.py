import os
import shutil
post_path = os.path.expanduser('~')+'/Hexo/source/_posts/'
def clear_obs_content(dir):
    # 检查目标目录是否存在
    if not os.path.exists(dir):
        print(f"目录 {dir} 不存在。")
        return

    # 遍历目录下的所有文件和文件夹
    for item in os.listdir(dir):
        item_path = os.path.join(dir, item)

        # 检查是否以 [OBS] 开头
        if item.startswith("[OBS]"):
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)  # 删除文件夹及其内容
                print(f"文件夹 {item_path} 已删除。")
            elif os.path.isfile(item_path):
                os.remove(item_path)  # 删除文件
                print(f"文件 {item_path} 已删除。")
clear_obs_content(post_path)
