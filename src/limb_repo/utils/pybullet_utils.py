"""Utilities for working with PyBullet."""

import pybullet_utils.bullet_client as bc


def get_good_joints(p: bc.BulletClient, body_id: int):
    """Get the joints that are not locked."""
    good_joints = []
    for i in range(p.getNumJoints(body_id)):
        joint_info = p.getJointInfo(body_id, i)
        if joint_info[2] != 4:  # if not locked
            good_joints.append(i)
    return good_joints
