#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct CommentNode {
    int comment_id;
    char user_id[50];
    char content[101];
    char timestamp[20];
    int likes;
    struct CommentNode** replies;
    int reply_count;
} CommentNode;

CommentNode* create_comment(int id, const char* user, const char* content,
                            const char* timestamp, int likes) {
    CommentNode* node = (CommentNode*)malloc(sizeof(CommentNode));
    node->comment_id = id;
    strncpy(node->user_id, user, 49);
    node->user_id[49] = '\0';
    strncpy(node->content, content, 100);
    node->content[100] = '\0';
    strncpy(node->timestamp, timestamp, 19);
    node->timestamp[19] = '\0';
    node->likes = likes;
    node->replies = NULL;
    node->reply_count = 0;
    return node;
}

void add_reply(CommentNode* parent, CommentNode* child) {
    parent->reply_count++;
    parent->replies = (CommentNode**)realloc(parent->replies,
                                             parent->reply_count * sizeof(CommentNode*));
    parent->replies[parent->reply_count - 1] = child;
}

void free_comment_tree(CommentNode* node) {
    if (!node) return;
    for (int i = 0; i < node->reply_count; i++) {
        free_comment_tree(node->replies[i]);
    }
    free(node->replies);
    free(node);
}

static void flatten_recursive_helper(CommentNode* node, CommentNode*** result,
                                     int* capacity, int* size) {
    if (!node) return;

    if (*size >= *capacity) {
        *capacity = (*capacity == 0) ? 4 : (*capacity) * 2;
        *result = (CommentNode**)realloc(*result, (*capacity) * sizeof(CommentNode*));
    }
    (*result)[(*size)++] = node;

    for (int i = 0; i < node->reply_count; i++) {
        flatten_recursive_helper(node->replies[i], result, capacity, size);
    }
}

CommentNode** flatten_recursive(CommentNode* comment, int* returnSize) {
    CommentNode** result = NULL;
    int capacity = 0;
    int size = 0;
    flatten_recursive_helper(comment, &result, &capacity, &size);
    *returnSize = size;
    return result;
}

#define STATE_START 0
#define STATE_REPLIES_DONE 1

typedef struct StackFrame {
    CommentNode* node;
    int state;
} StackFrame;

CommentNode** flatten_iterative(CommentNode* comment, int* returnSize) {
    CommentNode** result = NULL;
    int capacity = 0;
    int size = 0;

    StackFrame* stack = NULL;
    int stack_capacity = 0;
    int stack_size = 0;

    if (stack_size >= stack_capacity) {
        stack_capacity = (stack_capacity == 0) ? 4 : stack_capacity * 2;
        stack = (StackFrame*)realloc(stack, stack_capacity * sizeof(StackFrame));
    }
    stack[stack_size].node = comment;
    stack[stack_size].state = STATE_START;
    stack_size++;

    while (stack_size > 0) {
        StackFrame frame = stack[--stack_size];

        if (frame.state == STATE_START) {
            if (size >= capacity) {
                capacity = (capacity == 0) ? 4 : capacity * 2;
                result = (CommentNode**)realloc(result, capacity * sizeof(CommentNode*));
            }
            result[size++] = frame.node;

            if (stack_size >= stack_capacity) {
                stack_capacity *= 2;
                stack = (StackFrame*)realloc(stack, stack_capacity * sizeof(StackFrame));
            }
            stack[stack_size].node = frame.node;
            stack[stack_size].state = STATE_REPLIES_DONE;
            stack_size++;

            for (int i = frame.node->reply_count - 1; i >= 0; i--) {
                if (stack_size >= stack_capacity) {
                    stack_capacity *= 2;
                    stack = (StackFrame*)realloc(stack, stack_capacity * sizeof(StackFrame));
                }
                stack[stack_size].node = frame.node->replies[i];
                stack[stack_size].state = STATE_START;
                stack_size++;
            }
        }
    }

    free(stack);
    *returnSize = size;
    return result;
}

typedef struct NodeList {
    CommentNode* node;
    struct NodeList* next;
} NodeList;

NodeList* create_node_list(CommentNode* node) {
    NodeList* nl = (NodeList*)malloc(sizeof(NodeList));
    nl->node = node;
    nl->next = NULL;
    return nl;
}

void free_node_list(NodeList* list) {
    while (list) {
        NodeList* tmp = list;
        list = list->next;
        free(tmp);
    }
}

int count_comments_tail_helper(NodeList* nodes, int acc) {
    if (!nodes) return acc;
    CommentNode* node = nodes->node;
    NodeList* rest = nodes->next;
    NodeList* children = NULL;
    for (int i = node->reply_count - 1; i >= 0; i--) {
        NodeList* new_node = create_node_list(node->replies[i]);
        new_node->next = children;
        children = new_node;
    }
    if (children) {
        NodeList* tail = children;
        while (tail->next) tail = tail->next;
        tail->next = rest;
        rest = children;
    }
    free_node_list(nodes);
    return count_comments_tail_helper(rest, acc + 1);
}

int count_comments_tail(CommentNode* comment) {
    NodeList* start = create_node_list(comment);
    return count_comments_tail_helper(start, 0);
}

int count_comments_loop(CommentNode* comment) {
    int count = 0;
    CommentNode** stack = NULL;
    int stack_capacity = 0;
    int stack_size = 0;

    if (stack_size >= stack_capacity) {
        stack_capacity = (stack_capacity == 0) ? 4 : stack_capacity * 2;
        stack = (CommentNode**)realloc(stack, stack_capacity * sizeof(CommentNode*));
    }
    stack[stack_size++] = comment;

    while (stack_size > 0) {
        CommentNode* node = stack[--stack_size];
        count++;
        for (int i = 0; i < node->reply_count; i++) {
            if (stack_size >= stack_capacity) {
                stack_capacity *= 2;
                stack = (CommentNode**)realloc(stack, stack_capacity * sizeof(CommentNode*));
            }
            stack[stack_size++] = node->replies[i];
        }
    }
    free(stack);
    return count;
}

CommentNode* create_sample_thread() {
    CommentNode* c101 = create_comment(101, "Alice", "This recipe looks amazing!", "t1", 10);
    CommentNode* c201 = create_comment(201, "Bob", "I tried it last night!", "t2", 5);
    CommentNode* c301 = create_comment(301, "Alice", "What did you think?", "t3", 2);
    CommentNode* c401 = create_comment(401, "Bob", "It was delicious!", "t4", 8);
    CommentNode* c202 = create_comment(202, "Charlie", "Can I use olive oil instead?", "t5", 3);
    CommentNode* c302 = create_comment(302, "Alice", "Yes, that works too!", "t6", 1);

    add_reply(c101, c201);
    add_reply(c101, c202);
    add_reply(c201, c301);
    add_reply(c301, c401);
    add_reply(c202, c302);

    return c101;
}



int main() {
    CommentNode* root = create_sample_thread();

    int size1;
    CommentNode** flat_rec = flatten_recursive(root, &size1);
    printf("Recursive flatten (%d nodes):\n", size1);
    for (int i = 0; i < size1; i++) {
        printf("  %d: %.20s...\n", flat_rec[i]->comment_id, flat_rec[i]->content);
    }
    free(flat_rec);

    int size2;
    CommentNode** flat_iter = flatten_iterative(root, &size2);
    printf("\nIterative flatten (%d nodes):\n", size2);
    for (int i = 0; i < size2; i++) {
        printf("  %d: %.20s...\n", flat_iter[i]->comment_id, flat_iter[i]->content);
    }
    free(flat_iter);

    printf("\nLoop count: %d\n", count_comments_loop(root));
    printf("Tail recursive count: %d\n", count_comments_tail(root));

    free_comment_tree(root);
    return 0;
}

