#!/usr/local/bin/python

# sgftokifu.py
# Copyright (C) 2006  Manuel Bertrand Cabral (manuel.cabral@gmail.com)
#
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import sgflib,sys, os,math
import Image,ImageDraw,ImageFont


def _ascval(char):

    #checks if char is valid
    #upper case characters come after lower case, so the order is ab...yzAB...YZ
    if (ord('a') > ord(char) or ord(char) > ord('z')) and (ord('A') > ord(char) or ord(char) > ord('Z')):
        return -1

    ret = -1

    if ord('A') <= ord(char) and ord(char) <= ord('Z'):
        ret = ord(char)-ord('A')+ord('z')-ord('a')+1

    elif ord('a') <= ord(char) and ord(char) <= ord('z'):
        ret = ord(char) - ord('a')

    else:
        print "Whoever made this program is very, very dumb"

    return ret


class BadNodeException(Exception):
    pass
    

class KNode:
    """
    self.move - tuple with the move in the form (Color,x,y), for example: (B,0,5)
    self.children - list with children Nodes
    
    self.maxindex - index of the largest tree
    self.size - size of the tree that has this node as root


    """

    
    def __init__(self, cursor):
        gotmove = self.getmovefromnode(cursor.node)

        nocount = False

        if gotmove[0] == None:
            #if the node is invalid, it will be ignored
            #it cannot be counted when the tree length is calculated
            self.move = None
            nocount = True
            
        else:
            self.move = gotmove
            

        self.children = []

        childnum = len(cursor.children)

        lentotal = 0
        lenmax = -1

        self.maxindex = None
        
        for i in range(childnum):
            cursor.next(i)
            treelen = self.makechildren(cursor)
            cursor.previous()
            lentotal += treelen
            if treelen > lenmax:
                #the largest children tree is the one just added
                self.maxindex = len(self.children)-1
                
        if nocount:
            self.size = lentotal
        else:
            self.size = lentotal + 1

    
    def makechildren(self, cursor):
        childnode = KNode(cursor)
        self.children.append(childnode)
        return childnode.size

    def getmovefromnode(self, node):
        color = None
        move = None
        x = None
        y = None
        if node.data.has_key('W'):
            color = 'W'
            move = node.data['W'].data[0]
        elif node.data.has_key('B'):
            color = 'B'
            move = node.data['B'].data[0]

        if color == None or move == None:
            return (None, None, None)
        try:
            x = _ascval(move[0])
            y = _ascval(move[1])
        except:
            return (None, None, None)

        if x == -1 or y == -1:
            return (None, None, None)

        return (color,x,y)








class Kifu:

    fontfile = "FreeSans.ttf"

    def __init__(self, imgsize, boardsize, filename, reps, reptextsize, textspacement, inittextspacement, xtextspacement):

        self.imgsize = imgsize
        self.boardsize = boardsize
        self.filename = filename

        inc = imgsize/(boardsize-1+2)

        self.stonesize = inc*0.9

        i = 1
        while(True):
            f = ImageFont.truetype(self.fontfile,i)
            tsx = f.getsize("999")[0]
            tsy = f.getsize("999")[1]
            if tsx > self.stonesize * 0.85 and tsy > self.stonesize * 0.85:
                self.font = ImageFont.truetype(self.fontfile,i-1)
                break
            i += 1

        if reptextsize == -1:
            self.textfont = self.font
        else:
            self.textfont = ImageFont.truetype(self.fontfile,reptextsize)

        textheight = self.textfont.getsize("999 at 999")[1]
        textwidth = self.textfont.getsize("999 at 999")[0]

        boardend = int(math.ceil(imgsize - inc+ (self.stonesize/2)))

        textspacewidth = imgsize - (2*inc)
        repsperline = textspacewidth / (textwidth+xtextspacement)
        self.repsperline = repsperline
        self.xtextinc = textwidth+xtextspacement
        self.xtextinit = inc

        repstotallines = int(math.ceil((reps+0.0) / repsperline))
        
        repstextsize = (textheight + textspacement)*repstotallines + inittextspacement

        if repstextsize < imgsize-boardend:
            totalysize = imgsize
        else:
            totalysize = boardend + repstextsize


        self.repinc = textheight + textspacement 
        self.repinit = boardend+inittextspacement

        addsize = (textheight + textspacement)*repstotallines

        self.image = Image.new('1',(imgsize,totalysize))

        self.draw = ImageDraw.Draw(self.image)

        self.draw.rectangle( [ (0,0),(imgsize,totalysize)],fill=1,outline=1)

    


            
        
        

        self.points = []
        for i in range(boardsize):
            self.points.append((i+1)*inc)

        minpoint = min(self.points)
        maxpoint = max(self.points)

        for x in self.points:
            self.draw.line([ (x,minpoint) , (x,maxpoint)],fill=0)
                             

        for y in self.points:
            self.draw.line([ (minpoint,y) , (maxpoint,y)],fill=0)

        self.image.save(self.filename)

    def placestone(self,num,color,x,y):

        if num > 999:
            print "number",num,"too large. can't print kifu"

        if color == 'B' or color == 'b':
            fillcolor = 0
            tcolor = 1
        elif color == 'w' or color == 'W':
            fillcolor = 1
            tcolor = 0

        xpoint = self.points[x]
        ypoint = self.points[y]

        s = self.stonesize/2

        self.draw.ellipse( [ (xpoint-s,ypoint-s),(xpoint+s,ypoint+s) ] , fill= fillcolor , outline = 0 )

        if num != -1:
            numstr = str(num)
            tsx = self.font.getsize(numstr)[0]/2
            tsy = self.font.getsize(numstr)[1]/2

            self.draw.text( [ (xpoint-tsx,ypoint-tsy) ],numstr,fill=tcolor,font=self.font)

        self.image.save(self.filename)

    def writerep(self,repnum, stonenum, firststone):

        
        repline = ((repnum-1) / self.repsperline)
        reppos = ((repnum-1) % self.repsperline)
        
        xpoint = self.xtextinit + reppos * self.xtextinc
        ypoint = self.repinit + (repline * self.repinc)

        string = str(stonenum) + " at " + str(firststone)

    
        self.draw.text( [ (xpoint,ypoint) ] , string , fill=0, font = self.textfont )
        self.image.save(self.filename)

            


class KifuMaker:

    def __init__(self, knode, imgsize, boardsize, textsize, ytextspacement, inityspacement, xtextspacement, filedir,filename,fileformat):

        self.imgsize = imgsize
        self.boardsize = boardsize
        self.ytextspacement = ytextspacement
        self.inityspacement = inityspacement
        self.xtextspacement = xtextspacement
        self.textsize = textsize
        self.filedir = filedir
        self.fileformat = fileformat
        self.filename = filename

                
        self.moves = []

        currnode = knode
        while len(currnode.children) > 0 :
            if currnode.move != None:
                self.moves.append(currnode.move)
#            print currnode.maxindex
            currnode = currnode.children[currnode.maxindex]


    def kill(self,boardstate,groupset):
        for stonex,stoney in groupset:
            boardstate[stonex][stoney] = 'U'

    def countstoneliberties(self,boardstate,x,y):

        libs = 0

        for dx,dy in [ (0,1) , (0,-1) , (1,0) , (-1,0)]:
            if boardstate[x+dx][y+dy] == 'U':
                libs += 1
        
        return libs
                    
                 
    def creategroup(self,boardstate,x,y,groupset):
        pset = set()
        pset.add((x,y))
        if pset.issubset(groupset):
            return groupset

        groupset = groupset.union(pset)

        for dx,dy in [ (0,1) , (0,-1) , (1,0) , (-1,0)]:
            if boardstate[x+dx][y+dy] == boardstate[x][y]:
                g = self.creategroup(boardstate,x+dx,y+dy,groupset)
                groupset = groupset.union(g)

        return groupset

    def oppositecolor(self,char1, char2):
        if (char1 == 'W' and char2 == 'B') or (char1 == 'B' and char2 == 'W'):
            return True
        else:
            return False

    #checks if any stones adjacent to (x,y) should be killed
    def killcheck(self, boardstate,x,y):

        if boardstate[x][y] == 'U' or boardstate[x][y] == 'E':
            return

        groups = []
        for dx,dy in [ (0,1) , (0,-1) , (1,0) , (-1,0)]:
            if self.oppositecolor(boardstate[x][y],boardstate[x+dx][y+dy]):
                newgroup = self.creategroup(boardstate,x+dx,y+dy,set())

                addme = True
                for g in groups:
                    if newgroup == g:
                        addme = False
                if addme:
                    groups.append(newgroup)


        for g in groups:
            grouplibs = 0
            for stone in g:
                grouplibs += self.countstoneliberties(boardstate,stone[0],stone[1])
            if grouplibs == 0:
                self.kill(boardstate,g)
                
        
       

    def drawkifus(self, stonesperkifu):

        movenum = len(self.moves)
        kifunum = int( math.ceil( (movenum + 0.0)/stonesperkifu))

        #keeps boardstate (dead stones removed). uses sentinels on all 4 sides
        #'U' - unnocupied square
        #'E' - edge of the board
        boardstate = [ ['U' for i in range(self.boardsize+2) ] for i in range(self.boardsize+2)  ]

        for x in range(self.boardsize+2):
            for y in (0,self.boardsize+1):
                boardstate[x][y] = 'E'
                boardstate[y][x] = 'E'


        lastmove = 0
        for k in range(kifunum):

            firstmove = lastmove + 1
            kifumoves = self.moves[lastmove:lastmove+stonesperkifu]
            lastmove += stonesperkifu

            reps = 0
            dictmoves = {}
            # {(x,y) : move }

            movesfinal = []

            i=firstmove
            for move in kifumoves:
                #update boardstate
                x = move[1] + 1
                y = move[2] + 1
                boardstate[x][y] = move[0]
                self.killcheck(boardstate, x,y)

                
                if dictmoves.has_key( (move[1], move[2] )):                    # (x,y)
                    
                    reps += 1
                    movesfinal.append( ('R', dictmoves[ (move[1], move[2] )], reps ))
                else:
                    movesfinal.append(move)
                    dictmoves[(move[1], move[2] )] = i
                i += 1
            

            kifuname = os.path.join(self.filedir + self.filename) + "_" + str(k+1) + self.fileformat

            kifu = Kifu(self.imgsize,self.boardsize,kifuname,reps,self.textsize,
                        self.ytextspacement,self.inityspacement,
                        self.xtextspacement)


            for x in range(1,self.boardsize+1):
                for y in range(1,self.boardsize+1):
                    if boardstate[x][y] == 'U':
                        continue
                    elif boardstate[x][y] == 'E':
                        print "Can't draw kifu. Edge out of place."
                        printbug()
                    else:
                        kifu.placestone(-1,boardstate[x][y],x-1,y-1)
                    

            mnum = firstmove
            for move in movesfinal:
                if move[0] == 'R':
                    kifu.writerep(move[2], mnum,move[1])
                elif move[0] == 'W' or move[0] == 'B':
                    kifu.placestone(mnum,move[0], move[1], move[2])
                mnum += 1


def printusage():
    print "Usage: python sgftokifu.py sgf_file [outputdir=outputdir] [fileformat=fileformat] [filename=filename] [imagesize=image size] [spk=number of stones per kifu]"
    print "File formats: png, jpg, gif"

def printbug():
    print "This is supposed to happen. Please view README file for information on how to report this error."

def joinlist(alist):
    string = ""
    for element in alist:
        string = string + element
    return string

    
def main(argv=sys.argv):
    
    if len(argv) < 2:
        printusage()
        return -1
    
    sgffile = argv[1]
    test = sgffile.split('.')
    if test[-1] != 'sgf':
        print "The first argument must be a .sgf file"
        printusage()
        return

    #initialize variable for input parameters
    params = {}

    #read sgf file
    file = open(sgffile)
    text = file.read()
    parser = sgflib.SGFParser(text)
    coll = parser.parse()
    c = coll.cursor()

    #get board size
    node = c.node
    try:
        boardsize = int(node.data['SZ'].data[0])
    except:
        boardsize = 19



    #default values
    params  = { "fileformat" : "png",
                "filename" : joinlist(sgffile.split('.')[:-1]),
                "imagesize" : 1000*boardsize/19,
                "spk" : 100,
                "outputdir" : ""
        }
    

    for arg in argv[2:]:
        test = arg.split('=')
        if test[0] == "outputdir":
            outputdir = os.path.normpath(test[1])
            
        if test[0] == "fileformat":
            if test[1] != "jpg" and test[1] != "gif" and test1 != "png":
                print "Invalid file format"
                printusage()
            else:
                params["fileformat"] = test[1]
            
        if test[0] == "filename":
            params["filename"] = test[1]

        if test[0] == "imagesize":
            params["imagesize"] = int(test[1])


        if test[0] == "spk":
            params["spk"] = int(test[1])

    
    



    fileformat = "." + params["fileformat"]




    textparams = { "fontsize" : -1,
                   "ytextspacement" : 3*params["imagesize"]/1000,
                   "inityspacement" : 10*params["imagesize"]/1000,
                   "xtextspacement" : 40*params["imagesize"]/1000        }

    k = KNode(c)
    km = KifuMaker(k,params["imagesize"],boardsize,textparams["fontsize"],textparams["ytextspacement"],textparams["inityspacement"],
                   textparams["xtextspacement"],params["outputdir"],params["filename"],fileformat)
    km.drawkifus(params["spk"])
          
    

main()

        

        
            
