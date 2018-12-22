# -*- coding: utf-8 -*-

import Core_Lib as Core


# === CLASSES ==========================================================================================================
class HorizonsCharacter(Core.GenericCharacter):
    def __init__(self, name, dexterity, constitution, stamina, reflexes, perception, erudition, concentration,
                 ingeniosity, charisma, persuasion, empathy):
        Core.GenericCharacter.__init__(self, name)


class CharAttribute:
    def __init__(self, value):
        self.value = value
