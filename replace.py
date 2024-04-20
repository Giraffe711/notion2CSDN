import os
import re

def findPhotoLink():
     # 定义正则表达式，用于匹配imageUrl的值
    regex = r'"imageUrl":"(https?://[^"]+)"'

    # 计算目标文件的绝对路径（假设你的脚本位于某个路径下）
    script_dir = os.path.dirname(__file__)  # 获取当前脚本的路径
    target_path = os.path.join(script_dir, ".\output\http\csdn_img_blog_oss_cn_beijing_aliyuncs_com_csdn.txt")  # 请替换your_target_file.json为实际的文件名


    try:
        with open(target_path, "rb") as file:
            file_content = file.read().decode("utf-8",'ignore')
        file.close()
        # 使用正则表达式搜索匹配的URL
        matches = re.findall(regex, file_content)
        if matches:
            # 提取匹配的第一个组（即圆括号中的部分）作为imageUrl
            # print("Found URL:", matches)
            a=1
        else:
            print("No matching URL found.")

    except FileNotFoundError:
        print("File not found. Please check the path:", target_path)
    return matches

def uploadPhoto(photopath):
    #photopath = "Mist"
    for filename in os.listdir(photopath):
         os.environ['photo']=f"{photopath}/{filename}"
         cmd = f"nuclei  -code -t upload.yaml -u csdn-img-blog.oss-cn-beijing.aliyuncs.com  -v -sresp"
         os.system(cmd)
    

def replaceMarkdown(l,MarkdownFile):
    regex = r'!\[.*?\]\(.*?\)'
    try:
        with open(f"{MarkdownFile}","rb") as f:
            file_content = f.read().decode("utf-8",'ignore')
        f.close()
        # print(file_content)
        matches = re.findall(regex,file_content)
        if matches:
            # print(matches)
            # print(matches,l)
            for i in range(len(matches)):
                img = f'![img]({l[i]})'
                # print(f"matches[i]={matches[i]}")
                # print(f"img={img}")
                # print(file_content)
                file_content = file_content.replace(matches[i],img)
            with open(MarkdownFile.replace(".md","_csdn.md"),"w",encoding='utf-8') as f:
                f.write(file_content)
        else:
            print("no match")
    except   Exception as e:
        print(f"Can't open {str(e)}")


if __name__ == "__main__":
    try:
        photoPath = "Mist"
        uploadPhoto(photoPath)
        l = findPhotoLink()
        markDownFile = "Mist2.md"
        replaceMarkdown(l,markDownFile)
    except Exception e:
        print(str(e))
    