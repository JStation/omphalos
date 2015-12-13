

class Environment(object):
    def __init__(self, variables):
        self._variables = variables

    def add_to_variable(self, variable_id, amount=1):
        variable = self.get_variable(variable_id)
        variable.add(amount)

    def subtract_from_variable(self, variable_id, amount=1):
        variable = self.get_variable(variable_id)
        variable.subtract(amount)

    def get_variable(self, variable_id):
        for variable in self._variables:
            if variable.variable_id == variable_id:
                return variable


class EnvironmentVariable(object):
    def __init__(self, variable_id, name, description, amount, max, min):
        self._variable_id = variable_id
        self._name = name
        self._description = description
        self._amount = amount
        self._max = max
        self._min = min

    @property
    def variable_id(self):
        return self._variable_id

    @property
    def name(self):
        return self._name

    @property
    def amount(self):
        return self._amount

    def add(self, amount):
        self._amount += amount
        if self.max is not None and self._amount > self.max:
            self._amount = self.max

    def subtract(self, amount):
        self._amount -= amount
        if self.min is not None and self._amount < self.min:
            self._amount = self.min

    @property
    def max(self):
        return self._max

    @property
    def min(self):
        return self._min

    @classmethod
    def from_json(cls, json_data):
        environment_variable = cls(
            variable_id=json_data['id'],
            name=json_data['name'],
            description=json_data['description'],
            amount=json_data.get('amount', 0),
            max=json_data.get('max', None),
            min=json_data.get('min', None)
        )

        return environment_variable
