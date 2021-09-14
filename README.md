# blenderTouchNav
A blender addon for touchscreen-friendly buttons to undo and rotate canvas plus some simplified defaults for 2D Animation.

# Concept:
My teenage kids like drawing in Krita but want to animate.  They found the default 2d animation setup of Blender to be difficult and intimidating.  Mainly they like to use old surface tablets to draw without needing a keyboard...which is a challenge in Blender.  Finding certain crucial settings can be a lot to remember, for example the data properties tab to change layers in Grease Pencil. This is an attempt to give the most convenient startup and workflow possible to get drawing immediately without getting bogged down in the depths of Blender's endless options.  
  

# Installation:
*  Download the files
*  In Blender 2.8 or above go to `Edit->Preferences` and choose the `Add-ons` tab
*  Hit the `Install...` button and choose the `blender touch nav addon.py` file
*  Check the box next to the addon name to activate (3D View: Touch Navigation for 2D animation and tablets)

The "Touchscreen Buttons" panel should now be visible at the bottom of the Tools tab in the 3D view sidebar.  
You can drag it to the top of the tools tab for easier access.

# Blender default file (optional):  
I've also included a blender default file to make a new 2d Animation start with the most convenient view available.  
All you need to do is open it then choose `File->Defaults->Save Startup File`.  
  
It differs from the 2.93 blank 2D animation in the following ways:
*  The tool tab on the sidebar is opened
*  Touchscreen Buttons are at the top of the tab and Current Tool at the bottom
*  The greasepencil object timeline/keyframes are in the Dope Sheet window
*  Vertex Color is selected by default instead of material
*  A light blue color is selected (our preference for rough sketching)
*  Brush strength set to full
*  Brush radius set to 25px
*  Same settings for 2D Full Canvas layout
*  Object Data Properties tab is selected in the Properties window to show layers
*  Onion skin set to show 2 keyframes with a lower opacity and more discernable green and red colors
*  Brush Pack v2 by Daniel Martinez Lara is appended (watch out for the automatic material change, you may need to set it back to Solid Stroke after using a custom brush) 

Let me know if you have any suggestions on how to make this the perfect blender startup file to keep kids engaged.
