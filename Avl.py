# ============================================================
#  AVL TREE — Full Implementation in Python
#  Self-balancing BST: guaranteed O(log n) on all operations
# ============================================================


class Node:

    def __init__(self, data):
        self.data = data    # The value stored in this node
        self.left = None    # Left child — holds smaller values
        self.right = None   # Right child — holds larger values
        self.height = 1     # Height of this node (leaf starts at 1)


class AVLTree:

    def __init__(self):
        self.root = None    # Empty tree — no nodes yet

    # --------------------------------------------------------
    # get_height()
    # Returns the height of a node.
    # If the node is None (empty), height is 0.
    # --------------------------------------------------------
    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    # --------------------------------------------------------
    # get_balance()
    # Balance factor = left height - right height.
    # A balanced node has a factor in {-1, 0, 1}.
    # > 1 means left-heavy; < -1 means right-heavy.
    # --------------------------------------------------------
    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # --------------------------------------------------------
    # rotate_right() — fixes a Left-Left imbalance.
    # z is the unbalanced node. y (z's left child) rises up
    # to take z's place. z drops down to become y's right child.
    #
    #       z                y
    #      / \              / \
    #     y   T4    ->     x   z
    #    / \                  / \
    #   x   T3               T3  T4
    # --------------------------------------------------------
    def rotate_right(self, z):
        y = z.left       # y will become the new subtree root
        T3 = y.right     # T3 moves from y's right to z's left

        y.right = z      # z drops down to y's right
        z.left = T3      # T3 fills the gap left by y

        # Heights must be updated bottom-up (z first, then y)
        z.height = 1 + max(self.get_height(z.left),
                           self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))

        return y         # y is now the root of this subtree

    # --------------------------------------------------------
    # rotate_left() — fixes a Right-Right imbalance.
    # Mirror image of rotate_right.
    #
    #     z                  y
    #    / \                / \
    #   T1   y     ->      z   x
    #       / \           / \
    #      T2   x        T1  T2
    # --------------------------------------------------------
    def rotate_left(self, z):
        y = z.right      # y will become the new subtree root
        T2 = y.left      # T2 moves from y's left to z's right

        y.left = z       # z drops down to y's left
        z.right = T2     # T2 fills the gap left by y

        z.height = 1 + max(self.get_height(z.left),
                           self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left),
                           self.get_height(y.right))

        return y

    # --------------------------------------------------------
    # insert() — Public entry point.
    # Updates the root with the result of the recursive insert.
    # --------------------------------------------------------
    def insert(self, data):
        self.root = self._insert(self.root, data)

    # --------------------------------------------------------
    # _insert() — Private recursive insert.
    # Two-pass approach:
    #   Pass 1 (going down):  insert like a normal BST.
    #   Pass 2 (going up):    update heights, fix imbalances.
    # --------------------------------------------------------
    def _insert(self, node, data):
        # --- Pass 1: Standard BST insertion ---
        if node is None:
            return Node(data)           # Found the right spot
        if data < node.data:
            node.left = self._insert(node.left, data)
        elif data > node.data:
            node.right = self._insert(node.right, data)
        else:
            return node                 # Duplicates are ignored

        # --- Pass 2: Update height of this ancestor node ---
        node.height = 1 + max(self.get_height(node.left),
                               self.get_height(node.right))

        # --- Pass 2: Check balance and apply the right rotation ---
        balance = self.get_balance(node)

        # Case 1 — Left-Left: new node went into left subtree's left side
        if balance > 1 and data < node.left.data:
            return self.rotate_right(node)

        # Case 2 — Right-Right: new node went into right subtree's right side
        if balance < -1 and data > node.right.data:
            return self.rotate_left(node)

        # Case 3 — Left-Right: new node went into left subtree's right side
        # Fix: rotate left child left first, then rotate root right
        if balance > 1 and data > node.left.data:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Case 4 — Right-Left: new node went into right subtree's left side
        # Fix: rotate right child right first, then rotate root left
        if balance < -1 and data < node.right.data:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node  # Node is balanced — no rotation needed

    # --------------------------------------------------------
    # delete() — Public entry point.
    # --------------------------------------------------------
    def delete(self, data):
        self.root = self._delete(self.root, data)

    # --------------------------------------------------------
    # _delete() — Private recursive delete.
    # Same two-pass approach as insert:
    #   Pass 1: find and remove the node (3 sub-cases).
    #   Pass 2: update heights and re-balance on the way back up.
    # --------------------------------------------------------
    def _delete(self, node, data):
        if node is None:
            return node  # Value not found — nothing to delete

        # --- Pass 1: Navigate to the node ---
        if data < node.data:
            node.left = self._delete(node.left, data)
        elif data > node.data:
            node.right = self._delete(node.right, data)
        else:
            # Node found — 3 cases:

            # Case A: No left child — replace node with right child
            if node.left is None:
                return node.right

            # Case B: No right child — replace node with left child
            elif node.right is None:
                return node.left

            # Case C: Two children — replace data with in-order successor
            # (smallest value in the right subtree), then delete successor
            successor = self._get_min_node(node.right)
            node.data = successor.data
            node.right = self._delete(node.right, successor.data)

        # --- Pass 2: Update height ---
        node.height = 1 + max(self.get_height(node.left),
                               self.get_height(node.right))

        # --- Pass 2: Re-balance using the same 4 cases as insert ---
        balance = self.get_balance(node)

        # Case 1 — Left-Left
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)

        # Case 2 — Left-Right
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Case 3 — Right-Right
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)

        # Case 4 — Right-Left
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    # --------------------------------------------------------
    # _get_min_node()
    # Walks left until there's no more left child.
    # The leftmost node is always the smallest in a BST.
    # --------------------------------------------------------
    def _get_min_node(self, node):
        while node.left:
            node = node.left
        return node

    # --------------------------------------------------------
    # search() — Public entry point.
    # --------------------------------------------------------
    def search(self, data):
        return self._search(self.root, data)

    # --------------------------------------------------------
    # _search()
    # At each node, go left if smaller, right if larger.
    # Guaranteed O(log n) because AVL height is always bounded.
    # --------------------------------------------------------
    def _search(self, node, data):
        if node is None:
            return False            # Reached a dead end
        if data == node.data:
            return True
        if data < node.data:
            return self._search(node.left, data)
        return self._search(node.right, data)

    # --------------------------------------------------------
    # inorder() — Public entry point.
    # Collects results then prints in sorted order.
    # Left -> Root -> Right always yields ascending output in a BST.
    # --------------------------------------------------------
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        print(" -> ".join(map(str, result)))

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.data)
            self._inorder(node.right, result)


# ============================================================
#  DRIVER CODE
# ============================================================

if __name__ == "__main__":
    avl = AVLTree()

    # Insert values — AVL silently rotates to stay balanced
    for val in [30, 20, 40, 10, 25, 35, 50]:
        avl.insert(val)

    avl.inorder()
    # Output: 10 -> 20 -> 25 -> 30 -> 35 -> 40 -> 50

    print(avl.search(25))   # True
    print(avl.search(99))   # False

    avl.delete(20)          # Replaced by in-order successor (25)
    avl.inorder()
    # Output: 10 -> 25 -> 30 -> 35 -> 40 -> 50
