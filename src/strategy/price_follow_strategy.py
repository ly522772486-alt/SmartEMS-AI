from src.config.unit_config import (
    MIN_POWER,
    MAX_POWER
)

class PriceFollowStrategy:

    def get_target_power(self, pred_price):

        # 低价区
        if pred_price < 260:
            return 120

        # 中间价区
        elif pred_price < 380:
            return 240

        # 高价区
        elif pred_price < 420:
            return 300

        # 尖峰区
        else:
            return MAX_POWER