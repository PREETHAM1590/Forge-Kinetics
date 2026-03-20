from __future__ import annotations

import random


def add_noise(value: float, epsilon: float = 1.0) -> float:
	if epsilon <= 0:
		raise ValueError("epsilon must be > 0")
	scale = 1.0 / epsilon
	return value + random.uniform(-scale, scale)

