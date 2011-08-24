import os

class GameObject(object):
    """Core object every game item is derived from, this is mostly a placeholder. One point,
    Verbs have the format:
    def verb(iobj, preposition)
    """
    def __init__(self, name):
	self.name = name
	self.location = None
	
    def _v_move(self, target):
        """Moves this object to the target"""
        old_loc = self.location
        target._accept(self)

        if old_loc:
            old_loc._remove(self)


class Container(GameObject):
    """Objects that can have an inventory"""
    def _accept(self, target):
        """Callback function that's called when something moves into the object."""
        self.contents.append(target)
        target.location = self

    def _remove(self, target):
        """Callback function that's called when something leaves this object"""
        if target in self.contents:
            self.contents.remove(target)

    def __init__(self, name):
	GameObject.__init__(self, name)
        self.contents = []
        pass


class Player(Container):
    """A player object. Holds a reference to his location."""
    def __init__(self):
	Container.__init__(self, "player")
        self.location = None

class Note(GameObject):
    def __init__(self, name, desc = None, text = None):
	GameObject.__init__(self, name)
	self.desc= None
	self.text = None

class Room(Container):
    """A room is a container, holding all objects and any players. Rooms are linked by named exits."""
    def __init__(self, name, desc):
        Container.__init__(self, name)
        self.desc = desc
        self.exits = dict()


    def link(self, target, out_name, back_name = None):
        """Links one room to another with an optional back exit."""
        self.exits[out_name] = target
        if back_name:
            target.exits[back_name] = self


    def _accept(self, target):
        Container._accept(self, target)
        if target == player:
	    self._v_look()

    def _v_look(self):
        """Response to the look command"""
	### ASSIGNMENT 1: Modify this method to list the room's contents in addition to the description and the exit list.
        print """%s
%s"""%(self.name, self.desc)
        exit_list = self.exits.keys()

	print "You see " + ", ".join([ item.name for item in self.contents ])
	

        print "You see exits to: [%s]"%(", ".join(exit_list))
        print ""


def dispatch(command):
    """We take a command, find the right objects it's talking about, then dispatch it on the dobj and the iobj,
    essentially it becomes
    dobj._v_command(iobj) where iobj is the target. First we have to find the objects in the available object list and pass those directly if possible
    If not, we send in the of the command as arguments"""

    # We operate in the context of the player and his location. Special case some nonsense, first we check for exits.
    abbreviations = {"n": "north", "s":"south", "e":"east", "w":"west", "i":"inventory", "l":"look"}

    # Swap the abbreviation for the command if we have it
    verb = abbreviations.get(command.verb, command.verb)

    # First check for exits
    loc = player.location
    if command.iobj == command.dobj == None or verb == "go":
        direction = command.dobj or verb
        exit = loc.exits.get(direction)
        if exit:
            return player._v_move(exit)


    # Other special case thing we do is 'look'
    if verb == "look" and command.iobj == command.dobj == None:
        return player.location._v_look()


    print "I don't understand what you mean."


class Command(object):
    """Encapsulates the concept of a 'command', modeled after LambdaMOO's command parser, parsing out into a
    <verb> <direct object> <preposition> <indirect object>"""

    def __init__(self, verb, dobj, prep, iobj):
        self.verb = verb
        self.dobj = dobj
        self.prep = prep
        self.iobj = iobj
        pass

    def __repr__(self):
        return "Command: %s, %s, %s, %s"%(self.verb, self.dobj, self.prep, self.iobj)


    @staticmethod
    def parse(line):
        """Take a line of text, normalize it and turn into into a command. Returns null if there's no way to parse it"""
        # Save some room for special forms, like say, emote, eval later.

        # Todo: Preserve commands by quotes
        words = line.lower().strip().split(" ")
        tokens = [ word.strip() for word in words ]

        command = dobj = prep = iobj = None

        # Degenerate case, single word command
        command = tokens[0]
        if len(tokens) == 1:
            return Command(command, None, None, None)

        # Second degenerate case, single direct object
        if len(tokens) == 2:
            return Command(command, tokens[1], None, None)
        
        # First, find the preposition
        prep_list = ["in", "at", "under", "over"]

        idx = None
        for p in prep_list:
            try:
                idx = tokens.index(p)

                if idx == 0:
                    # We can have prepositions as verbs if they're special cases, like exit names
                    # ie: 'in' should be short for 'go in'
                    return None

                prep = tokens[idx]
                break

            except:
                pass

        # If we don't have a preposition, assume the first token is the command, all the rest are the dobj
        if idx is None:
            command = tokens[0]
            if len(tokens) > 1:
                dobj = " ".join(tokens[1:])

        else:
            # We have a preposition, split the dobj and the iobj if they're there
            if len(tokens) > 2 and idx > 1:
                dobj = " ".join(tokens[1:idx])
            else:
                dobj = None

            if len(tokens)-1 != idx:
                iobj = " ".join(tokens[idx+1:])
            else:
                # There's a preposition but no iobj, bad command
                return None

            # Special form 'look at fish', is basically equivalent to 'look fish', where the fish is the direct object
            # in the event we have an iobj but no dobj, we swap them to make the ordering make more sense
            if dobj is None:
                dobj = iobj
                iobj = None
        
        return Command(command, dobj, prep, iobj)

player = None

def main():
    """Main loop"""

    # First we initiate a couple of rooms and a player.
    daisies = Room("Daisy Field", "You are standing in a field of daisies. The flowers make your nose itch.")
    outside_house = Room("Outside the House", "There is a dilapidated house looking sad and unused. Boards cover the door, but you think you can pry them loose. You can see the field of daisies to the south.")
    inside_house = Room("Inside the House", "A patchwork roof looms above you. The house isn't quite as derelict as it seems from the outside. You can see that once upon a time, this used to be a grand dwelling. Now there's nothing but remnants of memories of ghosts long dead.")

    daisies.link(outside_house, "north", "south")
    outside_house.link(inside_house, "in", "out")

    global player

    player = Player()
    player._v_move(daisies)

    mailbox = Container("mailbox")
    letter = Note("letter")
    letter._v_move(mailbox)
    mailbox._v_move(outside_house)
    
    sign = Note("sign")
    sign._v_move(outside_house)
    

    while True:
        # Main loop, parse user input
        line = raw_input(">")
        command = Command.parse(line)
        print ""

        # Watch for some special commands
        if command.verb in ["exit", "quit"]:
            break

        dispatch(command)

    print "Thanks for playing!"


if __name__ == "__main__":
    main()
