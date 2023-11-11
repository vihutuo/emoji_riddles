import flet as ft
import random
import mymodules.emoji as emoji
import time


def IndexView(page, params):
  def user_letter_box_clicked(e):
    pass
  def CreateUserLetterBoxes(word):
    length = len(word)
    for i in range(length):
        btn_1 = ft.OutlinedButton("",
                            width=40,
                            height=40,
                        
                            on_click = user_letter_box_clicked,      
                                  
                            style=ft.ButtonStyle(
                              shape=ft.RoundedRectangleBorder(radius=7), padding=4))
        if word[i] == " ":
          btn_1.disabled = True
          btn_1.text = " "
        row_user_letters.controls.append(btn_1)
      
  def close_dlg():
        dlg_modal.open = False
        page.update()
  def open_dlg():
        dlg_modal.content.value = "Score : " + str(score)
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()
  def restart(e):
    close_dlg()
    nonlocal score
    nonlocal count
    score= 0
    count=0
    txt_score.value = score
    fld_input.disabled = False
    
    LoadNewImage()
    page.update()
    
  def LoadNewImage():
    nonlocal selected_ind
    selected_ind = random.randint(0, len(lst_images) - 1)
    file_name = lst_images[selected_ind][0]
    correct_answer = lst_images[selected_ind][1]
    img_1.src = "emoji images/" + file_name
    img_1.update()
    print("New quetion loaded")

  def check_answer(e):
    nonlocal score
    nonlocal count
    #fld_input.disabled = True
    #fld_input.update()
    correct_answer = lst_images[selected_ind][1]
    user_answer = fld_input.value
    if user_answer.lower() == correct_answer.lower():
      txt_msg.value = "Correct"
      score += 10
      txt_score.value = score
      txt_score.update()
    else:
      txt_msg.value = "Wrong"
    txt_msg.update()
    time.sleep(1)
    fld_input.value = ""
    
    fld_input.update()
    count += 1
    if count >= 4: #Game Over
      open_dlg()
      txt_msg.update()
    else:
      LoadNewImage()
      fld_input.disabled = False
      
      fld_input.update()
      fld_input.focus()
      fld_input.update()
      
      

  lst_images =emoji.GetAllImages()
  selected_ind = 0
  score = 0
  count = 0
  #print(lst_images)
  dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Game Over"),
        content=ft.Text("Score : " + str(score)),
        actions=[
            ft.TextButton("OK", on_click=restart),

        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=restart,
    )
  
  img_1 = ft.Image(src="", width=300)
  txt_msg = ft.Text("")
  fld_input = ft.TextField(label="", on_submit=check_answer)
  appbar = ft.AppBar(
                      title=ft.Text("Emoji Word Game"),        
                      bgcolor=ft.colors.SURFACE_VARIANT
                    )

  txt_scorelabel = ft.Text("SCORE")
  txt_score = ft.Text("0")
  row_score = ft.Row(controls=[txt_scorelabel,txt_score])
  row_top=ft.Row(controls =[])
  row_user_letters = ft.Row()
  
  page.views.append(
           ft.View(
             "/",
           [appbar,row_score,row_top,img_1,fld_input,txt_msg],
                  )
            )
  page.update()
  LoadNewImage()
