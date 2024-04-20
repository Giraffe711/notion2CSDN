# 为什么我要写这个东西？

平时我写wp都是在 notion 上面写的，写完想发到csdn的话有一个问题没有解决，那就是图片上传，我从notion上面导出wp到本地，图片都会保存到本地而不是带则图床链接的md文件，所以当上传到csdn上的时候就会有一个非常重复的问题就是图片上传，图片少还好，图片多就是重复劳动- -，很烦，所以想要把notion导出的md文件直接转化图片到csdn图床上。这样在导入md到csdn后直接就能识别。

# upload.yaml





```yaml
id: csdn

info:
  name: upload Photo  To csdn
  author: Someb0dy
  severity: critical
  description: upload Photos  To csdn
  reference:
    - https://github.com/someb0dy
  metadata:
    max-request: 2
  tags: csdn

code:
 -  engine:
      - python3.9
      - py
      - python3
    source: |
      import base64
      import os
      with open(os.environ.get("photo"), "rb") as f:
            data = f.read()
      f.close()
      data = base64.b64encode(data)
      print(data.decode("utf-8"))

http:
  - raw:
      - |
        POST / HTTP/1.1
        HOST: {{Hostname}}
        Sec-Ch-Ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"
        Accept: application/json, text/javascript, */*; q=0.01
        Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryAypgl6336RNmBZ8D
        Sec-Ch-Ua-Mobile: ?0
        User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36
        Sec-Ch-Ua-Platform: "Windows"
        Origin: https://editor.csdn.net
        Sec-Fetch-Site: cross-site
        Sec-Fetch-Mode: cors
        Sec-Fetch-Dest: empty
        Referer: https://editor.csdn.net/
        Accept-Encoding: gzip, deflate
        Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
        Priority: u=1, i
        Connection: close

        ------WebKitFormBoundaryAypgl6336RNmBZ8D
        Content-Disposition: form-data; name="key"

        direct/4f911209f9***************4599862f62.png(here  you need to change it to your upload photo http request)
        ------WebKitFormBoundaryAypgl6336RNmBZ8D
        Content-Disposition: form-data; name="policy"

        eyJl......(here  you need to change it to your upload photo http request)
        ------WebKitFormBoundaryAypgl6336RNmBZ8D
        Content-Disposition: form-data; name="OSSAccessKeyId"

        L......(here  you need to change it to your upload photo http request)
        ------WebKitFormBoundaryAypgl6336RNmBZ8D
        Content-Disposition: form-data; name="success_action_status"

        200
        ------WebKitFormBoundaryAypgl6336RNmBZ8D
        Content-Disposition: form-data; name="signature"

        +/P......(here  you need to change it to your upload photo http request)
        ------WebKitFormBoundaryAypgl6336RNmBZ8D
        Content-Disposition: form-data; name="callback"

        eyJjYWx......(here  you need to change it to your upload photo http request)
        ------WebKitFormBoundaryAypgl6336RNmBZ8D
        Content-Disposition: form-data; name="file"; filename="Untitled 0.png"
        Content-Type: image/png

        {{base64_decode(code_response)}}
        ------WebKitFormBoundaryAypgl6336RNmBZ8D--
    matchers:
      - type: word
        part: body
        words:
          - "imageUrl"
    extractors:
      - type: regex
        part: body
        regex:
          - "\"imageUrl\":\"((.*?))\""

# digest: 4a0a0047304502200a421f68db06c5e48cf053c26220444074867dc6c2942824495546a80578d22b022100f6d6d3e249a691f7a26b16490f65ba854f51664151f585fa456d3f9482baf6aa:cc5eba844f734383650c5b1a2d587ba0
```



这部分的内容通过抓上传图片的包，替换http raw部分，图片的位置继续用  **{{base64_decode(code_response)}}** 占位

# replace.py

```python
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
    
```

# Usage

- Export notion 到本地 (md文件，图片文件夹)
- capture a upload photo http request
- 你需要安装nuclei  Referer: https://github.com/projectdiscovery/nuclei

![img](https://img-blog.csdnimg.cn/direct/73b0ae1d44124b6eb34af7a44655f08d.png)



![image-20240420173052248](https://img-blog.csdnimg.cn/direct/c7e21ce7e0cf47898f012205efab79bf.png)

```http
{"code":200,"data":{"hostname":"https://img-blog.csdnimg.cn/","imageUrl":"https://img-blog.csdnimg.cn/direct/95722********897******.webp","width":"300","targetObjectKey":"direct/95722ee7*********.webp","x-image-suffix":"webp","height":"300"},"msg":"success"}
```

响应就是类似上面这样的一个数据包

你需要把请求的内容除了图片位置继续使用  **{{base64_decode(code_response)}}** 占位 ，其他替换掉upload.yaml 里面http的部分

接下来我们需要给这个模板签名，不然执行不了，每次修改**upload.yaml** 也都需要**签名**

```powershell
nuclei  -code -t upload.yaml -u csdn-img-blog.oss-cn-beijing.aliyuncs.com    -v -sign
```

第一次输入sign 参数，会让你填sign的密码，然后记住每次修改完 upload.yaml，都需要执行一次**sign**



- 前面导出的marddown文件复制一个备份，Mist2.md,修改replace.py 里面的图片路径以及
- 运行 replace.py ,你就会得到一个 _csdn.md 的文件，这个文件可以直接导入到 csdn，这样就可以快乐的玩耍了



## notice

http 上传文件的请求不是一直生效的，是持续一段时间可以上传，如果失效了，重新抓一个包，重新给upload.yaml 签名
签名失败的话，把upload下面哪一行digest 删除重新签名试试



# imglink.py

这个用来放到一个html里面做展示效果