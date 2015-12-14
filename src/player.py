import pyglet


class FailedCriticalObjective(Exception):
    pass


class NotEnoughMoney(Exception):
    pass


class DoesNotOwnAsset(Exception):
    pass


class AssetQuantityTooLittle(Exception):
    pass


class Player(object):
    """
    Place to store player's assets and money
    """

    def __init__(self):
        self._assets = set()

    @property
    def assets(self):
        return self._assets

    def get_asset(self, asset_id):
        for a in self._assets:
            if asset_id == a.asset_id:
                return a

        return None

    def has_asset(self, asset_id):
        return bool(self.get_asset(asset_id))

    def add_asset(self, asset_id, quantity=1):
        player_asset = self.get_asset(asset_id)

        if player_asset is None:
            player_asset = PlayerAsset(asset_id, 0)
            self._assets.add(player_asset)

        player_asset += quantity

    def subtract_asset(self, asset_id, quantity=1):
        player_asset = self.get_asset(asset_id)
        player_asset -= quantity
        if player_asset.quantity == 0:
            self._assets.remove(player_asset)


class PlayerAsset(object):
    def __init__(self, asset_id, quantity, tracked=False):
        self._asset_id = asset_id
        self._quantity = quantity
        self._tracked = tracked

    def __add__(self, quantity):
        self.add(quantity)

    def __sub__(self, quantity):
        self.subtract(quantity)

    def add(self, quantity=1):
        self._quantity += quantity

    def subtract(self, quantity=1):
        if self._quantity < quantity:
            raise AssetQuantityTooLittle
        self._quantity -= quantity

    @property
    def get_display_document(self):
        return pyglet.text.document.UnformattedDocument('%s: %s' % (self.asset_id, int(self.quantity)))

    @property
    def asset_id(self):
        return self._asset_id

    @property
    def quantity(self):
        return self._quantity

    @property
    def tracked(self):
        return self._tracked

    @tracked.setter
    def tracked(self, tracked):
        self._tracked = tracked
