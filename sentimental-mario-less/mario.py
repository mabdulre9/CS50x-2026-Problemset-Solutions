while True:
    height = input("Height: ")

    if not height.isdigit():
        continue

    height = int(height)

    if height > 8 or height < 1:
        continue

    for i in range(1,height+1):
        print(f'{" "*(height-i)}{"#" * i}')
    break   
