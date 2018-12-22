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

        self.health_gauge = CharGauge(self.constitution, 10)
        self.stamina_gauge = CharGauge(self.stamina, 5)

        self.status = STATUS['OK']

        self.skills = []
        self.stuff = []

    def set_attribute(self, attribute, value):
        """
        :type attribute: str
        :type value: int
        """
        if attribute == 'dexterity':
            self.dexterity.set_value(value)
        elif attribute == 'constitution':
            self.constitution.set_value(value)
            self.health_gauge.refresh()
        elif attribute == 'stamina':
            self.stamina.set_value(value)
            self.stamina_gauge.refresh()
        elif attribute == 'reflexes':
            self.reflexes.set_value(value)
        elif attribute == 'perception':
            self.perception.set_value(value)
        elif attribute == 'erudition':
            self.erudition.set_value(value)
        elif attribute == 'concentration':
            self.concentration.set_value(value)
        elif attribute == 'ingeniosity':
            self.ingeniosity.set_value(value)
        elif attribute == 'charisma':
            self.charisma.set_value(value)
        elif attribute == 'persuasion':
            self.persuasion.set_value(value)
        elif attribute == 'empathy':
            self.empathy.set_value(value)
        else:
            raise CharAttributeException('Attribute "' + attribute + '" is unknown.')

    def variate_gauge(self, gauge, amount):
        """
        :type gauge: str
        :type amount: int
        """
        if gauge == 'health':
            self.health_gauge.variate(amount)
        elif gauge == 'stamina':
            self.stamina_gauge.variate('stamina')

    def restore_health(self):
        self.health_gauge.replenish()

    def restore_stamina(self):
        self.stamina_gauge.replenish()

    def set_status(self, status):
        """
        :type status: CharStatus
        """
        if status in STATUS:
            self.status = status
        else:
            raise HorizonsException("Status doesnt exist.")
        

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
    def __init__(self, linked_attribute=None, offset=0):
        self.linked_attribute = linked_attribute
        self.offset = int(offset)
        self.max = self.offset + self.linked_attribute.value
        self.value = self.max

    def variate(self, amount):
        if self.value + amount > self.max:
            self.value = self.max
        else:
            self.value += amount

    def replenish(self):
        self.value = self.max

    def refresh(self):
        self.max = self.offset + self.linked_attribute.value


class CharSkill:
    def __init__(self, name, description, mastery, linked_attribute=None, is_special=False):
        """
        :type name: str
        :type description: str
        :type mastery: str
        :type linked_attribute: CharAttribute
        :type is_special: bool
        """
        self.name = str(name)
        self.description = str(description)
        self.linked_attribtue = linked_attribute
        self.is_special = is_special
        self.mastery = str(mastery)

    def set_mastery(self, mastery):
        mastery_list = ['Rudimentary',
                        'Basic',
                        'Professionnal',
                        'Expert',
                        'Living Legend']
        if mastery in mastery_list:
            self.mastery = mastery
        else:
            self.mastery = 'Basic'      # TODO | Consider sending a signal #

    def get_test(self):
        if self.is_special:
            return 'Special skill, see description...'

        offset = self.linked_attribtue.value
        if self.mastery == 'Rudimentary':
            test = '1d12'
        elif self.mastery == 'Basic':
            test = '1d20'
        elif self.mastery == 'Professionnal':
            test = '1d20 + 1d6'
        elif self.mastery == 'Expert':
            test = '1d20 + 1d12'
        elif self.mastery == 'Living Legend':
            test = '1d20 + 1d12 + 1d8'
        else:
            raise CharSkillException('Skill mastery "' + self.mastery + '" is unknown.')

        return str(offset) + ' ' + test


class CharItem:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class CharStatus:
    def __init__(self, name, description, attribute_list, modificator_list):
        """
        :type name: str
        :type description: str
        :type attribute_list: list
        :type modificator_list: list
        """
        self.name = name
        self.description = description
        self.attribute_list = attribute_list
        self.modificator_list = modificator_list


# === STATUS ===========================================================================================================
# TODO | Complete... #
STATUS = {'OK': CharStatus('OK', "", [], [])}


# === EXCEPTIONS =======================================================================================================
class HorizonsException(Exception):
    def __init__(self):
        self.message = 'HORIZONS Exception'


class CharSkillException(HorizonsException):
    def __init__(self, string):
        self.message += ' > Character skill:' + str(string)

class CharAttributeException(HorizonsException):
    def __init__(self, string=''):
        self.message += ' > Character Attribute:' + str(string)


# class CharAttributeLimitException(CharAttributeException):
#     def __init__(self):
#         self.message += 'Attribute value outside limits.'
