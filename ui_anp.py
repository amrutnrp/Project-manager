# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 14:55:12 2024

@author: amrut
"""

# from dearpygui.dearpygui import *
import dearpygui.dearpygui as dpg
import sys,os
from ctypes import windll

from db_handler_anp import *
from tkinter.filedialog import askopenfilename
# from tkinter.filedialog import asksaveasfilename
from tkinter import filedialog

if not os.path.exists(os.path.join (os.getcwd(),'fonts' )):
    print ('font folder doesn\'t exist.. Quitting program')
    raise SystemExit()
windll.shcore.SetProcessDpiAwareness(1)

def d():
    dpg.destroy_context()
d()
dpg.create_context()
with dpg.theme() as win1_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (200,200,200), category=dpg.mvThemeCat_Core) #menubar
        dpg.add_theme_color(dpg.mvThemeCol_Header, (131, 180, 215), category=dpg.mvThemeCat_Core)
        
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (143, 143, 143), category=dpg.mvThemeCat_Core) # main window
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 15, category=dpg.mvThemeCat_Core)
        
        dpg.add_theme_color(dpg.mvThemeCol_Button, (200,200,200), category=dpg.mvThemeCat_Core)    # buttons
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (230,230,230) , category=dpg.mvThemeCat_Core)
        
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (230,230,230), category=dpg.mvThemeCat_Core)   # search 
        dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (131, 180, 215), category=dpg.mvThemeCat_Core)
        
        dpg.add_theme_color(dpg.mvThemeCol_Border, (90,90,90), category=dpg.mvThemeCat_Core) # border
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (143, 143, 143), category=dpg.mvThemeCat_Core) # add/edit/del window
        
with dpg.font_registry() as win1_font_registry:
    regular_font = dpg.add_font('fonts/glacial_font.otf', 21)

with dpg.theme() as disp_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (230,230,230),           category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0),                   category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Border, (150,150,150),             category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (192, 179, 197),      category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (137, 129, 129),    category=dpg.mvThemeCat_Core)
        
#+======================================= styling declaration done ========================================

def browse_n_fill(sender):
    if sender not in browse_map.keys():
        print ("who sent it.. error")
    _path =  ''
    if sender != prjfol_b :
        _path = askopenfilename(title="Choose script file", )
    else:
        _path = filedialog.askdirectory()
    if _path != '':
        dpg.configure_item(browse_map[sender], default_value = _path)
    return



with dpg.window(tag= "addscrpt_win", pos = (250,30),  no_resize = True, show= False, no_title_bar=True, modal=True) as win2:
    dpg.add_spacer( height=10)
    with dpg.group(horizontal=True):
        dpg.add_input_text(default_value="", hint="Script name",width=290, on_enter=True, tag= 'scrnm')
        dpg.add_text("    Enter script name")
    dpg.add_spacer( height=10)
    with dpg.group(horizontal=True):
        prjfol   = dpg.add_input_text(default_value="", hint="Project Folder",width=280, on_enter=True,tag=  'prjfol')
        prjfol_b =dpg.add_button(label= "Browse project folder", width=160, callback = browse_n_fill)
    dpg.add_spacer( height=10)
    with dpg.group(horizontal=True):
        scrpath   = dpg.add_input_text(default_value="", hint="Script path",width=290, on_enter=True,tag = 'scrpath')
        scrpath_b = dpg.add_button(label= "Browse file path", width=150,callback = browse_n_fill)
    dpg.add_spacer( height=10)
    with dpg.group(horizontal=True):
        dpg.add_combo(("1","2"), default_value ="", tag= 'sel_gr', width=210)
        dpg.add_combo(("1","2"), default_value ="", tag= 'sel_utl', width=210)
    # with dpg.group(horizontal=True):
        # icopath   = dpg.add_input_text(default_value="", hint="Icon path",width=290, on_enter=True,tag= 'icopath')
        # icopath_b = dpg.add_button(label= "Browse thumbnail", width=150,callback = browse_n_fill)
    dpg.add_spacer( height=30)
    # with dpg.drawlist(width=440, height=240):  # or you could use dpg.add_drawlist and set parents manually
        # dpg.draw_polygon(points=[[1,1], [439,1], [439,238], [1,238], [1,1]], color=[255,0,0],thickness=5 )
    # dpg.add_spacer( height=10)
    with dpg.group(horizontal=True):
        dpg.add_button(label = "Add", width=220, callback = add_script_ui, tag = 'addscript_ok')
        dpg.add_button(label= "Cancel", width=220, callback =Reset_addedit )


browse_map = { prjfol_b:prjfol,
               scrpath_b : scrpath,
              # icopath_b: icopath
              }

#===================================add script button done =========================

def select_View(sender):
    if sender == util_view:
        dpg.set_item_label(util_view, "Util View *")
        dpg.set_item_label(grop_view, "Group View ")
        dpg.set_item_label(flat_view, "Flat View ")
        set_view_mode(1)
        render_scripts()
    elif sender == grop_view:
        dpg.set_item_label(util_view, "Util View ")
        dpg.set_item_label(grop_view, "Group View *")
        dpg.set_item_label(flat_view, "Flat View ")
        set_view_mode(2)
        render_scripts()
    else:
        dpg.set_item_label(util_view, "Util View ")
        dpg.set_item_label(grop_view, "Group View")
        dpg.set_item_label(flat_view, "Flat View *")
        set_view_mode(0)
        render_scripts()


with dpg.window(tag= "Main Window", pos = (0,0),  no_resize = False) as win1:
    with dpg.menu_bar(label="Main menu bar"):
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Save dashboard", callback=save_dashboard)
            dpg.add_menu_item(label="Open dashboard", callback=open_dashboard)
        with dpg.menu(label="Add"):
            dpg.add_menu_item(label="Add script",callback = enable_addscr_window )
            dpg.add_menu_item(label="Add group",callback = lambda: dpg.configure_item("addgrp_win", show=True) )
        with dpg.menu(label="Delete"):
            dpg.add_menu_item(label="Delete script", callback = enable_del_window, tag = 'del_scr')
            dpg.add_menu_item(label="Delete group", callback = enable_del_window, tag = 'del_grp')
        with dpg.menu(label="View"):
            util_view = dpg.add_menu_item(label="Util View", callback = select_View)
            grop_view = dpg.add_menu_item(label="Group View", callback  = select_View)
            flat_view = dpg.add_menu_item(label="Flat View *", callback  = select_View)
        with dpg.menu(label="Tools"):
            dpg.add_menu_item(label="Validate paths- RFU " )
            dpg.add_menu_item(label="View all groups", callback  = view_raw , tag = 'seeg')
            dpg.add_menu_item(label="View all scripts", callback  = view_raw , tag = 'sees')
            # dpg.add_menu_item(label="Button", callback  = render_scripts )
        with dpg.menu(label="Help"):
            dpg.add_menu_item(label="About", callback=open_website)
    dpg.add_button(label = "Run", pos= (400,690), width = 100, height= 40, callback =run_script)
    dpg.add_button(label = "Edit", pos= (510,640), width = 100, height= 40, callback =enable_Edit_window)
    dpg.add_button(label = "Open Folder", pos= (400,640), width = 100, height= 40,callback = open_folder)
    dpg.add_text("Project Name :", pos= (20,640))
    dpg.add_input_text(default_value= "",hint="Project Name will appear here", pos= (130,640),width = 250, tag= 'prj_nm', readonly = True)
    dpg.add_input_text(default_value="", hint="Folder path",width=360, pos= (20,670), tag= 'folder', readonly = True)
    dpg.add_input_text(default_value="", hint="Script path",width=360, pos= (20,700), tag= 'f_path', readonly = True)

    dpg.add_input_text(default_value="", hint="Search Keyword",width=360, pos= (980,640), tag= 'search', callback = search_kw)



with dpg.window(tag="Dashboard", no_title_bar=True, no_resize=True, no_close=True, no_collapse=True, no_move=True,
            pos = (15, 40 ), width=960, height=590) as win6:
    dpg.add_spacer( height=1)
with dpg.window(tag="Info", no_title_bar=True, no_resize=True, no_close=True, no_collapse=True, no_move=True,
            pos = (980, 40 ), width=350, height=590) as win5:
    dpg.add_text(label=  "info", tag = 'info',    wrap = 340)


#=============================  main layout done  =============================

with dpg.window(tag= "addgrp_win", pos = (250,30),  no_resize = True, show= False, no_title_bar=True, modal=True) as win3:
    dpg.add_spacer( height=10)
    with dpg.group(horizontal=True):
        dpg.add_input_text(default_value="", hint="Group name",width=290, on_enter=True, tag= 'grpnm')
        dpg.add_text("    Enter script name")
    dpg.add_spacer( height=10)
    with dpg.group(horizontal=True):
        dpg.add_button(label = "Add", width=220, callback = add_group_ui)
        dpg.add_button(label= "Cancel", width=220, callback = lambda: dpg.configure_item("addgrp_win", show=False) )



with dpg.window(tag= "delete_win", pos = (250,30),  no_resize = False, show= False, no_title_bar=True, modal=True) as win4:
    dpg.add_spacer( height=10)
    with dpg.group(horizontal=True):
        dpg.add_combo(("Yes", "No", "Maybe"), label="Combo", tag= 'delnm')
        # dpg.add_combo(items=('1','2'), width=290, on_enter=True, tag= 'delnm')
        dpg.add_text("Select Item to delete")
    dpg.add_spacer( height=10)
    with dpg.group(horizontal=True):
        dpg.add_button(label = "Delete", width=220, callback = del_items_ui)
        dpg.add_button(label= "Cancel", width=220, callback = lambda: dpg.configure_item("delete_win", show=False) )


#=============================  add group and delete window done ==============

dpg.bind_item_theme(win1, win1_theme)  # toolbar
dpg.bind_item_theme(win2, win1_theme)  # addscript win
dpg.bind_item_theme(win3, win1_theme)  # add group
dpg.bind_item_theme(win4, win1_theme)  # del window
dpg.bind_item_theme(win5, disp_theme)  # readme window
dpg.bind_item_theme(win6, win1_theme)  # dashboard


dpg.bind_item_font(win1, regular_font)  # toolbar
dpg.bind_item_font(win2, regular_font)  # addscript win
dpg.bind_item_font(win3, regular_font)  # add group
dpg.bind_item_font(win4, regular_font)  # del window
dpg.bind_item_font(win5, regular_font)  # readme window
dpg.bind_item_font(win6, regular_font)  # dashboard



dpg.create_viewport(title='Project Manager', width=1360, height=800 )
def clean_up():
    retention_list = ['retention_list', 'this', 'obj_dict','layout','','']
    this = sys.modules[__name__]
    for n in dir():
        if n not in retention_list:  delattr(this, n)
    del this, retention_list, n

def gui_kick_off():
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Main Window", True)
    dpg.start_dearpygui()
    dpg.stop_dearpygui()
    dpg.destroy_context()
def main():
    cwd = os.getcwd()
    db_path = os.path.join(cwd,'prjj_record.db')
    check_n_create_database ( db_path )
    refresh()
    # Start app
    print ('main reached')
    gui_kick_off()
if __name__ == '__main__':
    main()
