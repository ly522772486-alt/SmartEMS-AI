class XGBoostModel:
    @staticmethod
    def train(X_train, y_train, random_state=42):
        try:
            from xgboost import XGBRegressor
        except Exception:
            from sklearn.ensemble import GradientBoostingRegressor

            model = GradientBoostingRegressor(random_state=random_state)
            model.fit(X_train, y_train)
            model.backend_name = "sklearn-gradient-boosting"

            return model

        model = XGBRegressor(
            n_estimators=100,
            learning_rate=0.05,
            max_depth=3,
            objective="reg:squarederror",
            random_state=random_state,
        )
        model.fit(X_train, y_train)
        model.backend_name = "xgboost"

        return model

    @staticmethod
    def predict(model, X_test):
        return model.predict(X_test)
