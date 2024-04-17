# filepath = 'C:\\Users\\Daria\\Workspace\\OOP_second_sem\\week 9\\week_9_linked_list\\test.txt'

class Node:
    def __init__(self, item, next=None):
        self.item = item
        self.next = next

class Stack:

    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def push(self, item):
        self.head = Node(item, self.head)

    def pop(self):
        item = self.head.item
        self.head = self.head.next
        return item

    @property
    def peek(self):
        return self.head.item

    def __len__(self):
        count = 0
        current = self.head
        while current is not None:
            count +=1
            current = current.next
        return count

    def __str__(self):
        s = ''
        cur = self.head
        while cur is not None:
            s = str(cur.item) + ' ' +s
            cur = cur.next
        return 'bottom -> '+ s+'<- top'

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        file_list = file.readlines()
        for i, el in enumerate(file_list):
            el = el.strip()
            file_list[i] = el
        return file_list


def review_brackets(lines):
    salary = 0
    bracket_map = {'[': ']', '(': ')', '{': '}', '<': '>'}
    bracket_close = {']': '[', ')': '(', '}': '{', '>': '<'}
    for i, line in enumerate(lines):
        salary_index = 1
        stk = Stack()
        # print(stk)
        for j, bracket in enumerate(line):
            if bracket in bracket_map.keys():
                stk.push(bracket)
                # print("done")
            elif bracket_map.get(bracket) is None:
                if stk.is_empty():
                    new_bracket = bracket_close[bracket]
                    line = new_bracket + line
                    salary += salary_index
                    salary_index *= 2
                elif bracket_map[stk.peek] == bracket:
                    stk.pop()
                elif bracket_map[stk.peek] != bracket:
                    new_bracket = bracket_map[stk.peek]
                    line = line[:j] + new_bracket + line[j + 1:]
                    salary += salary_index
                    salary_index *= 2
                    stk.pop()
        while not stk.is_empty():
            new_bracket = bracket_map[stk.peek]
            line = line + new_bracket
            salary += salary_index
            salary_index *= 2
            stk.pop()

        lines[i] = line
    return (salary, lines)


def write_correct_lines(lines, filename):
    with open(filename, "w+", encoding='utf-8') as file1:
        for line in lines:
            line = line + '\n'
            file1.write(line)

# filepath_2 = 'C:\\Users\\Daria\\Workspace\\OOP_second_sem\\week 9\\week_9_linked_list\\test2.txt'
# print(read_file(filepath_2))
# print(review_brackets(read_file(filepath_2))[0])
# write_correct_lines(review_brackets(read_file(filepath_2))[1], 'aaa')