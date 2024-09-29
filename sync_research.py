import os
import shutil
import yaml
import re

obsidian_path = os.path.expanduser('~')+'/Desktop/ResearchPlanet/'
hexo_path = os.path.expanduser('~')+'/Hexo/source/_obsidian/'
post_path = os.path.expanduser('~')+'/Hexo/source/_posts/'

print("Target path: "+hexo_path)

ignore = [".git", ".gitignore", ".obsidian", "template"]

validTagsForThumbnail = ["Unity","nvim", "hexo", "debate", "AI", "python", "Reading"]

def replace_image_syntax(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式替换 ![[Pasted image xxxx.png]] 为 ![](Pasted image xxxx.png)
    updated_content = re.sub(r'!\[\[(.*?\.png)\]\]', r'![](\1)', content)
    updated_content = re.sub(r'!\[\[(.*?\.jpg)\]\]', r'![](\1)', updated_content)
    updated_content = re.sub(r'!\[\]\((.+?)\)', lambda match: f"![]({match.group(1).replace(' ', '_')})", updated_content)

    # 将替换后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

def modifyFrontMatter(dir):
    res_line = ""
    with open(dir, 'r') as f:
        lines = f.readlines()
        i = 0
        while lines[i].strip() != '---':
            i += 1
        i += 1
        front_matter = ''
        while lines[i].strip() != '---':
            front_matter += lines[i]
            i += 1
        data = yaml.safe_load(front_matter)
        data['title'] = data['id']
        del data['id']
        data['toc'] = True

        # assign thumbnail and cover based on tags
        if data['tags'] is not None:
            for tag in data['tags']:
                if tag in validTagsForThumbnail:
                    data['thumbnail'] = "/thumb/"+tag+".png"
                    data['cover'] = "/gallery/"+tag+".png"
                    break

        front_matter = yaml.safe_dump(data)
        res_line = ['---\n'] + [line + '\n' for line in front_matter.split('\n')] + ['---\n'] + lines[i+1:]
        #print(res_line)
    with open(dir, 'w') as f:
        f.writelines(res_line)

def copy_files(src_dir, dst_dir, depth = 0):
    updated = False
    for entry in os.scandir(src_dir):
        if entry.name not in ignore:
            print("\t"*depth + "Get " + entry.name + " in " + str(src_dir))
            src_path = os.path.join(src_dir, entry.name)
            dst_path = os.path.join(dst_dir, entry.name)
            if entry.is_file() and entry.name.endswith('.md'):
                os.makedirs(os.path.dirname(dst_path),exist_ok=True)
                if not os.path.exists(dst_path) or os.path.getmtime(src_path) > os.path.getmtime(dst_path):
                    shutil.copy2(src_path, dst_path)
                    modifyFrontMatter(dst_path)
                    replace_image_syntax(dst_path)
                    print("\t"*depth + "Update file")
                    updated = True
                else:
                    print("\t"*depth + "Duplicated file")
            elif entry.is_file() and (entry.name.endswith('.jpg') or entry.name.endswith('.png')): # photos
                os.makedirs(os.path.dirname(dst_path),exist_ok=True)
                if not os.path.exists(dst_path) or os.path.getmtime(src_path) > os.path.getmtime(dst_path):
                    shutil.copy2(src_path, dst_path)
                    print("\t"*depth + "Update img")
                    updated = True
                else:
                    print("\t"*depth + "Duplicated img")
            elif entry.is_dir():
                print("\t"*depth + "SubDir, Go deeper")
                copy_files(src_path, dst_path, depth+1)
    return updated

def copy_imgs(src_dir, dst_dir):
    # 检查源文件夹是否存在
    if not os.path.exists(src_dir):
        return

    # 如果目标文件夹不存在，则创建它
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # 复制所有文件和文件夹
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)

        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)
            if ' ' in src_path:
            # 生成新文件名，将空格替换为下划线
                new_item_name = item.replace(' ', '_')
                old_file_path = dst_path
                new_file_path = os.path.join(dst_dir, new_item_name)

                # 重命名文件
                os.rename(old_file_path, new_file_path)





def migrate_files(src_dir, dst_dir, prefix = "[OBS]"):
    for entry in os.scandir(src_dir):
        src_path = os.path.join(src_dir, entry.name)
        entry_root, _ = os.path.splitext(entry.name)
        dst_path = os.path.join(dst_dir, prefix + entry.name)
        src_img_path = os.path.join(src_dir, "img")
        dst_img_path = os.path.join(dst_dir, prefix + entry_root)
        if entry.is_file() and entry.name.endswith('.md'):
            os.makedirs(os.path.dirname(dst_path),exist_ok=True)
            shutil.copy2(src_path, dst_path)
            copy_imgs(src_img_path, dst_img_path)
        elif entry.is_dir():
            migrate_files(src_path, dst_dir, prefix + entry.name + "-")
if os.path.exists(hexo_path):
    shutil.rmtree(hexo_path)
updated = copy_files(obsidian_path, hexo_path)
migrate_files(hexo_path, post_path)
