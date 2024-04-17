from typing import Any


class Node:
    def __init__(self, data=None, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next


class CycleLinkedList:
    def __init__(self, head=None) -> None:
        self.head = head

    def empty(self):
        if self.head is None:
            return True
        return False

    def search(self, x):
        probe = self.head
        if probe is None:
            return None
        if probe.data == x:
            return probe
        else:
            probe = probe.next
        while probe != self.head:
            if probe.data == x:
                return probe
            probe = probe.next
        return -1

    def head_insert(self, data):
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
        current = self.search(current)
        if current:
            new_node = Node(data)
            new_node.next = current.next
            new_node.prev = current
            current.next.prev = new_node    
            current.next = new_node

    def insert_after_by_clockwise(self, data, val):
        """
        вставляє після поточного елементу за годинниковою стрілкою
        """
        current = data - 1
        if current % 23 == 0:
            current = val
        current = self.search(current)
        if current:
            new_node = Node(data)
            new_node.next = current.next.next
            new_node.prev = current.next
            current.next.next.prev = new_node
            current.next.next = new_node

    def delete_anti_clockwise(self, current):
        """
        вставляє після поточного елементу за годинниковою стрілкою
        """
        current = self.search(current - 1)
        # probe.data = 9
        probe = current.prev.prev.prev.prev.prev.prev.prev
        probe.prev.next = probe.next
        probe.next.prev = probe.prev
        # повертати що стоїть наступне після видаленого
        return probe.data, probe.next

    def stringify(self):
        probe = self.head
        if probe:
            print(probe.data, end=" ")
            probe = probe.next
            while probe is not self.head:
                print(probe.data, end=" ")
                probe = probe.next
        print()


# link_list_1 = CycleLinkedList()
# head in
# link_list_1.head_insert(3)
# link_list_1.head_insert(2)
# link_list_1.head_insert(1)
# link_list_1.stringify()
# =============================================
# link_list_1.stringify()
# link_list_1.head_insert(0)
# # print(link_list_1.head.data)
# counter = 1
# for i in range(1, 23):
#     if counter % 8 == 1 and counter > 7:
#         counter = 1
#     # print(counter)
#     # link_list_1.stringify()
#     link_list_1.insert_after_by_clockwise(i)
#     counter += 1
# ===============================================   
# link_list_1.insert_after_by_clockwise(1)
# link_list_1.insert_after_by_clockwise(2)
# link_list_1.insert_after_by_clockwise(3)
# link_list_1.insert_after_by_clockwise(4)
# link_list_1.insert_after_by_clockwise(5)
# link_list_1.insert_after_by_clockwise(6)
# link_list_1.insert_after_by_clockwise(7)
# ======
# link_list_1.stringify()

def play_cardgame(num_players, num_cards):
    players_points = {x: 0 for x in range(1, num_players + 1)}

    link_list_1 = CycleLinkedList()
    link_list_1.head_insert(0)
    current = link_list_1.head
    counter = 1
    val=0
    for i in range(1, num_cards):
        if counter % num_players == 1 and counter > num_players - 1:
            counter = 1
        # print(counter)
        if i % 23 == 0:
            players_points[counter] += i
            deleting = link_list_1.delete_anti_clockwise(i)
            players_points[counter] += deleting[0]
            # print(players_points[counter])
            current = deleting[1]
            val = current.data
        else:
            link_list_1.insert_after_by_clockwise(i,val)
            current = current.next
        counter += 1
    max_key = max(zip(players_points.values(), players_points.keys()))[1]

    # link_list_1.stringify()
    if players_points[max_key] == 0:
        return (0, set())
    return (players_points[max_key], set([max_key]))



print(play_cardgame(50, 24000))
# link_list_1 = CycleLinkedList()
# link_list_1.head_insert(0)
# print(link_list_1.head.data)
# print(link_list_1.head.prev.data)
# print(link_list_1.head.next.data)
