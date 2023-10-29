import flet as ft
from dotenv import load_dotenv

import os

def QuestionView(page:ft.Page,params):
  def letter_clicked(e):
    con_1.content.value = chr(ord(con_1.content.value) + 1)
    con_1.update()
    
  question_no=params["id"] 
  txt = ft.Text(f"Question {question_no}")
  btn = ft.ElevatedButton("Home",on_click=lambda _: page.go("/"))
  appbar = ft.AppBar(
                      title=ft.Text("Question"), 
                      bgcolor=ft.colors.SURFACE_VARIANT
                    )

  load_dotenv()
  txt_letter1 = ft.Text("A",text_align=ft.TextAlign.CENTER,size=22)
  str = (f"Values\n :  {page.url=}"
         f"\n{page.client_ip=}"
         f"\nsalt={os.getenv('salt')}"
         )
  txt_status = ft.Text(str, text_align=ft.TextAlign.CENTER, size=22)


  con_1 = ft.Container(
                        content=txt_letter1,
                        border=ft.border.all(2,ft.colors.AMBER_800),
                        width=35,
                        height=35,
                        bgcolor="#e8d8e6",     
                        on_click=letter_clicked 
                       )
  page.views.append(ft.View("/question",[appbar,txt,txt_status,btn,con_1]))
  page.update() 