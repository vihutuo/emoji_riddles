from pydantic import BaseModel

class UserEmojiItem(BaseModel):
  is_complete : bool = False  
  hint_positions : list[int] = []
  word_letters : str  = ""
  hint_counts : int = 0
  
  #def __init__(self):
   # self.is_complete = False
   # self.hint_positions = [] #indexes
   # self.word_letters = "" # random letters
   #self.hints_count = 0
  def SetWordLetters(self,s):
    self.word_letters = s[:]
class ListUserEmojiItem(BaseModel):
      items: list[UserEmojiItem] = []
    