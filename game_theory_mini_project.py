# import necessary packages
import random
import graphviz
from typing import Optional

class TreeNode:
    """  
    This class creates a TreeNode object. 

    A TreeNode is used to represent the nodes in the binary tree. 

    Args:
        key (int): Unique id of the TreeNode object
        turn (int): integer used to determine the turn of the player
        parent (Optional[TreeNode]): stores any parent node to the TreeNode
    
    Attributes:
        key (int): unique id of the TreeNode object
        turn (str): binary value that can either be 1 or 2. 1 indicates a node that player 1 will choose and 2 otherwise.
        payoff (tuple[int, int]): tuple containing 2 integers representing the payoffs for player 1 and player 2 respectively. The payoffs are randomly generated from 1 to 10. 
        parent (TreeNode): TreeNode indicating the parent node of this node, else None if it's the root node.
        left (Optional[TreeNode]): References the TreeNode child on the left of this node
        right (Optional[TreeNode]): References the TreeNode child on the right of this node
    """
    def __init__(self, key: int, turn: int,  parent: Optional["TreeNode"] = None):
        self.key = key
        self.turn = f"{turn%2+1}"
        self.payoff = (random.randint(1,10), random.randint(1,10))
        self.parent = parent
        self.left = None
        self.right = None

def determine_child_nodes(num_nodes: int) -> list[int]:
    """
    This function is used to generate the indexes of the nodes chosen to have child nodes.

    The random package is used to generate a sample of node indexes from a range of values. This method is used to introduce a degree of randomness to the generation of the binary tree and ensures that the binary tree will not necessarily be a full binary tree. 

    Args:
        num_nodes (int): Determines the number of nodes available to have child nodes.

    Returns:
        list[int]: List containing the indexes of the nodes chosen to generate child nodes
    """
    # if statement checking that the number of nodes more than 1
    if num_nodes > 1:
        # randomly generate the number of nodes that will have child nodes at this level
        num_child = random.randint(1, num_nodes)

        # random sample (without replacement) of size num_child, containing the indexes of the nodes chosen to have children
        indexes = random.sample(range(0, num_nodes), num_child)
        return indexes
    else:
        # if there is only one node available that can have child nodes, return index 0 as there's only one option
        return [0]

def build_tree(m: int = 3) -> TreeNode:
    """
    This function is used to generate a binary tree, with levels determined by the user.

    The binary tree generates at least 1 pair of child nodes at each stage, up to the stage stated by the user. 

    Args:
        m (int): number of stages to be generated

    Returns:
        TreeNode: a reference to the root of the binary tree.
    """
    # node_key of the root node
    node_key = 1

    # creating the root node
    root = TreeNode(key = node_key, turn = 0)

    # if statement ensuring that the number of nodes to be generated >= 1, hence is a valid stage for the binary tree.
    if m >= 1:
        # empty list that will store the TreeNodes that are leaf nodes in this binary tree
        leaf_nodes = []

        # for loop repeating m times to generate m stages
        for idx in range(m):
            # empty list storing new nodes generated in this stage
            new_nodes = []
            # if statement checking that there are leaf nodes inside leaf_nodes
            if len(leaf_nodes) > 0:
                # obtaining the number of leaf nodes at the current stage
                num_leaf_nodes = len(leaf_nodes)
                
                # randomly generating the indexes of the nodes that will have a child node
                nodes_with_child = determine_child_nodes(num_nodes=num_leaf_nodes)

                # for loop iterating through each node index
                for node_idx in nodes_with_child:

                    # obtaining the node from the leaf_nodes list at index node_idx
                    node = leaf_nodes[node_idx]
                    
                    # incrementing the unique TreeNode id by 1 to create a new id
                    node_key += 1

                    # Generating and assigning the left child node
                    node.left = TreeNode(key = node_key, turn = idx, parent = node)

                    # incrementing the unique TreeNode id by 1 to create a new id
                    node_key += 1

                    # Generating and assigning the right child node
                    node.right = TreeNode(key = node_key,turn = idx, parent = node)

                    # adding the left and right child nodes to new_nodes
                    new_nodes.append(node.left)
                    new_nodes.append(node.right)
            else:
                # if no leaf nodes exist in leaf_nodes, the root node is appended to the list
                new_nodes.append(root)

            # leaf_nodes now updated to the new_nodes created at this stage
            leaf_nodes = new_nodes
    return root

def better_node(node1: TreeNode, node2: TreeNode, turn: str) -> TreeNode:
    """
    This function is used to determine which node the current player will choose, depending on the corresponding payoff.

    Args:
        node1 (TreeNode): TreeNode reference to first node
        node2 (TreeNode): TreeNode reference to second node
        turn (str): string indicating the player who will be making the choice. This determines the corresponding payoff that will be considered.
    
    Returns
        TreeNode: TreeNode referencing the node that will be chosen by the player
    """
    # if statement checking if the first player is making the choice this turn
    if turn == "1":
        # determining the payoffs received by the first player from the first and second nodes
        node_1_payoff = node1.payoff[0]
        node_2_payoff = node2.payoff[0]

        # if statement checking if the payoffs received from both nodes by player 1 are equal
        if node_1_payoff == node_2_payoff:
            # randomly choosing between the 2 nodes with equal probability as the player does not have any incentive to choose one node over the other
            return random.choice([node1, node2])
        
        # elif statement checking if payoff of node 1 > node 2, which makes it the better node and will be returned
        elif node_1_payoff > node_2_payoff:
            return node1
        
        else: 
            # else, node2 is returned as the payoff receieved is better than node1
            return node2
    else:
        # determining the payoffs received by the second player from the first and second nodes
        node_1_payoff = node1.payoff[1]
        node_2_payoff = node2.payoff[1]

        # if statement checking if the payoffs received from both nodes by player 2 are equal
        if node_1_payoff == node_2_payoff:
            # randomly choosing between the 2 nodes with equal probability as the player does not have any incentive to choose one node over the other
            return random.choice([node1, node2])
        
        # elif statement checking if payoff of node 1 > node 2, which makes it the better node and will be returned
        elif node_1_payoff > node_2_payoff:
            return node1
        
        else:
            # else, node2 is returned as the payoff receieved is better than node1
            return node2
        
def find_best(parent_node: TreeNode) -> TreeNode:
    """
    This function is used to find the node that will be chosen based on reasonable Nash Equilibrium, starting from a parent node.

    This function is called iteratively and functions like a divide and conquer algorithm, where the problem is constantly divides into two halfs, solved and have it's results returned.
    
    This function also simulates the process of finding the reasonable NE using backwards induction.

    Args:
        parent_node (TreeNode): TreeNode referencing the parent_node to start searching from

    Return:
        TreeNode: TreeNode referencing the child node that will be chosen based on reasonable Nash Equilibrium
    """

    # if statement checking if the parent node has any child nodes
    if not parent_node.left:
        # parent node returned as it's a leaf node
        return parent_node
    else:
        # obtaining the player turn at this stage
        player_turn = parent_node.turn

        # finding the resulting nodes from the left and right child nodes using backwards induction
        left_node = find_best(parent_node.left)
        right_node = find_best(parent_node.right)

        # determining the better node between the two resulting nodes, taking into account the current player's turn
        better_child_node = better_node(left_node, right_node, player_turn)

        # returning the resulting child node
        return better_child_node

def visualize_binary_tree(root: TreeNode, spe_node: TreeNode) -> None:
    """
    This function is used to generate an image visualization of the binary tree. The resulting image will be of 'png' format and the resulting node from rational NE is highlighted in red. 

    This function does not run any algorithms, instead it is purely used for visualization of the binary tree and the resulting solution.

    Functions:
        add_node_edges: refer to documentation of the function below

    Args:
        root (TreeNode): TreeNode referencing the root node of the binary tree
        spe_node (TreeNode): TreeNode referencing the node from rational NE
    
    Return:
        None
    """
    # creating the graphviz digraph object
    dot = graphviz.Digraph()

    def add_nodes_edges(node: TreeNode, unique_id: str) -> None:
        """
        This function is used to add the directed edges to the respective nodes

        Args:
            node (TreeNode): TreeNode referencing the target node
            unique_id (str): unique id for the node on graphviz diagram

        Return:
            None
        """
        
        # generating the string id for the left and right child nodes, if any
        right_id = unique_id + "R"
        left_id = unique_id + "L"

        # if statement checking if there are any child nodes
        if node.left:
            # creating the parent node with an empty label
            dot.node(unique_id, label="")

            # if statement checking if the left child node has no children (i.e. a leaf node)
            if not node.left.left:
                # if statement checking if the leaf node is the result node from rational NE
                if node.left.key == spe_node.key:
                    # creating the leaf node with a red fill to indicate it's the resulting node
                    dot.node(left_id, label=str(node.left.payoff), style='filled', fillcolor='red')
                else:
                    # else create a white leaf node with the payoff as it's label
                    dot.node(left_id, label=str(node.left.payoff))
            else:
                # since node is not a leaf node, create a blank white node
                dot.node(left_id, label="")
            
            # adding the directed edge from parent node to the child node with label indidcating the node's turn
            dot.edge(unique_id, left_id, label = f"L{node.turn}")

            # adding the node edges for the left node and it's children
            add_nodes_edges(node.left, left_id)

            # if statement checking if the right child node has no children (i.e. a leaf node)
            if not node.right.right:
                # if statement checking if the leaf node is the result node from rational NE
                if node.right.key == spe_node.key:
                    # creating the leaf node with a red fill to indicate it's the resulting node
                    dot.node(right_id, label=str(node.right.payoff), style='filled', fillcolor='red')
                else:
                    # else create a white leaf node with the payoff as it's label
                    dot.node(right_id, label=str(node.right.payoff))
            else:
                # since node is not a leaf node, create a blank white node
                dot.node(right_id, label="")

            # adding the directed edge from parent node to the child node with label indidcating the node's turn
            dot.edge(unique_id, right_id, label = f"R{node.turn}")

            # adding the node edges for the right node and it's children
            add_nodes_edges(node.right, right_id)

    # start from root with unique id "R"
    add_nodes_edges(root, "R")

    # output png file showing a visual of the generated binary tree
    dot.render('binary_tree', view=True, format='png')

if __name__ == "__main__":
    try:
        # obtaining user input for the number of stages to generate
        user_input = int(input("Enter the number of stages you wish to generate:"))

        # building the binary tree with m stages
        root = build_tree(user_input)

        # finding the resulting node from the rational NE
        spe_node = find_best(root)

        # printing the payoff of the resulting node
        print("This is the reasonable Nash Equilibrium node", spe_node.payoff)

        # creating the png visual of the generated binary tree
        visualize_binary_tree(root, spe_node)
    
    # ValueError raised when a non valid integer is the user_input
    except ValueError:
        print("Input a valid integer!")
    

