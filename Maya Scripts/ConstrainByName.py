import maya.cmds as cmd

# Settings
IGNORE_TIPS = True
BYPASS_GUI = True

# Globals
# Waiting for a button to be pressed. 0=wait, 1=done, -1=cancelled
CONTINUE = 0

def main():
    print("Running ConstrainByName")
    # Get selected objects
    roots = cmd.ls(sl=True, long=True)
    if len(roots) != 2:
        cmd.confirmDialog(title="Error", message="Must select two roots")
        return
   	
    # Asking the user which one drives which, and assigning the roots to variables
    destRoot = None
    sourceRoot = cmd.confirmDialog(
        title="Constrain descendents by name",
        message="Which of the roots is the source?",
        button=[roots[0], roots[1], "Cancel"],
        defaultButton=roots[0])
    
    # If cancelled or X'd out, stop the script
    if sourceRoot not in roots:
        print("Cancelled")
        return
    # The one that wasn't clicked must be the destination root
    elif sourceRoot == roots[0]:
        destRoot = roots[1]
    else:
        destRoot = roots[0]
    
    # Getting the descendents of each root
    sourceDescendents = cmd.listRelatives(sourceRoot, allDescendents=True, fullPath=True)
    destDescendents = cmd.listRelatives(destRoot, allDescendents=True, fullPath=True)
    
    sourcePrefixes = 2
    sourceSuffixes = 0
    destPrefixes = 1
    destSuffixes = 0
    
    if not BYPASS_GUI:
        # Create Prefix Menu window to ask how many prefixes and suffixes
        # Close it if it was already open
        if cmd.window("prefixMenu", exists=True):
            cmd.deleteUI("prefixMenu")
            
        # Create window UI
        prefixMenu_window = cmd.window("prefixMenu", title="Prefix Menu", w=400, h=500, mnb=False, mxb=False)
        pm_mainLayout = cmd.columnLayout(w=400,h=500)
        pm_rowColumnLayout = cmd.rowColumnLayout(
            numberOfColumns=2,
            columnWidth=[(1,300), (2,300)],
            columnOffset=[(1,"both",10), (2,"both",10)])
        # row 0
        cmd.text(label="")
        cmd.text(label="")
        # row 1
        pm_root0Pre_text = cmd.text("Ignore how many prefixes in " + roots[0] + "?", align="left")
        pm_root1Pre_text = cmd.text("Ignore how many prefixes in " + roots[1] + "?", align="left")
        # row 2
        pm_root0Pre_field = cmd.intField(minValue=0, value=2)
        pm_root1Pre_field = cmd.intField(minValue=0, value=2)
        # row 3
        cmd.text(label="")
        cmd.text(label="")
        # row 4
        pm_root0Suf_text = cmd.text("Ignore how many suffixes in " + roots[0] + "?", align="left")
        pm_root1Suf_text = cmd.text("Ignore how many suffixes in " + roots[1] + "?", align="left")
        # row 5
        pm_root0Suf_field = cmd.intField(minValue=0, value=0)
        pm_root1Suf_field = cmd.intField(minValue=0, value=0)
        # row 6
        cmd.text(label="")
        cmd.text(label="")
        cmd.text(label="")
        cmd.text(label="")
        cmd.text(label="")
        cmd.text(label="")
        # row 9
        pm_confirm = cmd.button("Confirm", c=PrefixMenu_Confirm)
        pm_cancel = cmd.button("Cancel")
        
        CONTINUE = 0
        
        cmd.showWindow(prefixMenu_window)
        
        # TODO fix busy wait
        while CONTINUE == 0: # Continue is changed from zero by pressing the Confirm button
            pass # wait
        
        # Now that the button has been pressed, we can use the data in the window
        sourcePrefixes = cmd.intField("pm_root1Suf_field", q=True, value=True)
        # TODO destinationPrefixes and other
        destPrefixes = 1
        sourceSuffixes = 0
        destSuffixes = 0
        
        print(sourcePrefixes)
    
    
    # Go through all the descendents
    for srcDesc in sourceDescendents:
        if len(srcDesc)>=3 and srcDesc[-3:].lower() == "tip" and IGNORE_TIPS:
            continue 
            
        # Trim the name down to just "RightArm" for example
        try:
            srcDesc_trim = TrimPrefixes(srcDesc, delim=':', numPrefixes=sourcePrefixes, numSuffixes=sourceSuffixes)
        except:
            # If one of the names is irregularly short, it's not going to be a match, so skip it
            print("{} name too short".format(srcDesc))
            continue
            
        # Look for a match
        for destDesc in destDescendents:
            # Trim the name
            try:
                destDesc_trim = TrimPrefixes(destDesc, delim=':', numPrefixes=destPrefixes, numSuffixes=destSuffixes)
            except:
                # If one of the names is irregularly short, it's not going to be a match, so skip it
                print("{} name too short".format(destDesc))
                continue
                
            #print(srcDesc_trim + " vs. " + destDesc_trim)
            if srcDesc_trim == destDesc_trim:
                # Create the constraint
                #print("Constraining " + destDesc_trim + " to " + srcDesc_trim)
                constraint = None
                try:
                    constraint = cmd.parentConstraint(srcDesc, destDesc, maintainOffset=True)
                except RuntimeError as e:
                    if "Targets must be of type transform." in str(e):
                        print("{} is not a transform".format(srcDesc_trim))
                        break
                    elif "Could not add constraint or connections." in str(e):
                        print("{} could not be constrained to {}".format(srcDesc_trim, destDesc_trim))
                        break
                    else:
                        raise
                else:
                    print("{} constrained to {}".format(srcDesc_trim, destDesc_trim))
                    break
                print("why am i here")
    return

def PrefixMenu_Confirm():
    
    return 

# Utility

def TrimPrefixes(str, delim='_', numPrefixes=2, numSuffixes=0):
    """Returns the string but without the first [numPrefixes] prefixes and last [numSuffixes] suffixes
    (ex. RemovePrefixes("j_RIG_Hips",num=2) returns "Hips")"""
    finalStr = ""
    str_words = str.split(delim) # List of strings
    for eachWord in str_words[numPrefixes:(len(str_words)-numSuffixes)]: # Rebuild string excluding the first [num] words
        finalStr += eachWord + delim # Adding the delimiter character in between each word
    return finalStr[:-1] # Remove last character of finalStr

main()