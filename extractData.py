from lxml import etree
import os

path = 'data'
dir = os.listdir(path)

fout = open('midpoint.csv','w')
fout.write('user_id'+','+'user_name'+','+'time'+','+'comment'+','+'shoucang'+','+'zhuanfa'+','+'pinglun'+','+'dianzan'+','+'device'+','+'url\n')

for sub_dir in dir:
    sub_path = path + os.sep + sub_dir
    files = os.listdir(sub_path)
    print('Start collecting data from:', sub_path)
    for file in files:
        try:
            file_path = sub_path + os.sep + file 
            fin = open(file_path, mode='r', encoding='unicode_escape')
            source = fin.read().replace('\\','')
            page = etree.HTML(source)
            user_div = page.xpath("//div[@class='WB_cardwrap S_bg2 clearfix']")
            for each in user_div:
                mid_div = each.xpath(".//div[@mid]")[0]
                mid = mid_div.attrib.get('mid')
                comment_div = each.xpath(".//p[@class='comment_txt']")[0]
                username = comment_div.attrib.get('nick-name').encode('unicode_escape').decode()
                comment = etree.tostring(comment_div, method='text', encoding='unicode_escape').decode()
                time_div = each.xpath(".//div[@class='feed_from W_textb']")[0]
                time = time_div[1].text if time_div[0].tag != 'a' else time_div[0].text
                url = time_div[1].attrib.get('href') if time_div[0].tag != 'a' else time_div[0].attrib.get('href')
                device = time_div[-1].text.encode('unicode_escape').decode()
                feed_div = each.xpath(".//ul[@class='feed_action_info feed_action_row4']")[0]
                shoucang = '0' if len(feed_div[0].xpath(".//em"))==0 or feed_div[1].xpath(".//em")[0].text==None else feed_div[0].xpath(".//em")[0].text
                zhuanfa = '0' if len(feed_div[1].xpath(".//em"))==0 or feed_div[1].xpath(".//em")[0].text==None else feed_div[1].xpath(".//em")[0].text
                pinglun = '0' if len(feed_div[2].xpath(".//em"))==0 or feed_div[2].xpath(".//em")[0].text==None else feed_div[2].xpath(".//em")[0].text
                dianzan = '0' if len(feed_div[3].xpath(".//em"))==0 or feed_div[3].xpath(".//em")[0].text==None else feed_div[3].xpath(".//em")[0].text
                data = (mid+','+username+','+time+','+comment+','+shoucang+','+zhuanfa+','+pinglun+','+dianzan+','+device+','+url).replace('\\t','').replace('\\n','').replace('\\u200b','')
                fout.write(data+'\n')
            fin.close()
        except Exception as err:
            print ("Something wrong with", file_path,'\n', err)

fout.close()

# rewrite the file, because of the problem about chinese characters encoded by unicode_escape and utf-8
fout = open('final.csv','w')
f = open('midpoint.csv','r',encoding='unicode_escape')
s = f.read()
data = s.split('\n')
for line in data:
    fout.write(line+'\n')
fout.close()