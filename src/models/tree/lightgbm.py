class LightGBMModel:
    @staticmethod
    def train(X_train, y_train, random_state=42):
        try:
            from lightgbm import LGBMRegressor
        except Exception:
            from sklearn.ensemble import GradientBoostingRegressor

            model = GradientBoostingRegressor(random_state=random_state)
            model.fit(X_train, y_train)
            model.backend_name = "sklearn-gradient-boosting"

            return model

        model = LGBMRegressor(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=3,
            random_state=random_state,
            verbose=-1,
        )
        model.fit(X_train, y_train)
        model.backend_name = "lightgbm"

        return model

    @staticmethod
    def predict(model, X_test):
        return model.predict(X_test)
