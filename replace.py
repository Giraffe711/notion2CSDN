import os
import re
oss_target = "csdn-img-blog.obs.cn-north-4.myhuaweicloud.com"
ossResultFile = oss_target.replace("-","_").replace(".","_") + "_csdn"
print(ossResultFile)

def findPhotoLink():
     # 定义正则表达式，用于匹配imageUrl的值
    regex = r'"imageUrl":"(https?://[^"]+)"'

    # 计算目标文件的绝对路径（假设你的脚本位于某个路径下）
    script_dir = os.path.dirname(__file__)  # 获取当前脚本的路径
    
    target_path = os.path.join(script_dir, f"output{os.sep}http{os.sep}{ossResultFile}.txt")  # 请替换your_target_file.json为实际的文件名


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
# 自定义排序键函数
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def uploadPhoto(photopath):
    #photopath = "Mist"
    l = os.listdir(photopath)
    l.sort(key=natural_sort_key)
    for filename in l:
        # print(filename)
         os.environ['photo']=f"{photopath}/{filename}"
         cmd = f"nuclei  -code -t upload.yaml -u csdn-img-blog.oss-cn-beijing.aliyuncs.com  -v -sresp"
         cmd = cmd.replace("csdn-img-blog.oss-cn-beijing.aliyuncs.com",f"{oss_target}")
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
            # print(len(matches))
            with open ("imglink.txt","w") as ff:
                for i in l:
                    ff.write(i+"\n")
            ff.close()
            # print(len(l))
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
        photoPath = "../wp/MonitorsThree 6451ca5678634577a0cab77daf1d55fc"
        # uploadPhoto(photoPath)
        l = findPhotoLink()
        markDownFile = "../wp/MonitorsThree 6451ca5678634577a0cab77daf1d55fc.md"
        replaceMarkdown(l,markDownFile)
    except Exception as e:
        print(str(e))
    