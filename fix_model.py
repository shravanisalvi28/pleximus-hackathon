content = open('agent.py', encoding='utf-8').read()
content = content.replace('model: str = "gemini-2.5-flash"', 'model: str = "gemini-3.6-flash"')
open('agent.py', 'w', encoding='utf-8').write(content)
if 'gemini-3.6-flash' in content:
    print('SUCCESS: model is now gemini-3.6-flash')
else:
    print('ERROR: model not updated')
