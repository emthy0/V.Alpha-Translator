url="https://lhscan.net/read-sobiwaku-zero-no-saikyou-kenshi-demo-noroi-no-soubi-kawai-nara-9999-ko-tsuke-hodai-raw-chapter-10.html"
def autostrip(url):
    url=url.lstrip('https://lhscan.net/read').rstrip('.html').split('-')
    chap=url[len(url)-1]
    name=''
    for i in range(len(url)-3):
        i+=1
        name+=str(url[i]+'_')
    name=name.capitalize().rstrip('raw_')   
    return name,chap

def lazystrip(urlo):
    url=urlo.lstrip('https://lhscan.net/read').rstrip('.html').split('-')
    chap=url[len(url)-1]
    name=''
    lazyurls=['']
    for i in range(len(url)-3):
        i+=1
        name+=str(url[i]+'_')
    name=name.capitalize().rstrip('raw_') 
    for i in range(int(chap)):
        lazyurl=str(urlo.rstrip(str(chap) +'.html')+str(i+1)+'.html')
        lazyurls.append(lazyurl)
    return name,chap,lazyurls
