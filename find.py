import fitz
import os
import os


def _parse_highlight(annot, wordlist):
    points = annot.vertices
    #print(points)
    quad_count = int(len(points) / 4)
    sentences = ['' for i in range(quad_count)]
    for i in range(quad_count):
        r = fitz.Quad(points[i * 4: i * 4 + 4]).rect
        words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
        sentences[i] = ' '.join(w[4] for w in words)
    sentence = ' '.join(sentences)
    return sentence


filePath = 'C:\\Users\\lxj\\Desktop\\房屋租赁合同'

all_pairs=[]

for k in os.listdir(filePath):

    mupdf_doc = fitz.open(os.path.join(filePath,k))
    pages = mupdf_doc.page_count
    # for mupdf_page in mupdf_doc:
    for page in range(pages):
        mupdf_page = mupdf_doc.load_page(page)
        wordlist = mupdf_page.get_text("words")  # list of words on page
        wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x
        #print(wordlist)
        for annot in mupdf_page.annots():
            # underline / highlight / strikeout / squiggly : 8 / 9 / 10 / 11
            if annot.type[0] == 8:
                item=_parse_highlight(annot, wordlist)
                all_pairs.append([k,item])

#写入文件
with open(os.path.join('C:\\Users\\lxj\\Desktop',"res.txt"),"w") as f:
    print(all_pairs,file=f)

#读出文件
with open(os.path.join('C:\\Users\\lxj\\Desktop',"res.txt"),"r") as f:
    res=eval(f.readline())

print(res)