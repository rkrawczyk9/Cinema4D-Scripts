# 3D Animation Scripts
Here are some scripts I've made for my own use. Feel free to use them too!

**generate_books**               Creates instances of a book to fit my bookshelf.

**assign_mats**                  Used after generate_books_2.py to randomly assign one of the colored materials I made in the scene to a book.

**zero_active_objs**             Simply sets all local transforms to 0 (or 1 for scale.)

**joints_to_rot+offset_ctrls**   In progress. Will create FK controls for a joint hierarchy.

**constrain_recv_rig_4**         In progress. Essentially I am trying to manually retarget an animated skeleton to a new skeleton which can have different proportions. Was going to use this for my motion capture data for my senior film, but Cinema 4D's Motion Solver tag works better.

**find#replace**                 Batch renames selected objects. Supports inserting sequential numbers, and a way to replace any digit.

**constrain_geonulls**           Constrains your segmented geometry pieces (stored in nulls a.k.a. 'geonulls') to their respective joints in the rig. The match is determined by naming

**extract_xz**                   A step in my mocap prep process. Transfers the global X and Z keyframes of the Hips to a new parent null, and centers the animation. This is to make blending between motion clips more seamless - then if you ignore the null's position during blending, the hips will not slide around due to the two clips having different Hips locations.
