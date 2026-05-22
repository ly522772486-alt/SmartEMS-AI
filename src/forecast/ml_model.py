from sklearn.linear_model import LinearRegression


class MLModel:

    @staticmethod
    def train_linear_regression(X_train, y_train):

        """
        训练线性回归模型
        """

        model = LinearRegression()

        model.fit(X_train, y_train)

        return model

    @staticmethod
    def predict(model, X_test):

        """
        模型预测
        """

        predictions = model.predict(X_test)

        return predictions


class LinearRegressionModel(MLModel):
    """Alias for scripts that expect a model-style class name."""
