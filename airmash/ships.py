class Ship:
    def __init__(self, *args, **kwargs):
        self.__dict__.update(**kwargs)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__dict__.__repr__()

    def __getitem__(self, key):
        return self.__dict__[key]

ships = [
    None,
    Ship(
        name = "Raptor",
        turnFactor = .065,
        accelFactor = .225,
        maxSpeed = 5.5,
        minSpeed = .001,
        brakeFactor = .025,
        energyLight = .6,
        collisions = [
            [0, 5, 23],
            [0, -15, 15],
            [0, -25, 12]
        ]
    ),
    Ship(
        name = "Goliath",
        turnFactor = .04,
        accelFactor = .15,
        maxSpeed = 3.5,
        minSpeed = .001,
        brakeFactor = .015,
        energyLight = .9,
        collisions = [
            [0, 0, 35],
            [50, 14, 16],
            [74, 26, 14],
            [30, 8, 23],
            [63, 22, 15],
            [-50, 14, 16],
            [-74, 26, 14],
            [-30, 8, 23],
            [-63, 22, 15]
        ]
    ),
    Ship(
        name = "Mohawk",
        turnFactor = .07,
        accelFactor = .275,
        maxSpeed = 6,
        minSpeed = .001,
        brakeFactor = .025,
        energyLight = .3,
        collisions = [
            [0, -12, 15],
            [0, 0, 17],
            [0, 13, 15],
            [0, 26, 15]
        ]
    ),
    Ship(
        name = "Tornado",
        turnFactor = .055,
        accelFactor = .2,
        maxSpeed = 4.5,
        minSpeed = .001,
        brakeFactor = .025,
        energyLight = .5,
        collisions = [
            [0, 8, 18],
            [14, 12, 13],
            [-14, 12, 13],
            [0, -12, 16],
            [0, -26, 14],
            [0, -35, 12]
        ]
    ),
    Ship(
        name = "Prowler",
        turnFactor = .055,
        accelFactor = .2,
        maxSpeed = 4.5,
        minSpeed = .001,
        brakeFactor = .025,
        energyLight = .75,
        collisions = [
            [0, 11, 25],
            [0, -8, 18],
            [19, 20, 10],
            [-19, 20, 10],
            [0, -20, 14]
        ]
    )
]