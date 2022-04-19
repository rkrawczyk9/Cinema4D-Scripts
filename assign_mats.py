import c4d
from c4d import gui
import random

def main():
    bookmatnames = ["grey","black","white","bookbase","salmon","olive","yellow","teal","purple","muck","orange","grey","black","blue","sky","green"]

    allmats = doc.GetMaterials()
    bookmats = []
    for m in allmats:
        if m.GetName() in bookmatnames:
            bookmats.append(m)

    books = doc.SearchObject("books").GetChildren()
    for book in books:
        tag = c4d.TextureTag()
        tag.SetMaterial(random.choice(bookmats))
        tag[c4d.TEXTURETAG_PROJECTION]=c4d.TEXTURETAG_PROJECTION_UVW
        book.InsertTag(tag)
    c4d.EventAdd()

if __name__=='__main__':
    main()