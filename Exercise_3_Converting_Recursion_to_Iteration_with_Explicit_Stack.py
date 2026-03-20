import sys
import time
import tracemalloc


STATE_START = 0
STATE_REPLIES_DONE = 1


class Comment:
    def __init__(self, text, replies=None):
        self.text = text
        if replies is None:
            self.replies = []
        else:
            self.replies = replies


def flatten_recursive(comment):
    result = [comment.text]
    for reply in comment.replies:
        result += flatten_recursive(reply)
    return result


def flatten_iterative(comment):
    result = []
    stack = [(comment, STATE_START)]

    while len(stack) > 0:
        node, state = stack.pop()

        if state == STATE_START:
            result.append(node.text)
            stack.append((node, STATE_REPLIES_DONE))

            i = len(node.replies) - 1
            while i >= 0:
                stack.append((node.replies[i], STATE_START))
                i -= 1

        elif state == STATE_REPLIES_DONE:
            pass

    return result


def count_comments_recursive(comment):
    total = 1
    for reply in comment.replies:
        total += count_comments_recursive(reply)
    return total


def count_comments_tail(comment, accumulator):
    accumulator += 1

    if len(comment.replies) == 0:
        return accumulator

    if len(comment.replies) > 1:
        raise ValueError("This tail recursive version only works for a single-chain thread.")

    return count_comments_tail(comment.replies[0], accumulator)


def count_comments_loop(comment):
    total = 0
    current = comment

    while current is not None:
        total += 1

        if len(current.replies) == 0:
            current = None
        else:
            if len(current.replies) > 1:
                raise ValueError("This loop version only works for a single-chain thread.")
            current = current.replies[0]

    return total


def count_comments_iterative(comment):
    total = 0
    stack = [comment]

    while len(stack) > 0:
        node = stack.pop()
        total += 1

        i = len(node.replies) - 1
        while i >= 0:
            stack.append(node.replies[i])
            i -= 1

    return total


def build_example():
    subreply1 = Comment("SubReply1")
    reply1 = Comment("Reply1", [subreply1])
    reply2 = Comment("Reply2")
    comment1 = Comment("Comment1", [reply1, reply2])
    return comment1


def build_chain(depth):
    root = Comment("Comment1")
    current = root

    for i in range(2, depth + 1):
        new_node = Comment("Comment" + str(i))
        current.replies = [new_node]
        current = new_node

    return root


def measure(func, arg):
    tracemalloc.start()
    start = time.perf_counter()

    result = func(arg)

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return result, peak, (end - start) * 1000


def main():
    print("===== Test 1: Flatten comment thread =====")
    root = build_example()

    print("Input structure: Comment1 -> [Reply1 -> [SubReply1], Reply2]")

    r1 = flatten_recursive(root)
    r2 = flatten_iterative(root)

    print("flatten_recursive output:", r1)
    print("flatten_iterative output:", r2)

    if r1 == ["Comment1", "Reply1", "SubReply1", "Reply2"] and r2 == ["Comment1", "Reply1", "SubReply1", "Reply2"]:
        print("Flatten result is correct.")
    else:
        print("Flatten result is wrong.")

    print()
    print("===== Test 2: Count comments =====")
    print("Expected total comments: 4")

    c1 = count_comments_recursive(root)
    c2 = count_comments_iterative(root)

    print("count_comments_recursive:", c1)
    print("count_comments_iterative:", c2)

    if c1 == 4 and c2 == 4:
        print("Count result is correct.")
    else:
        print("Count result is wrong.")

    print()
    print("===== Test 3: Tail recursion and while loop =====")
    chain = build_chain(5)
    print("Single-chain depth: 5")

    c3 = count_comments_tail(chain, 0)
    c4 = count_comments_loop(chain)

    print("count_comments_tail:", c3)
    print("count_comments_loop:", c4)

    if c3 == 5 and c4 == 5:
        print("Tail recursion and loop results are correct.")
    else:
        print("Tail recursion and loop results are wrong.")

    print()
    print("===== Test 4: Simple performance comparison =====")
    depths = [5, 10, 50, 100, 500]
    print("Python recursion limit:", sys.getrecursionlimit())

    for d in depths:
        chain = build_chain(d)
        print()
        print("Depth =", d)

        try:
            result1, peak1, time1 = measure(flatten_recursive, chain)
            print("Recursive: length =", len(result1), ", peak memory =", peak1, "B, time = %.3f ms" % time1)
        except RecursionError:
            print("Recursive: RecursionError")

        result2, peak2, time2 = measure(flatten_iterative, chain)
        print("Iterative: length =", len(result2), ", peak memory =", peak2, "B, time = %.3f ms" % time2)

    print()
    print("Program finished.")


if __name__ == "__main__":
    main()
