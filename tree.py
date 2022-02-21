from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Node:
    value: str
    isLeaf: bool = False
    subnodes: dict[Node] = field(default_factory = dict)

    def add(self, item):
        if self.value != item:
            prefix = item[:len(self.value) + 1]
            if prefix in self.subnodes:
                self.subnodes[prefix].add(item)
            else:
                newNode = Node(prefix)
                newNode.add(item)
                self.subnodes[prefix] = newNode
        else:
            self.isLeaf = True
    
    def leafCount(self):
        return sum([n.leafCount() for n in self.subnodes.values()]) + (1 if self.isLeaf else 0)

    def __str__(self, tabDepth = 0) -> str:
        return (
            "\t" * tabDepth + 
            "Node {0} contains {1} subnodes:\n".format(self.value, len(self.subnodes)) +
            "\n".join([x.__str__(tabDepth+1) for x in self.subnodes.values()])
        )

    def __contains__(self, item):
        print("called contains on ", self.value)
        if self.value == item:
            return True

        prefix = item[:len(self.value) + 1]
        return prefix in self.subnodes and item in self.subnodes[prefix]

    def __len__(self) -> int:
        return 1 + sum(len(n) for n in self.subnodes.values())


if __name__ == '__main__':
    from wordlist import GUESSES

    top = Node("")
    for word in GUESSES:
        #print(word)
        top.add(word)


    print(len(top))
    print(top)