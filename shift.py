

import re
import io
import argparse
from sys import stdout
from os import path,rename,remove

def textfont(gs,c,s,f):
    tag=re.compile('<[^>]*>')
    ftag=['<font']
    if c: ftag.append(' color="%s"'%(c,))
    if s: ftag.append(' size="%s"'%(s,))
    if f: ftag.append(' face="%s"'%(f,))
    ftag.append('>%s</font>')
    ftag=''.join(ftag)

    ls=[]
    for g in gs:
        g=tag.sub('',g)
        ls=g.split('\n')
        
        
        ls=[ftag%(ls[i],) if i>1 and i<len(ls)-2 else ls[i] 
            for i in range(len(ls))]
        yield '\n'.join(ls)
        del ls[:]

def tomilisecs(text):

    h,m,s,ms=map(lambda x:int(x),re.split(',|:',text))
    return ms+s*1000+m*60*1000+h*3600*1000

def totimecode(ms):
    ms=int(ms)
    h=int(ms/(3600*1000))
    m=int((ms-h*3600*1000)/(60*1000))
    s=int((ms-h*3600*1000-m*60*1000)/1000)
    ms=ms%1000
    return '%02d:%02d:%02d,%03d'%(h,m,s,ms)


def shiftmilisecs(f,ms):
    with io.open(f,'r',encoding='utf8') as f:
        ls=[]
        for l in f:
            ls.append(l)
            if l=='\n':
                t1,t2=ls[1].split(' --> ')
                ls[1]='%s --> %s\n'%(
                    totimecode(tomilisecs(t1)+ms),
                    totimecode(tomilisecs(t2)+ms)) 
                yield ''.join(ls)
                del ls[:]

def shiftsecs(f,s):
    for g in shiftmilisecs(f,s*1000):
        yield g

def writesrt(gs,f,k):
    destfile='%s.renamed%s'%path.splitext(f)
    with io.open(destfile,'w',encoding='utf8') as d:
        for g in gs:
            d.write(g)
    if k:
        stdout.write('\033[92m[done]:\033[0m %s\n'%(destfile))
    else:
        remove(f)
        rename(destfile,f)
        stdout.write('\033[92m[done]:\033[0m %s\n'%(f))

if __name__=='__main__':
    
    p=argparse.ArgumentParser()
    p.add_argument('file',nargs='+')
    g=p.add_mutually_exclusive_group()
    g.add_argument(
        '-s',
        '--secs',
        help='number of seconds to be shifted',
        type=int,
        default=0)
    g.add_argument(
        '--milisecs',
        help='number of miliseconds to be shifted',
        type=int,
        default=0)
    p.add_argument(
        '--colour',
        type=str,
        default='#ffccff')
    p.add_argument(
        '--size',
        type=str,
        default=None)
    p.add_argument(
        '--face',
        type=str,
        default='Courier New')
    p.add_argument(
        '--keep-original',
        action='store_true',
        dest='keeporiginal')


    args=p.parse_args()
    
    from signal import signal,SIGPIPE,SIG_DFL
    signal(SIGPIPE,SIG_DFL)
    
    for f in args.file: 
        action=shiftmilisecs(
            f,
            args.secs*1000 if args.secs else args.milisecs)
        if args.colour or args.size or args.face:
            action=textfont(action,args.colour,args.size,args.face)
    
        writesrt(action,f,args.keeporiginal)




