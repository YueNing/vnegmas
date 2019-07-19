def get_sum(data):
    sum = 0
    for index, value in enumerate(data):
        sum = sum + value
        yield index, sum

def process_average(data):
    sum = get_sum(data)
    average = []
    for _ in range(len(data)):
        index, value = next(sum)
        average.append(value / (index+1))
    return average

def process_average_sim(data):
    average = []
    for index, k in enumerate(data):
        sum = 0
        for _ in range(index):
            sum += k
            aver = sum / (index+1)
            average.append(aver)
    return average

if __name__ == "__main__":
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    print(process_average(data))