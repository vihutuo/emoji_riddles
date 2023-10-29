import flet as ft
import random
import string
import mymodules.emoji as emoji
import mymodules.utils as utils
import mymodules.item_navigator
import mymodules.user_emoji_item

import time


def IndexView(page, params):
  def SaveAllData():
    data = lst_py_user_emoji_items.model_dump()
    print("Data Saved")
    page.client_storage.set("lshss.emoji.user_emoji_items", data)
    
  def LoadAllData():
      nonlocal lst_py_user_emoji_items
      if page.client_storage.contains_key("lshss.emoji.user_emoji_items"):
          try:
            data=page.client_storage.get("lshss.emoji.user_emoji_items")
          #  print("data",data)
            lst_py_user_emoji_items = mymodules.user_emoji_item.ListUserEmojiItem(**data) 
            #print("user_emoji_items",user_emoji_items)
            print("Data Loaded")  
            print("Count items", len(lst_py_user_emoji_items.items))
          except Exception as error:
            print("Error loading save data",error)
            lst_py_user_emoji_items = mymodules.user_emoji_item.ListUserEmojiItem() 


  def GameOver():
    #WON
    def close_dlg(e):
        dlg_modal.open = False
        nav_items.move_next()
        
        page.update()
      
    nonlocal  is_game_over
    is_game_over = True
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Congratulations"),
        content=ft.Text("You Won!",size=40),
        actions=[
            ft.TextButton("OK",on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    page.dialog = dlg_modal
    dlg_modal.open = True
    
    page.update()
    
  def on_nav_change_item(e):
    nonlocal selected_ind
    selected_ind = nav_items.current-1
    SaveAllData()
    NewGame()
    #print(f"{nav_items.current=}")
  
  def get_current_user_emoji_item():
    return user_emoji_items[selected_ind]
  
  def return_all_user_letters():
    if get_current_user_emoji_item().is_complete:
      return
      
    for x in user_letters:
      return_user_letter(x)
      
  def update_all_user_letters(update=True):
     return_all_user_letters()
     do_update= False
     for i in  range(len(user_letters)):
         if i in user_emoji_items[selected_ind].hint_positions:
           if user_letters[i].text != correct_answer[i]:
             disable_word_letter(correct_answer[i])   
             
             #return_user_letter(user_letters[i]) 
             do_update=True
             user_letters[i].disabled = True
             user_letters[i].text = correct_answer[i]
             #print("Remove",correct_answer[i])
             #user_letters[i].update()
             
     if do_update and update:
       row_user_letters.update()
       
       
  def disable_word_letter(letter):
     for x in  row_word_letters.controls:
       
       if x.text == letter and x.disabled==False:
         #print(f"{x.text=}")
         x.disabled = True
         x.text = ""
         #x.opacity = 0
         x.update()
         break
       
  def hint_clicked(e):
    if hints_remaining >0:
      old_hint_positions = user_emoji_items[selected_ind].hint_positions
      #print(f"{old_hint_positions=}")
      set_old_hints  = set(old_hint_positions)
      unrevealed_positions = set_old_hints.symmetric_difference(range(0,len(correct_answer)))
      #remove white spaces from unrevealed_positions
      for i,x in enumerate(correct_answer):
        
        if x == "\n" or x == " ":
          unrevealed_positions.remove(i)
          
      print(type(unrevealed_positions))
      reveal_count = 2
      if len(unrevealed_positions) < reveal_count:
        reveal_count= len(unrevealed_positions)
      #print(f"{unrevealed_positions=}")
      #print(f"{reveal_count=}")
      hint_positions = random.sample(sorted(unrevealed_positions),reveal_count)
      
      for x in hint_positions:
        old_hint_positions.append(x)
        
      update_all_user_letters()
      #print("Hint positions",user_emoji_items[selected_ind].hint_positions)

      if txt_hint_text.opacity == 0:
        txt_hint_text.opacity = 1
        txt_hint_text.update()
      check_answer()
      
      
  def check_answer():
    
     
    e=get_current_user_emoji_item()
    if e.is_complete:
       return
      
    i=0
    for x in user_letters:
       
       if x.text != correct_answer[i] or x.text == "":
         return
       
       i+=1    
    #Won
    e.is_complete = True
    for x in user_letters:
       x.style.bgcolor  = ft.colors.PRIMARY
       x.update()
    #GameOver()     
     
  def return_user_letter(letter_ctrl):
    alphabet = letter_ctrl.text
    if alphabet!="" and not letter_ctrl.disabled :
       letter_ctrl.data.text = alphabet
       #e.control.data.opacity = 1
       letter_ctrl.data.update()
       letter_ctrl.text = ""
       letter_ctrl.update()
       # check_answer()

  def user_letter_box_clicked(e):
    if get_current_user_emoji_item().is_complete:
      return 
    return_user_letter(e.control)
     
  def word_letter_box_clicked(e):
    alphabet = e.control.text
    if alphabet != "":
      for x in  user_letters:
       if x.text == "" and x.disabled == False:
          x.text = alphabet
          x.data = e.control
          
          x.update()
          e.control.text=""
         # e.control.opacity =0
          e.control.update()
          page.update()
          #print("Checking",x.text)
          check_answer()
          break
          
  def CreateWordLetterBoxes(word):

    #check if letters were already generated
    if not user_emoji_items[selected_ind].word_letters :    
            
          extra_letters = 0
          if len(word)<=8:
            extra_letters = 5
          elif len(word)<= 14: 
            extra_letters = 4
          else:
            extra_letters = 1          
          rnd_string = random.sample(string.ascii_uppercase,extra_letters)
          rnd_word = word+"".join(rnd_string)
          rnd_word= rnd_word.replace(" ","")
          rnd_word= rnd_word.replace("\n","")
          rnd_word = utils.ShuffleString(rnd_word)
      
          user_emoji_items[selected_ind].SetWordLetters(rnd_word)
      
    rnd_word = user_emoji_items[selected_ind].word_letters
    for i in range(len(rnd_word)):
        btn_1 = ft.OutlinedButton(rnd_word[i],
                            width=40,
                            height=40,      
                            on_click = word_letter_box_clicked,        
                            style=ft.ButtonStyle(
                              shape=ft.RoundedRectangleBorder(radius=20), 
                              padding=3))
        row_word_letters.controls.append(btn_1)  
    #row_word_letters.update()
      
  def CreateUserLetterBoxes(word):
    length = len(word)
    spacing=5
    r = ft.Row(alignment=ft.MainAxisAlignment.CENTER,spacing=spacing)
    e= get_current_user_emoji_item()
    alphabet = ""
    disable = False
    bgcolor = ft.colors.SECONDARY
    if e.is_complete:
        disable = True
        bgcolor = ft.colors.PRIMARY
    for i in range(length):
        if e.is_complete:
          alphabet = word[i]
        btn_1 = ft.ElevatedButton(alphabet,
                            width=37,
                            height=37,
                            disabled=disable ,      
                                             
                                
                            on_click = user_letter_box_clicked,      
                                  
                            style=ft.ButtonStyle(  
                              shape=ft.RoundedRectangleBorder(radius=7), 
                              padding=0,
                              bgcolor= bgcolor,
                              color=ft.colors.WHITE,               
                              
                                        )
                               )
        if word[i] == " ":
          btn_1.disabled = True
          btn_1.text = " "
          btn_1.opacity=0
        elif word[i] == "\n":
          btn_1.disabled = True
          btn_1.text = "\n"
          #btn_1.opacity=0
          #btn_1.width=0
          btn_1.visible = False
          row_user_letters.controls.append(r)
          r = ft.Row(alignment=ft.MainAxisAlignment.CENTER,spacing=spacing)
        
          
        r.controls.append(btn_1)
       
        user_letters.append(btn_1)
    row_user_letters.controls.append(r)
    #row_user_letters.update()
      
  def restart_clicked(e):
    NewGame()
  def NewGame():
    nonlocal is_game_over
    is_game_over= False
    user_letters.clear()
    row_user_letters.controls.clear()
    row_word_letters.controls.clear()
    hint_count = 0
    LoadNewImage()
    CreateUserLetterBoxes(correct_answer)
    
    if  user_emoji_items[selected_ind].is_complete:
       row_word_letters.update()
       hint_btn.disabled = True
       hint_btn.update()
    else:  
       CreateWordLetterBoxes(correct_answer)
       hint_btn.disabled = False
       hint_btn.update()
      
    update_all_user_letters(False)

    txt_hint_text.opacity = 0
    txt_hint_text.value = hint
    txt_hint_text.update()
    print("Correct Answer",correct_answer)
    page.update()
    
    
  def LoadNewImage():
    #nonlocal selected_ind
    nonlocal correct_answer
    nonlocal hint
    
    file_name = lst_images[selected_ind][0]
    correct_answer = lst_images[selected_ind][1].upper()
    hint = lst_images[selected_ind][2].title()
    
   
    txt_emote.value = file_name
    txt_emote.update()
    #print("New quetion loaded")
      
  #####Game variables
  lst_images =emoji.GetAllEmotes()
  #page.client_storage.remove("lshss.emoji.user_emoji_items")

  lst_py_user_emoji_items  = mymodules.user_emoji_item.ListUserEmojiItem()
  
  LoadAllData()
  user_emoji_items = lst_py_user_emoji_items.items
  if user_emoji_items == []:
      #print("EMPTY")
      for x in lst_images :
        user_emoji_items.append(mymodules.user_emoji_item.UserEmojiItem())
  #print(user_emoji_items)
  user_letters = []
  #all_emotes = emoji.GetAllEmotes()
  selected_ind = 0
  correct_answer = ""
  is_game_over = False
  hint=""
  hints_remaining = 5 
  #img_1 = ft.Image(src="", width=300)
  txt_msg = ft.Text("")
  txt_hint_text= ft.Text("",opacity =0,size=18, color=ft.colors.SECONDARY)
  txt_emote= ft.Text("🕸 + 🏃‍♂️",size=65 )
  appbar = ft.AppBar(
                      title=ft.Text("Emoji Enigma",font_family="Roberto"),        
                      bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
                ft.IconButton(ft.icons.RESTART_ALT,on_click=restart_clicked,icon_color="Green"), 
                    
                ]
                            
                    )
  
  
  hint_btn  =  ft.ElevatedButton(text="🔆Hint",width=75,height=25, 
                                   on_click=hint_clicked,
                                   style=ft.ButtonStyle(
                                       shape=ft.RoundedRectangleBorder(radius=3),
                                       bgcolor="yellow",padding=1
                                                )
                                   )
                                   
  
  txt_question_no= ft.Text("1/20")
  nav_items = mymodules.item_navigator.ItemNavigator(1,len(lst_images),1,on_change_item=on_nav_change_item) 
  
   
  
  row_user_letters = ft.Column(width=365,alignment=ft.MainAxisAlignment.CENTER)
  row_word_letters = ft.Row(width=365,wrap=True,alignment=ft.MainAxisAlignment.CENTER,spacing=6)

  #page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
  page.views.append(
           ft.View(
             "/",
           [appbar,
           
            ft.Container(content=txt_emote,height=100),
            ft.Container(content=row_user_letters,margin=ft.margin.symmetric(0),height=130),
            hint_btn,
            txt_hint_text,
            ft.Container(content=row_word_letters,margin=ft.margin.symmetric(0),height=130),
            ft.Row(controls=[nav_items],alignment=ft.MainAxisAlignment.CENTER),                           
                      
                     
           ],
           horizontal_alignment=ft.CrossAxisAlignment.CENTER,
           scroll = ft.ScrollMode.AUTO
            
                ),
            
    
            )

  page.update()
  
  print(page)
  NewGame()