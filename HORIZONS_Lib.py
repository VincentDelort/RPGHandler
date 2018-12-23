import Core_Lib as Core


# === CLASSES ==========================================================================================================
class HorizonsCharacter(Core.GenericCharacter):
    def __init__(self, name, description, dexterity, constitution, stamina, reflexes, perception, erudition,
                 concentration, ingeniosity, charisma, persuasion, empathy):
        Core.GenericCharacter.__init__(self, name, description)

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

    def set_status_from_list(self, status):
        """
        :type status: CharStatus
        """
        if status in STATUS:
            self.status = status
        else:
            raise CharStatusException('Status isnt listed.')

    def set_status_from_scratch(self, name, description, attribute_list, modificator_list):
        """
        :type name: str
        :type description: str
        :type attribute_list: list
        :type modificator_list: list
        """
        self.status = CharStatus(name, description, attribute_list, modificator_list)

    def add_skill(self, name, description, mastery, linked_attribute=None, is_special=False):
        """
        :type name: str
        :type description: str
        :type mastery: str
        :type linked_attribute: CharAttribute
        :type is_special: bool
        """
        self.skills.append(CharSkill(name, description, mastery, linked_attribute, is_special))

    def get_skill_by_name(self, name):
        """
        :type name: str
        """
        for skill in self.skills:
            if skill.name == name:
                return skill
        return None

    def set_skill_mastery(self, skill_name, mastery):
        """
        :type skill_name: str
        :type mastery: str
        """
        skill = self.get_skill_by_name(skill_name)
        skill.set_mastery(mastery)

    def delete_skill(self, skill_name):
        """
        :type skill_name: str
        """
        skill = self.get_skill_by_name(skill_name)
        self.skills.remove(skill)

    def add_item(self, name, description):
        """
        :type name: str
        :type description: str
        """
        self.stuff.append(CharItem(name, description))

    def get_item_by_name(self, item_name):
        """
        :type item_name: str
        """
        for item in self.stuff:
            if item.name == item_name:
                return item
        return None

    def edit_item(self, name, new_description):
        """
        :type name: str
        :type new_description: str
        """
        item = self.get_item_by_name(name)
        item.description = new_description

    def delete_item(self, name):
        """
        :type name: str
        """
        item = self.get_item_by_name(name)
        self.stuff.remove(item)


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
            raise HorizonsException("Skill mastery doesnt exist.")

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
    def __init__(self, string):
        self.message = 'HORIZONS Exception: ' + str(string)


class CharStatusException(HorizonsException):
    def __init__(self, string):
        self.message = 'HORIZONS Exception > Character status: ' + str(string)


class CharSkillException(HorizonsException):
    def __init__(self, string):
        self.message = 'HORIZONS Exception > Character skill: ' + str(string)


class CharAttributeException(HorizonsException):
    def __init__(self, string=''):
        self.message = 'HORIZONS Exception > Character Attribute: ' + str(string)


# class CharAttributeLimitException(CharAttributeException):
#     def __init__(self):
#         self.message += 'Attribute value outside limits.'
