import html

PRISM_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Prism Syntax Highlighted Python Code</title>
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-atom-dark.min.css" rel="stylesheet" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<style>
  body {{
    background-color: #282c34;
    color: #abb2bf;
    font-family: Consolas, monospace;
    padding: 2rem;
  }}
  .code-container {{
    max-width: 900px;
    margin: auto;
  }}
</style>
</head>
<body>
  <h1>Python Code with Prism Syntax Highlight</h1>
  <div class="code-container">
    <pre><code class="language-python line-numbers">{escaped_code}</code></pre>
  </div>
</body>
</html>
'''

def main():
    print("Paste your Python code below. End input with an empty line (just press Enter twice):")
    lines = []
    while True:
        line = input()
        if line == '':
            break
        lines.append(line)
    code = "\n".join(lines)
    
    escaped_code = html.escape(code)
    html_output = PRISM_TEMPLATE.format(escaped_code=escaped_code)
    
    print("\n\n--- Generated HTML ---\n")
    print(html_output)

if __name__ == '__main__':
    main()
