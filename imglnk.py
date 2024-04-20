# generate_html.py

# 读取所有的图片链接
with open('imglink.txt', 'r') as file:
    links = [line.strip() for line in file.readlines() if line.strip()]

# 生成HTML内容
html_content = '<html><body>\n'
for link in links:
    html_content += f'<img src="{link}" />\n'
html_content += '</body></html>'

# 将HTML内容写入到一个HTML文件中
with open('images.html', 'w') as html_file:
    html_file.write(html_content)