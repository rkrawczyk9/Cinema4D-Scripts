import c4d
from c4d import gui
import random

#first shelf z -150 second shelf z -50 size 2.582
#            y 357.25+2.582      y 309+2.582
#starting point z = -250+2.582

start = c4d.Vector(-724.424, 357.25+2.582/2, -250+2.582/2)
shelfSpaceY = 48.25#-2.582*2

shelfSpaces = [[100,100,100,0  ,0  ,0  ,0  ,0  ],
               [100,100,100,100,100,100,100,100],
               [100,100,100,100,100,100,100,100],
               [100,100,100,100,100,100,100,100],
               [48 ,48 ,48 ,48 ,48 ,48 ,48 ,0  ],
               [100,100,100,100,100,100,0  ,0  ],
               [100,100,100,100,100,100,0  ,0  ],
               [100,100,100,100,100,0  ,0  ,0  ]]
#gaps = [[start z, width z, stack ct, stack height, margin], ...]
null = [0,0,0,0,0]
gaps = [[null,null,null,null,null,null,null,null],
        [[35,30,0,0, 0],[30,40,0,0,0],null,null,[5,30,4,10,10],null,null,null],
        [null,null,[45,10,4,13,1],[10,35,0,0,0],[35,30,0,0,0],[45,30,4,20,2],[15,35,5,33,1],null],
        [[30,15,0,0,0],[7,35,6,30,2],[55,30,7,38,1],null,[0,40,0,0,0],null,[25,35,0,0,0],null],
        [null,[0,25,0,0,0],null,null,null,[0,48-2.582,5,20,14],[0,20,0,0,0,],null],
        [[80,20,0,0,0],[75,25,0,0,0],[55,20,0,0,0],[35,30,0,0,0],[40,10,0,0,0],null,null,null],
        [null,null,[65,35,0,0,0],[0,45,7,35,10],[75,25,0,0,0],[65,45,0,0,0],null,null],
        [null,null,null,null,[50,47,0,0,0],[15,40,0,0,0],null,null]]

def main():
    print("hi")
    gui.MessageDialog("hi")

    #mass correcting shelfSpaces values
    for c in range(0,8):
        for r in range(0,8):
            shelfSpaces[c][r] -= 2.582

    template = doc.SearchObject("book template")

    booksNull = c4d.BaseObject(c4d.Onull)
    booksNull.InsertUnder(template)

    for c in range(0,8):
        for r in range(0,8):
            if(shelfSpaces[c][r] != 0):

                #fill shelf
                spaceTaken = 0
                while(shelfSpaces[c][r] - spaceTaken > .15):
                    
                    print("making book")
                    #make book
                    book = c4d.BaseObject(c4d.Oinstance)
                    book[c4d.INSTANCEOBJECT_LINK] = template
                    #book = template.GetClone()
                
                    #calculates previous shelf space taken up to this point
                    prevShelvesSpace = 0
                    c_temp = 0
                    while(c_temp < c):
                        prevShelvesSpace += shelfSpaces[c_temp][0]
                        prevShelvesSpace += 2.582#width of shelf divider
                        c_temp+=1
                
                    #put in position
                    book.SetAbsPos(c4d.Vector( start[0], (start[1] - shelfSpaceY * r), (start[2] + prevShelvesSpace + spaceTaken) ))
                
                    #if approaching gap
                    if shelfSpaces[c][r]-gaps[c][r][0] - spaceTaken < .25:
                        thickness = (shelfSpaces[c][r]-gaps[c][r][0]-spaceTaken)
                    #if only enough space for 2 books
                    elif shelfSpaces[c][r]-gaps[c][r][0] - spaceTaken < 1:
                        thickness = (shelfSpaces[c][r]-gaps[c][r][0]-spaceTaken)/2
                    #if up against shelf
                    elif shelfSpaces[c][r]-spaceTaken < 1.25:
                        thickness = (shelfSpaces[c][r]-spaceTaken)
                    else:
                        thickness = random.normalvariate(.85,.27)
                
                    #randomize length
                    length = random.normalvariate(.85,.13)
                
                    book.SetAbsScale(c4d.Vector(length,length,thickness))
                
                    #randomize color/apply random material from layer?
                    #
                
                    #insert into scene and update space taken
                    book.InsertUnder(booksNull)
                
                    spaceTaken += 3.936*thickness
                    
                    
                    c4d.EventAdd()

    gui.MessageDialog("done")


def makeStack(gap):#gap=[start z, z width, book ct, height, margin (split)]
    gui.MessageDialog("makin a stack")

#def makeBook(template,booksNull,c,r,spaceTaken):
    #print("making book")
    #make book
    #book = c4d.BaseObject(c4d.Oinstance)
    #book[c4d.INSTANCEOBJECT_LINK] = template
    #book = template.GetClone()

    #calculates previous shelf space taken up to this point
    #prevShelvesSpace = 0
    #c_temp = 0
    #while(c_temp < c):
        #prevShelvesSpace += shelfSpaces[c_temp][0]
        #prevShelvesSpace += 2.582#width of shelf divider
        #c_temp+=1
#
    #put in position
    #book.SetAbsPos(c4d.Vector( start[0], (start[1] - shelfSpaceY * r), (start[2] + prevShelvesSpace + spaceTaken) ))
#
    #if approaching gap
    #if shelfSpaces[c][r]-gaps[c][r][0] - spaceTaken < .25:
        #thickness = (shelfSpaces[c][r]-gaps[c][r][0]-spaceTaken)
    #if only enough space for 2 books
    #elif shelfSpaces[c][r]-gaps[c][r][0] - spaceTaken < 1:
        #thickness = (shelfSpaces[c][r]-gaps[c][r][0]-spaceTaken)/2
    #if up against shelf
    #elif shelfSpaces[c][r]-spaceTaken < 1.25:
        #thickness = (shelfSpaces[c][r]-spaceTaken)
    #else:
        #thickness = random.normalvariate(.85,.27)
#
    #randomize length
    #length = random.normalvariate(.85,.13)
#
    #book.SetAbsScale(c4d.Vector(length,length,thickness))
#
    #randomize color/apply random material from layer?
    #

    #insert into scene and update space taken
    #book.InsertUnder(booksNull)
#
    #return 3.936*thickness

# Execute main()
if __name__=='__main__':
    doc.StartUndo()
    main()
    c4d.EventAdd()
    doc.EndUndo()