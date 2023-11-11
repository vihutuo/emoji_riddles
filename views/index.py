import os
import flet as ft
import random
import string
import mymodules.emoji as emoji
import mymodules.utils as utils
import mymodules.item_navigator
import mymodules.user_emoji_item
import mymodules.analytics
import mymodules.print_debug
import pendulum
from dotenv import load_dotenv
import json

async def IndexView(page:ft.Page, params):

  async def UpdateHintsRemaining(new_value):
      nonlocal hints_remaining
      hints_remaining = new_value
      badge_hint.text = f"{hints_remaining}"

      if hints_remaining<=0:
          hint_btn.disabled = True
      else:
          hint_btn.disabled = False
      await badge_hint.update_async()

  async def UpdateScore():
      score = GetScore()
      txt_score.value = "Score : " + str(score)
      print("Score",score)
      analytics.UpdateMatch(score)
      await txt_score.update_async()

  async def update_player_name(new_name):
      nonlocal player_name
      player_name = new_name
      txt_playername.spans[0].text = player_name
      await txt_playername.update_async()

  async def player_name_clicked(e):
      txt_name = ft.Ref[ft.TextField]()
      async def close_dlg_ok(e):
          await update_player_name(txt_name.current.value)
          dlg_modal.open = False
          await page.update_async()
          await  SavePlayerName()
          analytics.UpdateUser(player_name)

      async def close_dlg_cancel(e):
          dlg_modal.open = False
          await page.update_async()

      dlg_modal = ft.AlertDialog(
          modal=True,
          title=ft.Text("Enter your name"),
          content=ft.TextField(ref=txt_name, hint_text="Enter your name",value=player_name,max_length=10),
          actions=[
              ft.TextButton("OK", on_click=close_dlg_ok),
              ft.TextButton("Cancel", on_click=close_dlg_cancel),
          ],
          actions_alignment=ft.MainAxisAlignment.CENTER,
      )
      page.dialog = dlg_modal
      dlg_modal.open = True

      await page.update_async()


  def GetScore():
      score = 0
      for x in lst_py_user_emoji_items.items:
          if x.is_complete:
              score += 1
      return score

  def get_high_score_table(json_data):
      #print("Drawinh HS table")
      data = json_data
      #print(data)
      tbl = ft.DataTable(columns=[
                                ft.DataColumn(ft.Text("Name")),
                                ft.DataColumn(ft.Text("Score"),numeric=True),
                                ft.DataColumn(ft.Text("Date")),
                            ],
                            heading_row_height=0,
                            column_spacing=50,
                            rows=[]
                        )
      for item in data:
          try:
            end_time = pendulum.parse(item["end_time"]).format("DD MMM")
          except Exception:
              print("Error time")
              end_time = ""
          try:
              tbl.rows.append(ft.DataRow(
                           cells=[
                                ft.DataCell(ft.Text(item["player_name"])),
                                ft.DataCell(ft.Text(item["score"])),
                                ft.DataCell(ft.Text(str(end_time))),
                                ]))
          except Exception as error:
              print(str(error))

      return tbl

  async def page_on_connect(e):
      await print_bug.print_msg("Session connect")

  async def page_on_disconnect(e):
      #await print_bug.print_msg("Session disconnect")
      #await SaveAllData()
      print("Session disconnect")

  async def page_on_close(e):
      pass
      #await SaveAllData()
      #await print_bug.print_msg("Session Close")

  async def page_on_error(e):
      await print_bug.print_msg(str(e))
      #await page.update_async()

  async def reset_save_data():
      analytics.userid = ""
      new_player_name = "Player" +  str(random.randrange(1,1000))
      await update_player_name(new_player_name)

      analytics.SetMatchID(0)
      analytics.StartSession(page.client_ip, page.client_user_agent, player_name, page.platform, page.session_id)

      if await page.client_storage.contains_key_async("lshss.emoji.user_emoji_items"):
          await page.client_storage.remove_async("lshss.emoji.user_emoji_items")
          print("Save data gone")
      if await page.client_storage.contains_key_async("lshss.emoji.score"):
          await page.client_storage.remove_async("lshss.emoji.score")
      if await page.client_storage.contains_key_async("lshss.emoji.userid"):
          await page.client_storage.remove_async("lshss.emoji.userid")
      if await page.client_storage.contains_key_async("lshss.emoji.player_name"):
          await page.client_storage.remove_async("lshss.emoji.player_name")
      if await page.client_storage.contains_key_async("lshss.emoji.match_id"):
          await page.client_storage.remove_async("lshss.emoji.match_id")

      nonlocal lst_py_user_emoji_items
      nonlocal user_emoji_items
      nonlocal  hints_remaining
      hints_remaining = 3
      lst_py_user_emoji_items = mymodules.user_emoji_item.ListUserEmojiItem()
      lst_py_user_emoji_items.FillEmptyItems(len(lst_images))
      user_emoji_items = lst_py_user_emoji_items.items
      analytics.StartMatch("")
      await NewGame()
      await UpdateHintsRemaining(hints_remaining)

      #await LoadAllData()

  async def SaveUserId():
      await page.client_storage.set_async("lshss.emoji.user_id", analytics.userid)

  async def SaveMatchID(match_id):
      if match_id > 0:
         await page.client_storage.set_async("lshss.emoji.match_id", match_id)

  async def SavePlayerName():
      await page.client_storage.set_async("lshss.emoji.player_name", player_name)

  async def SaveAllData():

        data = lst_py_user_emoji_items.model_dump()
       # print("Data Saved")
        await page.client_storage.set_async("lshss.emoji.user_emoji_items", data)
        await SavePlayerName()
        await SaveUserId()
        await SaveMatchID(analytics.match_id)

  async def load_match_id():
      match_id = 0
      if await page.client_storage.contains_key_async("lshss.emoji.match_id"):
          try :
              match_id = await page.client_storage.get_async("lshss.emoji.match_id")
              match_id = int(match_id)
              if match_id > 0:
                   analytics.SetMatchID(match_id)
          except Exception as error:
             print("Error loading match id")
             return match_id

      return match_id


  async def load_player_name():
      nonlocal player_name

      if await page.client_storage.contains_key_async("lshss.emoji.player_name"):
          try :
              player_name = await page.client_storage.get_async("lshss.emoji.player_name")
          except Exception as error:
             print("Error loading player name")

  async def load_user_id():
      if await page.client_storage.contains_key_async("lshss.emoji.user_id"):
         # print("Loading userid")
          try :
              analytics.userid = await page.client_storage.get_async("lshss.emoji.user_id")
          except Exception as error:
             print("Error loading userid")
      else:

          print("Userid not in storage")

  async def LoadAllData():
      nonlocal lst_py_user_emoji_items
      nonlocal  user_emoji_items

      #lst_py_user_emoji_items = mymodules.user_emoji_item.ListUserEmojiItem()
      #lst_py_user_emoji_items.FillEmptyItems(len(lst_images))
      #user_emoji_items = lst_py_user_emoji_items.items

      await load_player_name()
      await load_user_id()
      await load_match_id()
      if await page.client_storage.contains_key_async("lshss.emoji.user_emoji_items"):
          try:
            data=await page.client_storage.get_async("lshss.emoji.user_emoji_items")
          #  print("data",data)
            lst_py_user_emoji_items = mymodules.user_emoji_item.ListUserEmojiItem(**data)
            user_emoji_items = lst_py_user_emoji_items.items
            #print("user_emoji_items",user_emoji_items)
            #print("Data Loaded")
            #print("Count items", len(lst_py_user_emoji_items.items))
          except Exception as error:
            print("Error loading save data",error)
            lst_py_user_emoji_items = mymodules.user_emoji_item.ListUserEmojiItem()
            lst_py_user_emoji_items.FillEmptyItems(len(lst_images))
            user_emoji_items = lst_py_user_emoji_items.items

      else:
            print("Loading fresh ")
            lst_py_user_emoji_items = mymodules.user_emoji_item.ListUserEmojiItem()
            lst_py_user_emoji_items.FillEmptyItems(len(lst_images))
            user_emoji_items = lst_py_user_emoji_items.items

  async def GameOver():
    #WON
    async def close_dlg(e):
        dlg_modal.open = False
        await nav_items.move_next()
        
        await page.update_async()
      
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
    
    await page.update_async()
    
  async def on_nav_change_item(e):
    nonlocal selected_ind
    selected_ind = nav_items.current-1
    #await SaveAllData()
    await NewGame()
    #print(f"{nav_items.current=}")
  
  def get_current_user_emoji_item():
    return user_emoji_items[selected_ind]
  
  async def return_all_user_letters():
    if get_current_user_emoji_item().is_complete:
      return
      
    for x in user_letters:
      await return_user_letter(x)
      
  async def update_all_user_letters(update=True):
     await return_all_user_letters()
     do_update= False
     for i in  range(len(user_letters)):
         if i in user_emoji_items[selected_ind].hint_positions:
           if user_letters[i].text != correct_answer[i]:
             await disable_word_letter(correct_answer[i])
             
             #return_user_letter(user_letters[i]) 
             do_update=True
             user_letters[i].disabled = True
             user_letters[i].text = correct_answer[i]
             #print("Remove",correct_answer[i])
             #user_letters[i].update_async()
             
     if do_update and update:
       await row_user_letters.update_async()
       
  async def disable_word_letter(letter):
      ue = get_current_user_emoji_item()
      if ue.is_complete:
          #print("Complete")
          return
      for x in row_word_letters.controls:
          if x.text == letter and not x.disabled:
             #print(f"{x.text=}")
             x.disabled = True
             x.text = ""
             #x.opacity = 0
             await x.update_async()
             break
       
  async def hint_clicked(e):
    if hints_remaining >0:
      await UpdateHintsRemaining(hints_remaining - 1)
      old_hint_positions = user_emoji_items[selected_ind].hint_positions
      #print(f"{old_hint_positions=}")
      set_old_hints = set(old_hint_positions)
      unrevealed_positions = set_old_hints.symmetric_difference(range(0,len(correct_answer)))
      #remove white spaces from unrevealed_positions
      for i,x in enumerate(correct_answer):
        
        if x == "\n" or x == " ":
          unrevealed_positions.remove(i)
          
      #print(type(unrevealed_positions))
      reveal_count = 3
      if len(unrevealed_positions) < reveal_count:
        reveal_count= len(unrevealed_positions)
      #print(f"{unrevealed_positions=}")
      #print(f"{reveal_count=}")
      hint_positions = random.sample(sorted(unrevealed_positions),reveal_count)
      
      for x in hint_positions:
        old_hint_positions.append(x)
        
      await update_all_user_letters()
      #print("Hint positions",user_emoji_items[selected_ind].hint_positions)

      if txt_hint_text.opacity == 0:
        txt_hint_text.opacity = 1
        await txt_hint_text.update_async()
      await check_answer()

      
  async def check_answer():
    e = get_current_user_emoji_item()
    if e.is_complete:
       return
    i = 0
    for x in user_letters:
       if x.text != correct_answer[i] or x.text == "":
         return
       i += 1
    #Won
    e.is_complete = True
    await UpdateScore()
    await UpdateHintsRemaining(hints_remaining+1)
    for x in user_letters:
       x.style.bgcolor = ft.colors.PRIMARY
       await x.update_async()
    await SaveAllData()
    #GameOver()     
     
  async def return_user_letter(letter_ctrl):
    alphabet = letter_ctrl.text
    if alphabet!="" and not letter_ctrl.disabled :
       letter_ctrl.data.text = alphabet
       #e.control.data.opacity = 1
       await letter_ctrl.data.update_async()
       letter_ctrl.text = ""
       await letter_ctrl.update_async()
       # check_answer()

  async def user_letter_box_clicked(e):
    if get_current_user_emoji_item().is_complete:
      return 
    await return_user_letter(e.control)
     
  async def word_letter_box_clicked(e):
    alphabet = e.control.text
    if alphabet != "":
      for x in  user_letters:
       if x.text == "" and x.disabled == False:
          x.text = alphabet
          x.data = e.control
          await x.update_async()
          e.control.text=""
         # e.control.opacity =0
          await e.control.update_async()
          #page.update()
          #print("Checking",x.text)
          await check_answer()
          break
          
  async def CreateWordLetterBoxes(word):
    #check if letters were already generated
    if not user_emoji_items[selected_ind].word_letters :
          extra_letters = 0
          if len(word)<=8:
            extra_letters = 5
          elif len(word)<= 14: 
            extra_letters = 4
          else:
            extra_letters = 1          
          rnd_string = random.sample(string.ascii_uppercase, extra_letters)
          rnd_word = word+"".join(rnd_string)
          rnd_word= rnd_word.replace(" ","")
          rnd_word= rnd_word.replace("\n","")
          rnd_word = utils.ShuffleString(rnd_word)

      
          user_emoji_items[selected_ind].SetWordLetters(rnd_word)
      
    rnd_word = user_emoji_items[selected_ind].word_letters
    #print(rnd_word)
    for i in range(len(rnd_word)):
        btn_1 = ft.OutlinedButton(rnd_word[i],
                            width=40,
                            height=40,      
                            on_click = word_letter_box_clicked,        
                            style=ft.ButtonStyle(
                              shape=ft.RoundedRectangleBorder(radius=20), 
                              padding=3))
        row_word_letters.controls.append(btn_1)  
    await row_word_letters.update_async()
      
  def CreateUserLetterBoxes(word):
    length = len(word)
    spacing=3
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
                            width=36,
                            height=36,
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
      
  async def restart_clicked(e):
      #txt_msg.value = ""
      #await txt_msg.update_async()
      async def close_dlg_yes(e):
          dlg_modal.open = False
          await reset_save_data()
          await page.update_async()

      async def close_dlg(e):
          dlg_modal.open = False
          await page.update_async()
      dlg_modal = ft.AlertDialog(
          modal=True,
          title=ft.Text("Please confirm"),
          content=ft.Text("Are you sure you want to delete all saved data?"),
          actions=[
              ft.TextButton("Yes", on_click=close_dlg_yes),
              ft.TextButton("No", on_click=close_dlg),
          ],
          actions_alignment=ft.MainAxisAlignment.END,
          on_dismiss=lambda e: print("Modal dialog dismissed!"),
      )
      page.dialog = dlg_modal
      dlg_modal.open = True
      await page.update_async()


  async def show_high_scores(e):

          data = analytics.get_high_scores(10,0)
          #await print_bug.print_msg(data)
          async def close_dlg(e):
              dlg_modal.open = False
              await page.update_async()
          dlg_modal = ft.AlertDialog(
              modal=True,
              title=ft.Text("High Scores"),
              content=get_high_score_table(data),
              #content=ft.Text("hhh"),
              actions=[
                  ft.TextButton("OK", on_click=close_dlg),
              ],
              actions_alignment=ft.MainAxisAlignment.CENTER,
          )
          page.dialog = dlg_modal
          dlg_modal.open = True

          await page.update_async()


  async def NewGame():
    nonlocal is_game_over
    is_game_over= False
    user_letters.clear()
    row_user_letters.controls.clear()
    row_word_letters.controls.clear()
    hint_count = 0
    await LoadNewImage()
    CreateUserLetterBoxes(correct_answer)
    
    if  user_emoji_items[selected_ind].is_complete:
       #row_word_letters.update()
       hint_btn.disabled = True
       #hint_btn.update()
    else:  
       await CreateWordLetterBoxes(correct_answer)
       hint_btn.disabled = False
       #hint_btn.update()
      
    await update_all_user_letters(False)

    txt_hint_text.opacity = 0
    txt_hint_text.value = hint

    #txt_hint_text.update()
    #print("Correct Answer",correct_answer)
    await UpdateScore()
    await page.update_async()
    
    
  async def LoadNewImage():
    #nonlocal selected_ind
    nonlocal correct_answer
    nonlocal hint
    
    file_name = lst_images[selected_ind][0]
    correct_answer = lst_images[selected_ind][1].upper()
    hint = lst_images[selected_ind][2].title()
    txt_emote.value = file_name
    await txt_emote.update_async()
    #print("New question loaded")
      
  #####Game variables
  lst_images = emoji.GetAllEmotes()
  #page.client_storage.remove("lshss.emoji.user_emoji_items")
  player_name = "Player" + str(random.randrange(1,1000))
  lst_py_user_emoji_items = mymodules.user_emoji_item.ListUserEmojiItem()
  user_emoji_items = None
  score = 0

  load_dotenv()
  analytics = mymodules.analytics.Analytics(3,
                                            os.getenv('salt'),
                                            os.getenv('pepper'),
                                            os.getenv('analytics_domain'),
                                            os.getenv('this_domain')
                                            )

  await LoadAllData()

  user_letters = []
  selected_ind = 0

  correct_answer = ""
  is_game_over = False
  hint=""
  hints_remaining = 3
  #img_1 = ft.Image(src="", width=300)
  txt_msg = ft.Text("")
  txt_hint_text= ft.Text("",opacity=0, size=18, color=ft.colors.SECONDARY)
  txt_emote = ft.Text("🕸 + 🏃‍♂️",size=65, font_family="NotoEmoji" )
  txt_debug = ft.Text("", size=18, color=ft.colors.TERTIARY)


  txt_playername = ft.Text(style=ft.TextThemeStyle.LABEL_LARGE,spans=[ft.TextSpan(player_name, on_click=player_name_clicked,
                                                      style=ft.TextStyle(
                                                      decoration=ft.TextDecoration.UNDERLINE,
                                                      decoration_style=ft.TextDecorationStyle.DOTTED,
                                                      size=18,
                                                      color=ft.colors.SECONDARY
                                                                   )
                                               )
                                   ]
                          )
  txt_score = ft.Text(str(GetScore()),size=18,color=ft.colors.SECONDARY)
  #txt_score_text = ft.Text("Score ")


  appbar = ft.AppBar(
                      title=ft.Text("Emoji Enigma"),
                      bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
                ft.IconButton(ft.icons.RESTART_ALT,on_click=restart_clicked,icon_color=ft.colors.PRIMARY),
                ft.IconButton(content=ft.Text("🥇",size=16), on_click=show_high_scores, icon_color="Green"),

        ]
                            
                    )
  
  
  hint_btn  =  ft.ElevatedButton(text=f"🔆Hint",width=75,height=25,
                                   on_click=hint_clicked,

                                   style=ft.ButtonStyle(
                                       shape=ft.RoundedRectangleBorder(radius=3),
                                       bgcolor="yellow",padding=1
                                                )
                                   )
                                   
  badge_hint = ft.Badge(content=hint_btn,text=f"{hints_remaining}",


                        )
  txt_question_no= ft.Text("1/20")
  nav_items = mymodules.item_navigator.ItemNavigator(1,len(lst_images),1,on_change_item=on_nav_change_item) 
  
   
  
  row_user_letters = ft.Column(width=365,alignment=ft.MainAxisAlignment.CENTER)
  row_word_letters = ft.Row(width=365,wrap=True,alignment=ft.MainAxisAlignment.CENTER,spacing=6)
  line_1 = ft.Divider(height=1, color=ft.colors.SECONDARY_CONTAINER)
  #page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
  page.views.append(
           ft.View(
             "/",
           [appbar,
            ft.Row(controls=[txt_playername,txt_score],alignment=ft.MainAxisAlignment.SPACE_BETWEEN,width=350),
            line_1,
            ft.Container(content=txt_emote,height=100),
            ft.Container(content=row_user_letters,margin=ft.margin.symmetric(0),height=130),
            badge_hint,
            txt_hint_text,
            ft.Container(content=row_word_letters,margin=ft.margin.symmetric(0),height=130),
            ft.Row(controls=[nav_items],alignment=ft.MainAxisAlignment.CENTER),
            txt_debug,
                      
                     
           ],
           horizontal_alignment=ft.CrossAxisAlignment.CENTER,
           scroll = ft.ScrollMode.AUTO
            
                ),
            
    
            )

  await page.update_async()


  analytics.StartSession(page.client_ip,page.client_user_agent, player_name,page.platform,page.session_id)
  analytics_match_started = False
  if analytics.match_id <= 0:
     analytics.StartMatch("")
  print_bug = mymodules.print_debug.PrintDebug(txt_debug,False)
  #await print_bug.print_msg(page.__str__())
  page.on_close = page_on_close
  page.on_connect = page_on_connect
  page.on_disconnect = page_on_disconnect
  page.on_error = page_on_error
  print(page)
  #print("ClientID",page.client_ip)

  await NewGame()