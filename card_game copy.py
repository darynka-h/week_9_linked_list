"""Implemented faculty game"""
from typing import Any


class Node:
    """Class Node"""
    def __init__(self, data=None, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


class CycleLinkedList:
    """class CycleLinkedList"""
    def __init__(self, head=None) -> None:
        self.head = head

    def empty(self):
        """Check if linked list is empty"""
        if self.head is None:
            return True
        return False

    def search(self, unknown: Node):
        """Search required element"""
        probe = self.head
        if probe is None:
            return None
        if probe.data == unknown:
            return probe
        else:
            probe = probe.next
        while probe != self.head:
            if probe.data == unknown:
                return probe
            probe = probe.next
        return -1

    def head_insert(self, data):
        """Insert element at the head"""
        new_node = Node(data)
        if self.empty():
            new_node.prev = new_node
            new_node.next = new_node
        else:
            new_node.next = self.head
            new_node.prev = self.head.prev
            self.head.prev.next = new_node
            self.head.prev = new_node
        self.head = new_node

    def tail_insert(self, data):
        """Insert in the tail element"""
        new_node = Node(data)
        if self.empty():
            new_node.prev = new_node
            new_node.next = new_node
            self.head = new_node
        else:
            new_node.prev = self.head.prev
            new_node.next = self.head
            new_node.prev.next = new_node
            self.head.prev = new_node

    def insert_after(self, current, data):
        """Insert after some element"""
        current = self.search(current)
        if current:
            new_node = Node(data)
            new_node.next = current.next
            new_node.prev = current
            current.next.prev = new_node
            current.next = new_node

    def insert_after_by_clockwise(self, data, node: Node):
        """
       insert element after by clockwise
        """
        current = node
        if current:
            new_node = Node(data)
            new_node.next = current.next.next
            new_node.prev = current.next
            current.next.next.prev = new_node
            current.next.next = new_node

    def delete_anti_clockwise(self, current):
        """
        delete elment after clockwise
        """
        probe = current.prev.prev.prev.prev.prev.prev.prev
        probe.prev.next = probe.next
        probe.next.prev = probe.prev
        return probe.data, probe.next

    def stringify(self):
        """Stringify list elements"""
        probe = self.head
        if probe:
            print(probe.data, end=" ")
            probe = probe.next
            while probe is not self.head:
                print(probe.data, end=" ")
                probe = probe.next
        print()


def play_cardgame(num_players: int, num_cards: int) -> tuple:
    """The function predict luck player number based on
    count of players in game and number of cards
    """
    players_points = {x: 0 for x in range(1, num_players + 1)}

    link_list_1 = CycleLinkedList()
    link_list_1.head_insert(0)
    current = link_list_1.head
    counter = 1

    for i in range(1, num_cards):
        if counter % num_players == 1 and counter > num_players - 1:
            counter = 1
        if i % 23 == 0:
            players_points[counter] += i
            deleting = link_list_1.delete_anti_clockwise(current)
            players_points[counter] += deleting[0]
            current = deleting[1]
        else:
            link_list_1.insert_after_by_clockwise(i, current)
            current = current.next.next
        counter += 1
    max_key = max(zip(players_points.values(), players_points.keys()))[1]

    if players_points[max_key] == 0:
        return (0, set())
    return (players_points[max_key], set([max_key]))



# print(play_cardgame(100, 20_000_000))
