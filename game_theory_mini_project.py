# import necessary packages
import random
import graphviz
from typing import Optional

class TreeNode:
    """
    This class creates a TreeNode object. 

    A TreeNode is used to represent the nodes in the binary tree. 

    Args:

    
    
    """
    def __init__(self, key: int, turn: int,  parent: Optional["TreeNode"] = None):
        self.key = key
        self.turn = f"{turn%2+1}"
        self.payoff = (random.randint(1,10), random.randint(1,10))
        self.parent = parent
        self.left = None
        self.right = None

def determine_child_nodes(num_nodes: int) -> list[int]:
    if num_nodes > 1:
        num_child = random.randint(1, num_nodes)
        indexes = random.sample(range(0, num_nodes), num_child)
        return indexes
    else:
        return [0]

def build_tree(m: int = 3) -> tuple[TreeNode, list[TreeNode]]:
    node_key = 1
    root = TreeNode(key = node_key, turn = 0)
    if m >= 1:
        leaf_nodes = []
        for idx in range(m):
            new_nodes = []
            if len(leaf_nodes) > 0:
                num_leaf_nodes = len(leaf_nodes)
                nodes_with_child = determine_child_nodes(num_nodes=num_leaf_nodes)
                for node_idx in nodes_with_child:
                    node = leaf_nodes[node_idx]
                    node_key += 1
                    node.left = TreeNode(key = node_key, turn = idx, parent = node)
                    node_key += 1
                    node.right = TreeNode(key = node_key,turn = idx, parent = node)
                    new_nodes.append(node.left)
                    new_nodes.append(node.right)
            else:
                new_nodes.append(root)
            leaf_nodes = new_nodes
    return root, new_nodes

def find_parent_nodes(nodes: list[TreeNode]) -> list[TreeNode]:
    unique_nodes = set()
    parent_nodes = []
    for node in nodes:
        unique_nodes.add(node.parent)
    for node in unique_nodes:
        parent_nodes.append(node)
    return parent_nodes

def choose_random_node(node1: TreeNode, node2: TreeNode) -> TreeNode:
    prob = random.random()
    if prob >= 0.5:
        return node1
    else:
        return node2

def better_node(node1: TreeNode, node2: TreeNode, turn: str) -> TreeNode:
    if turn == "1":
        node_1_payoff = node1.payoff[0]
        node_2_payoff = node2.payoff[0]
        if node_1_payoff == node_2_payoff:
            return choose_random_node(node1, node2)
        elif node_1_payoff > node_2_payoff:
            return node1
        else:
            return node2
    else:
        node_1_payoff = node1.payoff[1]
        node_2_payoff = node2.payoff[1]
        if node_1_payoff == node_2_payoff:
            return choose_random_node(node1, node2)
        elif node_1_payoff > node_2_payoff:
            return node1
        else:
            return node2
        
def find_best(parent_node: TreeNode) -> TreeNode:
    if not parent_node.left:
        return parent_node
    else:
        player_turn = parent_node.turn
        left_node = find_best(parent_node.left)
        right_node = find_best(parent_node.right)
        better_child_node = better_node(left_node, right_node, player_turn)
        return better_child_node

def visualize_binary_tree(root: TreeNode, spe_node: TreeNode) -> None:
    dot = graphviz.Digraph()
    # Use a unique identifier for each node
    def add_nodes_edges(node: TreeNode, unique_id: str):
        right_id = unique_id + "R"
        left_id = unique_id + "L"
        if node.left:
            dot.node(unique_id, label="")
            if not node.left.left:
                if node.left.key == spe_node.key:
                    dot.node(left_id, label=str(node.left.payoff), style='filled', fillcolor='red')
                else:
                    dot.node(left_id, label=str(node.left.payoff))
            else:
                dot.node(left_id, label="")
            dot.edge(unique_id, left_id, label = f"L{node.turn}")
            add_nodes_edges(node.left, left_id)
        if node.right:
            if not node.right.right:
                if node.right.key == spe_node.key:
                    dot.node(right_id, label=str(node.right.payoff), style='filled', fillcolor='red')
                else:
                    dot.node(right_id, label=str(node.right.payoff))
            else:
                dot.node(right_id, label="")
            dot.edge(unique_id, right_id, label = f"R{node.turn}")
            add_nodes_edges(node.right, right_id)

    # Start from root with unique id "R"
    add_nodes_edges(root, "R")
    dot.render('binary_tree', view=True, format='png')

if __name__ == "__main__":

    try:
        user_input = int(input("Enter the number of stages you wish to generate:"))
        root, leaf_nodes = build_tree(user_input)
        parent_leaf_nodes = find_parent_nodes(leaf_nodes)
        spe_node = find_best(root)
        print("This is the reasonable Nash Equilibrium node", spe_node.payoff)
        visualize_binary_tree(root, spe_node)
    except ValueError:
        print("Input a valid integer!")
    

