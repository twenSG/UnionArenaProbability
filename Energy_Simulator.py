#!/usr/bin/env python
# coding: utf-8

# In[33]:


import random

def request_input():
    while True:
        # Request the highest cost of cards, ensuring it's between 3 and 8
        highest_cost = int(input("Enter the highest cost card in the deck (between 3 and 8): "))
        if highest_cost < 3 or highest_cost > 8:
            print("The highest cost card must be between 3 and 8. Please enter a valid value.")
            continue
        
        # Request number of cards for each cost, limiting based on the highest cost
        zero_costs = int(input("Enter the number of 0-cost cards: "))
        one_costs = int(input("Enter the number of 1-cost cards: "))
        two_costs = int(input("Enter the number of 2-cost cards: "))
        two_energy_cards = int(input("Enter the number of 2-cost cards that produce 2 energy: "))
        three_costs = int(input("Enter the number of 3-cost cards: "))
        three_energy_cards = int(input("Enter the number of 3-cost cards that produce 2 energy: "))
        
        # Only ask for 4-cost or higher cards if highest cost allows it
        if highest_cost >= 4:
            four_costs = int(input("Enter the number of 4-cost cards: "))
        else:
            four_costs = 0
        
        if highest_cost >= 5:
            five_costs = int(input("Enter the number of 5-cost cards: "))
        else:
            five_costs = 0
        
        if highest_cost >= 6:
            six_costs = int(input("Enter the number of 6-cost cards: "))
        else:
            six_costs = 0
        
        if highest_cost >= 7:
            seven_costs = int(input("Enter the number of 7-cost cards: "))
        else:
            seven_costs = 0
        
        if highest_cost == 8:
            eight_costs = int(input("Enter the number of 8-cost cards: "))
        else:
            eight_costs = 0
        
        event_cards = int(input("Enter the number of Event cards (cards that do not produce energy): "))

        # Check the total number of cards
        total_cards = (zero_costs + one_costs + two_costs + two_energy_cards +
                       three_costs + three_energy_cards + four_costs + five_costs +
                       six_costs + seven_costs + eight_costs + event_cards + 4 + 4)  # 4 Final cards + 4 Special cards

        if total_cards == 50:
            # Return the deck composition if total cards are correct
            return {
                "highest_cost": highest_cost,
                "zero_costs": zero_costs,
                "one_costs": one_costs,
                "two_costs": two_costs,
                "two_energy_cards": two_energy_cards,
                "three_costs": three_costs,
                "three_energy_cards": three_energy_cards,  # Added 3-cost cards that produce 2 energy
                "four_costs": four_costs,
                "five_costs": five_costs,
                "six_costs": six_costs,
                "seven_costs": seven_costs,
                "eight_costs": eight_costs,  # Added 8-cost cards (if applicable)
                "event_cards": event_cards
            }
        else:
            # Ask the user to correct their inputs
            print(f"The total number of cards in the deck is {total_cards}. It must add up to exactly 50.")
            print("Please adjust the input values.")

def draw_cards(cards):
    # Create a list representing the deck based on the card counts
    deck = (
        [0] * cards["zero_costs"] +
        [1] * cards["one_costs"] +
        [2] * cards["two_costs"] +
        [3] * cards["three_costs"] +
        [4] * cards["four_costs"] +
        [5] * cards["five_costs"] +
        [6] * cards["six_costs"] +
        [7] * cards["seven_costs"] +  # 7-cost cards
        [8] * cards["eight_costs"] +  # 8-cost cards
        ["2E"] * cards["two_energy_cards"] +  # "2E" represents 2-cost cards producing 2 energy
        ["3E"] * cards["three_energy_cards"]  # "3E" represents 3-cost cards producing 2 energy
    )

    # Add 4 "Final" cards (3-cost, no energy) and 4 "Special" cards to the deck
    deck.extend([3] * 4)  # "Final" cards (3-cost)
    deck.extend([3] * 4)  # "Special" cards (treated as 3-cost cards)

    # Add "Event" cards (no energy produced) to the deck
    deck.extend([0] * cards["event_cards"])  # Event cards don't produce energy

    # Draw 7 random cards from the deck
    drawn_cards = random.sample(deck, 7)
    return drawn_cards

def calculate_energy(drawn_cards):
    # Calculate the energy produced by the drawn cards, excluding Event, Final, and Special cards
    energy = 0
    for card in drawn_cards:
        if card == "2E":
            energy += 2  # 2-cost card that produces 2 energy
        elif card == "3E":
            energy += 2  # 3-cost card that produces 2 energy
        elif isinstance(card, int) and card not in [0, 3]:  # Exclude Event, Final, Special cards
            energy += 1  # All other cards produce 1 energy
    return energy

def calculate_highest_cost(drawn_cards):
    # Determine the highest cost card in the drawn hand, excluding Event, Final, and Special cards
    highest_cost = 0
    for card in drawn_cards:
        if isinstance(card, int) and card != 3:  # Exclude 3-cost "Final" and "Special" cards
            highest_cost = max(highest_cost, card)
        elif card in ["2E", "3E"]:  # Special energy-producing cards
            highest_cost = max(highest_cost, 2)  # Treat them as 2-cost cards
    return highest_cost

def check_energy_requirement(cards):
    # Draw 7 random cards from the deck
    drawn_cards = draw_cards(cards)

    # Check if there is at least 1 zero-cost card and another 0-cost or 1-cost card
    if drawn_cards.count(0) == 0:
        return False  # Hand is not functional due to no 0-cost card
    
    # Ensure at least one additional 0-cost or 1-cost card is available for energy generation
    if drawn_cards.count(0) + drawn_cards.count(1) < 2:
        return False  # Not enough cards to generate energy for a higher-cost card

    # Calculate the total energy available from the drawn cards
    energy_available = calculate_energy(drawn_cards)

    # Find the highest cost card in the drawn hand
    highest_cost = calculate_highest_cost(drawn_cards)

    # Check if the available energy is sufficient to play the highest-cost card
    return energy_available >= highest_cost

def simulate_hands(cards, num_simulations=10000):
    playable_hands = 0

    for _ in range(num_simulations):
        if check_energy_requirement(cards):
            playable_hands += 1

    probability = playable_hands / num_simulations
    return probability

def main():
    while True:
        # Request input for the deck composition
        cards = request_input()

        # Simulate 10,000 hands and calculate the probability of a playable hand
        probability = simulate_hands(cards, num_simulations=10000)

        print(f"The probability of having a playable hand is: {probability * 100:.2f}%")

        # Ask the user if they want to start over
        restart = input("Do you want to try again with a different deck? (yes/no): ").strip().lower()
        if restart != 'yes':
            break

# Call the main function to run the program
if __name__ == "__main__":
    main()


# In[ ]:




