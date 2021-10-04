from pymongo import MongoClient

sal = float(input(f'Введите зарплату в руб.:'))
sal_val = sal / 75
PY_COL = MongoClient('localhost', 27017).client['hh_db'].python
find_vac = PY_COL.find({'$or':
                            [{'cur': 'руб', '$or':
                                [{'sal_from': {'$gt': sal}},
                                 {'sal_to': {'$gt': sal}}]},
                             {'cur': 'USD', '$or':
                                 [{'sal_from': {'$gt': sal_val}},
                                  {'sal_to': {'$gt': sal_val}}]}]})

print(*find_vac, sep='\n')


