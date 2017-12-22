class Mob():
    def __init__(self, id, owner, data={}):
        self.online = True
        self.id = id
        self.owner = owner
        self.active = True
        self._handlers = {}
        self.update(data)

    def despawn(self):
        self.active = False
        self._handle_change('despawn', True, False)

    def update(self, data, new_owner=None):

        if new_owner is not None:
            old_owner = self.owner
            self.owner = new_owner
            self._handle_change('owner', old_owner, new_owner)

        old = self.__dict__.copy()

        self.type = self._get_default(data, 'type', 0)
        self.posX = self._get_default(data, 'posX', 0)
        self.posY = self._get_default(data, 'posY', 0)
        self.speedX = self._get_default(data, 'speedX', 0)
        self.speedY = self._get_default(data, 'speedY', 0)
        self.accelX = self._get_default(data, 'accelX', 0)
        self.accelY = self._get_default(data, 'accelY', 0)
        self.maxSpeed = self._get_default(data, 'maxSpeed', 0)

        for key in self.__dict__.keys():
            value = self.__dict__.get(key)
            old_value = old.get(key)
            if value != old_value and old_value is not None:
                self._handle_change(key, old_value, value)

                if key == 'posX' or key == 'posY':
                    self._handle_change('position', (old.get('posX'), old.get('posY')), (self.posX, self.posY))
                
                if key == 'speedX' or key == 'speedY':
                    self._handle_change('speed', (old.get('posX'), old.get('posY')), (self.posX, self.posY))

    def _handle_change(self, key, old_value, new_value):
        handler = self._handlers.get(key, None)
        if handler is not None and callable(handler):
            handler(self, key, old_value, new_value)

    def _get_default(self, data, name, default):
        return data.get(name, self.__dict__.get(name, default))

    def on_change(self, key, handler):
        self._handlers[key] = handler
