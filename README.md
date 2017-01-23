# LinkedNavControl
Ableton Live Controller Remote Script for Session navigation and control 
that can be linked to another controller's "Red Box" session focus.


# Usage
**LinkedNavControl** is a virtual controller that grew out of the need to 
automate the Session View within Ableton Live:

- Without setting up MIDI mapping,
- Without setting up complex Follow Actions for every track & clip,
- Not using any Max-for-Live (M4L) devices or tools. 

The goal was to be able to use Live for a live band, providing in-ear 
click track and cues as well as backing tracks, automatically progressing 
through the Session View Scenes for various parts of each song in a set 
list (_e.g. Song 1: Intro --> Verse 1 --> Pre-Chorus --> Chorus --> etc._). 


This provides several benefits:

- The ability to quickly jump into a specific section of a song for rehearsal,
- Alter the arrangement during performance:
  - Loop/Vamp over a section before continuing the arrangement,
  - Repeat a previous section and continue playing the arrangement,
  - Manually skip over a section of the arrangement.

An additional requirement that grew out of developing this virtual 
controller was the ability to link to Live's linked session management.
Linking the virtual controller's session with the session of a physical 
control surface (such as the Novation Launchpad) allows the highlighted
session ring ("Red Box") of the physical control surface to be automated 
as well.  This means that the active control area of the physical controller 
can be updated from the virtual controller as needed.


## How it works
**LinkedNavControl** makes use of Ableton Live's Remote Script Python API. 
The script creates a virtual Control Surface device in the exact same way
that natively supported controllers are created.  The only difference is 
that **LinkedNavControl** is intended to be attached to a virtual MIDI device 
instead of a real physical piece of hardware.  Functions are pre-defined 
within the script and automatically mapped to MIDI Note and/or CC values. 
When the virtual Control Surface receives one of these MIDI messages, 
the mapped function is executed. The MIDI messages to trigger the functions 
may come from any source that will output to the virtual MIDI device 
(_e.g. physical Control Surface, MIDI clip, external software, etc._).

Typical usage would involve setting up the **LinkedNavControl** virtual Control 
Surface to receive MIDI input from the virtual MIDI device, and a dedicated
MIDI Track with preset MIDI Clips to output commands to the virtual MIDI 
device. When the MIDI Clip is fired, the commands will trigger the functions
within the **LinkedNavControl**. This allows for timing of the commands to 
be tightly associated with the content of the rest of the Clips within 
a Scene. Transitions and linked Session Control states can be programmed 
to occur as needed to achieve the desired arrangement flow.


## Setting up the controller
The controller is intended to be attached to a virtual MIDI loop-back 
device. There are various resources available explaining how to set up
a virtual MIDI device for both Windows and Mac environments.

[**LINK:** Ableton instructions on using virtual MIDI devices](  
https://help.ableton.com/hc/en-us/articles/209774225-Using-virtual-MIDI-buses-in-Live)


[**LINK:** Ableton instructions on installing 3rd party Remote Scripts](
https://help.ableton.com/hc/en-us/articles/209072009-How-to-install-a-third-party-Remote-Script)



### Acknowledgments and References:

- Development of this Remote Script borrows heavily from _wiffbi's_ 
[**Selected Track Control (STC)**](http://stc.wiffbi.com/) code base (found 
[here](https://github.com/wiffbi/Selected_Track_Control)). The original 
Remote Script would've suited the goals of **LinkedNavControl** with the 
exception of not supporting linked Session management. There were also 
quite a few more advanced features within **STC** that were not needed for 
the scope of **LinkedNavControl**, so only the required function/MIDI mapping
elements were imported.

- The following forum post by _bobavenger_ was also very helpful in figuring
out how to create a linked SessionControl object:  
https://forum.ableton.com/viewtopic.php?p=1637316#p1637316

- [_Julien Bayle_](http://julienbayle.net/) has created some excellent 
resources for learning about Ableton Live's Remote Script implementation 
and programming. 

  - http://julienbayle.net/ableton-live-9-midi-remote-scripts/
  - http://julienbayle.net/PythonLiveAPI_documentation/Live9.6.xml
  - https://github.com/gluon/AbletonLive9_RemoteScripts

- Closely related to _Julien's_ content is the following [blog series](
http://remotescripts.blogspot.com/):
  - [Introduction to the Framework Classes](
http://remotescripts.blogspot.com/2010/03/introduction-to-framework-classes.html)
  - [Introduction to the Framework Classes Part 2](
http://remotescripts.blogspot.com/2010/04/introduction-to-framework-classes-2.html)
  - [Introduction to the Framework Classes Part 3](
http://remotescripts.blogspot.com/2010/05/introduction-to-framework-classes-3.html)
  - [Introduction to the Framework Classes Part 4](
http://remotescripts.blogspot.com/2010/09/introduction-to-framework-classes-4.html)

