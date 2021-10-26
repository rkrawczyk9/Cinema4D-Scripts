import c4d
from c4d import gui

def error(string):
    print(string)
    gui.MessageDialog(string)
    return

def main():
    doc.StartUndo()

    findreplace = gui.InputDialog("Find#Replace or type help")
    ## Special cases
    if findreplace == "help":
        helpstr = "Use the format FindThis#ReplaceWithThis to rename selected objects.\nKey:"
        helpstr += "\n# separates find string from replace string\n$n inserts number here starting at n, in selection order"
        helpstr += "\n$X signifies any digit in place of $X. Only one of these is supported per find string"
        helpstr += "\n\nExample: strap_$X#bigstrap_$1 will replace 'strap_4' and 'strap_9' with 'bigstrap_1', 'bigstrap_2', etc."
        helpstr += "\n\nLeave 'Find' blank to replace whole name.\nType just $+postfix_here to add whatever postfix_here is to the end."
        gui.MessageDialog(helpstr)
        return
    elif findreplace[:2] == "$+":
        print("Adding " + findreplace[2:] + " to the end of each object")
        for obj in doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER | c4d.GETACTIVEOBJECTFLAGS_CHILDREN):
            name = obj.GetName()
            name += findreplace[2:]
            doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, obj)
            obj.SetName(name)
        return
    
    ## Tokenize
    try:
        find, replace = findreplace.split("#")
    except ValueError:
        if findreplace.find("#") == -1:
            print("Converting no-delimiter input to replace-only input")
            replace = findreplace
            find = ""
        else:
            raise ValueError("too many values to unpack")

    origs = []
    news = []
    
    ## Parse starting no
    ns = []
    for i in range(len(replace)):
        if replace[i] == "$":
            new_n = replace[i+1]
            if new_n.isdigit():
                ns.append(int(new_n))
            else:
                gui.MessageDialog("Expected digit after $")
    
    ## Find and Replace
    for obj in doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER | c4d.GETACTIVEOBJECTFLAGS_CHILDREN):
        name = obj.GetName()
        origs.append(name)

        ## Find $X in name and prepare name and find for matching
        if find != "":
            find = find.replace("$X", "!")
            for i in range(len(name)):
                if len(find)+i-1 > len(name):
                    print("lost cause")
                    break
                if name[i] == find[0]:
                    for j in range(1, len(find)):
                        if name[i+j].isdigit() and find[0+j] == "!":
                            name = name[:i+j] + "!" + name[i+j+1:]
                            print("now it's " + name)
                        elif name[i+j] != find[0+j]:
                            break
        ## Parse replace string
        curr_n = 0
        replace_n = ""
        i = 0
        while i < len(replace):
            char = replace[i]
            if char != "$":
                replace_n += char
            else:
                if len(ns) == curr_n:
                    ns.append(int(replace[i+1]))
                elif len(ns) < curr_n:
                    error("uh oh ns is not populated")
                    return
                replace_n += str(ns[curr_n])
                ns[curr_n] += 1
                curr_n += 1
                i += 1 ## Skip next char
            i += 1

        if find != "":
            print("replacing " + find + " with " + replace_n + " within " + name)
            name = name.replace(find,replace_n)
            print("now it's " + name)
        else:
            print("find was blank, setting name (" + name + ") to " + replace_n)
            name = replace_n
        ## Finalize
        doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL, obj)
        obj.SetName(name)
        news.append(name)
        print()

    print_origsnews = "Renamed\t"
    for i in range(len(origs)):
        print_origsnews += origs[i] + " to " + news[i] + "\n\t\t"
    gui.MessageDialog(print_origsnews)
    doc.EndUndo()
    c4d.EventAdd()
    return

if __name__=='__main__':
    main()
