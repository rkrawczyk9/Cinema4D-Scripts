import c4d
from c4d import gui
import sys
import os
sys.path.append(os.path.dirname(__file__))
import rhelpers
#rhelpers.init()

EXCLUDE_HEAD = False
ONLY_INCLUDE_M6_HEAD = True
BYPASS_CALCULATE = False

def main():
    # Find PLA GEO's inside the selected highpolys
    pla_geos = []
    for highpoly in doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER):
        pla_geo = FindObjWithName(rhelpers.UnfoldRig(highpoly), "PLA GEO", objType=c4d.Onull)
        if pla_geo is not None:
            pla_geos.append(pla_geo)

    doc.StartUndo()
    ExportPointCache(pla_geos)
    doc.EndUndo()

def ExportPointCache(roots):
    """Makes a point cache on direct children, then lets user export as Alembic"""
    doc = c4d.documents.GetActiveDocument()
    DeselectAll()
    for root in roots:
        # Only include head if this is M6, ONLY_INCLUDE_M6_HEAD is true, and EXCLUDE_HEAD is false
        exclude_head = True
        if EXCLUDE_HEAD or (not ONLY_INCLUDE_M6_HEAD) or "M6" in GetFirstAncestor(root).GetName():
            exclude_head = False

        plaObjs = []
        for obj in root.GetChildren():
            # Delete backup objects
            if "save" in obj.GetName().lower():
                c4d.GePrint("-deleted " + obj.GetName())
                doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, obj)
                obj.Remove()
            elif "head" in obj.GetName().lower() and exclude_head:
                continue
            else:
                # What remains is the PLA objects we need to export
                # Delete existing tag
                existingTag = None
                for tag in obj.GetTags():
                    if tag.GetType() == 1021302:
                        c4d.GePrint("-deleted " + tag.GetName())
                        doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, tag)
                        tag.Remove()


                obj.SetBit(c4d.BIT_ACTIVE)
                plaObjs.append(obj)

        c4d.CallCommand(12236) # Make Editable

        c4d.CallCommand(100004788, 50051) # New Point Cache Tag

        DeselectAll()

        for plaObj in plaObjs:
            if not BYPASS_CALCULATE:
                # Set up Point Cache tag
                pointCache = plaObj.GetFirstTag()
                c4d.CallButton(pointCache, c4d.ID_CA_GEOMCACHE_TAG_STORE) # Store State button
                c4d.CallButton(pointCache, c4d.ID_CA_GEOMCACHE_TAG_CALCULATE) # Calculate button

            # Clean PLA objects of all expressions+bindings except Point Cache
            for tag in plaObj.GetTags():
                # Delete expression tags
                #if tag.GetName() in ('Weight', 'Constraint', 'Xpresso', 'Motion Solver', 'IK', 'IK-Spline', 'Pose Morph'):
                TYPE_CONSTRAINT = 1019364
                TYPE_MOTIONSOLVER = 1055068
                TYPE_IK = 1019561
                TYPE_IKSPLINE = 1019862
                if tag.GetType() in (c4d.Tmgweight, c4d.Tposemorph, c4d.Texpresso, c4d.Taligntospline, TYPE_CONSTRAINT, TYPE_MOTIONSOLVER, TYPE_IK, TYPE_IKSPLINE):
                    c4d.GePrint("-deleted " + tag.GetName())
                    doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, tag)
                    tag.Remove()

            # Delete Spline Wraps and Skins
            for child in plaObj.GetChildren():
                if child.GetType() in (c4d.Oskin, 1019221):
                    c4d.GePrint("-deleted " + child.GetName())
                    doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, child)
                    child.Remove()

            # Select each to export together
            plaObj.SetBit(c4d.BIT_ACTIVE)

        # Export each root's objects
        characterName = GetFirstAncestor(root).GetName()
        gui.MessageDialog("Point Caches created and populated for Point Level Animation of "+characterName+". Now you can export :)\n\nRemember to set the start/end frame.")
        c4d.CallCommand(60000, 8) # Export as Alembic


def DeselectAll():
    objs = c4d.documents.GetActiveDocument().GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    for obj in objs:
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj)
        obj.DelBit(c4d.BIT_ACTIVE)

def GetFirstAncestor(obj):
    firstAncestor = obj
    while firstAncestor.GetUp() is not None:
        firstAncestor = firstAncestor.GetUp()
    return firstAncestor

def FindObjWithName(objList, objName, objType=None, removePrefixes=True, contains=False):
    """Searches an object list for the first object with a specific name"""
    prefixes = "_:"
    if not removePrefixes:
        prefixes = ""

    if contains:
        for obj in objList:
            if objName in rhelpers.RemoveAllPrefixes(obj.GetName(), prefixes) and (objType==None or obj.GetType()==objType):
                return obj
    else: # must be exact match
        for obj in objList:
            if objName == rhelpers.RemoveAllPrefixes(obj.GetName(), prefixes) and (objType==None or obj.GetType()==objType):
                return obj
    return None

# Execute main()
if __name__=='__main__':
    main()