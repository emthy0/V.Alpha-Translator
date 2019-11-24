import os
def dl_step(laziness):
    os.chdir('./src')
    if laziness=='lazy':
        os.chdir('./jpn')
        url = str(input('Please enter lhscan index url here : '))
        chaps = int(input('Since Chap :'))
        lazy_name,lazy_chap,urls=lazystrip(url)
        if not os.path.exists(lazy_name):
            os.makedirs(lazy_name)
        os.chdir(lazy_name)
        for i in range((lazy_chap - int(chaps))):
            i+=int(chaps)
            if not os.path.exists(i):
                os.makedirs(i)
            os.chdir(i)
            src_download(urls[i])
            os.chdir('..')
        exit()
    elif laziness == 'diligent':
        fullpath='./src'
        lang=''
        state=0
        while state < 3:                                               #menu
            while state==0:
                while lang.count('')!=4:
                    lang_path,lang,fullpath,state=menu('lang',fullpath,state)
                    if lang.count('')!=4:print('Only 3-Char Language code allow')

            while state==1: 
                src_title_path,title,fullpath,state=menu('Manga name',fullpath,state)
            while state==2:
                src_chap_path,chap,fullpath,state=menu('Chapter',fullpath,state)
            print('Working on ',os.getcwd())
    else:
        url = str(input('Please enter your lhscan url here : '))
        auto_name,auto_chap=autostrip(url)
        ck=('./jpn/'+auto_name+'/'+auto_chap)
        if os.path.exists(ck): 
            print('Already Downloaded')
            print('Entering Downloaded Dir')
            os.chdir(ck)
            print('Working on ',os.getcwd())
            lang='jpn'
        else:
            print('Do you want to use auto generate source folder:')
            print('/src/jpn/',auto_name,'/',auto_chap,'/')
            dirmode=str(input('(y/n)'))
            if dirmode=='y':
                lang='jpn'
                os.chdir('./jpn')
                if not os.path.exists(auto_name):
                    os.makedirs(auto_name)
                os.chdir(auto_name)
                if not os.path.exists(auto_chap):
                    os.makedirs(auto_chap)
                    os.chdir(auto_chap)
                print('Working on ',os.getcwd())
            else:
                fullpath='./src'
                lang=''
                state=0
                while state < 3:                                               #menu
                    while state==0:
                        while lang.count('')!=4:
                            lang_path,lang,fullpath,state=menu('lang',fullpath,state)
                            if lang.count('')!=4:print('Only 3-Char Language code allow')
                    while state==1: 
                        src_title_path,title,fullpath,state=menu('Manga name',fullpath,state)
                    while state==2:
                        src_chap_path,chap,fullpath,state=menu('Chapter',fullpath,state)
                    print('Working on ',os.getcwd())
            src_download(url)
    return lang