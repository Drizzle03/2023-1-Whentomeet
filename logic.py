from typing import List, Set, Tuple, Dict
import uuid

"""
key: uuid v4 or created by themselves
value: list of tuple(user_id, unavailable time)
"""
room2timetable: Dict[str, List[Tuple[str, int]]] = dict()


def get_available_time(room_id: str) -> List[Tuple[int, int]]:
    busy_hours: Set[int] = {item[1] for item in room2timetable[room_id]}
    available_hours: List[Tuple[int, int]] = []

    for start_hour in range(24):
        if start_hour not in busy_hours:
            end_hour = start_hour
            while end_hour < 23 and end_hour + 1 not in busy_hours:
                end_hour += 1
            available_hours.append((start_hour, end_hour))

    return available_hours


def post_item(room_id: str, user_name: str, time: int) -> None:
    room2timetable.setdefault(room_id, []).append((user_name, time))


def create_new_room() -> None:
    room_id = str(uuid.uuid4())
    room2timetable[room_id] = []


def main():
    if __name__ == '__main__':
        post_item('ID1', 'daniel', 9)
        post_item('ID1', 'ted', 10)

        post_item('ID2', 'user1', 10)
        post_item('ID2', 'user2', 11)
        post_item('ID2', 'user3', 12)

        print(room2timetable)

        # 가능한 시간대 출력
        print(get_available_time('ID1'))
        print(get_available_time('ID2'))


main()
