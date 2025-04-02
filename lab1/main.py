from controller.UltimateController import UltimateController


class Application:
    def __init__(self):
        self.controller = UltimateController()
    def start_app(self):
        self.controller.open_start_view()



if __name__ == "__main__":
    app = Application()
    app.start_app()