import json
class InputModule:
    def read_queries(self, json_file):
        try:
            with open(json_file) as f:
                json_data = json.load(f)
            return json_data
        except json.JSONDecodeError as e:
            print("Invalid JSON syntax:", e)
            return []
        except Exception as e:
            print(e)
            return []