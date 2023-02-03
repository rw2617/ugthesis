from otree.api import *
import random

doc = """
This is an ultimatium bargaining game.
"""


class C(BaseConstants):
    NAME_IN_URL = 'no_comp'
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'no_comp/instructions.html'
    PLAYERS_PER_GROUP = 2


class Group(BaseGroup):
    price = models.CurrencyField(
        min=0,
        max=150,
        doc="""Amount offered by the seller""",
        label="Please enter an amount from 0 to 150",
    )

    value = models.IntegerField(
        
    )
    
    offer_selected = models.IntegerField(
        choices=[
            [1, 'Accept'],
            [2, 'Reject'],
        ]
)

class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
            for group in subsession.get_groups():
                group.value = random.choice([50, 150])
                print(group.value)

class Player(BasePlayer):
    price = models.IntegerField(
        min=0,
        max=150,
    )


# FUNCTIONS

def set_payoffs(group: Group):

    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    if group.offer_selected == 1:
        p1.payoff = group.price
        p2.payoff = group.value - group.price

    else:
        p1.payoff = 0
        p2.payoff = 0


# PAGES
class Introduction(Page):
    pass


class Propose(Page):
    """This page is only for seller
    seller offers a price. seller receives price and buyer receives
    value - price if buyer accepts. If buyer rejects, then both receive 0."""

    form_model = 'player'
    form_fields = ['price']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.id_in_group == 1:
            player.group.price = player.price


class ProposeWaitPage(WaitPage):
    pass


class Respond(Page):
    """This page is only for buyer
    buyer accepts or declines"""

    form_model = 'group'
    form_fields = ['offer_selected']

    
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2


    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            responder_payoff=group.value - group.price,
            )

class RespondWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    """This page displays the earnings of each player"""

    """@staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            responder_payoff1=group.value - group.price1,
            responder_payoff2=group.value - group.price2,
            )"""
    pass


page_sequence = [
    Introduction,
    Propose,
    ProposeWaitPage,
    Respond,
    RespondWaitPage,
    Results,
]