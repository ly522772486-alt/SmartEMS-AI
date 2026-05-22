class BiddingStrategy:
    """Simple price-label driven bidding strategy."""

    @staticmethod
    def classify_bid(price):
        if price >= 450:
            return "高价积极报价"
        if price >= 350:
            return "维持高可用出力"
        if price >= 250:
            return "常规报价"
        return "低价保守报价"

    @classmethod
    def add_bid_strategy(cls, df):
        result = df.copy()
        result["bid_strategy"] = result["price"].apply(cls.classify_bid)

        return result
