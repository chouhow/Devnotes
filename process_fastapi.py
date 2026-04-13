import re
import os

def html_to_text(html):
    # Remove script and style tags with content
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Replace common HTML elements with markdown equivalents
    # h1 -> h1
    html = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n', html, flags=re.DOTALL)
    html = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', html, flags=re.DOTALL)
    html = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', html, flags=re.DOTALL)
    html = re.sub(r'<h4[^>]*>(.*?)</h4>', r'\n#### \1\n', html, flags=re.DOTALL)
    
    # Paragraphs
    html = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\1\n', html, flags=re.DOTALL)
    
    # Code blocks - pre/code
    html = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', 
                  lambda m: '\n```python\n' + re.sub(r'<[^>]+>', '', m.group(1)).strip() + '\n```\n', 
                  html, flags=re.DOTALL)
    
    # Inline code
    html = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', html, flags=re.DOTALL)
    
    # Bold
    html = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', html, flags=re.DOTALL)
    
    # Italic
    html = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', html, flags=re.DOTALL)
    html = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', html, flags=re.DOTALL)
    
    # Links
    html = re.sub(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', html, flags=re.DOTALL)
    
    # Lists
    html = re.sub(r'<ul[^>]*>', '\n', html)
    html = re.sub(r'</ul>', '\n', html)
    html = re.sub(r'<ol[^>]*>', '\n', html)
    html = re.sub(r'</ol>', '\n', html)
    html = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', html, flags=re.DOTALL)
    
    # Tables - basic
    def table_to_md(t):
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', t, flags=re.DOTALL)
        lines = []
        for ri, row in enumerate(rows):
            cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, flags=re.DOTALL)
            cells = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
            if cells:
                lines.append('| ' + ' | '.join(cells) + ' |')
                if ri == 0:
                    lines.append('| ' + ' | '.join(['---'] * len(cells)) + ' |')
        return '\n'.join(lines) + '\n'
    
    html = re.sub(r'<table[^>]*>(.*?)</table>', table_to_md, html, flags=re.DOTALL)
    
    # Blockquotes
    html = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1\n', html, flags=re.DOTALL)
    
    # Horizontal rule
    html = re.sub(r'<hr[^>]*/?>', '\n---\n', html)
    
    # Remove all remaining HTML tags
    html = re.sub(r'<[^>]+>', '', html)
    
    # Clean up whitespace
    html = re.sub(r'\n{3,}', '\n\n', html)
    html = html.strip()
    
    return html


def extract_main_content(html):
    """Extract the main tutorial content from the page"""
    # Try to find the main content area
    # The tutorial pages have content in article or main div
    patterns = [
        r'<article[^>]*>(.*?)</article>',
        r'<main[^>]*>(.*?)</main>',
        r'<div[^>]*class="[^"]*article[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, html, flags=re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1)
    
    # Fallback: remove nav/header/footer
    cleaned = re.sub(r'<nav[^>]*>.*?</nav>', '', html, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'<header[^>]*>.*?</header>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'<footer[^>]*>.*?</footer>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    return cleaned


def process_page(num, title_cn):
    with open(f"E:/page_{num}.html", encoding="utf-8") as f:
        html = f.read()
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    page_title = title_match.group(1) if title_match else ""
    
    # Extract h1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    h1 = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else page_title
    
    # Extract main content
    content = extract_main_content(html)
    
    # Convert to markdown
    md = html_to_text(content)
    
    # Build full document
    doc = f"# {title_cn}\n\n"
    doc += f"> 原文：https://fastapi.tiangolo.com/tutorial/\n\n"
    doc += md
    
    return doc


pages = [
    ("21", "FastAPI 21 - 查询参数字符串验证 (Query Parameters String Validations)"),
    ("22", "FastAPI 22 - 路径参数数值验证 (Path Parameters Numeric Validations)"),
    ("23", "FastAPI 23 - 请求体多个参数 (Body - Multiple Parameters)"),
    ("24", "FastAPI 24 - 请求体字段 (Body - Fields)"),
    ("25", "FastAPI 25 - 请求体嵌套模型 (Body - Nested Models)"),
]

output_dir = "E:/BaiduSyncdisk/DevDocs/FastAPI"
os.makedirs(output_dir, exist_ok=True)

for num, title in pages:
    print(f"Processing page {num}...")
    doc = process_page(num, title)
    
    out_file = os.path.join(output_dir, f"FastAPI_{num}_*.md".replace("*", title.split(" - ")[1].split(" ")[0] + "_" + title.split(" - ")[2] if False else ""))
    
    # Generate filename
    filenames = {
        "21": "FastAPI_21_查询参数字符串验证_Query_Params_Str_Validations.md",
        "22": "FastAPI_22_路径参数数值验证_Path_Params_Numeric_Validations.md",
        "23": "FastAPI_23_请求体多个参数_Body_Multiple_Params.md",
        "24": "FastAPI_24_请求体字段_Body_Fields.md",
        "25": "FastAPI_25_请求体嵌套模型_Body_Nested_Models.md",
    }
    out_path = os.path.join(output_dir, filenames[num])
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"Written: {out_path} ({len(doc)} chars)")
