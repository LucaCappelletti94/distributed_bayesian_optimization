from typing import Dict


space = {
    "x": (0, 20)  # This is the space of parameters to explore
}

def custom_loss(config: Dict, reporter):
    x = config.get("x")
    reporter(my_custom_loss=x**2)