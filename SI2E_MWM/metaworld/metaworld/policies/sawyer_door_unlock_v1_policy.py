from __future__ import annotations

from typing import Any

import numpy as np
import numpy.typing as npt

from metaworld.policies.action import Action
from metaworld.policies.policy import Policy, assert_fully_parsed, move


class SawyerDoorUnlockV1Policy(Policy):
    @staticmethod
    @assert_fully_parsed
    def _parse_obs(obs: npt.NDArray[np.float64]) -> dict[str, npt.NDArray[np.float64]]:
        return {
            "hand_pos": obs[:3],
            "lock_pos": obs[3:6],
            "unused_info": obs[6:],
        }

    def get_action(self, obs: npt.NDArray[np.float64]) -> npt.NDArray[np.float32]:
        o_d = self._parse_obs(obs)

        action = Action({"delta_pos": np.arange(3), "grab_effort": 3})

        action["delta_pos"] = move(
            o_d["hand_pos"], to_xyz=self._desired_pos(o_d), p=25.0
        )
        action["grab_effort"] = 1.0

        return action.array

    @staticmethod
    def _desired_pos(o_d: dict[str, npt.NDArray[np.float64]]) -> npt.NDArray[Any]:
        pos_curr = o_d["hand_pos"]
        pos_lock = o_d["lock_pos"] + np.array([-0.03, -0.03, -0.1])

        if np.linalg.norm(pos_curr[:2] - pos_lock[:2]) > 0.04:
            return pos_lock + np.array([0.0, 0.0, 0.3])
        elif abs(pos_curr[2] - pos_lock[2]) > 0.02:
            return pos_lock
        else:
            return pos_lock + np.array([0.1, 0.0, 0.0])
