function bubble (input, len)
    isSorted = false
    while isSorted == false do
        isSorted = true
        for x = 1, len - 1, 1 do
            y = x + 1
            a = input[x]
            b = input[y]
            if a > b then
                isSorted = false
                temp = a
                input[x] = b
                input[y] = temp
            end
        end
    end
end

array = {2,5,1,0,7}
length = 5

bubble(array, length)

temp = array[1]
print(temp)
temp = array[2]
print(temp)
temp = array[3]
print(temp)
temp = array[4]
print(temp)
temp = array[5]
print(temp)