from sklearn.ensemble import RandomForestRegressor


class RandomForestModel:
    @staticmethod
    def train(X_train, y_train, random_state=42, n_estimators=100):
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            random_state=random_state,
        )
        model.fit(X_train, y_train)

        return model

    @staticmethod
    def predict(model, X_test):
        return model.predict(X_test)
