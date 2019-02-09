import datetime
class TreeNode:
    def __init__(self, **kwargs):
        # This node's stuff
        self.text = kwargs.get('text', 'this node')
        self.done = False
        self.created_on = kwargs.get(
            'created_on',
            datetime.datetime.now().strftime("(%Y-%m-%d %H:%M:%S)"))
        self.finished_on = kwargs.get(
            'finished_on',
            'DOES NOT APPLY')

        # Relationships with other nodes
        self.children = []
        self.parent = None
        if kwargs.get("parent", None):
            kwargs["parent"].add_child(self)
        self.update_depth()

    # For serializing to JSON
    def to_dict(self):
        return {
            "text": self.text,
            "children": [ c.to_dict() for c in self.children],
            "info": {
                "done": str(self.done),
                "created": str(self.created_on),
                "finished": str(self.finished_on) if self.done else "task not finished"
            }
        }

    @staticmethod
    def from_dict(d):
        if not dict:
            return TreeNode()

        node_info = d["info"]
        node = TreeNode(text=d["text"], created_on=node_info["created"], finished_on=node_info["finished"])

        for c in d["children"]:
            node.add_child(TreeNode.from_dict(c))

        return node


    def update_depth(self):
        self.depth = self.parent.depth + 1 if self.parent else 0

    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        child.update_depth()

    def remove_child(self, child):
        self.children.remove(child)

    def is_done(self):
        for c in self.children:
            if not c.is_done():
                return False

        return self.done

    def __str__(self):
        indent = '|' + '----' * self.depth
        return indent + self.text + f"[created: {self.created_on}, finished: {self.finished_on}]"

    def print_tree(self):
        lines = [str(self)]
        for c in self.children:
            lines.append(c.print_tree())

        return '<br>'.join(lines)

    def ancestors(self):
        ancestors = []
        current = self
        while current:
            ancestors.append(str(current))
            current = current.parent
        return '\n'.join(reversed(ancestors))

def get_command():
    return input("enter command")

class TreeManager:
    def __init__(self):
        self.root_nodes = []
        self.current_task = None
        self.operations = {
            "subtask": self.subtask,
            "done": self.done,
            "next-task": self.next_task
        }

    def to_dict(self):
        return {
            "root_nodes": [r.to_dict() for r in self.root_nodes],
            "current_task": self.current_task.text if self.current_task is not None else "--NONE--"
        }

    @staticmethod
    def from_dict(d):
        tm = TreeManager()
        tm.root_nodes = [TreeNode.from_dict(rn) for rn in d["root_nodes"]]
        tm.current_task = None
        return tm

    def execute_command(self, command):
        words = command.split();
        if not words:
            raise IndexError("Missing Command: Must supply a command")
        operation = words[0]
        args = ' '.join(words[1:])
        print("EXECUTE_COMMAND(): operation = {}, args = {}".format(operation,args))
        if operation in ["enqueue", "next-task"]:
            if not args:
                raise IndexError("Missing Command : This command must have an argument")
            self.next_task(args)
        elif operation in [ "subtask", "call", "push"]:
            if not args:
                raise IndexError("Missing Command : This command must have an argument")
            self.subtask(args)
        elif operation in ["return", "done", "pop"]:
            self.done()
        else:
            print("UNKNOWN OPERATION " + operation)
            return

        self.check_if_done()

    def check_if_done(self):
        # CHECK IF WE ARE DONE (find next undone task if not)
        if self.current_task is None:
            # Might be done, check that no tasks are not done,
            # if we make it all the way through the loop, print and quit.
            for n in self.root_nodes:
                if not n.is_done():
                    self.current_task = n
                    break
            else:
                print("EVERYTHING IS DONE")
                self.print_tree()

    def print_tree(self):
        lines = []
        for n in self.root_nodes:
            lines.append(n.print_tree())

        return '->' + '\n->'.join(lines)

    def next_task(self, task):
        self.root_nodes.append(TreeNode(text=task))

    def subtask(self, task):
        new_task = TreeNode(text=task)
        if self.current_task is not None:
            self.current_task.add_child(new_task)
        else:
            self.root_nodes.append(new_task)
        self.current_task = new_task

    def done(self):
        self.current_task.done = True
        if not self.current_task.is_done():
            print("Cannot mark done, task has unfinished children")
            self.current_task.done = False
            for c in self.current_task.children():
                if not c.is_done():
                    self.current_task = c
                    break
            else:
                raise Exception("Can't happen, is_done() would have returned True")

        else:
            self.current_task.finished_on = datetime.datetime.now().strftime("(%Y-%m-%d %H:%M:%S)")
            self.current_task = self.current_task.parent

def make_test_tree():
    root = TreeNode(text="This is the root node of the tree")
    root.add_child(TreeNode(text="This is a sub-task of root"))
    root.children[0].add_child(TreeNode(text="This is a sub-sub-task of root"))
    root.add_child(TreeNode(text="This is another child of root"))
    return root

if __name__ == "__main__":
    a = TreeNode()
    b = TreeNode()
    c = TreeNode()
    a.add_child(b)
    print("INPUT : " + input("say something"))
    try:
        a.remove_child(c)
    except ValueError:
        pass

    run()

