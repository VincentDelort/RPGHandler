import Core_Lib as Core


# === CLASSES ==========================================================================================================
class HorizonsCharacter(Core.GenericCharacter):
    def __init__(self, name, dexterity, constitution, stamina, reflexes, perception, erudition, concentration,
                 ingeniosity, charisma, persuasion, empathy):
        Core.GenericCharacter.__init__(self, name)

        self.dexterity = CharAttribute('dexterity', dexterity)
        self.constitution = CharAttribute('constitution', constitution)
        self.stamina = CharAttribute('stamina', stamina)
        self.reflexes = CharAttribute('reflexes', reflexes)
        self.perception = CharAttribute('perception', perception)
        self.erudition = CharAttribute('erudition', erudition)
        self.concentration = CharAttribute('concentration', concentration)
        self.ingeniosity = CharAttribute('ingeniosity', ingeniosity)
        self.charisma = CharAttribute('charisma', charisma)
        self.persuasion = CharAttribute('persuasion', persuasion)
        self.empathy = CharAttribute('empathy', empathy)


class CharAttribute:
    def __init__(self, name, value):
        self.name = name
        self.min = -4
        self.max = 4
        if self.min <= value <= self.max:
            self.value = int(value)
        else:
            self.value = 0

    def set_value(self, value):
        if self.min <= value <= self.max:
            self.value = value
        else:
            pass        # TODO | signal ? #


class CharGauge:
    def __init__(self, linked_attribute=None):
        self.linked_attribute = linked_attribute
        self.max = 0
        self.value = 0

    def variate(self, amount):
        if self.value + amount > self.max:
            self.value = self.max
        else:
            self.value += amount

    def replenish(self):
        self.value = self.max


class HPGauge(CharGauge):
    def __init__(self, constitution):
        """
        :param constitution:
        :type constitution: CharAttribute
        """
        CharGauge.__init__(self, linked_attribute=constitution)
        self.max = 10 + self.linked_attribute.value
        self.value = self.max

# === EXCEPTIONS =======================================================================================================
# class HorizonsException(Exception):
#     def __init__(self):
#         self.message = 'HORIZONS Exception'
#
#
# class CharAttributeException(HorizonsException):
#     def __init__(self, string=''):
#         self.message += ' > Character Attribute:' + str(string)
#
#
# class CharAttributeLimitException(CharAttributeException):
#     def __init__(self):
#         self.message += 'Attribute value outside limits.'
