
from random import choice


# (dx, dy)
DIRECTIONS = (
    (1, 0),    # 오른쪽
    (-1, 0),   # 왼쪽
    (0, 1),    # 아래
    (0, -1),   # 위
)


def is_connected_to_core(shape):
    """모든 몸통이 중심핵 (0, 0)과 연결되어 있는지 확인"""

    shape_set = set(shape)

    # 중심핵은 반드시 존재
    if (0, 0) not in shape_set:
        return False

    visited = {(0, 0)}
    stack = [(0, 0)]

    while stack:
        x, y = stack.pop()

        for dx, dy in DIRECTIONS:
            next_pos = (x + dx, y + dy)

            if next_pos in shape_set and next_pos not in visited:
                visited.add(next_pos)
                stack.append(next_pos)

    return len(visited) == len(shape_set)


def make_shape(parent_shape):
    """
    부모의 shape를 받아 돌연변이를 일으킨
    새로운 shape를 반환한다.

    좌표는 항상 (x, y) 형식이다.
    """

    shape = list(parent_shape)

    # --------------------------------
    # 몸통 추가
    # --------------------------------

    if choice((True, False)):

        shape_set = set(shape)
        possible = set()

        # 기존 몸통의 상하좌우에 붙일 수 있는 위치 찾기
        for x, y in shape:

            for dx, dy in DIRECTIONS:

                new_pos = (x + dx, y + dy)

                if new_pos not in shape_set:
                    possible.add(new_pos)

        # 붙일 수 있는 위치가 있으면 하나 추가
        if possible:
            shape.append(choice(tuple(possible)))

    # --------------------------------
    # 몸통 삭제
    # --------------------------------

    else:

        # 중심핵 (0, 0)은 삭제하지 않음
        removable = []

        for pos in shape:

            if pos == (0, 0):
                continue

            # 일단 해당 몸통을 제거해봄
            test_shape = shape.copy()
            test_shape.remove(pos)

            # 중심핵에서 모든 몸통이 연결되어 있는지 확인
            if is_connected_to_core(test_shape):
                removable.append(pos)

        # 삭제 가능한 몸통 중 하나를 랜덤으로 삭제
        if removable:
            remove_pos = choice(removable)
            shape.remove(remove_pos)

    # 새로운 shape 반환
    return tuple(shape)

