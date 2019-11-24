# -*- coding: utf-8 -*- 
import os

def menu(title,root,state):
    hold=1
    while hold ==1:
        print('Please select '+str(title))
        if title =='lang': root='./src'
        #get sub directory
        subd=[]
        for i,j,k in os.walk('.',topdown = True):
            subd=subd+j   
            break 

        #create menu
        for i in range(len(subd)):                      
            print(('\t'+str(i+1)+'.'+subd[i]))
        print('\n')
        target=input('Pick a folder Number from the menu (enter n to create New folder) :')
        crn=''
        try: target2=int(target)
        except ValueError :target2=-1
        
        if  (target2-1 in range(len(subd))) :           #Succeed path
            path='./'+subd[target2-1]
            fullpath=root+'/'+subd[target2-1]
            print('PATH is set to " '+fullpath+'"')
            os.chdir(path)
            state+=1
            return path,subd[target2-1],fullpath,state
            hold=0        
        elif (target2 == 0) and (state >= 1):      #go back
            os.chdir('..')
            state-=1
            return 0,0,0,state
            hold=0
        #Uncompleted path
        elif target !='n':                              #Dir not exist
            print('Directory does not exist.')
        crn=str(input('Do you want to create new source directory. (y/n) : '))
        if crn == 'y' :
            newname=str(input('enter new directory name:'))
            if not os.path.exists(newname):
                os.makedirs(newname)
            elif os.path.exists(newname):print('DIR existed')
        else:continue      
