from src.config.unit_config import (
    MIN_POWER,
    MAX_POWER,
    RAMP_UP,
    RAMP_DOWN
)

class DispatchOptimizer:

    def optimize(self, current_power, target_power):

        delta = target_power - current_power

        # 升负荷限制
        if delta > RAMP_UP:
            actual_power = current_power + RAMP_UP

        # 降负荷限制
        elif delta < -RAMP_DOWN:
            actual_power = current_power - RAMP_DOWN

        # 正常可达
        else:
            actual_power = target_power

        # 边界保护
        actual_power = max(MIN_POWER, actual_power)
        actual_power = min(MAX_POWER, actual_power)

        return actual_power