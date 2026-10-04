from collections import defaultdict


# 1.
moscow = {201, 202, 203, 204}
kazan = {203, 204, 205, 206}

print('any city:', moscow & kazan)
print('only moscow:', moscow - kazan)
print('only kazan:', kazan - moscow)
print('count goods:', len(moscow | kazan))

print('\n=================================\n')

# 2.

queries = [
    "чехол",
    "iphone",
    "чехол",
    "наушники",
    "iphone",
    "iphone",
    "кабель",
    "чехол",
    "iphone",
]

print('count request:', len(queries))
stat_request = {}
for i in queries:
    stat_request[i] = 1 + stat_request.get(i, 0)
print('every request:', stat_request)
ma = max(stat_request.values())
print('max request:', [i for i in stat_request if stat_request[i] == ma])
print('part max:', max(stat_request.values()) / sum(stat_request.values()))
print('rare request:', [i for i in stat_request if stat_request[i] == 1])

print('\n=================================\n')


# 3.

orders = [
    {"id": 1, "buyer": "anya", "status": "delivered", "amount": 900},
    {"id": 2, "buyer": "boris", "status": "returned", "amount": 4_500},
    {"id": 3, "buyer": "anya", "status": "delivered", "amount": 1_500},
    {"id": 4, "buyer": "vera", "status": "delivered", "amount": 3_200},
    {"id": 5, "buyer": "boris", "status": "delivered", "amount": 700},
    {"id": 6, "buyer": "gleb", "status": "returned", "amount": 2_100},
]
print('amount return:', sum(i['amount'] for i in orders
                            if i['status'] == 'returned'))
print('return buyers:', set(i['buyer'] for i in orders
                            if i['status'] == 'returned'))
order_del = [i for i in orders if i['status'] == 'delivered']
print('order delivered:', len(order_del))
print('mean amount del', sum(i['amount'] for i in order_del) / len(order_del))

print('\n=================================\n')

# 4.

days = [
    {"day": "пн", "orders": 20, "revenue": 40_000, "returns": 2},
    {"day": "вт", "orders": 16, "revenue": 19_200, "returns": 4},
    {"day": "ср", "orders": 25, "revenue": 55_000, "returns": 1},
    {"day": "чт", "orders": 10, "revenue": 12_000, "returns": 3},
    {"day": "пт", "orders": 30, "revenue": 48_000, "returns": 3},
]

print('total revenue:', sum(i['revenue'] for i in days))
ma = max(i['revenue'] for i in days)
print('days with max revenue:', [i['day'] for i in days if i['revenue'] == ma])
print('mean revenue:', {i['day']: i['revenue']/i['orders'] for i in days})
print('>20% returns:', [i['day'] for i in days
                        if i['returns'] / i['orders'] > 0.2])

print('\n=================================\n')


# 5.

reviews = [
    {"id": 1, "product": "Чехол", "stars": 5},
    {"id": 1, "product": "Чехол", "stars": 3},
    {"id": 1, "product": "Чехол", "stars": 4},
    {"id": 2, "product": "Наушники", "stars": 2},
    {"id": 2, "product": "наушники", "stars": 2},
    {"id": 2, "product": "НАУШНИКИ", "stars": 5},
    {"id": 3, "product": "Планшет", "stars": 5},
    {"id": 4, "product": "Колонка", "stars": 4},
    {"id": 4, "product": "Колонка", "stars": 4},
    {"id": 5, "product": "Кабель", "stars": 1},
]

for i in reviews:
    i['product'] = i['product'].lower()

grouped_reviews = defaultdict(list)
for i in reviews:
    grouped_reviews[i['product']].append(i['stars'])
mean_reviews = grouped_reviews.copy()
for i in mean_reviews:
    mean_reviews[i] = sum(mean_reviews[i]) / len(mean_reviews[i])
print('mean reviews:', mean_reviews)
print('bad good with 2 reviews:', min(i for i in mean_reviews
                                      if len(grouped_reviews[i]) >= 2))
count_bad_review = sum(1 if i['stars'] <= 2 else 0 for i in reviews)
print('count bad review', count_bad_review)
print('part bad review:', count_bad_review / len(reviews))
