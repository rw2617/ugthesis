from otree.api import *
import random

doc = """
This is an ultimatium bargaining game.
"""


class C(BaseConstants):
    NAME_IN_URL = 'no_comp'
    NUM_ROUNDS = 2
    INSTRUCTIONS_TEMPLATE = 'no_comp/instructions.html'
    PLAYERS_PER_GROUP = 2
    SELLER_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'


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
        label="Make a selection.",
        initial=0,
        choices=[
            [1, 'Accept'],
            [2, 'Reject'],
        ]
    )

    offer_selected2 = models.IntegerField(
        label="Make a selection.",
        initial=0,
        choices=[
            [2, 'Reject'],
        ]
    )


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):

    for group in subsession.get_groups():
        group.value = random.choice([50, 150])

class Player(BasePlayer):
    price = models.IntegerField(
        min=0,
        max=150,
    )


# FUNCTIONS

def set_payoffs(group: Group):

    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    offer_selected = group.field_maybe_none('offer_selected')
    offer_selected2 = group.field_maybe_none('offer_selected2')

    if offer_selected == 1:
        p1.payoff = group.price
        p2.payoff = group.value - group.price

    if offer_selected == 2:
        p1.payoff = 0
        p2.payoff = 0

    if offer_selected2 == 2:
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

    @staticmethod
    def get_form_fields(player):
        if player.group.price > player.group.value:
            return ['offer_selected2']
        else:
            return ['offer_selected']

    form_model = 'group'
    
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

class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.group_randomly(fixed_id_in_group=True)


page_sequence = [
    Introduction,
    Propose,
    ProposeWaitPage,
    Respond,
    RespondWaitPage,
    Results,
    ShuffleWaitPage,
]

