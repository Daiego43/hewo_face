
import pathlib
from game.main.window import MainWindow
from game.settings import SettingsLoader
from game.objects.hewo.hewo import HeWo
from game.objects.multimedia.multimedia import MultimediaGameObj, MultimediaLayout


RESOURCES_PATH = pathlib.Path(__file__).parent.parent / "resources"
def main():
    # -------------------------------------------------------- load window config
    window_settings = SettingsLoader().load_settings("game.settings.window")
    hewo_settings = SettingsLoader().load_settings("game.settings.hewo")
    # -------------------------------------------------------- create main window
    main_window = MainWindow(
        settings=window_settings,# change to "media" to boot directly into the multimedia layout
    )

    # -------------------------------------------------------- build layouts
    hewo_layout = HeWo(settings=hewo_settings)

    # Minimal multimedia layout example; paths must exist in your project


    multimedia_objects = []
    for img in pathlib.Path(RESOURCES_PATH).glob("*.mp4"):
        png_path = img.resolve()
        print(png_path)
        if png_path.exists():
            multimedia_objects.append(
                #MultimediaGameObj(png_path,loop=False, audio='ffplay')
                MultimediaGameObj(png_path,loop=True, audio='ffplay')
            )

    multimedia_layout = MultimediaLayout(objects=multimedia_objects, bg_color=(0, 0, 0))
    # -------------------------------------------------------- enter loop
    main_window.layout_dict = {
        "hewo": hewo_layout,
        "media": multimedia_layout,
    }
    main_window.active_layout = "media"
    main_window.run()


if __name__ == "__main__":
    main()
