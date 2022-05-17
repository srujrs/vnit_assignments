import sys 

list = [int(x) for x in sys.argv[1:]]

nums = list[1:]

nums.sort()

div_list = [1]

for i in range(2, int(nums[0]**0.5) + 1):
    com_div = True

    if nums[0] % i == 0:
        for j in range(1, list[0]):
            if nums[j] % i != 0:
                com_div = False
                break 
        if com_div:
            div_list.append(i)

        com_div = True

        other_div = nums[0] // i

        if other_div != i:
            for j in range(1, list[0]):
                if nums[j] % other_div != 0:
                    com_div = False
                    break 
            if com_div:
                div_list.append(other_div)

div_list.sort()

size = len(div_list)

for i in range(size - 1):
    print(div_list[i], end=" ")

print(div_list[size - 1], end="")