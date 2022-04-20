Here are some scripts I've made for my own use. Feel free to use them too!

# C4D Utility

**find#replace** - Batch renames selected objects. Supports inserting sequential numbers, and a way to replace any digit.

**printType** - Prints the int corresponding to the type of the selected object(s). Useful for the types that do not yet have an enum you can use, like in R23 there's no c4d.Tcachardefinition yet, so printType can tell you to use 1054858 instead.

**Color_Rig** - Sets the display color of descendents (assuming you're selecting the root of a rig) according to my naming convention.

**RHelpers** - A file with all my utility functions. Currently troubleshooting how to call them from the file in C4D, rather than copy/pasting into each new script.



# C4D -> UE4 pipeline

1. Connecting geo to any rig

**constrain_geonulls** - Constrains your segmented geometry pieces (stored in nulls a.k.a. 'geonulls') to their respective joints in the rig. The match is determined by naming
Saves ~10 min per bind attempt

**bind_geonulls** - A more compatible alternative to constrain_geonulls. (Most packages can import skin weights but not always constraints.) Binds segmented geometry pieces to their respective joints in the rig based on naming. Saves ~20 min per bind attempt.



2. Importing mocap

**extract_xz** - Transfers the global X and Z keyframes of the Hips to a new parent null, and centers the animation. This is to make blending between motion clips more seamless - then if you ignore the null's position during blending, the hips will not slide around due to the two clips having different Hips locations. Saves ~5 min per mocap clip, and adds exactness.


3. Animate

Scripts can't help me with that :)


4. Connect highpoly rig to animation rig

**find_src_bones_for_hpRig** - Quickly sets up either of my highpoly rigs to be driven by an animation rig. Saves ~2 min per export attempt per character per scene. (Lots of export attempts while troubleshooting how to import into Unreal)


5. Bake and export animation
**export_pointCache** - Saves a point cache for each PLA object and starts export to alembic file. Saves ~5 min per export attempt per character per scene.

**delete_tags** - Deletes expression tags on highpoly rig bind skeleton so export is guaranteed to use the baked animation.

**delete_empties** - Deletes empty nulls in the rig so they don't get exported.

**export_baked_skeleton** - Calls **delete_tags** and **delete_empties** and starts export to FBX. Saves ~2 min per export per character per scene.



...

?. Import rendered frames into After Effects

**MoveFrames.bat** - Windows batch file which, given a folder of unorganized frames, puts them into new subfolders for each sequence, so that Ae can recognize them as Image Sequences. Works based on name.



# Maya Scripts
I'm in the process of learning Maya, and so far I really like Maya's Python API! There are easy ways to do the important things.

**Constrain By Name** - In progress. Parent-Constrains each joint in a skeleton to its same-name counterpart in another skeleton. Includes a window for the user to say how many prefixes are in the names of the skeletons, so the script can work on any two skeletons.
