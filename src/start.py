import argparse
from src.gui import MainUI, calc_window_size

APP_NAME = "ICanDraw"
__VERSION__ = '1.0.0'
icon_path = '../files/app_icon.ico'
app_intro = "You are about to Draw like a pro on Skribbl.io"


def start(**kwargs):
    main_ui = MainUI(
        app_name=f"{APP_NAME} v{__VERSION__}",
        icon=icon_path,
        size=calc_window_size(app_intro),
        intro=app_intro,
        **kwargs,
    )
    main_ui.start_gui()
    return 1


def cli():
    desc = '''argument description here'''
    parser = argparse.ArgumentParser(
        description=desc,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '-n', '--name',
        help="Name to display on skribbl",
        type=str,
        default="ICanDraw2",
    )

    parser.add_argument(
        '-l', '--language',
        help="Language to play",
        type=str,
        default="English"
    )

    return parser.parse_args()


if __name__ == '__main__':
    start(**vars(cli()))
