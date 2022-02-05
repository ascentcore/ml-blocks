states = ["booting", "empty", "ingesting",
          "processing", "storing", "statics", "training", "pending"]


stages = {f'{key}': index for index, key in enumerate(states)}
