from math import factorial
import random
# import time
import itertools

def combinations(n, k):
  return factorial(n) / (factorial(k) * factorial(n - k))

def calculate_variants(players, cards_in_deck, cards_per_player):
  return combinations(cards_in_deck, players * cards_per_player)

def calculate_chance(players, cards_in_deck, cards_per_player, specific_combination):
  total_variants = calculate_variants(players, cards_in_deck, cards_per_player)
  specific_combination_count = count_combination(deck, specific_combination)
  return specific_combination_count / total_variants

def count_combination(deck, specific_combination):
  count = 0
  for card in deck:
    if card in specific_combination:
      count += 1
  return count

def generate_deck():
  suits = ['h', 'd', 's', 'c']
  types = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
  
  deck = [{'type': type, 'suit': suit} for suit in suits for type in types]
  
  return deck

def shuffle_deck(deck):
  random.shuffle(deck)
  return deck

def card(type, suit):
  return {'type': type, 'suit': suit}

def card_to_string(card):
  return card['type'] + card['suit']

def deal_cards(deck, players, cards_per_player):
  player_hands = [[] for _ in range(players)]
  for _ in range(cards_per_player):
    for player in player_hands:
      player.append(deck.pop())
  return player_hands

# start_time = time.time()

players = 6
cards_per_player = 2
specific_combination = [card('9', 's'), card('A', 'd')]

use_default = input("Use default values? (y/n): ")

if use_default == 'n':
  try: 
    players = int(input("Enter the number of players: "))
  except ValueError: 
    print("Invalid input. Using default value of 6 players.")
    players = 6
    
  try:
    cards_per_player = int(input("Enter the number of cards per player: "))
  except ValueError:
    print("Invalid input. Using default value of 2 cards per player.")
    cards_per_player = 2

  try:
    specific_combination = [card(type, suit) for type, suit in input("Enter the specific combination (e.g. 9s Ad): ").split()]
  except ValueError:
    print("Invalid input. Using default value of 9s and Ad.")
    specific_combination = [card('9', 's'), card('A', 'd')]

deck = generate_deck()
# shuffle_deck(deck)
cards_in_deck = len(deck)


# player_hands = deal_cards(deck, players, cards_per_player)

# for i, hand in enumerate(player_hands, start=1):
#   print(f"Player {i}'s hand: {hand}")

# end_time = time.time()
# execution_time = (end_time - start_time) * 1000

# print(f"Execution Time: {execution_time}ms")
print(f"Chance of getting {', '.join(card_to_string(card) for card in specific_combination)} in a {players}-player game: {calculate_chance(players, cards_in_deck, cards_per_player, specific_combination)}")
print(f"Total Variants: {calculate_variants(players, cards_in_deck, cards_per_player)}")

def card_value(card):
    if card['type'].isdigit():
        return int(card['type'])
    elif card['type'] == 'J':
        return 11
    elif card['type'] == 'Q':
        return 12
    elif card['type'] == 'K':
        return 13
    elif card['type'] == 'A':
        return 14

def hand_value(hand):
    return sum(card_value(card) for card in hand)

def hand_rank(hand):
  values = [card_value(card) for card in hand]
  suits = [card['suit'] for card in hand]
  values.sort(reverse=True)

  def is_flush():
    return len(set(suits)) == 1

  def is_straight():
    return len(set(values)) == 5 and (max(values) - min(values) == 4 or values == [14, 5, 4, 3, 2])

  def kind(n):
    for value in set(values):
      if values.count(value) == n:
        return value
    return None

  def two_pair():
    pairs = [value for value in set(values) if values.count(value) == 2]
    return sorted(pairs, reverse=True) if len(pairs) == 2 else None

  if is_flush() and is_straight() and max(values) == 14:  # Royal Flush
    return (10,)
  elif is_flush() and is_straight():  # Straight Flush
    return (9, max(values))
  elif kind(4):  # Four of a Kind
    return (8, kind(4), kind(1))
  elif kind(3) and kind(2):  # Full House
    return (7, kind(3), kind(2))
  elif is_flush():  # Flush
    return (6,) + tuple(values)
  elif is_straight():  # Straight
    return (5, max(values))
  elif kind(3):  # Three of a Kind
    return (4, kind(3), kind(1), kind(1))
  elif two_pair():  # Two Pair
    return (3,) + tuple(two_pair()) + (kind(1),)
  elif kind(2):  # One Pair
    return (2, kind(2), kind(1), kind(1), kind(1))
  else:  # High Card
    return (1,) + tuple(values)

def simulate_game(deck, specific_combination, players):
  
  # Deal two private cards to each player
  deck = [card for card in deck if card not in specific_combination]
  print(len(deck))
  player_hands = deal_cards(deck, players, 2)
  deck.append(player_hands[players - 1][0])
  deck.append(player_hands[players - 1][1])
  player_hands[players - 1] = specific_combination
  
  first_hand = player_hands[players - 1]
  
  # Deal five community cards
  community_cards = [deck.pop() for _ in range(5)]
  
  # Each player makes their best possible five-card poker hand
  player_hands = [hand + community_cards for hand in player_hands]
  
  # Determine the rank of each hand
  player_hands = [(max(hand_rank(comb) for comb in itertools.combinations(hand, 5)), hand) for hand in player_hands]
  # print(player_hands)
  # Check if the specific combination is the highest hand
  highest_hand = max(player_hands, key=lambda x: x[0])
  print([card['type'] + card['suit'] for card in highest_hand[1]])
  if highest_hand[1] == first_hand + community_cards:
    return True
  return False

def simulate_games(deck, specific_combination, players, simulations=1000):
  wins = 0
  for _ in range(simulations):
    # Create a new shuffled deck for each game
    game_deck = shuffle_deck(deck.copy())
    
    # Simulate a game and check if the specific combination wins
    if simulate_game(game_deck, specific_combination, players):
      wins += 1
  
  # Calculate the winning odds
  winning_odds = wins / simulations
  return winning_odds

# Simulate games and print the estimated winning odds
winning_odds = simulate_games(deck, specific_combination, players)
print(f"Estimated winning odds: {winning_odds * 100}%")