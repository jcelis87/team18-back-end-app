import os
import json
import pandas as pd


def get_image(img_id: str, ext: str):

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    ASSETS_FOLDER = os.path.join(THIS_FOLDER, """assets""")

    directory_list = list()
    for root, dirs, files in os.walk(ASSETS_FOLDER, topdown=False):
        for name in dirs:
            my_path = os.path.join(root, name)
            directory_list.append(my_path)
            if img_id == name:
                my_files = os.listdir(my_path)
                for my_file in my_files:
                    my_file_path = os.path.join(my_path, my_file)
                    file_name, file_ext = os.path.splitext(my_file)
                    if os.path.exists(my_file_path) and ext == file_ext:
                        if ext == ".json":
                            print(my_file_path)
                            print(my_file)
                            return my_file_path
                        else:
                            print(my_file_path)
                            print(my_file)
                            # return FileResponse(my_file_path, media_type="image/jpeg", filename=my_file)
                            # FileResponse(
                            #     my_file, media_type="image/jpg", filename="example.jpg")

                        # return FileResponse(my_file, media_type="image/jpeg", filename=my_file)
                    # return {"error": "File not found!",
                    #         "path": my_file}


get_image('2', ".json")
