from otree.api import *



doc = """
This is an ultimatium bargaining game.
"""


class C(BaseConstants):
    NAME_IN_URL = 'classicug'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'classicug/instructions.html'
    # Initial amount allocated to each player
    ENDOWMENT = cu(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    price = models.CurrencyField(
        min=0,
        max=C.ENDOWMENT,
        doc="""Amount offered by P1""",
        label="Please enter an amount from 0 to 100",
    )
    
    offer_accepted = models.BooleanField(
        label="Do you accept this offer?",
    )


class Player(BasePlayer):
    pass


# FUNCTIONS
def sent_back_amount_max(group: Group):
    return group.price


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.price
    p2.payoff = C.ENDOWMENT - group.price


    if group.offer_accepted == False:
        p1.payoff = 0
        p2.payoff = 0


# PAGES
class Introduction(Page):
    pass


class Propose(Page):
    """This page is only for P1
    P1 offers a price. P1 receives price and P2 receives
    endowment - price if P2 accepts. If P2 rejects, then both receive 0."""

    form_model = 'group'
    form_fields = ['price']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class ProposeWaitPage(WaitPage):
    pass


class Respond(Page):
    """This page is only for P2
    P2 accepts or declines"""

    form_model = 'group'
    form_fields = ['offer_accepted']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):

        group = player.group
        responder_payoff = C.ENDOWMENT - group.price
        return dict(responder_payoff=responder_payoff)

class RespondWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    """This page displays the earnings of each player"""

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(responder_payoff=C.ENDOWMENT - group.price)


page_sequence = [
    Introduction,
    Propose,
    ProposeWaitPage,
    Respond,
    RespondWaitPage,
    Results,
]
