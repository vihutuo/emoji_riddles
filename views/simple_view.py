import flet as ft
def SimpleView(page,params):
  def submit_clicked(e):
       
       col_1.controls.append( ft.Text(fld_name.value))
       col_1.update()
  
  fld_name = ft.TextField(label="Enter name")
  btn_submit = ft.ElevatedButton("Submit",on_click=submit_clicked)
  appbar = ft.AppBar(title=ft.Text("Simple View"), bgcolor=ft.colors.SURFACE_VARIANT)
  row1 = ft.Row(controls=[fld_name,btn_submit])
  col_1 = ft.Column()
  page.views.append(ft.View("/",[appbar,row1,col_1]))
  page.update()
    