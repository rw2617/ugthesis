from otree.api import *
import random

doc = """
This is an ultimatium bargaining game.
"""


class C(BaseConstants):
    NAME_IN_URL = 'competition'
    NUM_ROUNDS = 2
    INSTRUCTIONS_TEMPLATE = 'comp/instructions.html'
    PLAYERS_PER_GROUP = 3
    SELLER1_ROLE = 'Seller'
    SELLER2_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'


class Player(BaseGroup):
    price1 = models.IntegerField(
        min=0,
        max=150,
    )

    price2 = models.IntegerField(
        min=0,
        max=150,
    )

    #offer_selected, both prices less than value
    offer_selected = models.IntegerField(
        label="Make a selection.",
        initial=0,
        choices=[
            [1, 'Accept offer from Seller 1'],
            [2, 'Accept offer from Seller 2'],
            [3, 'Reject both'],
        ]
    )

    #offer_selected2, price1 less than value, price2 greater than value
    offer_selected2 = models.IntegerField(
        label="Make a selection.",
        initial=0,
        choices=[
            [1, 'Accept offer from Seller 1'],
            [3, 'Reject'],
        ]
    )

    #offer_selected3, price1 greater than value, price2 less than value
    offer_selected3 = models.IntegerField(
        label="Make a selection.",
        initial=0,
        choices=[
            [2, 'Accept offer from Seller 2'],
            [3, 'Reject'],
        ]
    )

    #offer_selected4, both prices greater than value
    offer_selected4 = models.IntegerField(
        label="Make a selection.",
        initial=0,
        choices=[
            [3, 'Reject'],
        ]
    )

    value = models.IntegerField(
        
    )


class Group(BaseGroup):
    price1 = models.CurrencyField(
        min=0,
        max=150,
        doc="""Amount offered by the Seller 1""",
        label="Please enter an amount from 0 to 150",
    )

    price2 = models.CurrencyField(
        min=0,
        max=150,
        doc="""Amount offered by the Seller 2""",
        label="Please enter an amount from 0 to 150",
    )

    value = models.IntegerField(
        
    )


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    for group in subsession.get_groups():
        group.value = random.choice([50, 150])
        for player in group.get_players():
            player.value = group.value


def set_payoffs(group):

    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p3 = group.get_player_by_id(3)

    offer_selected = p3.field_maybe_none('offer_selected')
    offer_selected2 = p3.field_maybe_none('offer_selected2')
    offer_selected3 = p3.field_maybe_none('offer_selected3')
    offer_selected4 = p3.field_maybe_none('offer_selected4')

    if group.offer_selected == 3 or group.offer_selected2 == 3 or group.offer_selected3 == 3 or group.offer_selected4 == 3:
        p1.payoff = 0
        p2.payoff = 0
        p3.payoff = 0

    if group.offer_selected == 2 or group.offer_selected3 == 2:
        p1.payoff = 0
        p2.payoff = group.price2
        p3.payoff = group.value - group.price2

    if group.offer_selected == 1 or group.offer_selected2 == 1:
        p1.payoff = group.price1
        p2.payoff = 0
        p3.payoff = group.value - group.price1
        


# PAGES
class Introduction(Page):
    pass


class Propose(Page):
    """This page is only for seller
    seller offers a price. seller receives price and buyer receives
    value - price if buyer accepts. If buyer rejects, then both receive 0."""

    @staticmethod
    def get_form_fields(player):
        if player.id_in_group == 1:
            return ['price1']
        else:
            return ['price2']

    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1 or player.id_in_group == 2
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.id_in_group == 1:
            player.group.price1 = player.price1
        if player.id_in_group == 2:
            player.group.price2 = player.price2


class ProposeWaitPage(WaitPage):
    pass


class Respond(Page):
    """This page is only for buyer
    buyer accepts or declines"""

    @staticmethod
    def get_form_fields(player):
        if player.group.price1 > player.group.value and player.group.price2 > player.group.value:
            return ['offer_selected4']
        if player.group.price1 > player.group.value and player.group.price2 <= player.group.value:
            return ['offer_selected3']
        if player.group.price1 <= player.group.value and player.group.price2 > player.group.value:
            return ['offer_selected2']
        else:
            return ['offer_selected']

    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 3

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            responder_payoff1=group.value - group.price1,
            responder_payoff2=group.value - group.price2,
            )


class RespondWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    """This page displays the earnings of each player"""
    """@staticmethod
    def vars_for_template(player: Player):
        return dict(
            payoff=participant.payoff,
        )"""


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
