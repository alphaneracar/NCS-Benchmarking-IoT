import json
import ast
from src.site_coordinator import SiteCoordinator


class LinuxCoordinator(SiteCoordinator):

    def __init__(
        self,
        site,
        experiment_id,
        nodes,
        num):
        super().__init__(
            site,
            experiment_id,
            nodes,
            'linux',
            num=num
        )

