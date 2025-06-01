import pathlib
from hewo.main.window import MainWindow
from hewo.settings import SettingsLoader
from hewo.objects.hewo import HeWo
from hewo.objects.multimedia import MultimediaGameObj, MultimediaLayout
import importlib.resources as res

RESOURCES_PATH = pathlib.Path(__file__).parent.parent / "resources"


def main():
    window_settings = SettingsLoader().load_settings("hewo.settings.window")
    hewo_settings = SettingsLoader().load_settings("hewo.settings.hewo")
    multimedia_settings = SettingsLoader().load_settings("hewo.settings.multimedia")
    main_window = MainWindow(settings=window_settings)

    # build layouts
    hewo_layout = HeWo(settings=hewo_settings)

    resources_root = res.files("hewo.resources") if res.is_resource else pathlib.Path("game/resources")
    multimedia_layout = MultimediaLayout(settings=multimedia_settings)

    main_window.layout_dict = {"hewo": hewo_layout,
                               "media": multimedia_layout}
    main_window.active_layout = window_settings["active_layout"]
    main_window.desintegrate_time = 1
    main_window.run()


if __name__ == "__main__":
    main()
