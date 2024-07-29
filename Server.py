import socket
import pickle

def calculate_submatrix(matrix, start_i, start_j, size):
    submatrix = [row[start_j:start_j + size] for row in matrix[start_i:start_i + size]]
    max_sum = sum(sum(row) for row in submatrix)
    return submatrix, max_sum

def collect_results(matrix, results):
    print("Результаты:")
    for result in results:
        start_i, start_j, size = result['start_i'], result['start_j'], result['size']
        max_submatrix, max_sum = result['max_submatrix'], result['max_sum']
        print(f"Подматрица с максимальной суммой ({size}x{size}) начиная с позиции ({start_i}, {start_j}):")
        for row in max_submatrix:
            print(row)
        print("Сумма элементов в подматрице:", max_sum)
        print()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(5)

    print("Вычислительный узел запущен.")

    try:
        while True:
            client_socket, address = server_socket.accept()
            print(f"Подключение получено от {address}")

            data = client_socket.recv(1024)
            if not data:
                continue

            data = pickle.loads(data)
            matrix = data['matrix']
            matrix_size = len(matrix)
            max_submatrix_size = min(matrix_size, matrix_size)  # Максимальный размер подматрицы

            results = []
            for size in range(2, max_submatrix_size + 1):
                for start_i in range(matrix_size - size + 1):
                    for start_j in range(matrix_size - size + 1):
                        max_submatrix, max_sum = calculate_submatrix(matrix, start_i, start_j, size)
                        results.append({
                            'start_i': start_i,
                            'start_j': start_j,
                            'size': size,
                            'max_submatrix': max_submatrix,
                            'max_sum': max_sum
                        })

            client_socket.send(pickle.dumps(results))
            collect_results(matrix, results)
            client_socket.close()

    except KeyboardInterrupt:
        print("Сервер остановлен.")
        server_socket.close()

if __name__ == "__main__":
    main()
