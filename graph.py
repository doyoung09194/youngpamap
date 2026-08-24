import heapq
from collections import defaultdict

DONGAM_FLOORS = ['B', '1', '2', '3', '4', '5']
YEONGPA_FLOORS = ['B', '1', '2', '3', '4', '5']

DONGAM_ROOMS = {
    'B': [
        ('동암B01','소강당'),('동암B02','동암B02'),('동암B03','동암B03'),
        ('동암B04','동암B04'),('동암B05','동암B05'),('동암B06','창고'),('동암B07','동암B07'),
        ('동암B08','다목적실5'),('동암B09','다목적실5(연결)'),('동암B10','다목적실4'),('필표실','필표실'),
    ],
    '1': [
        ('동암101','음악실'),('동암102','중학교 교무실'),('동암103','중학교 교무실'),
        ('동암104','Wee클래스'),('동암105','회의실'),('동암106','보건실'),('동암107','2HB 커리어존'),
        ('동암108','2HB'),('동암109','2HB(하)'),('동암110','과학실(생명)'),
    ],
    '2': [
        ('동암201','컴퓨터실'),('동암202','동암202'),('동암203','동암203'),
        ('동암204','외국어실A'),('동암205','제1교무실'),('동암206','공용6'),('동암207','제1교무실'),
        ('동암208','1-1'),('동암209','1-2'),('동암210','제2교무실'),
    ],
    '3': [
        ('동암301','음악실'),('동암302','중'),('동암303','명상실'),
        ('동암304','진로연구실'),('동암305','제3교무실'),('동암306','공용6실'),('동암307','제3교무실'),
        ('동암308','공용4'),('동암309','공용3'),('동암310','특별실A'),
    ],
    '4': [
        ('동암401','과학실(물리)'),('동암402','3-7'),('동암403','3-8'),
        ('동암404','3-9'),('동암405','설렘(ON)실'),('동암406','3-10'),('동암407','방송실'),
        ('동암408','3-11'),('동암409','공용2'),('동암410','제4교무실'),
    ],
    '5': [
        ('동암501','과학실(지학)'),('동암502','3-6'),('동암503','3-5'),
        ('동암504','3-4'),('동암505','3HB'),('동암506','3-3'),('동암507','자기주도학습실(3학년)'),
        ('동암508','3-2'),('동암509','3-1'),('동암510','과학실(화학)'),
    ],
}
DONGAM_STAIR_AFTER = {'L': 2, 'M': 6}

YEONGPA_ROOMS = {
    'B': [
        ('영파B01','급식실'),
    ],
    '1': [
        ('영파103','성적처리실(동사실)'),('영파104','회의실'),('영파105','교장실'),('영파106','회의실'),
        ('영파107','행정실(고)'),('영파108','문서관리실'),('영파109','이사장실'),('영파110','문서관리실'),('영파111','행정실(중)'),
        ('영파113','관리실'),('영파114','공용7'),('영파115','미술실A'),('영파116','미술실B'),
        ('영파117','공용8'),('영파118','특별실B(다목적실1)'),('영파119','음악실A'),('영파120','특별실B(다목적실1)'),('영파121','음악실B'),('영파122','관리실'),
    ],
    '2': [
        ('영파201','교사연수실A'),('영파202','1-3'),('영파203','수업연구실'),
        ('영파204','1-4'),('영파205','1-11'),('영파206','1-5'),('영파207','1-10'),
        ('영파208','1-6'),('영파209','1-9'),('영파210','1-7'),('영파211','1-8'),
        ('영파212','도서실'),('영파213','영파213'),('영파214','도서실'),('영파215','도서실'),
        ('영파216','도서실'),('영파217','도서실'),('영파218','도서실'),('영파219','도서실'),('영파220','도서실'),('영파221','교사연수실B'),
    ],
    '3': [
        ('영파301','2-6'),('영파302','2-7'),('영파303','수업연구실(3층)'),
        ('영파304','2-8'),('영파305','2-11'),('영파306','2-9'),('영파307','2-10'),('영파308','행사준비실'),
        ('창고_3층','창고'),('강당_3층','강당'),
    ],
    '4': [
        ('영파401','공용1'),('영파402','2-1'),('영파403','교사연구실'),
        ('영파404','2-2'),('영파405','2-5'),('영파406','2-3'),('영파407','2-4'),('영파408','자기주도학습실(2학년)'),
        ('다목적실2','다목적실2'),
    ],
    '5': [
        ('좌석_5층','좌석'),('다목적실3','다목적실3'),
    ],
}
YEONGPA_STAIR_AFTER = {'M': 10}


class SchoolGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.node_info = {}
        self._build()

    def _add(self, u, v, w, d1, d2):
        self.graph[u].append((v, w, d1))
        self.graph[v].append((u, w, d2))

    def _fn(self, f):
        return -1 if f == 'B' else int(f)

    def _build(self):
        for floor, rooms in DONGAM_ROOMS.items():
            nodes = [r[0] for r in rooms]
            for rid, rname in rooms:
                self.node_info[rid] = rname
            sL = f'동암_계단L_{floor}'
            sM = f'동암_계단M_{floor}'
            sR = f'동암_계단R_{floor}'
            for s in [sL, sM, sR]:
                self.node_info[s] = s
            corridor = []
            for i, rid in enumerate(nodes):
                corridor.append(rid)
                if i == DONGAM_STAIR_AFTER.get('L', -1):
                    corridor.append(sL)
                if i == DONGAM_STAIR_AFTER.get('M', -1):
                    corridor.append(sM)
            corridor.append(sR)
            for i in range(len(corridor) - 1):
                self._add(corridor[i], corridor[i+1], 1, '복도 이동', '복도 이동')

        for stair in ['L', 'M', 'R']:
            for i in range(len(DONGAM_FLOORS) - 1):
                f1, f2 = DONGAM_FLOORS[i], DONGAM_FLOORS[i+1]
                n1 = f'동암_계단{stair}_{f1}'
                n2 = f'동암_계단{stair}_{f2}'
                diff = abs(self._fn(f2) - self._fn(f1))
                self._add(n1, n2, diff*3,
                    f'계단 올라가기({f1}→{f2}층)',
                    f'계단 내려가기({f2}→{f1}층)')

        for floor, rooms in YEONGPA_ROOMS.items():
            nodes = [r[0] for r in rooms]
            for rid, rname in rooms:
                self.node_info[rid] = rname
            sM = f'영파_계단M_{floor}'
            sR = f'영파_계단R_{floor}'
            for s in [sM, sR]:
                self.node_info[s] = s
            corridor = []
            for i, rid in enumerate(nodes):
                corridor.append(rid)
                if i == YEONGPA_STAIR_AFTER.get('M', -1):
                    corridor.append(sM)
            corridor.append(sR)
            for i in range(len(corridor) - 1):
                self._add(corridor[i], corridor[i+1], 1, '복도 이동', '복도 이동')

        for stair in ['M', 'R']:
            for i in range(len(YEONGPA_FLOORS) - 1):
                f1, f2 = YEONGPA_FLOORS[i], YEONGPA_FLOORS[i+1]
                n1 = f'영파_계단{stair}_{f1}'
                n2 = f'영파_계단{stair}_{f2}'
                self._add(n1, n2, 3,
                    f'계단 올라가기({f1}→{f2}층)',
                    f'계단 내려가기({f2}→{f1}층)')

        for floor in ['1','2','3','4','5']:
            self._add(f'동암_계단R_{floor}', f'영파_계단M_{floor}', 2,
                      '영파관으로 이동', '동암관으로 이동')

    def dijkstra(self, start, end):
        dist = {start: 0}
        prev = {start: (None, '')}
        pq = [(0, start)]
        while pq:
            cost, u = heapq.heappop(pq)
            if cost > dist.get(u, float('inf')): continue
            if u == end: break
            for v, w, desc in self.graph[u]:
                nc = cost + w
                if nc < dist.get(v, float('inf')):
                    dist[v] = nc
                    prev[v] = (u, desc)
                    heapq.heappush(pq, (nc, v))
        if end not in dist:
            return None, []
        path, cur = [], end
        while cur:
            path.append(cur)
            cur = prev[cur][0]
        path.reverse()
        return dist[end], path

    def _stair_label(self, node):
        if '계단L' in node: return '왼쪽 계단'
        if '계단M' in node: return '가운데 계단'
        if '계단R' in node: return '오른쪽 계단'
        return '계단'

    def _floor_of(self, node):
        last = node.split('_')[-1]
        if last == 'B': return -1
        try: return int(last)
        except: return None

    def describe_path(self, path):
        if not path: return "경로를 찾을 수 없습니다."
        if len(path) == 1: return "현재 위치가 목적지입니다."

        sname = self.node_info.get(path[0], path[0])
        ename = self.node_info.get(path[-1], path[-1])
        lines = [
            f"📍 출발: {sname} ({path[0]})",
            f"🏁 도착: {ename} ({path[-1]})",
            "─" * 32,
        ]
        i, step = 0, 1
        while i < len(path) - 1:
            cur, nxt = path[i], path[i+1]
            if '계단' in nxt and '계단' not in cur:
                stair_label = self._stair_label(nxt)
                j = i + 1
                stair_kind = nxt.split('_계단')[1].split('_')[0]
                while j < len(path)-1 and '계단' in path[j] and f'_계단{stair_kind}_' in path[j]:
                    j += 1
                f1 = self._floor_of(path[i+1])
                f2 = self._floor_of(path[j-1]) if '계단' in path[j-1] else self._floor_of(path[j])
                if f1 is not None and f2 is not None and f1 != f2:
                    diff = f2 - f1
                    direction = '올라갑니다' if diff > 0 else '내려갑니다'
                    lines.append(f"  {step}. {stair_label}을 이용해 {abs(diff)}층 {direction}.")
                else:
                    lines.append(f"  {step}. {stair_label} 방향으로 이동합니다.")
                step += 1
                i = j
                continue
            if '계단R' in cur and '계단M' in nxt:
                if cur.startswith('동암'):
                    lines.append(f"  {step}. 연결 통로를 통해 영파관으로 이동합니다.")
                else:
                    lines.append(f"  {step}. 연결 통로를 통해 동암관으로 이동합니다.")
                step += 1
                i += 1
                continue
            if '계단' in cur and '계단' in nxt:
                i += 1; continue
            if '계단' in cur and '계단' not in nxt:
                i += 1; continue
            if nxt != path[-1]:
                i += 1; continue
            dest_name = self.node_info.get(nxt, nxt)
            lines.append(f"  {step}. {dest_name}({nxt})에 도착합니다. ✅")
            step += 1
            i += 1
        lines.append("─" * 32)
        return '\n'.join(lines)

    def get_all_rooms(self):
        """검색용 전체 교실 목록 반환"""
        rooms = []
        for rid, rname in self.node_info.items():
            if '계단' not in rid:
                rooms.append({'id': rid, 'name': rname})
        return sorted(rooms, key=lambda x: x['id'])