#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Worker:
    """
    Takes in requests from the scheduler and performs them and funnels the
    results back to the scheduler.

                      |--->[Worker]----|
                      |                |
    [Scheduler] ------|--->[Worker]----|----------->[Scheduler]
                      |                |
                      |--->[Worker]----|
    
    These requests entail transforming data provided into more digestable
    information. The worker delegates this task to a transformer instance

    Attributes:
        scheduler_name(str): name of scheduler receives requests from and
            pushes results to
    """

    def __init__(
        self, scheduler_name: str,
    ):
        pass

    def start():
        """
        Blocking call that listens for requests from the scheduler and pushes
        results back to the scheduler
        """
        pass
