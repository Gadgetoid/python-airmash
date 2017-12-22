
def ks(player, k, a, b):
    print("[{}] {}: {}".format(player.name, k, a))

class Player():
    def __init__(self, id, data={}):
        self.online = True
        self.id = id
        self.update(data)
        self._handlers = {}

        #self._handlers['upgrades'] = ks
        #self._handlers['keystate'] = ks

    def update(self, data):
        old = self.__dict__.copy()
        
        self.clock = self._get_default(data, 'clock', 0)
        self.status = self._get_default(data, 'status', 0)
        self.level = self._get_default(data, 'level', 0)
        self.name = self._get_default(data, 'name', "")
        self.team = self._get_default(data, 'team', 0)
        self.flag = self._get_default(data, 'flag', 0)
        self.keystate = self._get_default(data, 'keystate', 0)
        self.upgrades = self._get_default(data, 'upgrade', 0)
        self.posX = self._get_default(data, 'posX', 0)
        self.posY = self._get_default(data, 'posY', 0)
        self.rot = self._get_default(data, 'rot', 0)
        self.speedX = self._get_default(data, 'speedX', 0)
        self.speedY = self._get_default(data, 'speedY', 0)
        self.type = self._get_default(data, 'type', 0)
        self.score = self._get_default(data, 'score', 0)
        self.earnings = self._get_default(data, 'earnings', 0)
        self.totalkills = self._get_default(data, 'totalkills', 0)
        self.totaldeaths = self._get_default(data, 'totaldeaths', 0)
        self.energy = self._get_default(data, 'energy', 0)
        self.energyRegen = self._get_default(data, 'energyRegen', 0)
        self.health = self._get_default(data, 'health', 0)
        self.healthRegen = self._get_default(data, 'healthRegen', 0)

        # This comes from Rankings, not sure why it's x/y
        self.x = self._get_default(data, 'x', 0)
        self.y = self._get_default(data, 'y', 0)

        for key in self.__dict__.keys():
            value = self.__dict__.get(key)
            old_value = old.get(key)
            if value != old_value and old_value is not None:
                #print("Player {} {} changed from {} to {}".format(self.name, key, old_value, value))
                self._handle_change(key, old_value, value)

                if key == 'posX' or key == 'posY':
                    self._handle_change('position', (old.get('posX'), old.get('posY')), (self.posX, self.posY))
                
                if key == 'speedX' or key == 'speedY':
                    self._handle_change('speed', (old.get('posX'), old.get('posY')), (self.posX, self.posY))
                    

        #for key in self.__dict__.keys():
        #    value = self.__dict__[key]
        #    old_value = old[key]
        #    if value != old_value:
        #        print("Player {} {} changed from {} to {}".format(self.name, key, old_value, value))

    def _handle_change(self, key, old_value, new_value):
        handler = self._handlers.get(key, None)
        if handler is not None and callable(handler):
            handler(self, key, old_value, new_value)

    def _get_default(self, data, name, default):
        return data.get(name, self.__dict__.get(name, default))

    def on_change(self, key, handler):
        self._handlers[key] = handler