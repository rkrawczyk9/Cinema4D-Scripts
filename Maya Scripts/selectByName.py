import maya.cmds

ok = maya.cmds.promptDialog(title="Select By Name", message="Select names containing...", button=["OK", "Cancel"], defaultButton="OK", cancelButton="Cancel", dismissString="Cancel")

if ok:
    string = maya.cmds.promptDialog(query=True, text=True)
    print("Selecting objects containing the string {}".format(string))
    maya.cmds.select(maya.cmds.ls("*"+string+"*"))