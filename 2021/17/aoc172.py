from typing import Tuple, List

Target = Tuple[int,int,int,int] # min_x, min_y, max_x, max_y

def find_xs(target: Target) -> List[int]:
    max_x = target[2]
    initial_xs = []

    for initial_x in range(max_x+1):
        cur_x_velocity = initial_x
        cur_x_pos = 0
        while cur_x_velocity > 0 and cur_x_pos <= max_x:
            cur_x_pos += cur_x_velocity
            cur_x_velocity -= 1 # Don't care about negatives as they are not relevant at this target.
            if target[0] <= cur_x_pos <= target[2]: #in target
                initial_xs.append(initial_x)
                break

    return initial_xs

def does_it_hit(initial_x: int, initial_y: int, target: Target) -> bool:
    def past_target() -> bool:
        return cur_x_pos > target[2] or cur_y_pos < target[3]
    def in_target() -> bool:
        return target[0] <= cur_x_pos <= target[2] and target[1] >= cur_y_pos >= target[3]

    cur_x_pos, cur_y_pos = initial_x, initial_y
    x_velocity, y_velocity = initial_x, initial_y

    while not past_target():
        if in_target():
            return True

        if x_velocity > 0:
            x_velocity -= 1
        elif x_velocity < 0:
            x_velocity += 1

        y_velocity -= 1

        cur_x_pos += x_velocity
        cur_y_pos += y_velocity

    return False

def main():
    target: Target = (139,-89,187,-148)
    max_y = 147 #from first part
    initial_xs = find_xs(target)

    count = 0
    for x in initial_xs:
        for y in range(target[3],max_y+1):
            if does_it_hit(x,y,target):
                count += 1

    print(count)

if __name__ == "__main__":
    main()
