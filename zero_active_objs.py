import c4d
from c4d import gui
# Welcome to the world of Python

# Main function
def main():
    for o in doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER):
        o.SetRelPos(c4d.Vector(0))
        o.SetRelScale(c4d.Vector(1))
        o.SetRelRot(c4d.Vector(0))

# Execute main()
if __name__=='__main__':
    main()