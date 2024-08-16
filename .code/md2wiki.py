import re
import os
import sys

def markdown_to_wiki(markdown_text):
    # Headers
    wiki_text = re.sub(r'###### (.*)', r'====== \1 ======', markdown_text)
    wiki_text = re.sub(r'##### (.*)', r'===== \1 =====', wiki_text)
    wiki_text = re.sub(r'#### (.*)', r'==== \1 ====', wiki_text)
    wiki_text = re.sub(r'### (.*)', r'=== \1 ===', wiki_text)
    wiki_text = re.sub(r'## (.*)', r'== \1 ==', wiki_text)
    wiki_text = re.sub(r'# (.*)', r'= \1 =', wiki_text)

    # Bold
    wiki_text = re.sub(r'\*\*(.*?)\*\*', r"'''\1'''", wiki_text)
    wiki_text = re.sub(r'__(.*?)__', r"'''\1'''", wiki_text)

    # Italic
    wiki_text = re.sub(r'\*(.*?)\*', r"''\1''", wiki_text)
    wiki_text = re.sub(r'_(.*?)_', r"''\1''", wiki_text)

    # Strikethrough
    wiki_text = re.sub(r'~~(.*?)~~', r'<s>\1</s>', wiki_text)

    # Links
    wiki_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'[\2 \1]', wiki_text)

    # Images
    wiki_text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'[[\2|\1]]', wiki_text)

    # Unordered Lists
    wiki_text = re.sub(r'^\* ', r'* ', wiki_text, flags=re.MULTILINE)
    wiki_text = re.sub(r'^- ', r'* ', wiki_text, flags=re.MULTILINE)

    # Ordered Lists
    wiki_text = re.sub(r'^\d+\.', r'#', wiki_text, flags=re.MULTILINE)

    # Blockquotes
    wiki_text = re.sub(r'^> (.*)', r'> \1', wiki_text, flags=re.MULTILINE)

    # Code blocks
    wiki_text = re.sub(r'```\n(.*?)\n```', r'<code>\1</code>', wiki_text, flags=re.DOTALL)

    # Inline code
    wiki_text = re.sub(r'`(.*?)`', r'<code>\1</code>', wiki_text)

    # Horizontal line
    wiki_text = re.sub(r'---', r'----', wiki_text)

    # Escape characters
    wiki_text = re.sub(r'\\([\\`*_{}\[\]()#+\-.!])', r'\1', wiki_text)

    return wiki_text

def convert_markdown_file_to_wiki(input_file):
    # 获取输入文件的目录和文件名
    input_dir = os.path.dirname(input_file)
    input_filename = os.path.basename(input_file)
    
    # 构造输出文件路径
    output_filename = os.path.splitext(input_filename)[0] + '.dokuwiki'
    output_file = os.path.join(input_dir, output_filename)
    
    # 读取Markdown文件
    with open(input_file, 'r', encoding='utf-8') as md_file:
        markdown_text = md_file.read()
    
    # 转换为Wiki语法
    wiki_text = markdown_to_wiki(markdown_text)
    
    # 写入Wiki文件
    with open(output_file, 'w', encoding='utf-8') as wiki_file:
        wiki_file.write(wiki_text)
    
    print(f"Conversion complete. The DokuWiki file has been saved as {output_file}")

if __name__ == '__main__':
    input_markdown_file = r'C:\Users\12262\OneDrive\#成长资料\0_人生沉淀\1_程序与算法\DeepLearning\pytorch\code\Code\md.md'
    convert_markdown_file_to_wiki(input_markdown_file)
    # if len(sys.argv) != 2:
    #     print("Usage: python convert_md_to_wiki.py <input_markdown_file>")
    # else:
    #     input_markdown_file = sys.argv[1]
    #     input_markdown_file = r'C:\Users\12262\OneDrive\#成长资料\0_人生沉淀\1_程序与算法\DeepLearning\pytorch\code\Code\md.md'
    #     convert_markdown_file_to_wiki(input_markdown_file)
