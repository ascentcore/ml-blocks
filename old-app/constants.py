states = ["booting", "empty", "ingesting",
          "processing", "storing", "statics", "training", "predicting", "pending"]


stages = {f'{key}': index for index, key in enumerate(states)}

DEPENDENCY_DATA_TYPE = 0
DEPENDENCY_LOGIC_TYPE = 1