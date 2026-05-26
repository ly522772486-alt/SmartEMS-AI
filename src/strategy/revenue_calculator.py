from src.config.unit_config import (
    MARGINAL_COST,
    TIME_INTERVAL
)

class RevenueCalculator:

    def calculate_revenue(self, market_price, power):

        revenue = (
            market_price
            * power
            * TIME_INTERVAL
        )

        return revenue

    def calculate_cost(self, power):

        cost = (
            MARGINAL_COST
            * power
            * TIME_INTERVAL
        )

        return cost

    def calculate_profit(self, market_price, power):

        revenue = self.calculate_revenue(
            market_price,
            power
        )

        cost = self.calculate_cost(power)

        profit = revenue - cost

        return profit