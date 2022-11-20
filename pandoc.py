#!/usr/bin/env python3

import os
import shutil
from glob import glob


def process_lines(file, lines, folder):
    for line in lines:
        if line.startswith("!["):
            line = line.split("]")[0] + "](" + folder + line.split("]")[1].lstrip("(")
        elif line.startswith("[!["):
            line = line.split("]")[0] + "](" + folder + "]".join(line.split("]")[1:]).lstrip("(")
        else:
            pass
        file.write(line)
    file.write("\n\n")
    file.write("\\newpage")
    file.write("\n\n")    


TARGET_FOLDER = "_pandoc"     # The folder to store generated files 

if os.path.exists(TARGET_FOLDER):
    shutil.rmtree(TARGET_FOLDER)

os.mkdir(TARGET_FOLDER)

# 第一步 - 处理存在根文件夹下的内容（序，自序等)
# 序，自序等的文件名要以001，002等开头。
# 000保留给书的首页和目录

shutil.copyfile("src/_pandoc.md", TARGET_FOLDER + "/000_title_toc.md")     

files = glob("src/*.md")

for file in files:

    if file.split("/")[-1].startswith("_"):    # 非内容的系统文件，比如 _toc.yml, _config.yml，_pandoc.md
        continue  
    elif file.split("/")[-1] == "index.md":    # 网站首页，不必加入电子版里
        continue
    else:

        target = TARGET_FOLDER + "/" + file.split("/")[-1]
        
        with open(file, "r") as f_read:
            lines = f_read.readlines()

        with open(target, "w") as f_write:

            if not lines[0].startswith("# "):
                f_write.write("# ")

            process_lines(f_write, lines,  "src/")


# 第二步 - 处理存于子文件夹下的正文（各辑，各章)

source_folders = glob("src/*/")

for folder in source_folders:

    if "/_static/" in folder:           # 非内容的网站静态文件存于此文件夹
        continue

    files = glob(folder + "*.md")
    files.sort()

    if not folder + "00.md" in files:   # 存放内容的子文件夹必须有一个 00.md 文件作为该辑的目录
        continue

    chapter_file = TARGET_FOLDER + "/"+ folder.split("/")[1] + ".md"

    if os.path.exists(chapter_file):
        os.remove(chapter_file)

    with open(chapter_file, "a") as f_append:

        for file in files:

            with open(file, "r") as f_read:
                lines = f_read.readlines()

            if not "00.md" in file:
                f_append.write("#")

            process_lines(f_append, lines,  folder)