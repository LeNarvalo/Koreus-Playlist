# -*- coding: utf8 -*-
from urllib.request import urlopen
import os


pages = ['https://www.koreus.com/modules/newbb/topic209914.html',\
'https://www.koreus.com/modules/newbb/topic177927.html',\
'https://www.koreus.com/modules/newbb/topic77103.html',\
'https://www.koreus.com/modules/newbb/topic143074.html',\
'https://www.koreus.com/modules/newbb/topic126052.html',\
'https://www.koreus.com/modules/newbb/topic62907.html',\
'https://www.koreus.com/modules/newbb/topic132078.html',\
'https://www.koreus.com/modules/newbb/topic112261.html',\
'https://www.koreus.com/modules/newbb/topic104340.html',\
'https://www.koreus.com/modules/newbb/topic93040.html',\
'https://www.koreus.com/modules/newbb/topic165556.html',\
'https://www.koreus.com/modules/newbb/topic83478.html',\
'https://www.koreus.com/modules/newbb/topic118285.html',\
'https://www.koreus.com/modules/newbb/topic154790.html']

members = {}
chemin = os.path.expanduser('~\Liste des écoutes')
path = chemin+'\\log.txt'
LAST_TOPIC = 0

def first_time():
    global LAST_TOPIC
    for page in pages:
        p = urlopen(page)
        content= p.read().decode('utf-8')
        last = int(content.split('...')[1].split('</a>')[0].split('>')[1])
        topic_num = page.split('topic')[1]
        topic_num = int(topic_num[:topic_num.index('.html')])
        if topic_num > LAST_TOPIC:
            LAST_TOPIC = topic_num
        LAST_FP = 0
        LAST_PAGE = 0
        for i in range(last):
            URL = page.split('.html')[0]+'-'+str(i*20)+'.html'
            p = urlopen(URL)
            #print(url)
            contenu= p.read().decode('utf-8')
            SPLIT = contenu.split('<a rel="nofollow" href="/membre/')[1:]
            for m in SPLIT:            
                member = m[m.index('>')+1:m.index('</a>')]
                
                fp = m.split('href="#forumpost')[1]
                fp_num = int(fp[:fp.index('">')])
                fp = '#forumpost'+str(fp_num)
                
                do(fp, fp_num, member, m, LAST_PAGE, LAST_FP, LAST_TOPIC, topic_num, URL, i, last)

    for member in members:
        write_member_log(member)

def do(fp, fp_num, member, m, L_P, L_F, L_T, topic_num, URL, i, last):
    global members
    if member not in members:
        members[member]=[]#{'video':'','txt':'','img':'','url':'','where':''}
        
    TEXT = m.split('<div class="comText">')[1]
    TEXT = TEXT[:TEXT.index('<br clear="all" />')]            
    for x in ['</blockquote>']:
        TEXT = TEXT.replace(x,'')
    
    videos = []
    if '<iframe' in TEXT:
        for link in TEXT.split('<iframe')[1:]:
            src = link.split('src="')[1]
            src = 'src="'+src.split('"')[0]+'" '
            video = '<iframe '+src+'></iframe>'
            text=''
            if '<br />' in link:
                text = link.split('<br />')[1]
                text = text.split('</div>')[0]
            videos.append([video,text])
    
    imgs = []
    if '<a href="' in TEXT:
        for link in TEXT.split('<a href="')[1:]:
            if '<img' in link and not "image-invalide.png" in link and not "ipfs" in link and not 'gif' in link:
                img = link.split('<img')[1]
                img = img[:img.index('>')]
                src = img.split('src="')[1]
                src = src[:src.index('"')]
                src = src.replace(r"https://koreus.cdn.li/low/imgmu/",r"https://k.img.mu/")
                if '-' in src:
                    src = src[:src.index('-')]+src[-4:]
                    img = '<img src="'+src+'" >'
                    url = link[:link.index('">')]
                    imgs.append([img,url])
                    #print(link, src)

    
    for obj in videos:
        members[member].append({'video':obj[0],'txt':obj[1],'img':'','url':'','where':URL+fp})
    for obj in imgs:
        members[member].append({'video':'','txt':'','img':obj[0],'url':obj[1],'where':URL+fp})
    
    if i == last-1:
        if fp_num > L_F and topic_num == L_T:
            L_F = fp_num
            L_P = i+1
            #print('new fp',L_F)
            write_log([URL+fp,str(L_T),str(L_P),str(L_F)])

def write_log(liste):
    file = open(path,'w',encoding='utf-8')
    for x in liste:
        file.write(x+'\n')
    file.close()

def watch(member=members.keys()):
    PATH = chemin+'\\'+member
    
    pages = int(len(members[member])/20)
    if len(members[member]) % 20 != 0:
        pages += 1

    head1 = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<table>
<thead>
        <tr>
            <th colspan="4">'''
    if pages == 1:
        head2 = member
        head3 = ""
    else:
        head2 = member
        head2 += '   <a href="'+PATH+'\\'+str(2)+'.html"> > </a>   '
        head2 += '<a href="'+PATH+'\\'+str(pages-1)+'.html"> >| </a>'
        head3 = '''   <select onchange='location.href="'''+PATH.replace('\\','/')+'''/"+this.value;'>'''
        for x in range(1,pages+1):
            if x == 1:
                head3+='''<option value="'''+str(x)+'''.html"  selected>'''+str(x)+'''</option>'''
            else:
                head3+='''<option value="'''+str(x)+'''.html"  noselect>'''+str(x)+'''</option>'''
        head3 += '''</select>'''

    head4 = '''</th>
        </tr>
</thead>
</table>
<style>
table {
    width:100%;
    table-layout: fixed;
}
table, th, td {
    word-wrap:break-word;
    text-align:center;
    border: 0px solid black;
    border-collapse: collapse;
}

.equalDivide tr td { width:25%; }

img {max-height:100%; max-width:100%}

a { text-decoration: none; }

</style>
<table id="t01">

<tbody>
'''
    
    txt=head1+head2+head3+head4
    second_line = []
    page = 1
    for i,x in enumerate(members[member],start=1):
        if i == 1:
            txt+='<tr>\n'
        if x['video']!='':
            txt+='<td>'+x['video']+'</td>\n'
            second_line.append(x['txt'])
        elif x['img']!='' and x['url']!='':
            txt+='<td><a href="'+x['url']+'">'+x['img']+'</a></td>\n'
            second_line.append(x['url'])
        if i%4 == 0:
            txt+='</tr>\n<tr>\n'
            for z in second_line:
                txt+='<td>'+z+'</td>\n'
            txt+='</tr>\n'
            second_line=[]
        if i % 12 == 0 or i == len(members[member]):            
            txt += '<br>\n'            
            txt += '\n</tbody></table>'
            file = open(PATH+'\\'+str(page)+'.html','w',encoding='utf-8')
            file.write(txt)
            file.close()
            page += 1
            head2  = '<a href="'+PATH+'\\'+str(1)+'.html"> |< </a>   '
            head2 += '<a href="'+PATH+'\\'+str(page-1)+'.html"> < </a>   '
            head2 += member
            if page < pages:
                head2 += '   <a href="'+PATH+'\\'+str(page+1)+'.html"> > </a>'
                head2 += '   <a href="'+PATH+'\\'+str(pages)+'.html"> >| </a>'
                
            head3 = head3.replace('noselect','selected',1)
            txt=head1+head2+head3+head4
    
    os.startfile(PATH+'\\1.html')

def write_member_log(member):
    PATH = chemin+'\\'+member

    if not os.path.exists(PATH):
        os.mkdir(PATH)
        
    file = open(PATH+'\\log.txt',"w",encoding='utf-8')
    for x in members[member]:
        file.write('Video_: '+x['video']+'_: \n')
        file.write('Text_: '+x['txt']+'_: \n')
        file.write('Image_: '+x['img']+'_: \n')
        file.write('Url_: '+x['url']+'_: \n')
        file.write('Where_: '+x['where']+'_: \n')
        file.write('_____________________'+ '\n')
    file.close()

def create_members():
    global members
    for member in os.listdir(chemin):
        if os.path.isdir(chemin+'\\'+member):
            PATH = chemin+'\\'+member
            file = open(PATH+'\\log.txt',"r",encoding='utf-8')
            cont = file.readlines()
            file.close()
            for x in cont:
                if 'Video_: ' in x:
                    v = x.split('_: ')[1]
                if 'Text_: ' in x:
                    t = x.split('_: ')[1]
                if 'Image_: ' in x:
                    i = x.split('_: ')[1]
                if 'Url_: ' in x:
                    u = x.split('_: ')[1]
                if 'Where_: ' in x:
                    w = x.split('_: ')[1]
                    if member not in members:
                        members[member]=[]
                    members[member].append({'video':v,'txt':t,'img':i,'url':u,'where':w})

def update(page):
    p = urlopen(page)
    content= p.read().decode('utf-8')
    last = int(content.split('...')[1].split('</a>')[0].split('>')[1])
    topic_num = page.split('topic')[1]
    topic_num = int(topic_num[:topic_num.index('.html')])
    if last>LAST_PAGE:
        print('NEW PAGE')
    for i in range(LAST_PAGE-1,last):
        URL = page.split('.html')[0]+'-'+str(i*20)+'.html'
        p = urlopen(URL)
        contenu= p.read().decode('utf-8')
        
        SPLIT = contenu.split('<a rel="nofollow" href="/membre/')[1:]
        for m in SPLIT:            
            member = m[m.index('>')+1:m.index('</a>')]
            
            fp = m.split('href="#forumpost')[1]
            fp_num = int(fp[:fp.index('">')])
            fp = '#forumpost'+str(fp_num)
            if fp_num > LAST_FP:
                LAST_FP = fp_num
                do(fp, fp_num, member, m, LAST_PAGE, LAST_FP, LAST_TOPIC, topic_num, URL, i, last)



if not os.path.exists(chemin):
    os.mkdir(chemin)

if not os.path.exists(path):
    first_time()
    
else:
    file = open(path,"r",encoding='utf-8')
    contenu = file.readlines()
    file.close()
    LAST_URL = contenu[0][:-1]
    LAST_TOPIC = int(contenu[1][:-1])
    LAST_PAGE = int(contenu[2][:-1])
    LAST_FP = int(contenu[3][:-1])
    
    create_members()
    #update(LAST_URL)
