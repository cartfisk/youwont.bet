import math
import shutil
import os
from datetime import datetime

from wand.image import Image
# from wand.display import display

from server.constants import MASTER_IMAGE_PATH


def generate_composite(background_path, overlay_path, position, grid):
    background = open(background_path, "rb")
    overlay = open(overlay_path, "rb")
    coordinates = grid.get_coordinates_from_position(position)
    with Image(file=background) as background_img:
        with Image(file=overlay) as overlay_img:
            overlay_img.type = "grayscale"
            overlay_size = overlay_img.size
            overlay_img.crop(
                width=overlay_size[0], height=overlay_size[0], gravity="center"
            )
            overlay_img.resize(grid.column_width, grid.row_height)
            background_img.composite(
                overlay_img, left=coordinates.left, top=coordinates.top
            )
        overlay.close()
        background.close()
        background_img.save(filename=background_path)
    return True


class Coordinates:
    """Defines a point on an image defined by the top and left pixel positions"""

    top: int
    left: int

    def __init__(self, top, left):
        self.top = top
        self.left = left


class Grid:
    """Defines a pixel grid for image composition"""

    rows: int
    columns: int
    row_height: int
    row_gutter: int
    column_width: int
    column_gutter: int

    def __init__(
        self, rows, columns, row_height, row_gutter, column_width, column_gutter
    ):
        self.rows = rows
        self.columns = columns
        self.row_height = row_height
        self.row_gutter = row_gutter
        self.column_width = column_width
        self.column_gutter = column_gutter

    def get_coordinates_from_position(self, position):
        rows = self.rows
        columns = self.columns

        row = math.floor(position / columns)
        column = position % columns

        left = column * (self.column_width + self.column_gutter)
        top = row * (self.row_height + self.row_gutter)

        return Coordinates(left=left, top=top)


def save_copy_of_master(
    master_path=MASTER_IMAGE_PATH,
    iterations_folder="assets/images/composite/iterations",
):
    timestamp = datetime.now().timestamp()
    path_split = master_path.split(".")
    extension = path_split[len(path_split) - 1]
    ts_name = "{}.{}".format(timestamp, extension)
    backup_path = os.path.join(iterations_folder, ts_name)
    shutil.copy(master_path, backup_path)


master_grid = Grid(
    rows=10, columns=10, row_height=500, row_gutter=0, column_width=500, column_gutter=0
)


def update_master_image(
    submission_path, position, grid=master_grid, master_path=MASTER_IMAGE_PATH
):
    if position <= grid.rows * grid.columns:
        save_copy_of_master(
            master_path=master_path,
            iterations_folder="assets/images/composite/iterations",
        )
        generate_composite(master_path, submission_path, position, grid)
