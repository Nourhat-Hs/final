import random

bad_action = ["yell", "stalk", "scream", "murder", "bicker", "saw",
                 "steal","burn","destroy", "complain","fight", "kill", "shout", "hurt"]
good_action = [ "walk", "dream", "text","study", "play", "sing", "sew", "talk",
                "eat", "kiss", "craft", "sleep", "work", "laugh", "cry",
                 ]
all_actions = bad_action + good_action


def alex(a, b=None):
    if b != None:
        return "{} and {} both are not for me!".format(a + "ing", b + "ing")
    else:
        return "YESS! Time for {}".format(a + "ing")


def eli(a, b=None):
    if b != None:
        return "Yea, {} is an option. Or we could do some {}.".format(a + "ing", b + "ing")
    else:
        return "Hell No!, {} and {} are SUCK. We have to do some {}?".format(
            a + "ing")


def nina(a, b=None):
    suggestion = random.choice(all_actions)
    while (suggestion == a) or (suggestion == b):
        suggestion = random.choice(all_actions)

    if b == None:
        return "No, {} is not an option. We should do some {}?".format(a + "ing", suggestion + "ing")
    else:
        return "So We only get one option from the GREAT HOST? that is not fare!!." \
               " I say no to {}!".format(a + "ing", b + "ing", suggestion + "ing")


def livia(a, b=None):
    out = ""
    if good_action.__contains__(a) and b != None:
        out += "{} is disgusting ".format(a + "ing")
        if b != None and bad_action.__contains__(b):
            out += "Sure, both {} and {} seems ok to me".format(b + "ing")
        else:
            out += "and so does {}".format(b + "ing")
    elif bad_action.__contains__(a) and b != None:
        out += "Now you are talking {}! Let's go".format(a + "ing")
    else:
        out += "What? {} sucks. Not doing that".format(a + "ing")
    return out


bots_list = {'Alex': alex, 'Eli': eli, 'Nina': nina, 'Livia': livia}


def act_Bot(inp, activity, activity2=None):
    inp = str(inp).lower().capitalize()
    if inp in bots_list:
        return bots_list[inp](activity, activity2)
    else:
        return