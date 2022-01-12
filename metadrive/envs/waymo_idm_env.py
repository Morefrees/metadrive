from metadrive.envs.waymo_env import WaymoEnv
from metadrive.manager.waymo_idm_traffic_manager import WaymoIDMTrafficManager


class WaymoIDMEnv(WaymoEnv):
    """
    The Traffic in this environment will be controlled by IDM Policy
    """
    def setup_engine(self):
        super(WaymoIDMEnv, self).setup_engine()
        assert not self.config["no_traffic"], "Please set no_traffic to False to use this environment"
        self.engine.update_manager("traffic_manager", WaymoIDMTrafficManager())


if __name__ == "__main__":
    env = WaymoIDMEnv(
        {
            "use_render": True,
            # "agent_policy": WaymoIDMPolicy,
            "manual_control": True,
            # "debug":True,
            "no_traffic": False,
            # "start_case_index": 192,
            "case_num": 100,
            "waymo_data_directory": "/home/liquanyi/validation",
            "horizon": 1000,
            # "vehicle_config": dict(show_lidar=True,
            #                        show_lane_line_detector=True,
            #                        show_side_detector=True)
        }
    )
    success = []
    for i in range(env.config["case_num"]):
        env.reset(force_seed=3)
        while True:
            o, r, d, info = env.step([0, 0])
            assert env.observation_space.contains(o)
            c_lane = env.vehicle.lane
            long, lat, = c_lane.local_coordinates(env.vehicle.position)
            if env.config["use_render"]:
                env.render(
                    text={
                        # "routing_lane_idx": env.engine._object_policies[env.vehicle.id].routing_target_lane.index,
                        # "lane_index": env.vehicle.lane_index,
                        # "current_ckpt_index": env.vehicle.navigation.current_checkpoint_lane_index,
                        # "next_ckpt_index": env.vehicle.navigation.next_checkpoint_lane_index,
                        # "ckpts": env.vehicle.navigation.checkpoints,
                        # "lane_heading": c_lane.heading_theta_at(long),
                        # "long": long,
                        # "lat": lat,
                        # "v_heading": env.vehicle.heading_theta,
                        "seed": env.engine.global_seed + env.config["start_case_index"],
                        "reward": r,
                    }
                )

            # if d:
            #     if info["arrive_dest"]:
            #         print("seed:{}, success".format(env.engine.global_random_seed))
            #     break
