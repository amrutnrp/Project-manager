import sqlite3
import os
import shutil
# import tkinter as tk
import webbrowser
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import dearpygui.dearpygui as dpg
import tkinter.messagebox

db_path = 'prjj_record.db'
groups = []
script_details = []
delete_window_flag = True
script_names = []
script_selection_index = -1
view_mode = 0

def open_website():
    webbrowser.open("https://github.com/amrutnrp/Project-manager")

def popup(text):
    tkinter.messagebox.showinfo('stop!', text )
utility_tags = ["Current", "Complete", "Postponed", "Abandoned", "Legacy"]
dashboard_parent = 'Dashboard'

def check_n_create_database(db_path_arg):
    global db_path
    db_path = db_path_arg
    if not os.path.exists(db_path):
        print ('databse doesn\'t exist.. Creating one')
        conn = sqlite3.connect(db_path)
        conn.close()
        create_tables()
    else:
        conn = sqlite3.connect(db_path)
        conn.close()

def create_tables():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE \"GroupName\" (
                        group_nm text)""")
    c.execute("""CREATE TABLE \"Scripts\" (
                        script_name text,
                        script_path text,
                        script_file_path text,
                        thumbnail_path text,
                        utility_tag text,
                        grouptag text
                        )""")
    conn.commit()
    c.execute("""INSERT INTO "GroupName" (group_nm) VALUES (? )""", ("Default",))
    conn.commit()
    conn.close()

def add_script_todb(arg_list):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    script_name, script_path,script_file_path,  thumbnail_path, utility_tag, grouptag  = arg_list
    c.execute("""INSERT INTO "Scripts" (script_name, script_path,script_file_path, thumbnail_path, utility_tag, grouptag)
            VALUES (?, ?, ?, ?, ?, ? )""", (script_name, script_path,script_file_path, thumbnail_path, utility_tag, grouptag,))
    conn.commit()
    conn.close()

def add_group_todb(arg_grp_name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""INSERT INTO "GroupName" (group_nm)
            VALUES (? )""", (arg_grp_name,))
    conn.commit()
    conn.close()


# ==========================  db commmand related changes done ================================


def add_script_ui():
    if dpg.get_item_label('addscript_ok')[0]=='S':
        Edit_ok()
        return
    a= dpg.get_value('scrnm')
    b= dpg.get_value('prjfol')
    c= dpg.get_value('scrpath')
    d= dpg.get_value('icopath')
    util = dpg.get_value('sel_utl')
    grp = dpg.get_value('sel_gr')

    if a in script_names :
        popup ('script with same name already exists')
        return
    elif '' not in [a,b,c,d, util, grp] :
        add_script_todb([a,b,c,d,util ,grp])
        dpg.configure_item("addscrpt_win", show=False)
        print ('script added ')
        Reset_addedit()
        refresh()
        return
    else:
        popup ('data missing')
        return
def add_group_ui():
    a= dpg.get_value('grpnm')
    if a in groups:
        popup ('group name already present ')
        return
    elif a == '' :
        popup ('no name entered for group')
        return
    else:
        add_group_todb(a  )
        dpg.configure_item("addgrp_win", show=False)
        dpg.configure_item("grpnm", default_value="")
        print ('group added ')
        refresh()
        return


def del_items_ui():
    a= dpg.get_value('delnm')
    if a == 'Default':
        popup ('\'Default\' group can\'t be deleted ')
        return
    if delete_window_flag == True:
        table = "GroupName"
        lookup = 'group_nm'
        if a not in groups :
            popup ('Item doesn\'t exist', a)
            return
        # if any project is present in that group, then can't delete that group
        for i in script_details:
            if i[5] == a:
                popup ('This group has projects under it. Please move the projects into another group and try again ')
                return
    else:
        table = "Scripts"
        lookup = 'script_name'
        if a not in script_names :
            popup ('Item doesn\'t exist', a)
            return

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f"""DELETE FROM \"{table}\" WHERE {lookup} = ?""", (a,))
    conn.commit()
    conn.close()
    print (a, 'deleted from table ')
    dpg.configure_item("delete_win", show=False)
    dpg.configure_item("delnm", default_value = '')
    refresh()
    return


def enable_addscr_window(sender):
    dpg.configure_item("addscrpt_win", show=True)
    dpg.configure_item("sel_utl", items=utility_tags, default_value = "Current")
    dpg.configure_item("sel_gr", items=groups, default_value = "Default")
def enable_del_window(sender):
    # print (script_names)
    global delete_window_flag
    dpg.configure_item("delete_win", show=True)
    if sender == dpg.get_alias_id('del_grp') :
        print ('del group selected')
        delete_window_flag= True
        dpg.configure_item("delnm", items=groups, default_value = "Default")
    elif sender == dpg.get_alias_id('del_scr') :
        print ('del script selected')
        delete_window_flag = False
        dpg.configure_item("delnm", items=script_names, default_value = "")

def enable_Edit_window():
    if script_selection_index == -1 :
        popup ('select a project first')
        return
    ls = script_details [script_selection_index  ]
    dpg.configure_item("scrnm", default_value = ls[0] , readonly = True,)
    dpg.configure_item("prjfol",  default_value = ls[1] )
    dpg.configure_item("scrpath", default_value = ls[2])
    dpg.configure_item("icopath", default_value = ls[3] )
    dpg.configure_item("sel_utl", default_value =ls[4] , items=utility_tags)
    dpg.configure_item("sel_gr", default_value =ls[5] , items=groups)

    dpg.configure_item("addscript_ok", label = 'Save Changes' )
    dpg.configure_item("addscrpt_win", show=True)

def Reset_addedit():
    # dpg.configure_item("addscrpt_win", show=False)
    # if dpg.get_item_label('addscript_ok')[0] =='A':
        # return
    dpg.configure_item("addscript_ok", label = 'Add' )
    dpg.configure_item("scrnm", default_value = '', readonly = False )
    dpg.configure_item("prjfol",  default_value = '' )
    dpg.configure_item("scrpath", default_value = '')
    dpg.configure_item("icopath", default_value = '' )
    dpg.configure_item("sel_gr", default_value ="" )
    dpg.configure_item("sel_utl", default_value ="" )
    dpg.configure_item("addscrpt_win", show=False)
    global script_selection_index
    script_selection_index = -1


# ==========================  db related changes done ================================

def read_db ():
    conn = sqlite3.connect('prjj_record.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * from Scripts''')
    scr_ls = cursor.fetchall();
    cursor.execute('''SELECT * from GroupName''')
    grp_ls = cursor.fetchall();
    conn.close()
    global groups ,script_details, script_names
    groups = [ x[0] for x in grp_ls]
    script_details = list (scr_ls)
    script_names = [ x[0] for x in scr_ls ]
    # print (groups)
    # print (script_details)

def refresh():
    read_db()
    render_scripts ()

def open_dashboard():
    file_path = askopenfilename(title="Open Dashboard",
                                filetypes=[("Dashboard File (*.pydsh)", "*.pydsh")],
                                defaultextension=[("Dashboard File (*.pydsh)", "*.pydsh")])
    if file_path == "":
        return
    os.remove(db_path)
    original = file_path
    shutil.copyfile(original, db_path)

    refresh()

def save_dashboard():
    file_path = asksaveasfilename(title="Save Dashboard",
                                  initialfile="pyprojects Dashboard",
                                  filetypes=[("Dashboard File (*.pydsh)", "*.pydsh")],
                                  defaultextension=[("Dashboard File (*.pydsh)", "*.pydsh")])
    if file_path:
        target = file_path
        shutil.copyfile(db_path, target)


def open_folder():
    if script_selection_index == -1 :
        popup ('select a project first')
        return
    folder = script_details [script_selection_index ][1]
    if os.path.exists (folder):
        os.startfile   (folder )
        return
    else:
        popup ('folder doesn\'t exist')
        return

def run_script ():
    if script_selection_index == -1 :
        popup ('select a project first')
        return
    file = script_details [script_selection_index  ][2]
    if os.path.exists (file):
        os.startfile   (file )
        return
    else:
        popup ('file doesn\'t exist')
        return

def trim(text):
    return text[-min(38, len(text)):]

def make_horizontal_group(data, parent_arg):
    with dpg.group(horizontal=True, parent =parent_arg):
        for i in data:
            dpg.add_button(label= f"{i[0]}", width=180, height=50,tag= 'box' + str(i[-1]), callback = show_info)



def Edit_ok():
    global script_selection_index

    scrnm = script_details [script_selection_index ] [0]
    b= dpg.get_value('prjfol')
    c= dpg.get_value('scrpath')
    d= dpg.get_value('icopath')
    util = dpg.get_value('sel_utl')
    grp = dpg.get_value('sel_gr')

    if '' in [b,c,d, util, grp] :
        popup ('Cannot enter a blank field')
        return
    new_values = {
        'script_path'      : b,
        'script_file_path' : c,
        'thumbnail_path'   : d,
       'utility_tag'       : util,
        'grouptag'         : grp
    }
    set_clause = ', '.join([f"{key} = \'{value}\'" for key, value in new_values.items()])
    ss = f"""UPDATE  Scripts SET {set_clause} WHERE script_name = \'{scrnm}\'"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(ss)
    conn.commit()
    conn.close()

    print (scrnm , ' entry updated in table ')
    dpg.configure_item("delete_win", show=False)
    dpg.configure_item("delnm", default_value = '')
    dpg.configure_item("scrnm", readonly = False)
    Reset_addedit ()
    refresh()



def view_raw(sender):
    if sender == 'sees':
        table = 'Scripts'
    elif sender == 'seeg':
        table = 'GroupName'
    conn = sqlite3.connect('prjj_record.db')
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * from {table}''')
    result = cursor.fetchall();
    for i in (result):
        print (i)
    conn.commit()
    conn.close()

def render_scripts(mode= -1, filter_index = []):
    if len(filter_index) == 0:
        script_details_local = [ list(x) + [index] for index , x in enumerate(script_details) ]
    else:
        script_details_local = [  list(x) + [index] for index , x in enumerate(script_details) if index in  filter_index]
    if mode == -1:
        mode = view_mode
    dpg.delete_item(item= dashboard_parent, children_only = True)
    if mode == 0:
        row_data = []
        for index, A in enumerate (script_details_local):
            if len(row_data) == 5:
                make_horizontal_group (row_data, dashboard_parent)
                row_data = []
            row_data.append(A )
        else:
            make_horizontal_group (row_data, dashboard_parent)
        return

    if mode == 1: # based on util value
        table_of_keys = utility_tags
        key_index= 4
    else : # based on group value -- mode 2
        table_of_keys = groups
        key_index= 5
    new_scr_detail = []
    for key in table_of_keys:
        temp= []
        for index, A in enumerate (reversed(script_details_local)):
            if A[key_index] == key:
                temp.append( A )
        new_scr_detail .append(temp)
    row_data = []
    for ikey, key in enumerate ( table_of_keys ):
        tag_= f'tabb{key}{ikey}'
        with dpg.collapsing_header(label=key, tag= tag_, parent = dashboard_parent, default_open = True):
            row_data = []
            for A in new_scr_detail[ikey]:
                if len(row_data) == 5:
                    make_horizontal_group (row_data, tag_)
                    row_data = []
                row_data.append(A)
            else:
                make_horizontal_group (row_data, tag_)

def show_info(sender):
    script_id = int (sender[3:])

    ls = script_details[script_id]
    global script_selection_index

    script_selection_index = script_id

    dpg.configure_item("folder", default_value = trim(ls[1]))
    dpg.configure_item("f_path", default_value = trim(ls[2]))
    dpg.configure_item("prj_nm", default_value = ls[0])
    folder = ls[1]
    contents= "README doesn't exist"
    readme = '-'
    if os.path.exists(folder):
        files =  os.listdir(folder)
        for i in files:
            if "README." in i :
                readme = os.path.join(folder, i)
                break
    if readme != '-':
        with open(readme, "r") as f:
            contents = f.read()
    dpg.configure_item("info", default_value = contents)



#======================= all good till this point ==========================

def search_kw():
    text = dpg.get_value('search')
    filter_index = []
    for idx,i in enumerate( script_details ):
        if text.lower() in i[0].lower():
            filter_index.append (idx)
    if len(filter_index) == 0 and len(text) != 0:
        filter_index = [-1]
    render_scripts(filter_index = filter_index)

def set_view_mode (arg) :
    global view_mode
    view_mode = arg







