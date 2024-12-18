"""PyBullet environment for Limb Repositioning."""

from dataclasses import dataclass
from typing import Union

import numpy as np
import omegaconf
from omegaconf import OmegaConf
from scipy.spatial.transform import Rotation as R

from limb_repo.environments.pybullet_env import (
    PyBulletConfig,
    PyBulletEnv,
)
from limb_repo.structs import BodyState, LRState, Pose
from limb_repo.utils import pybullet_utils


@dataclass
class LRPyBulletConfig:
    """Configuration for a Limb Repo PyBullet environment."""

    pybullet_config: PyBulletConfig
    active_pose: Pose
    active_config: np.ndarray
    active_urdf: str
    passive_pose: Pose
    passive_config: np.ndarray
    passive_urdf: str
    wheelchair_pose: Pose
    # wheelchair_config: np.ndarray
    wheelchair_urdf: str
    robot_ee_to_human_ee: np.ndarray


class LRPyBulletEnv(PyBulletEnv):
    """Pybullet environment for Limb Repositioning."""

    def __init__(self, config: omegaconf.DictConfig) -> None:
        self.config = config

        ## Initialize empty pybullet simulation
        super().__init__(config.pybullet_config)

        ## Set initial values
        print("config active urdf", self.config.keys())
        self.active_urdf: str = self.config.active_urdf
        self.active_init_pose = np.array(self.config.active_pose)
        self.active_init_pos = np.array(self.active_init_pose[:3])
        self.active_init_orn = R.from_euler("xyz", self.active_init_pose[3:])
        self.active_init_config = np.array(self.config.active_config)
        self.active_init_state = BodyState(
            np.concatenate([self.active_init_config, np.zeros(6 + 6)])
        )
        self.active_n_dofs = len(self.active_init_config)
        self.active_ee_link_id = self.active_n_dofs - 1

        self.passive_urdf: str = self.config.passive_urdf
        self.passive_init_pose = np.array(self.config.passive_pose)
        self.passive_init_pos = np.array(self.passive_init_pose[:3])
        self.passive_init_orn = R.from_euler("xyz", self.passive_init_pose[3:])
        self.passive_init_config = np.array(self.config.passive_config)
        self.passive_init_state = BodyState(
            np.concatenate([self.passive_init_config, np.zeros(6 + 6)])
        )
        self.passive_n_dofs = len(self.passive_init_config)
        self.passive_ee_link_id = self.passive_n_dofs - 1

        ## Set useful rotations
        # rotates vector in active base frame to passive base frame: v_p = R @ v
        self.robot_base_to_human_base = (
            self.passive_init_orn.as_matrix().T @ self.active_init_orn.as_matrix()
        )
        self.robot_base_to_human_base_twist = np.block(
            [
                [self.robot_base_to_human_base, np.zeros((3, 3))],
                [np.zeros((3, 3)), self.robot_base_to_human_base],
            ]
        )
        # rotates active ee into passive ee, both in world frame: h_ee = R * r_ee
        self.robot_ee_to_human_ee = self.config.robot_ee_to_human_ee
        self.robot_ee_to_human_ee_twist = np.block(
            [
                [self.robot_ee_to_human_ee, np.zeros((3, 3))],
                [np.zeros((3, 3)), self.robot_ee_to_human_ee],
            ]
        )

        ## Load bodies into pybullet sim
        self.active_id = self.p.loadURDF(
            self.active_urdf,
            self.active_init_pos,
            self.active_init_orn.as_quat(),
            useFixedBase=True,
            flags=self.p.URDF_USE_INERTIA_FROM_FILE,
        )

        self.passive_id = self.p.loadURDF(
            self.passive_urdf,
            self.passive_init_pos,
            self.passive_init_orn.as_quat(),
            useFixedBase=True,
            flags=self.p.URDF_USE_INERTIA_FROM_FILE,
        )

        # Configure settings for sim bodies
        self.configure_body_settings()

        return

    def step(self) -> None:
        """Step the environment."""
        self.p.stepSimulation()

    def send_torques(self, body_id: int, torques: np.ndarray) -> None:
        """Send joint torques."""
        # to use torque control, velocity control must be disabled at every time step
        for j in pybullet_utils.get_good_joints(self.p, body_id):
            self.p.setJointMotorControl2(body_id, j, self.p.VELOCITY_CONTROL, force=0)

        # apply original torque command to robot
        self.p.setJointMotorControlArray(
            body_id,
            pybullet_utils.get_good_joints(self.p, body_id),
            self.p.TORQUE_CONTROL,
            forces=torques,
        )

    def set_body_state(self, body_id: int, state: BodyState) -> None:
        """Set the states of active or passive."""
        for i, joint_id in enumerate(
            pybullet_utils.get_good_joints(self.p, body_id)
        ):
            self.p.resetJointState(
                body_id,
                joint_id,
                (state.pos)[i],
                targetVelocity=state.vel[i],
            )

    def set_lr_state(self, state: LRState) -> None:
        """Set the states of active and passive."""
        self.set_body_state(state.active_kinematics, self.active_id)
        self.set_body_state(state.passive_kinematics, self.passive_id)

    def set_lr_constraint(self) -> None:
        """Create grasp constraint between active and passive ee."""
        self.cid = self.p.createConstraint(
            self.active_id,
            self.active_ee_link_id,
            self.passive_id,
            self.passive_ee_link_id,
            self.p.JOINT_FIXED,
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0, 1],
            R.from_matrix(self.robot_ee_to_human_ee).as_quat(),
        )

    def configure_body_settings(self) -> None:
        # remove friction terms as well contact stiffness and damping
        for i in range(self.p.getNumJoints(self.passive_id)):
            self.p.changeDynamics(
                self.passive_id,
                i,
                jointDamping=0.0,
                anisotropicFriction=0.0,
                maxJointVelocity=5000,
                linearDamping=0.0,
                angularDamping=0.0,
                lateralFriction=0.0,
                spinningFriction=0.0,
                rollingFriction=0.0,
                contactStiffness=0.0,
                contactDamping=0.0,
            )  # , jointLowerLimit=-6.283185 * 500, jointUpperLimit=6.283185 * 500)
        for i in range(self.p.getNumJoints(self.active_id)):
            self.p.changeDynamics(
                self.active_id,
                i,
                jointDamping=0.0,
                anisotropicFriction=0.0,
                maxJointVelocity=5000,
                linearDamping=0.0,
                angularDamping=0.0,
                lateralFriction=0.0,
                spinningFriction=0.0,
                rollingFriction=0.0,
                contactStiffness=0.0,
                contactDamping=0.0,
            ),  # , jointLowerLimit=-6.283185 * 200, jointUpperLimit=6.283185 * 200)

        # remove collision for both robot and human arms
        group = 0
        mask = 0
        for linkIndex in range(self.p.getNumJoints(self.passive_id)):
            self.p.setCollisionFilterGroupMask(self.passive_id, linkIndex, group, mask)
        for linkIndex in range(self.p.getNumJoints(self.active_id)):
            self.p.setCollisionFilterGroupMask(self.active_id, linkIndex, group, mask)

        # apply velocity control to panda arm to make it stationary
        for i in range(self.active_n_dofs):
            self.p.setJointMotorControl2(
                self.active_id, i, self.p.VELOCITY_CONTROL, targetVelocity=0, force=50
            )
        for i in range(self.passive_n_dofs):
            self.p.setJointMotorControl2(
                self.passive_id, i, self.p.VELOCITY_CONTROL, targetVelocity=0, force=50
            )

        for i in range(1000):
            self.p.stepSimulation()

        # enable force torque
        for joint in range(self.p.getNumJoints(self.active_id)):
            self.p.enableJointForceTorqueSensor(self.active_id, joint, 1)

        for joint in range(self.p.getNumJoints(self.passive_id)):
            self.p.enableJointForceTorqueSensor(self.passive_id, joint, 1)

    @staticmethod
    def parse_config(path_to_yaml: str) -> omegaconf.DictConfig:
        """Parse a configuration file."""
        config = omegaconf.DictConfig(OmegaConf.load(path_to_yaml))

        # to get around mypy "Keywords must be strings"
        # and "value after ** should be a mapping"
        config_dict = {str(key): value for key, value in dict(config).items()}

        config = OmegaConf.structured(LRPyBulletConfig(**config_dict))

        return config


if __name__ == "__main__":
    pass
