class ReverseQueue:
    def __init__(self, max_size=5):
        self.queue = []
        self.max_size = max_size

    # Check if the queue is empty
    def is_empty(self):
        return len(self.queue) == 0

    # Check if the queue is full
    def is_full(self):
        return len(self.queue) == self.max_size

    # Enqueue an element to the front (reverse behavior)
    def enqueue(self, data):
        if self.is_full():
            return
        self.queue.insert(0, data)  # Insert at the front (index 0)

    # Dequeue an element from the front (like stack pop behavior)
    def dequeue(self):
        if self.is_empty():
            return None
        removed_item = self.queue.pop(0)  # Remove from the front (index 0)
        return removed_item

    # Remove the rear element (last element in the list)
    def remove_rear(self):
        if self.is_empty():
            return None
        removed_item = self.queue.pop(-1)  # Remove from the rear (last element)
        return removed_item

    # Get the front element without removing it
    def front(self):
        if self.is_empty():
            return None
        return self.queue[0]

    # Get the rear element without removing it
    def rear(self):
        if self.is_empty():
            return None
        return self.queue[-1]

    # Get the current size of the queue
    def size(self):
        return len(self.queue)


    # Traverse the queue without removing elements
    def traverse(self):
        if self.is_empty():
            return []
        else:
            arr = [item for item in self.queue]
            return arr


# # Test the ReverseQueue with size 10
# reverse_queue = ReverseQueue(max_size=10)

# # Enqueue elements
# reverse_queue.enqueue(1)
# reverse_queue.enqueue(2)
# reverse_queue.enqueue(3)
# reverse_queue.display()  # Output: Queue: [3, 2, 1]

# # Remove the rear element
# reverse_queue.remove_rear()  # Output: Removed rear: 1
# reverse_queue.display()  # Output: Queue: [3, 2]

# # Traverse the queue without removing elements
# reverse_queue.traverse()
# # Output:
# # Traversing the queue:
# # Element at position 0: 3
# # Element at position 1: 2

# # Dequeue elements
# reverse_queue.dequeue()  # Output: Dequeued: 3
# reverse_queue.display()  # Output: Queue: [2]

# # Check the front and rear elements
# print(f"Front element: {reverse_queue.front()}")  # Output: Front element: 2
# print(f"Rear element: {reverse_queue.rear()}")    # Output: Rear element: 2

# # Check the size of the queue
# print(f"Size of the queue: {reverse_queue.size()}")  # Output: Size of the queue: 1
# class ReverseQueue:
#     def __init__(self, max_size=10):
#         self.queue = []
#         self.max_size = max_size

#     # Check if the queue is empty
#     def is_empty(self):
#         return len(self.queue) == 0

#     # Check if the queue is full
#     def is_full(self):
#         return len(self.queue) == self.max_size

#     # Enqueue an element to the front (reverse behavior)
#     def enqueue(self, data):
#         if self.is_full():
#             print("Queue is full!")
#             return
#         self.queue.insert(0, data)  # Insert at the front (index 0)
#         print(f"Enqueued: {data}")

#     # Dequeue an element from the front (like stack pop behavior)
#     def dequeue(self):
#         if self.is_empty():
#             print("Queue is empty!")
#             return None
#         removed_item = self.queue.pop(0)  # Remove from the front (index 0)
#         print(f"Dequeued: {removed_item}")
#         return removed_item

#     # Remove the rear element (last element in the list)
#     def remove_rear(self):
#         if self.is_empty():
#             print("Queue is empty!")
#             return None
#         removed_item = self.queue.pop(-1)  # Remove from the rear (last element)
#         print(f"Removed rear: {removed_item}")
#         return removed_item

#     # Get the front element without removing it
#     def front(self):
#         if self.is_empty():
#             print("Queue is empty!")
#             return None
#         return self.queue[0]

#     # Get the rear element without removing it
#     def rear(self):
#         if self.is_empty():
#             print("Queue is empty!")
#             return None
#         return self.queue[-1]

#     # Get the current size of the queue
#     def size(self):
#         return len(self.queue)

#     # Display the queue
#     def display(self):
#         if self.is_empty():
#             print("Queue is empty!")
#         else:
#             print("Queue:", self.queue)

#     # Traverse the queue without removing elements
#     def traverse(self):
#         if self.is_empty():
#             print("Queue is empty!")
#         else:
#             print("Traversing the queue:")
#             for index, item in enumerate(self.queue):
#                 print(f"Element at position {index}: {item}")


# # Test the ReverseQueue with size 10
# reverse_queue = ReverseQueue(max_size=10)