# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from typing import Match
from libqtile.config import Drag, Key, Screen, Group, Drag, Click, Rule, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.widget import Spacer
#import arcobattery

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')

@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [

# Most of our keybindings are in sxhkd file - except these

# SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod, "shift"], "c", lazy.window.kill()),


# SUPER + SHIFT KEYS

    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),


# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    ]

groups = []

group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]

#group_labels = ["I ", "II ", "III ", "IV ", "V ", "VI ", "VII ", "VIII ", "IX ", "X",]
#group_labels = ["???", "???", "???", "???", "???", "???", "???", "???", "???", "???",]
group_labels = ["Lab", "Web", "Files", "Vbox", "Pdf", "Zoom", "Vid", "Img", "Irc", "Music",]

group_layouts = ["monadtall", "max", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "float", "monadtall", "monadtall",]

#for i in range(len(group_names)):
#    groups.append(Group(i))

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

#__groups = {
#    1: Group("Lab", layout="monadtall", matches=[Match(wm_class=['code'])]),
#    2: Group("Web", layout="max", matches=[Match(wm_class=['firefox'])]),
#    2: Group("Files", layout="monadtall", matches=[Match(wm_class=['thunar', 'pcmanfm'])]),
#    3: Group("Vbox", layout="monadtall", matches=[Match(wm_class=['virtualbox manager', 'vmplayer'])]),
#    4: Group("Pdf", layout="monadtall", matches=[Match(wm_class=['libreoffice', 'libreoffice-startcenter', 'libreoffice-writer', 'libreoffice-calc', 'libreoffice-impress', 'libreoffice-draw', 'libreoffice-math'])]),
#    5: Group("Zoom", layout="monadtall", matches=[Match(wm_class=['zoom'])]),
#    6: Group("Vid", layout="monadtall", matches=[Match(wm_class=['vlc', 'mpv'])]),
#    7: Group("Img", layout="float", matches=[Match(wm_class=['gimp'])]),
#    8: Group("Irc", layout="monadtall", matches=[Match(wm_class=['discord', 'telegram'])]),
#    9: Group("Music", layout="monadtall", matches=[Match(wm_class=['spotify', 'deadbeef', 'mpoc'])]),
#}
#groups = [__groups[i] for i in __groups]

#group_names = [("Lab", {'layout': 'monadtall'}),
#               ("Web", {'layout': 'max'}),
#               ("Files", {'layout': 'monadtall'}),
#               ("Vbox", {'layout': 'monadtall'}),
#               ("Pdf", {'layout': 'monadtall'}),
#               ("Zoom", {'layout': 'monadtall'}),
#               ("Vid", {'layout': 'monadtall'}),
#               ("Img", {'layout': 'float'}),
#               ("Irc", {'layout': 'monadtall'}),
#               ("Music", {'layout': 'monadtall'})]
#groups = [Group(name , **kwargs) for name, kwargs in group_names]

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin":5,
            "border_width":2,
            "border_focus": "#fea63c",
            "border_normal": "#373839"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(margin=8, border_width=2, border_focus="#fea63c", border_normal="#373839"),
    layout.MonadWide(margin=8, border_width=2, border_focus="#fea63c", border_normal="#373839"),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme)
]

## COLORS ##

def init_colors():
    return [["#2F343F", "#2F343F"], # Bar bg (0)
            ["#2F343F", "#2F343F"], # Widgets bg (1)
            ["#ffffff", "#ffffff"], # Front Groups (2)
            ["#ff5555", "#ff5555"], # Widget Orange (3)
            ["#3e95fe", "#3e95fe"], # Blue? (4)
            ["#f3f4f5", "#f3f4f5"], # Inactive Groups (5)
            ["#cd1f3f", "#cd1f3f"], # Red? (6)
            ["#62FF00", "#62FF00"], # Green? (7)
            ["#fea63c", "#fea63c"], # Main Orange (8)
            ["#6E99CE", "#6E99CE"]] # Active Group (9)


colors = init_colors()


## WIDGETS ##

def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize = 12,
                padding = 2,
                background=colors[1])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
               widget.Sep(
                        linewidth = 0,
                        padding = 6,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.GroupBox(
                        font="Ubuntu Bold",
                        fontsize = 10,
                        margin_y = 3,
                        margin_x = 0,
                        padding_y = 5,
                        padding_x = 3,
                        borderwidth = 3,
                        disable_drag = True,
                        active = colors[8],
                        inactive = colors[2],
                        rounded = False,
                        highlight_method = "line",
                        this_current_screen_border = colors[3],
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.Prompt(
                       prompt = prompt,
                       font = "Ubuntu Mono",
                       padding = 10,
                       foreground = colors[3],
                       background = colors[1]
                       ),
               widget.Sep(
                        linewidth = 0,
                        padding = 40,
                        foreground = colors[2],
                        background = colors[0]
                        ),
               widget.WindowName(
                        font = "Ubuntu Mono",
                        foreground = colors[2],
                        background = colors[1],
                        padding = 0,
                        ),
               # widget.Net(
               #          font="Noto Sans",
               #          fontsize=12,
               #          interface="enp0s31f6",
               #          foreground=colors[2],
               #          background=colors[1],
               #          padding = 0,
               #          ),
               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               # widget.NetGraph(
               #          font="Noto Sans",
               #          fontsize=12,
               #          bandwidth="down",
               #          interface="auto",
               #          fill_color = colors[8],
               #          foreground=colors[2],
               #          background=colors[1],
               #          graph_color = colors[8],
               #          border_color = colors[2],
               #          padding = 0,
               #          border_width = 1,
               #          line_width = 1,
               #          ),
               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               # # do not activate in Virtualbox - will break qtile
               # widget.ThermalSensor(
               #          foreground = colors[5],
               #          foreground_alert = colors[6],
               #          background = colors[1],
               #          metric = True,
               #          padding = 3,
               #          threshold = 80
               #          ),
               # # battery option 1  ArcoLinux Horizontal icons do not forget to import arcobattery at the top
               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               # arcobattery.BatteryIcon(
               #          padding=0,
               #          scale=0.7,
               #          y_poss=2,
               #          theme_path=home + "/.config/qtile/icons/battery_icons_horiz",
               #          update_interval = 5,
               #          background = colors[1]
               #          ),
               # # battery option 2  from Qtile
               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               # widget.Battery(
               #          font="Noto Sans",
               #          update_interval = 10,
               #          fontsize = 12,
               #          foreground = colors[5],
               #          background = colors[1],
	           #          ),
               # widget.TextBox(
               #          font="FontAwesome",
               #          text=" ??? ",
               #          foreground=colors[6],
               #          background=colors[1],
               #          padding = 0,
               #          fontsize=16
               #          ),
               # widget.CPUGraph(
               #          border_color = colors[2],
               #          fill_color = colors[8],
               #          graph_color = colors[8],
               #          background=colors[1],
               #          border_width = 1,
               #          line_width = 1,
               #          core = "all",
               #          type = "box"
               #          ),
               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               # widget.TextBox(
               #          font="FontAwesome",
               #          text=" ??? ",
               #          foreground=colors[4],
               #          background=colors[1],
               #          padding = 0,
               #          fontsize=16
               #          ),
               # widget.Memory(
               #          font="Noto Sans",
               #          format = '{MemUsed}M/{MemTotal}M',
               #          update_interval = 1,
               #          fontsize = 12,
               #          foreground = colors[5],
               #          background = colors[1],
               #         ),
               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               widget.Systray(
                       background = colors[0], 
                       padding = 5
                       ),
               widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
               widget.TextBox(
                       text = '???',
                       foreground = colors[8],
                       background = colors[0],
                       padding = -1,
                       fontsize = 50
                       ),
               widget.Net(
                        interface="enp4s0",
                        foreground = colors[1],
                        background = colors[8],
                        format = "{down} ?????? {up}"
                        ),
               widget.TextBox(
                       text='???',
                       background = colors[8],
                       foreground = colors[4],
                       padding = -1,
                       fontsize = 50
                       ),
               widget.TextBox(
                       text = " ????",
                       foreground = colors[2],
                       background = colors[4],
                       padding = 0,
                       fontsize = 14
                       ),
               widget.Memory(
                       foreground = colors[2],
                       background = colors[4],
                       padding = 5
                       ),
               widget.TextBox(
                        text = "???",
                        background = colors[4],
                        foreground = colors[8],
                        padding = -1,
                        fontsize = 50
                        ),
               widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[1],
                       background = colors[8],
                       padding = 0,
                       scale = 0.6
                       ),
               widget.CurrentLayout(
                       foreground = colors[1],
                       background = colors[8],
                       padding = 5
                       ),
               widget.TextBox(
                        text = "???",
                        background = colors[8],
                        foreground = colors[4],
                        padding = -1,
                        fontsize = 50
                        ),
               widget.TextBox(
                        font = "FontAwesome",
                        text = " ??? ",
                        foreground = colors[2],
                        background = colors[4],
                        padding = 0,
                        fontsize = 16
                        ),
               widget.Clock(
                        foreground = colors[2],
                        background = colors[4],
                        fontsize = 12,
                        format = "%A,  %B %d   [ %H:%M ] "
                        ),
              ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, opacity=0.8)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, opacity=0.8))]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#    #####################################################################################
#    ### Use xprop fo find  the value of WM_CLASS(STRING) -> First field is sufficient ###
#    #####################################################################################
#     d[group_names[0]] = []
#     d[group_names[1]] = ["Firefox", "firefox" ]
#     d[group_names[2]] = ["Thunar", "thunar", "Pcmanfm", "pcmanfm", "Pcmanfm-qt", "pcmanfm-qt" ]
#     d[group_names[3]] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer", "virtualbox manager", "virtualbox machine", "vmplayer" ]
#     d[group_names[4]] = ["LibreOffice", "libreoffice", "libreoffice-startcenter", "libreoffice-writer", "libreoffice-calc", "libreoffice-impress", "libreoffice-draw", "libreoffice-math" ]
#     d[group_names[5]] = ["Zoom", "zoom" ]
#     d[group_names[6]] = ["Vlc", "vlc", "Mpv", "mpv" ]
#     d[group_names[7]] = ["Gimp", "gimp", "Inkscape", "inkscape" ]
#     d[group_names[8]] = ["Discord", "discord", "Telegram", "telegram" ]
#     d[group_names[9]] = ["Spotify", "Mpoc", "Deadbeef", "spotify", "mpoc", "deadbeef" ]
#     ######################################################################################

# wm_class = client.window.get_wm_class()[0]

# for i in range(len(d)):
#     if wm_class in list(d.values())[i]:
#         group = list(d.keys())[i]
#         client.togroup(group)
#         client.group.cmd_toscreen(toggle=False)
# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME



main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'Arcolinux-welcome-app.py'},
    {'wmclass': 'Arcolinux-tweak-tool.py'},
    {'wmclass': 'Arcolinux-calamares-tool.py'},
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},
    {'wmclass': 'makebranch'},
    {'wmclass': 'maketag'},
    {'wmclass': 'Arandr'},
    {'wmclass': 'feh'},
    {'wmclass': 'Galculator'},
    {'wmclass': 'arcolinux-logout'},
    {'wmclass': 'xfce4-terminal'},
    {'wname': 'branchdialog'},
    {'wname': 'Open File'},
    {'wname': 'pinentry'},
    {'wmclass': 'ssh-askpass'},

],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"
