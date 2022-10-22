def getTextOnly(soup):
    v = soup.text
    if v == None:
        c = soup.contents
        resulttext = ''
        for t in c:
            subtext = getTextOnly(t)
            resulttext += subtext + '\n'
        return resulttext
    else:
        return v.strip()