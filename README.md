# 3D Animation Scripts
Here are some scripts I've made for my own use. Feel free to use them too!

# C4D Scripts
I learned Cinema 4D first, and I used it for my senior animation, so I have developed quite a few scripts for it. Most make skeleton-wide changes.

**find#replace**                 Batch renames selected objects. Supports inserting sequential numbers, and a way to replace any digit.

**constrain_geonulls**           Constrains your segmented geometry pieces (stored in nulls a.k.a. 'geonulls') to their respective joints in the rig. The match is determined by naming

**bind_geonulls**                A more compatible alternative to constrain_geonulls. (Most packages can import skin weights but not always constraints.) Binds segmented geometry pieces to their respective joints in the rig based on naming.

**extract_xz**                   A step in my mocap prep process. Transfers the global X and Z keyframes of the Hips to a new parent null, and centers the animation. This is to make blending between motion clips more seamless - then if you ignore the null's position during blending, the hips will not slide around due to the two clips having different Hips locations.

# Maya Scripts
I'm in the process of learning Maya, and so far I really prefer Maya's Python API to C4D's.

**Constrain By Name**      In progress. Parent-Constrains each joint in a skeleton to its same-name counterpart in another skeleton. Includes a window for the user to say how many prefixes are in the names of the skeletons, so the script can work on any two skeletons.
