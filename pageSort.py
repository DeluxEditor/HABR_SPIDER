# Вычисление метрики по расположению искомых слов на странице (от начала)
def location_score(urlids):
    # Начальная инициализация словаря с парой url id : заранее большое значение. Потом это значение заменится на меньшее
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

    # Начальная инициализация словаря с парой url id : заранее большое значение. Потом это значение заменится на меньшее
    distance_scoredict = {}
    for combination in urlids:
        distance_scoredict[combination[0]] = 1000000

    # Перебираем каждую комбинацию и пытаемся перезаписать метрику в словарь (вычисленная < уже записанной)
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


# Нормализация метрики
def score_normalization(scoredict, desc_normalize=True):
    # Нормализация по максимуму
    if desc_normalize:
        maxval = max(scoredict.values())
        for (key, val) in scoredict.items():
            normalized_val = val / maxval
            scoredict = normalized_val
        return scoredict

    # Нормализация по минимуму
    minval = min(scoredict.values())
    for (key, val) in scoredict.items():
        normalized_val = minval / val
        scoredict[key] = normalized_val
    return scoredict
