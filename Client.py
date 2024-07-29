import socket
import pickle


def input_matrix():
    matrix = []
    print("Введите элементы матрицы (по строкам), разделенные пробелом:")
    while True:
        row = input().strip()
        if not row:
            break
        matrix.append(list(map(int, row.split())))
    return matrix

def main():
    matrix = input_matrix()
    tasks = [{'start_i': i, 'start_j': j, 'size': 2} for i in range(len(matrix) - 1) for j in range(len(matrix[0]) - 1)]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 12345))

    data = {'matrix': matrix, 'tasks': tasks}
    client_socket.send(pickle.dumps(data))

    results_data = client_socket.recv(4096)
    results = pickle.loads(results_data)

    max_sum = float('-inf')
    max_submatrix = None

    for result in results:
        if result['max_sum'] > max_sum:
            max_sum = result['max_sum']
            max_submatrix = result['max_submatrix']

    print("Подматрица с максимальной суммой:")
    for row in max_submatrix:
        print(row)
    print("Сумма элементов в подматрице:", max_sum)

    client_socket.close()

if __name__ == "__main__":
    main()


#norm