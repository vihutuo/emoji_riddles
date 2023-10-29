import flet as ft
from views.index import IndexView
from views.question import QuestionView
from views.simple_view import SimpleView


def main(page: ft.Page):
  page.fonts = {
     
      #"NotoEmoji": "NotoColorEmoji-Regular.ttf",
      "Roberto": "Roboto-Black.ttf"
  }
  
  page.title = "Emoji Enigma"
  page.theme_mode = "light"
  page.theme =ft.Theme(color_scheme_seed="green")

  def route_change(route):
    page.views.clear()
    troute = ft.TemplateRoute(page.route)
    IndexView(page, {})
    if troute.match("/question/:id"):
      params = {"id": troute.id}
      QuestionView(page, params)
    elif troute.match("/simple_view"):
      SimpleView(page, {})

  def view_pop(view):
    page.views.pop()
    top_view = page.views[-1]
    page.go(top_view.route)

  page.on_route_change = route_change
  page.on_view_pop = view_pop
  page.go(page.route)


#ft.app(target=main, assets_dir="assets",use_color_emoji=True)
ft.app(target=main, assets_dir="assets",use_color_emoji=True,view=ft.AppView.WEB_BROWSER)
