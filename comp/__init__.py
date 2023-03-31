from otree.api import *
import random

doc = """
This is an ultimatium bargaining game.
"""


class C(BaseConstants):
    NAME_IN_URL = 'competition'
    NUM_ROUNDS = 3
    INSTRUCTIONS_TEMPLATE = 'comp/Instructions.html'
    PLAYERS_PER_GROUP = 3
    SELLER1_ROLE = 'Seller'
    SELLER2_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'
    random_round = random.randint(1, NUM_ROUNDS)


class Player(BasePlayer):
    price1 = models.IntegerField(
        min=0,
        max=150,
        label="Please enter an amount from 0 to 150",
    )

    price2 = models.IntegerField(
        min=0,
        max=150,
        label="Please enter an amount from 0 to 150",
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

    value = models.IntegerField()

    round_payoff = models.CurrencyField()


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

    value = models.IntegerField()
    
    offer_selected = models.IntegerField()


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

    if offer_selected == 3 or offer_selected2 == 3 or offer_selected3 == 3 or offer_selected4 == 3:
        p1.round_payoff = 0
        p2.round_payoff = 0
        p3.round_payoff = 0

    if offer_selected == 2 or offer_selected3 == 2:
        p1.round_payoff = 0
        p2.round_payoff = group.price2
        p3.round_payoff = group.value - group.price2

    if offer_selected == 1 or offer_selected2 == 1:
        p1.round_payoff = group.price1
        p2.round_payoff = 0
        p3.round_payoff = group.value - group.price1

    if group.round_number == C.NUM_ROUNDS:
        p1.payoff = p1.in_round(C.random_round).round_payoff
        p2.payoff = p2.in_round(C.random_round).round_payoff
        p3.payoff = p3.in_round(C.random_round).round_payoff
        
    
    '''
    #actual payoff variable is the random one
    #save round payoff info 
    #if last round, payoff is the random

    random_payoff_round = models.IntegerField()
    round_payoff = models.CurrencyField()
    random_payoff_round = models.IntegerField()
    p1.payoff = 


    if group.round_number == C.NUM_ROUNDS:
            import random
            p1.random_payoff_round = random.randint(C.NUM_ROUNDS_NOBEL + 1, C.NUM_ROUNDS)
            p2.random_payoff_round = random.randint(C.NUM_ROUNDS_NOBEL + 1, C.NUM_ROUNDS)
            random_player_1 = p1.in_round(p1.random_payoff_round)
            random_player_2 = p2.in_round(p2.random_payoff_round)
            p1.payoff = random_player_1.round_payoff
            p2.payoff = random_player_2.round_payoff

        else:
            p1.round_payoff = p1.round_payoff
            p2.round_payoff = p2.round_payoff
    '''

# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


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
    def vars_for_template(player: Player):
        return dict(
            round_number=player.round_number,
        )
    
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
            round_number=player.round_number,
            )
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        p3 = player.group.get_player_by_id(3)

        offer_selected = p3.field_maybe_none('offer_selected')
        offer_selected2 = p3.field_maybe_none('offer_selected2')
        offer_selected3 = p3.field_maybe_none('offer_selected3')

        if offer_selected == 1 or offer_selected2 == 1:
            player.group.offer_selected = 1
        elif offer_selected == 2 or offer_selected3 == 2:
            player.group.offer_selected = 2
        else:
            player.group.offer_selected = 3


class RespondWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    """This page displays the earnings of each player"""
    """@staticmethod
    def vars_for_template(player: Player):
        return dict(
            payoff=participant.payoff,
        )"""
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            round_number=player.round_number,
        )


class FinalPayoffs(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            random_payoff = player.in_round(C.random_round).round_payoff,
            dollar_payoff = player.participant.payoff_plus_participation_fee(),
            r1_payoff = player.in_round(1).round_payoff,
            r2_payoff = player.in_round(2).round_payoff,
            r3_payoff = player.in_round(3).round_payoff,
            r4_payoff = player.in_round(4).round_payoff,
            r5_payoff = player.in_round(5).round_payoff,
            r6_payoff = player.in_round(6).round_payoff,
            r7_payoff = player.in_round(7).round_payoff,
            r8_payoff = player.in_round(8).round_payoff,
            r9_payoff = player.in_round(9).round_payoff,
            r10_payoff = player.in_round(10).round_payoff,
            r11_payoff = player.in_round(11).round_payoff,
            r12_payoff = player.in_round(12).round_payoff,
            r13_payoff = player.in_round(13).round_payoff,
            r14_payoff = player.in_round(14).round_payoff,
            r15_payoff = player.in_round(15).round_payoff,
            )

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
    FinalPayoffs,
    ShuffleWaitPage,
]
