import flet as ft
from views.index import IndexView
from views.question import QuestionView
from views.simple_view import SimpleView
import flet_fastapi
import os.path
from dotenv import load_dotenv
async def main(page: ft.Page):
  page.fonts = {
     
      #"NotoEmoji": "NotoColorEmoji-Regular.ttf",
     # "Roberto": "Roboto-Black.ttf"
  }
  
  page.title = "Emoji Enigma"
  page.theme_mode = "light"
  page.theme =ft.Theme(color_scheme_seed="green")

  async def route_change(route):
    page.views.clear()
    troute = ft.TemplateRoute(page.route)
    await IndexView(page, {})
    if troute.match("/question/:id"):
      params = {"id": troute.id}
      await QuestionView(page, params)
    elif troute.match("/simple_view"):
      await SimpleView(page, {})

  async def view_pop(view):
    page.views.pop()
    top_view = page.views[-1]
    await page.go_async(top_view.route)

  page.on_route_change = route_change
  page.on_view_pop = view_pop
  await page.go_async(page.route)

load_dotenv()

if os.getenv('uvicorn') == "0":
    ft.app(target=main, assets_dir="assets", use_color_emoji=True, view=ft.AppView.WEB_BROWSER)
    # ft.app(target=main, assets_dir="assets",view=ft.AppView.WEB_BROWSER)
else:
    app = flet_fastapi.app(main, assets_dir=os.path.abspath("assets"), use_color_emoji=True)




