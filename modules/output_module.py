import json
import os

class OutputModule:
    def save_data(self, data, directory_name,file_name):
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        if type(data) == list:
            with open(directory_name+file_name, "w") as f:
                json.dump(data, f)
                print("Data Saved")
        else:
            print("Invalid Format")
