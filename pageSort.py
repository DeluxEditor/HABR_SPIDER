# Вычисление метрики по расположению искомых слов на странице (от начала)
def location_score(urlids):
    # Инициализация словаря с парой url id : заранее большое значение
    location_scoredict = {}
    for combination in urlids:
        location_scoredict[combination[0]] = 1000000

    # Суммируем положения искомых слов на url и пытаемся записать в словарь(вычисленная < уже записанной)
    for combination in urlids:
        score = sum(combination[1:])    # 1 элемент списка всегда url id
        if score < location_scoredict[combination[0]]:
            location_scoredict[combination[0]] = score
    location_scoredict = score_normalization(location_scoredict, desc_normalize=False)
    print(f"Метрика расположения искомых слов: \n{location_scoredict}\n")
    return location_scoredict


# Вычисление метрики по расстоянию между искомыми словами на странице
def distance_score(urlids):
    if len(urlids[0]) < 3:  # Если меньше двух слов в комбинации - метрику не считаем (1 элмемент всегда url id)
        return None

    # Инициализация словаря с парой url id : заранее большое значение
    distance_scoredict = {}
    for combination in urlids:
        distance_scoredict[combination[0]] = 1000000

    # Перебираем каждую комбинацию и пытаемся записать в словарь (вычисленная < уже записанной)
    for combination in urlids:
        score = 0
        for idx in range(len(combination)):
            if idx == 0:
                continue
            score += abs(combination[1] - combination[idx])
        if score < distance_scoredict[combination[0]]:
            distance_scoredict[combination[0]] = score
    distance_scoredict = score_normalization(distance_scoredict, desc_normalize=False)
    print(f"Метрика расстояния между искомыми словами: \n{distance_scoredict}\n")
    return distance_scoredict


# Вычисление метрики по количеству вхождения слов на странице
def frequency_score(urlids):
    # Инициализация словаря с парой url id : нулевое значение
    frequency_scoredict = {}
    for combination in urlids:
        frequency_scoredict[combination[0]] = 0

    # Проверяем, если url id == key, то инкрементируем значение словаря
    for combination in urlids:
        for key, value in frequency_scoredict.items():
            if combination[0] == key:
                frequency_scoredict[key] = value + 1
    frequency_scoredict = score_normalization(frequency_scoredict, desc_normalize=True)
    print(f"Метрика частоты искомых слов: \n{frequency_scoredict}\n")
    return frequency_scoredict


# Нормализация метрики
def score_normalization(scoredict, desc_normalize=True):
    # Нормализация по максимуму
    if desc_normalize:
        maxval = max(scoredict.values())
        for (key, val) in scoredict.items():
            normalized_val = round(val / maxval, 4)
            scoredict[key] = normalized_val
        return scoredict

    # Нормализация по минимуму
    minval = min(scoredict.values())
    for (key, val) in scoredict.items():
        normalized_val = round(minval / val, 4)
        scoredict[key] = normalized_val
    return scoredict
