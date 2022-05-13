import logging
import os
# import numpy as np
# from sklearn.preprocessing import LabelEncoder
# from sklearn.ensemble import RandomForestClassifier


logger = logging.getLogger(__name__)


class Block:
    name = os.getenv("BLOCK_NAME", "Random Forest Classifier")

    loaders = ['file_loader', 'pandas_loader']

    def train(self, runtime):
        data = runtime.loader.dataset
        logger.info(len(data.index))
        features = list(data.columns)
        train_features = features[:-1]
        categorical_features = list(data.select_dtypes(['object']))
        logger.info(','.join(features))
        logger.info(','.join(train_features))
        logger.info(','.join(categorical_features))
        # for cat_col in categorical_features:
        #     le = LabelEncoder()
        #     data[cat_col] = le.fit_transform(data[cat_col])
        #     self.encoders[cat_col] = le

        # x_train = data[train_features].values
        # scale_x_train = np.array([self.map_to_search_domain_second_version(
        #     x, self.mins, self.maxes) for x in x_train])
        # y_train = data[features[-1]].values

        # self.model = RandomForestClassifier(random_state=0)
        # self.model.fit(scale_x_train, y_train)
        # accuracy_train = self.model.score(scale_x_train, y_train)

        # logger.info('Training complete')
        # logger.info(accuracy_train)
