from typing import List, Set, Tuple, Dict
import uuid

"""
key: uuid v4 or created by themselves
value: list of tuple(user_id, unavailable time)
"""
room2timetable: Dict[str, List[Tuple[str, Tuple[int, int]]]] = dict()
def get_available_time(room_id: str) -> List[Tuple[int, int]]:
    busy_hours_days: Set[int] = {item[1] for item in room2timetable[room_id]}
    available_hours: List[Tuple[int, int]] = []

    find_days = [[],[],[],[],[],[],[]]
    result_days = [[], [], [], [], [], [], []]

    for i in list(busy_hours_days):
        find_days[i[1]].append(i[0])

    for j in range(7):
        for start_hour in range(24):
            if start_hour not in find_days[j]:
                end_hour = start_hour
                while end_hour < 23 and end_hour + 1 not in find_days[j]:
                    end_hour += 1
                result_days[j].append((start_hour, end_hour))

    return result_days


def post_item(room_id: str, user_name: str, time: int, day: int) -> None:
    room2timetable.setdefault(room_id, []).append((user_name, (time, day)))


def create_new_room() -> None:
    room_id = str(uuid.uuid4())
    room2timetable[room_id] = []


def main():
    if __name__ == '__main__':
        post_item('ID1', 'daniel', 9)
        post_item('ID1', 'ted', 9)
        post_item('ID1', 'ted', 10)
        post_item('ID1', 'ted', 11)

        print(room2timetable)
        # 가능한 시간대 출력
        print(get_available_time('ID1'))


main()
