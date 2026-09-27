import pymupdf4llm as py

text = py.to_markdown("./dictionary/5000.pdf")
with open("./dictionary/2000.md", 'w' ,encoding='utf-8') as f:
    f.write(text)