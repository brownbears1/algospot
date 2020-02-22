"""

1. 시작 주유소는 내 맘대로 선택할 수 있음.
2. 선택한 주유소에서 시작해 다시 되돌아 올 가스가 남아 있으면 시작한 주유소 인덱스를 리턴, 그렇지 않으면 -1 리턴
3. 선택한 주유소가 i면 i+1로 넘어가야 한다.
4. 다음 주유소로 넘어갈 때, 코스트는 현재 주유소 i의 코스트이다. (cost[i])

예제 1)
gas  = [1,2,3,4,5]
cost = [3,4,5,1,2]

주유소 0, 주유소 1, 주유소 2 번에서는 시작을 할 수 없다.

주유소 0에서 시작하면 가스는 1이 채워지는데 주유소 1로 넘어가기 위한 비용은 3이므로 X
주유소 1에서 시작하면 가스는 2가 채워지는데 주유소 2로 넘어가기 위한 비용은 4이므로 X
주유소 2에서 시작하면 가스는 3이 채워지는데 주유소 3로 넘어가기 위한 비용은 5이므로 X

그래서 시작할 주유소는 3 또는 4가 된다.

주유소 3에서 시작한 케이스는 릿코드에 있으니 제외

1) 주유소 4에서 시작. 0 + 5 = 5
2) 주유소 0으로 이동. 5 - 2 + 1 = 4
3) 주유소 1로 이동. 4 - 3 + 2 = 3
4) 주유소 2로 이동. 3 - 5 + 3 = 1
5) 주유소 3으로 이동. 1 - 5 + 4 = 0
6) 주유소 4로 이동하기 위한 비용은 1인데 현재 남아있는 가스는 0으로 갈 수 없음.

"""
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        length = len(gas)
        target = {}

        # gas - cost 가 0보다 크거나 같으면 이동할 수 있으므로 먼저 해당되는 index를 모두 찾는다.
        # list에 append보다 dictionary에 input하는 방식이 약 20% 정도 빠르다.
        # {인덱스: ((gas - cost), cost)}
        # {3: (3, 1), 4: (3, 2)}
        for i, (g, c) in enumerate(zip(gas, cost)):
            spend = g - c
            if spend >= 0:
                target[i] = spend, c

        # 위에서 만든 타겟에서 정렬을 한다.
        # 정렬 기준은 (주유소 - 비용)이 큰 순으로 내림차순 정렬.
        # 만약 같다면 인덱스가 작은 순으로 오름차순 정렬한다
        # 정렬을 한 다음, index는 key에 존재하므로 key 값만 list 타입으로 추출한다.
        target_indices = list(map(lambda x: x[0], sorted(target.items(), key=lambda x: (-x[1][0], x[1][1]))))

        for index in target_indices:
            # 시작 인덱스는 cost를 소모하지 않으므로 gas_tank에 가스를 충전한다.
            gas_tank = gas[index]
            is_valid = True
            # 다음 주유소에 넘어가도록 시작 인덱스를 1 증가시킨다.
            start_index = index + 1

            for _ in range(length):
                start_gas_index = start_index % length
                start_cost_index = (start_index - 1) % length

                # 다음 주유소에 넘어갈 수 있는지 남아 있는 가스와 소모되는 가스를 차감.
                gas_tank -= cost[start_cost_index]
                # 남아 있는 가스가 음수면, 다음 주유소로 갈 수 없으므로 종료한다.
                if gas_tank < 0:
                    is_valid = False
                    break

                # 가장 마지막에는 위 로지만 필요하나 아래 로직도 호출을 하게 된다. 조건문을 넣으나 안넣으나 결과에는 상관이 없어서 패스

                # 방문한 주유소에서 채울 수 있는 가스를 충전한다.
                gas_tank += gas[start_gas_index]
                start_index += 1

            if is_valid:
                return index

        return -1
