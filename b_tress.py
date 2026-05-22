# ============================================================
#  B-TREE — Full Implementation in Python
#  Multi-key self-balancing tree for disk-based storage systems
# ============================================================
#
#  Key property — minimum degree t:
#    - Every non-root node has at least t-1 keys (and at most 2t-1 keys)
#    - Every internal node has at least t children (and at most 2t)
#    - All leaves sit at the same depth
#    - The tree grows in height ONLY when the root splits
#


class BTreeNode:

    def __init__(self, t, leaf=False):
        # Minimum degree — defines the key/children bounds for this tree
        self.t = t
        # True if this node has no children
        self.leaf = leaf
        # Stores up to 2t-1 keys
        self.keys = []
        # Stores up to 2t children (only meaningful for internal nodes)
        self.children = []


class BTree:

    def __init__(self, t):
        # t is the minimum degree:
        #   Every node holds between t-1 (min) and 2t-1 (max) keys
        #   A node is "full" when it reaches 2t-1 keys
        self.t = t
        self.root = BTreeNode(t, True)  # Start with an empty leaf root

    # --------------------------------------------------------
    # traverse() — In-order walk of the entire tree.
    # Visits left child, prints key, visits right child —
    # generalised to multiple keys per node by interleaving
    # all children between the keys they bound.
    # Time: O(n)
    # --------------------------------------------------------
    def traverse(self, node=None):
        if node is None:
            node = self.root
        for i in range(len(node.keys)):
            if not node.leaf:
                self.traverse(node.children[i])
            print(node.keys[i], end=' ')
        if not node.leaf:
            self.traverse(node.children[len(node.keys)])

    # --------------------------------------------------------
    # search() — Find a key in the tree.
    # At each node, scan keys left-to-right then descend into
    # the correct child gap. Returns (node, index) on success,
    # None if the key is not in the tree.
    # Time: O(log n)
    # --------------------------------------------------------
    def search(self, key, node=None):
        if node is None:
            node = self.root
        i = 0
        # Advance past all keys smaller than the target
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        # Check if we landed on the key
        if i < len(node.keys) and key == node.keys[i]:
            return (node, i)        # Found
        if node.leaf:
            return None             # Key not in tree
        return self.search(key, node.children[i])

    # --------------------------------------------------------
    # insert() — Public entry point.
    # If the root is full (2t-1 keys), split it BEFORE inserting.
    # This is the ONLY time a B-Tree grows in height —
    # always from the root upward, keeping all leaves at equal depth.
    # --------------------------------------------------------
    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            # Root is full — create a new root and split the old one
            new_root = BTreeNode(self.t, False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(new_root, key)
        else:
            self._insert_non_full(root, key)

    # --------------------------------------------------------
    # _insert_non_full() — Insert into a guaranteed non-full node.
    # Walk down the tree, splitting any full children PROACTIVELY
    # so we never need a second pass back up.
    # Time: O(log n)
    # --------------------------------------------------------
    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1

        if node.leaf:
            # Shift keys right to make room, then place the new key
            node.keys.append(0)         # Extend list by one slot
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key      # Place key in correct position
        else:
            # Find the child that should receive the key
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1                      # i is now the correct child index

            # If that child is full, split it before descending
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self._split_child(node, i)
                # After the split, node.keys[i] is the promoted middle key.
                # Decide which of the two halves to descend into.
                if key > node.keys[i]:
                    i += 1

            self._insert_non_full(node.children[i], key)

    # --------------------------------------------------------
    # _split_child() — Split a full child node into two.
    # full_child (at parent.children[index]) has 2t-1 keys.
    # Split it into two nodes of t-1 keys each.
    # Promote the middle key (index t-1) up to parent.
    #
    # Before:  parent [...] -> [full_child: k0..k(2t-2)]
    # After:   parent [..., middle_key, ...] ->
    #              [left: k0..k(t-2)] [right: k(t)..k(2t-2)]
    # --------------------------------------------------------
    def _split_child(self, parent, index):
        t = self.t
        full_child = parent.children[index]

        # Create a new node to hold the right half of full_child
        new_child = BTreeNode(t, full_child.leaf)

        middle_key = full_child.keys[t - 1]   # The key to promote to parent

        # Right half keys go to new_child (keys after the middle)
        new_child.keys = full_child.keys[t:]
        # Left half stays in full_child (middle key is promoted, not kept)
        full_child.keys = full_child.keys[:t - 1]

        # If internal node, split child pointers too
        if not full_child.leaf:
            new_child.children = full_child.children[t:]   # Right half children
            full_child.children = full_child.children[:t]  # Left half children

        # Stitch new_child into parent's children list
        parent.children.insert(index + 1, new_child)
        # Promote the middle key into parent's key list
        parent.keys.insert(index, middle_key)


# ============================================================
#  DRIVER CODE
# ============================================================

if __name__ == "__main__":
    # Minimum degree t=3 means:
    #   Each non-root node holds between 2 and 5 keys
    #   Each internal node has between 3 and 6 children
    btree = BTree(3)

    values = [10, 20, 5, 6, 12, 30, 7, 17]
    for value in values:
        btree.insert(value)

    print("Traversal of B-Tree:")
    btree.traverse()
    # Output: 5 6 7 10 12 17 20 30
    print()

    print(btree.search(12))  # (<BTreeNode object>, 0) — found
    print(btree.search(99))  # None — not in tree
