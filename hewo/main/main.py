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

    main_window = MainWindow(settings=window_settings)

    # build layouts
    hewo_layout = HeWo(settings=hewo_settings)

    resources_root = res.files("hewo.resources") if res.is_resource else pathlib.Path("game/resources")
    mp4 = resources_root / "test.mp4"
    img = resources_root / "img.png"
    multimedia_objects: list[MultimediaGameObj] = [
        # MultimediaGameObj(mp4, audio="ffplay", loop=True),
        MultimediaGameObj(img, position=(760, 0), velocity=(0, 0), loop=False, audio=False, object_name="ImageObj1",
                          size=(200, 200)),
        MultimediaGameObj(img, position=(0, 0), velocity=(0, 0), loop=False, audio=False, object_name="ImageObj2",
                          size=(200, 200)),
        MultimediaGameObj(mp4, position=(760, 200), velocity=(0, 0), loop=True, object_name="ImageObj3",
                          size=(200, 200)),
        MultimediaGameObj(mp4, position=(0, 200), velocity=(0, 0), loop=True, object_name="ImageObj4", size=(200, 200)),
        MultimediaGameObj(mp4, position=(0, 400), velocity=(0, 0), loop=True, object_name="ImageObj5", size=(960, 240)),
        # MultimediaGameObj(mp4, position=(380, 100), velocity=(0, 0), loop=False, audio='ffplay', object_name="ImageObj",size=(200, 200)),
    ]
    multimedia_layout = MultimediaLayout(multimedia_objects, bg_color=(0, 0, 0))

    main_window.layout_dict = {"hewo": hewo_layout,
                               "media": multimedia_layout}
    main_window.active_layout = "media"
    main_window.desintegrate_time = 1
    main_window.run()


if __name__ == "__main__":
    main()
