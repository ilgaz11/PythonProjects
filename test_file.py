def convert_to_decimal(num: str):
    power = len(num) - 1
    decimal = 0
    for digit in num:
        decimal += int(digit) * 2**power
        power -= 1
    return decimal

def binary_sum(a: str, b:str):
    dec1 = convert_to_decimal(a)
    dec2 = convert_to_decimal(b)
    sum = dec1 + dec2
    binary = ""
    while sum > 0:
        #print(sum)
        remainder = sum % 2
        sum = sum // 2
        #print(sum, remainder)
        binary += str(remainder)
    if not binary:
        binary = "0"
    return binary[::-1]

my_list = [1, 2, 3, 4, 5, 6]
my_list[:4] = [13]
#print(my_list)

integers = [1, 2, 3, 4, 5]
def print_with_pipes(lst: list):
    for i in range(len(lst)):
        lst[i] = str(lst[i])

    print(' | '.join(lst))

def print_list(lst):
    for sublist in lst:
        for item in sublist:
            print(item)

#does not work
def binary_search(nums: list, target: int):
        index = len(nums) // 2
        final_index = 0
        while nums[index] != target:
            if nums[index] < target:
                nums = nums[index: ]
                final_index += index
            else:
                nums = nums[: index]
            index = len(nums) // 2
            #print(index)
        return final_index


print(binary_search([0,1,2,3,4,5,6,7], 2))
lst = [1, 2, 3, 4]
k = lst.index(2)
print(k)








