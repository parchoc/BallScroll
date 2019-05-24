from PIL import ImageDraw, Image


def cmp(a, b):
    return (a > b) - (a < b)


codeList = [6, 7, 8, 5, 0, 1, 4, 3, 2]
pointsList = [
    (0, 0),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1)

]


def getDirection(x1, y1, x2, y2):
    dx = cmp(x2, x1)
    dy = cmp(y2, y1)
    hash_key = 3*dy + dx + 4

    return codeList[hash_key]


def codeToPoints(codes_list):
    points = [(0, 0)]
    min_x = 0
    min_y = 0
    for code in codes_list:
        points.append((points[-1][0] + pointsList[code][0], points[-1][1] + pointsList[code][1]))
        if points[-1][0] < min_x:
            min_x = points[-1][0]
        if points[-1][1] < min_y:
            min_y = points[-1][1]

    if (min_x < 0) or (min_y < 0):
        for i in range(len(points)):
            points[i] = (points[i][0] + abs(min_x), points[i][1] + abs(min_y))

    return points


def pointsToimage(points):
    width = 0
    height = 0
    for point in points:
        if point[0] > width:
            width = point[0]
        if point[1] > height:
            height = point[1]
    image = Image.new('1', (width+1, height+1), 1)
    drawer = ImageDraw.Draw(image)
    drawer.point(points, 0)

    return image


def fileToImage(path, name='image.jpg'):
    try:
        with open(path, 'r') as file:
            code = file.readline()
            code = [int(ch) for ch in code]
            points = codeToPoints(code)
            image = pointsToimage(points)
            image.save(name)
    except FileNotFoundError:
        print('File doesnt exist')
