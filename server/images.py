import math
import shutil
import os
from datetime import datetime

from wand.image import Image

from server.constants import MASTER_IMAGE_PATH, ORIENTATION_ROTATION_MAPPING


def generate_composite(background_path, overlay_path, position, grid):
    coordinates = grid.get_coordinates_from_position(position)
    with open(background_path, "rb") as background:
        with open(overlay_path, "rb") as overlay:
            with Image(file=background) as background_img:
                with Image(file=overlay) as overlay_img:
                    overlay_img.type = "grayscale"
                    short_side = min(iter(overlay_img.size))
                    rotate_right_degree = ORIENTATION_ROTATION_MAPPING.get(overlay_img.orientation, 0)
                    overlay_img.rotate(rotate_right_degree)
                    overlay_img.crop(
                        width=short_side, height=short_side, gravity="center"
                    )
                    overlay_img.resize(grid.column_width, grid.row_height)
                    background_img.composite(
                        overlay_img, left=coordinates.left, top=coordinates.top
                    )
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
    source=MASTER_IMAGE_PATH,
    destination="assets/images/composite/iterations",
    backup=True,
):
    timestamp = datetime.now().timestamp()
    path_split = source.split(".")
    extension = path_split[len(path_split) - 1]
    ts_name = "{}.{}".format(timestamp, extension)
    backup_path = os.path.join(destination, ts_name)
    master_name = "master.png"
    copy_path = os.path.join(destination, master_name)
    if backup:
        shutil.copy(source, backup_path)
    else:
        shutil.copy(source, copy_path)




def update_master_image(
    submission_path, position, master_path=MASTER_IMAGE_PATH
):
    grid = Grid(
        rows=10, columns=10, row_height=500, row_gutter=0, column_width=500, column_gutter=0
    )
    if position <= grid.rows * grid.columns:
        save_copy_of_master(
            source=master_path,
            destination="assets/images/composite/iterations",
            backup=True,
        )
        generate_composite(master_path, submission_path, position, grid)
        save_copy_of_master(
            source=master_path,
            destination="static",
            backup=False,
        )
