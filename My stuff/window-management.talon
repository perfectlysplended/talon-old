# These are custom user commands by Edward Huang
# Specifying Context in over to override commands
os: windows
#Below here is body above is context
-

#(win|window) (max|maximize|up): key(super-up)
(win|window) (min|minimize|down): key(super-down)
(win|window) right: key(super-right)
(win|window) left: key(super-left)
[win|window] full screen: user.toggle_fullscreen()

#For Right-click menu
#(win|window) menu: key(shift-f10)

(win|window) one: key(super-1)
(win|window) two: key(super-2)
(win|window) three: key(super-3)
(win|window) four: key(super-4)
(win|window) five: key(super-5)
(win|window) six: key(super-6)
(win|window) seven: key(super-7)
(win|window) eight: key(super-8)
(win|window) nine: key(super-9)
(win|window) ten: key(super-10)

#save that: (ctrl-s)

my custom phrase: "testing custom commands"

head : key(home)
tail : key(end)  



#Find and Replace custom command
hunt: key(ctrl-f)
hunt down: key(f3)
hunt up: key(shift-f3)



#Add commands for moving around the line
#use control left/right to move CURSOR by word; shift will highlight if held; up/down to do it by line
#The alternative is to use go word left go word right

#Notion shortcuts -better to make it browser only
^toggle: "> "
^page$: "/page"