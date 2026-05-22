# ============================================================
#  LINKED LIST — Full Implementation in Python
#  Explained like a story, built like a pro
# ============================================================

# ------------------------------------------------------------
# NODE — A single bead on the chain
# Think of it as a relay runner: holds a baton (data)
# and knows who runs next.
# ------------------------------------------------------------

class Node:

    def __init__(self, data):
        self.data = data   # The value this node holds
        self.next = None   # Points to the next node (no one yet)


# ------------------------------------------------------------
# LINKED LIST — The relay team manager
# Doesn't run the race itself — just knows who starts (head).
# ------------------------------------------------------------

class LinkedList:

    def __init__(self):
        self.head = None   # Empty list — no runners yet

    # --------------------------------------------------------
    # append() — Add a new runner at the END of the chain
    # Walk all the way to the last person, then hand off.
    # Time: O(n) — must walk the full list to find the tail.
    # Tip: a self.tail pointer would make this O(1).
    # --------------------------------------------------------
    def append(self, data):
        new_node = Node(data)
        if self.head is None:        # List is empty — this node leads
            self.head = new_node
            return
        current = self.head
        while current.next:          # Walk until the last node
            current = current.next
        current.next = new_node      # Last node points to the new one

    # --------------------------------------------------------
    # prepend() — Add a new runner at the FRONT of the chain
    # They jump to the start and point to the old head.
    # Time: O(1) — no walking needed.
    # --------------------------------------------------------
    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head    # New node points to old head
        self.head = new_node         # New node IS the new head

    # --------------------------------------------------------
    # insert_after() — Insert a runner AFTER a specific value
    # Find the target node, then stitch the new one in.
    # Time: O(n) — must scan for the target.
    # --------------------------------------------------------
    def insert_after(self, target_data, new_data):
        current = self.head
        while current:
            if current.data == target_data:
                new_node = Node(new_data)
                new_node.next = current.next   # New node takes over the "next"
                current.next = new_node        # Target now points to new node
                return
            current = current.next
        print(f"Value {target_data} not found in the list.")

    # --------------------------------------------------------
    # delete() — Remove a runner from the chain
    # Find the person BEFORE them, then make them skip over.
    # Time: O(n) — must scan for the target.
    # --------------------------------------------------------
    def delete(self, data):
        if self.head is None:
            print("List is empty. Nothing to delete.")
            return

        # Special case: removing the very first node
        if self.head.data == data:
            self.head = self.head.next
            return

        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next   # Skip over the target
                return
            current = current.next

        print(f"Value {data} not found in the list.")

    # --------------------------------------------------------
    # search() — Find a value in the chain
    # Walk node by node until you find it (or run out).
    # Returns True/False; prints position if found.
    # Time: O(n)
    # --------------------------------------------------------
    def search(self, data):
        current = self.head
        position = 0
        while current:
            if current.data == data:
                print(f"Found {data} at position {position}.")
                return True
            current = current.next
            position += 1
        print(f"{data} not found in the list.")
        return False

    # --------------------------------------------------------
    # length() — Count how many runners are in the chain
    # Time: O(n)
    # --------------------------------------------------------
    def length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    # --------------------------------------------------------
    # reverse() — Flip the entire chain around
    # Each runner forgets who's next and points backwards.
    # Three-pointer technique: prev, current, next_node.
    # Time: O(n)  |  Space: O(1) — in-place, no extra list.
    # --------------------------------------------------------
    def reverse(self):
        previous = None
        current = self.head
        while current:
            next_node = current.next   # Remember who's next
            current.next = previous    # Point backwards
            previous = current         # Move previous forward
            current = next_node        # Move current forward
        self.head = previous           # New head is the old tail

    # --------------------------------------------------------
    # display() — Read the whole chain aloud
    # Walk from head to tail, printing each value.
    # Time: O(n)
    # --------------------------------------------------------
    def display(self):
        if self.head is None:
            print("[ Empty List ]")
            return
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements) + " -> None")


# ============================================================
#  DRIVER CODE
# ============================================================

if __name__ == "__main__":
    ll = LinkedList()

    # Build the chain
    ll.append(10)
    ll.append(20)
    ll.append(30)
    ll.append(40)
    print("After appending 10, 20, 30, 40:")
    ll.display()
    # Output: 10 -> 20 -> 30 -> 40 -> None

    # Jump to the front
    ll.prepend(5)
    print("\nAfter prepending 5:")
    ll.display()
    # Output: 5 -> 10 -> 20 -> 30 -> 40 -> None

    # Insert in the middle
    ll.insert_after(20, 25)
    print("\nAfter inserting 25 after 20:")
    ll.display()
    # Output: 5 -> 10 -> 20 -> 25 -> 30 -> 40 -> None

    # Delete a node
    ll.delete(25)
    print("\nAfter deleting 25:")
    ll.display()
    # Output: 5 -> 10 -> 20 -> 30 -> 40 -> None

    # Search
    ll.search(20)    # Found 20 at position 2.
    ll.search(99)    # 99 not found in the list.

    # Length
    print(f"\nLength: {ll.length()}")  # 5

    # Reverse
    ll.reverse()
    print("\nAfter reversing:")
    ll.display()
    # Output: 40 -> 30 -> 20 -> 10 -> 5 -> None
