import flet as ft
class ItemNavigator(ft.UserControl):
  def __init__(self, start,stop,current,on_change_item):
      super().__init__()
      self.start=start
      self.stop=stop
      self.current = current
      self.on_change_item = on_change_item
      
      self.btn_previous = ft.IconButton(
                                      icon=ft.icons.NAVIGATE_BEFORE,
                                      tooltip="Previous",
                                      icon_size=40,
                                      on_click=self.previous_clicked
                                  )
      self.btn_next = ft.IconButton(
                                      icon=ft.icons.NAVIGATE_NEXT,
                                      tooltip="Next",
                                      icon_size=40,
                                      on_click=self.next_clicked
                           )
      self.EnableDisableButtons()

      self.txt_question_no= ft.Text(f"{current}/{stop}")
      self.row_nav = ft.Row(
                            controls = [self.btn_previous,self.txt_question_no,self.btn_next],
                            
                           )
    
      
  def EnableDisableButtons(self):
    self.btn_previous.disabled = False
    self.btn_next.disabled = False
    if self.current <= self.start :
      self.btn_previous.disabled = True 
    if self.current >= self.stop :
        self.btn_next.disabled = True
       
  async def previous_clicked(self, e):
    if self.current>self.start:
       self.current-=1
    self.EnableDisableButtons() 
    self.txt_question_no.value = f"{self.current}/{self.stop}"
    await self.update_async()
    await self.on_change_item(e)
     
  async def move_next(self):
    if self.current<self.stop:
       self.current+=1
       self.EnableDisableButtons() 
       print("Next Clicked")
       self.txt_question_no.value = f"{self.current}/{self.stop}"
       await self.txt_question_no.update_async()
       await self.update_async()
       await self.on_change_item(self)
       return True
    else:
       return False

  async def next_clicked(self, e):
     await self.move_next()
     #if self.current<self.stop:
     # self.current+=1
     #self.EnableDisableButtons() 
     #print("Next Clicked")
     #self.txt_question_no.value = f"{self.current}/{self.stop}"
     #self.txt_question_no.update()
     #self.update()
     #self.on_change_item(e)

  def build(self):
     # print("In Build")
      
      return  self.row_nav
      
      