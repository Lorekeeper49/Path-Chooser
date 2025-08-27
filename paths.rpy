# - Things you should edit

# Choice Filters: used to filter out paths for organization
#   keys: the category names to use for reference and display
#       variable to set: the defined global that changes with the buttons
#       hidden: determines if the category should be hidden if the player hasn't unlocked it
#       buttons: a list of the buttons associated
#           choice name: the name of the filter
#           variable value: the value the category variable is set to, don't use None, that is no filter
#           needed choices: the choices the player has to have made to unlock the filter
#           hidden: determines if the filter should be hidden if the player hasn't unlocked it
default example_choice_filters = {
    "category": { "variable to set": "example_var", "hidden": False,
        "buttons": [
        {"choice name": "example filter", "variable value": "example value", "needed choices": [], "hidden": False,}
        ]
    },
}

# Path Lists: the lists of paths you can take
#   title: The name of the path, the screen looks for "mod_assets/paths/" + title + ".png" for the thumbnail and expects it to be a 1920x1080 image 
#   needed choices: the choices the player has to have made to unlock the path
#   categories: the categories the path is associated with, used for filtering
#       keys: category name
#       value: the value the filter category needs to be to be shown besides None
#   label: the label to call when the player hits play
#   extra options: extra options that the player can select that change the path slightly
#       option name: the name of the option
#       needed choices: the choices the player has to have made to unlock the option
#       hidden: determines if the option should be hidden if the player hasn't unlocked it
#   hidden: determines if the path should be hidden if the player hasn't unlocked it
default example_path_list = [
    {"title": "Example Title", "needed choices": [], "categories": {"category": "example value"}, "label": "story", "extra options": [{"option name": "item", "needed choices": []}], "hidden": False,}
]

# define your choice filter variables here.  You must use define and not default or there will be an error.
# don't edit these variables in the story or reloading will reset them
define example_var = None

# - Things you shouldn't edit

# The list where all the players choices go when they make them, used to unlock different paths
default persistent.choices_made = []

# Extra items used in the path that the player selected
# Make sure you compensate for these at the start of the label with other variables as this will reset any time you reload or the player loads a save
define extra_selected = []

# The path the player has selected
define selected_path = -1

# Determines if the path should be shown based on which filters are selected
define path_shown = True

# Things you can edit if you want the screen to look different
# Forgive me if the default looks bland in color, I made this with a different mod in mind and had to change around a few things to make it free to use
# This must be called from the title screen using and action like Show("path_chooser", dissolve_scene, choice_filters, path_list) or the game will break attempting to jump out of context when it can't.
screen path_chooser(choice_filters, path_list):
    add "menu_bg"
    frame:
        xysize (640, 720)
        background "#08080880"
    hbox:
        vbox:
            frame:
                text "Filter choices" xalign 0.1 yalign 0.5 style "path_button_text"
                background "#20202080"
            viewport:
                mousewheel True
                draggable True
                has vbox
                for category in choice_filters:
                    for filt in choice_filters[category]["buttons"]:
                        $ path_shown = True
                        if choice_filters[category]["hidden"] and not all(item in persistent.choices_made for item in filt["needed choices"]):
                            $ path_shown = False
                            break
                    if path_shown:
                        frame:
                            text category xalign 0.1 yalign 0.5 style "path_button_text"
                        for filt in choice_filters[category]["buttons"]:
                            if not filt["hidden"] or all(item in persistent.choices_made for item in filt["needed choices"]):
                                button:
                                    hbox:
                                        yalign 0.5
                                        spacing 10
                                        if globals()[choice_filters[category]["variable to set"]] == filt["variable value"]:
                                            frame xysize (40, 40) background "#fff"
                                        else:
                                            frame xysize (40, 40) background "#000"
                                        if filt["needed choices"] is None or all(item in persistent.choices_made for item in filt["needed choices"]):
                                            text filt["choice name"] style "path_button_text"
                                        else:
                                            text "?" style "path_button_text"
                                    action If(filt["needed choices"] is None or all(item in persistent.choices_made for item in filt["needed choices"]), SetVariable(choice_filters[category]["variable to set"], filt["variable value"]))
                        button:
                            hbox:
                                yalign 0.5
                                spacing 10
                                if globals()[choice_filters[category]["variable to set"]] is None:
                                    frame xysize (40, 40) background "#fff"
                                else:
                                    frame xysize (40, 40) background "#000"
                                text "No filter" style "path_button_text"
                            action SetVariable(choice_filters[category]["variable to set"], None)
                        button:
                            hbox:
                                yalign 0.5
                                spacing 10
                                if globals()[choice_filters[category]["variable to set"]] == False:
                                    frame xysize (40, 40) background "#fff"
                                else:
                                    frame xysize (40, 40) background "#000"
                                text "Hide all" style "path_button_text"
                            action SetVariable(choice_filters[category]["variable to set"], False)
    vbox:
        spacing -4
        frame:
            xpos 640
            xsize 500
            text "Choose your path" xcenter 250 yalign 0.5 style "path_button_text"
        frame:
            xpos 636
            xysize (500, 640)
            background "#0000"
            viewport:
                mousewheel True
                draggable True
                has vbox
                spacing 10
                for i in range(len(path_list)):
                    for category in path_list[i]["categories"]:
                        $ path_shown = True
                        if (globals()[choice_filters[category]["variable to set"]] is not None and globals()[choice_filters[category]["variable to set"]] != path_list[i]["categories"][category]) or (path_list[i]["hidden"] and not all(item in persistent.choices_made for item in path_list[i]["needed choices"])):
                            $ path_shown = False
                            break
                    if path_shown:
                        button:
                            xysize (500, 300)
                            if path_list[i]["needed choices"] is None or all(item in persistent.choices_made for item in path_list[i]["needed choices"]):
                                text path_list[i]["title"] style "path_title" xcenter 250
                                add "mod_assets/paths/" + path_list[i]["title"] + ".png" xalign 0.25 yalign 0.5 zoom 0.2
                            else:
                                text "Locked Path" style "path_title" xcenter 250
                                frame xysize (384, 216) xalign 0.25 yalign 0.5 background "#000"
                            if selected_path == i:
                                background "#ffffff40"
                            else:
                                background "#00000000"
                            hover_background "#ffffff80"
                            action If(path_list[i]["needed choices"] is None or all(item in persistent.choices_made for item in path_list[i]["needed choices"]), [ToggleVariable("selected_path", i, -1)])
    vbox:
        spacing -4
        button:
            xysize (140, 140)
            xalign 1.0
            yalign 1.0
            xpos 1280
            background "#00000000"
            hover_background "#ffffff80"
            text "Back" style "path_button_text" xalign 0.5 yalign 0.5
            action Hide("path_chooser", dissolve_scene)          
        if selected_path != -1:
            frame:
                xalign 1.0
                xpos 1280
                xysize (144, 450)
                background "#0000"
                viewport:
                    mousewheel True
                    draggable True
                    has vbox
                    if path_list[selected_path]["extra options"] is not None:
                        for option in path_list[selected_path]["extra options"]:
                            if not option["hidden"] or all(item in persistent.choices_made for item in option["needed choices"]):
                                button:
                                    xysize (140, 140)
                                    if option["option name"] in extra_selected:
                                        background "#ffffff40"
                                    else:
                                        background "#00000000"
                                    hover_background "#ffffff80"
                                    if option["needed choices"] is None or all(item in persistent.choices_made for item in option["needed choices"]):
                                        text option["option name"] style "path_button_text" xalign 0.5 yalign 0.5
                                    else:
                                        text "?" style "path_button_text" xalign 0.5 yalign 0.5
                                    action If(option["needed choices"] is None or all(item in persistent.choices_made for item in option["needed choices"]), ToggleSetMembership(extra_selected, option["option name"]))
            button:
                xysize (140, 140)
                xalign 1.0
                yalign 1.0
                xpos 1280
                background "#00000000"
                hover_background "#ffffff80"
                text "Play" style "path_button_text" xalign 0.5 yalign 0.5
                action Function(renpy.jump_out_of_context, path_list[selected_path]["label"])

style path_button is gui_button

style path_button:
    size_group "navigation"
    background "#bb559980"
    hover_background "#ffaacc80"
    xsize 640
    ysize 80
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style path_frame:
    size_group "navigation"
    background "#bb559980"
    xsize 640
    ysize 80
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style path_button_text:
    properties gui.button_text_properties("navigation_button")
    font "gui/font/RifficFree-Bold.ttf"
    color "#fff"
    outlines [(4, "#b59", 0, 0), (2, "#b59", 2, 2)]
    hover_outlines [(4, "#fac", 0, 0), (2, "#fac", 2, 2)]
    insensitive_outlines [(4, "#fce", 0, 0), (2, "#fce", 2, 2)]

style path_text:
    properties gui.button_text_properties("navigation_button")
    font "gui/font/RifficFree-Bold.ttf"
    color "#fff"
    outlines [(4, "#b59", 0, 0), (2, "#b59", 2, 2)]

style path_title:
    properties gui.button_text_properties("navigation_button")
    font "gui/font/RifficFree-Bold.ttf"
    color "#fff"
    outlines [(4, "#b59", 0, 0), (2, "#b59", 2, 2)]
    size 34
    text_align 0.5