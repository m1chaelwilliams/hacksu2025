from constants import Constants
import random
class SpawnLoc:
    locations = [
        [
            (Constants.WINDOW_WIDTH / 2 - 50, 0),
            (Constants.WINDOW_WIDTH / 2 + 10, 0),
            (Constants.WINDOW_WIDTH / 2 + 30, 0),
        ],
        [ 
            (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT / 2 + 30),
            (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT / 2 - 10),
            (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT / 2 - 50),
        ],
        [  
            (Constants.WINDOW_WIDTH / 2 - 50, Constants.WINDOW_HEIGHT),
            (Constants.WINDOW_WIDTH / 2 + 10, Constants.WINDOW_HEIGHT),
            (Constants.WINDOW_WIDTH / 2 + 30, Constants.WINDOW_HEIGHT),
        ],
        [ 
            (0, Constants.WINDOW_HEIGHT / 2 + 30),
            (0, Constants.WINDOW_HEIGHT / 2 - 10),
            (0, Constants.WINDOW_HEIGHT / 2 - 50),
        ],
    ]
    def random_spawn_side() -> tuple[int, int]:
        spawn_side = random.choice(range(len(SpawnLoc.locations))) 
        spawn_slot = random.choice(SpawnLoc.locations[spawn_side]) 
        return spawn_slot

