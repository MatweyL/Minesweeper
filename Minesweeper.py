from copy import deepcopy
from random import randint
import os

def hash(x):
	return pow(int(x), 1) * 7 + pow(int(x), 2) * 17 + pow(int(x), 3) * 37

class Minefield(object):

	__alive = True
	__win = False
	__markedMines = 0#количество помеченных клеток-бомб
	__countOfOpenedCells = 0#количество открытых клеток
	__minefield = []#поле для игры
	__userMinefield = []#минное поле, которое видит игрок в процессе игры

	def __init__(self, cellCountX, cellCountY, minesCount, minesCoords = [], actions = []):#задание начальных параметров поля
		self.__cellCountX = cellCountX#количество клеток по оси абсцисс
		self.__cellCountY = cellCountY#количество клеток по оси ординат
		self.__minesCount = minesCount#количество мин
		self.__initialiseField()#создание пустых пользовательских и внутриигровых массивов
		if (len(minesCoords) != 0):
			for mineCoord in minesCoords:
				self.__minefield[mineCoord[1]][mineCoord[0]] = 'O'#Расстановка мин
			self.__setCellsNumbers()#установка количества мин-соседей у каждой клетки
			for action in actions:#Воспроизведение действий пользователя для восстановления поля
				if (action[2] == "Open"):
					self.openPoint(action[0], action[1])
				elif (action[2] == "Flag"):
					self.setPointBomb(action[0], action[1])
		else:
			self.__setMines()#установка мин на поле
			self.__setCellsNumbers()#установка количества мин-соседей у каждой клетки
			self.__saveStartParams()#сохранение стартовых данных об игре в файл

	def __saveStartParams(self):
		f = open('SavedGame.txt', 'w')
		f.write(str(self.__cellCountX)+ ' ' + str(self.__cellCountY) + ' ' + str(self.__minesCount))#в файл записываются параметры поля: количество ячеек по ширине, длине и количество мин
		for i in range(self.__cellCountY):#далее, с помощбю хеширования в файл записываются координаты бомб
			for j in range(self.__cellCountX):
				if (self.__minefield[i][j] == 'O'):
					f.write('\n' + str(hash(str(j))) + ' ' + str(hash(str(i))))
		f.close()

	def saveAction(self, x, y, action):#при каждом корректном действии пользователя открывается файл сохранения на дозапись
		f = open('SavedGame.txt', 'a')
		f.write('\n' + str(x)+ ' ' + str(y) + ' ' + action)#происходит запись действия игрока
		f.close()

	def isAlive(self):
		return self.__alive

	def isWin(self):
		return self.__win

	def isCorrectBounds(self, x, y):#если x и y находятся в допустимых значениях индексов массива минного поля, то возвращает True
		if (x >= 0 and x < self.__cellCountX and y >= 0 and y < self.__cellCountY):
			return True
		else:
			return False

	def checkWin(self):#если пользователь открыл все ячейки и пометил все мины, то он выиграл
		if (self.__markedMines == self.__minesCount and self.__cellCountX*self.__cellCountY - self.__minesCount == self.__countOfOpenedCells):
			self.__win = True

	def setPointBomb(self, x, y):#метод для установления в точке символ '!', означающего наличие бомбы
		if (self.__userMinefield[y][x] == '#'):#флаг может быть поставлен только в закрытую клетку
			self.__userMinefield[y][x] = '!'
			if (self.__minefield[y][x] == 'O'):#если помечена действительно бомба, то увеличиваем счетчик правильно отмеченных бомб
				self.__markedMines+=1
		elif (self.__userMinefield[y][x] == '!'):#если пользователь хочет снять флаг с клетки
			self.__userMinefield[y][x] = '#'
			if (self.__minefield[y][x] == 'O'):#если была помечена действительно бомба, то уменьшаем счетчик правильно отмеченных бомб
				self.__markedMines-=1

	def __recursionOpening(self, x, y):
		self.__countOfOpenedCells+=1#увеличение количества открытых клеток
		self.__userMinefield[y][x] = self.__minefield[y][x]
		if (self.__minefield[y][x] == ' '):
			for i in range(-1, 2):
				for j in range(-1, 2):
					if (not(i == 0 and j == 0) and self.isCorrectBounds(x + j, y + i) and self.__userMinefield[y + i][x + j] == '#'):
						self.__recursionOpening(x + j, y + i)

	def openPoint(self, x, y):#метод открытия клеток
		if (self.__minefield[y][x] == 'O'):#если пользователь попал в клетку с бомбой, то он проиграл
			self.__alive = False
		elif (self.__userMinefield[y][x] == '#' or self.__userMinefield[y][x] == '!'):
			self.__recursionOpening(x, y)#рекурсивное открытие области вокруг клетки

	def __initialiseField(self):
		tempUserMinefield = ['#' for j in range(0, self.__cellCountX)]#генерация массива из # для пользовательского поля
		tempMinefield = [' ' for j in range(0, self.__cellCountX)]#генерация массива из ' ' для внутриигрового поля
		for i in range(0, self.__cellCountY):
			self.__minefield.append(deepcopy(tempMinefield))
			self.__userMinefield.append(deepcopy(tempUserMinefield))

	def __setMines(self):
		settedMines = 0
		while (settedMines < self.__minesCount):
			x = randint(1, self.__cellCountX) - 1
			y = randint(1, self.__cellCountY) - 1
			if (self.__minefield[y][x] != 'O'):
				self.__minefield[y][x] = 'O'
				settedMines+=1

	def __getNumberOfMinesAround(self, x, y):
		answer = 0
		for i in range(-1, 2):#проход по области вокруг клетки
			for j in  range(-1, 2):
				if (self.isCorrectBounds(j + x, i + y) and self.__minefield[i + y][j + x] == 'O'):
					answer += 1
		if (answer == 0):
			answer = ' '
		return str(answer)


	def __setCellsNumbers(self):
		for i in range(0, self.__cellCountY):
			for j in range(0, self.__cellCountX):
				if (self.__minefield[i][j] != 'O'):
					self.__minefield[i][j] = self.__getNumberOfMinesAround(j, i)

	def __printCell(self, s):
		s = str(s)
		if (len(s) == 1):
			print(' ' + s + ' |', end='')
		elif (len(s) == 2):
			print(' ' + s + '|', end='')
		else:
			print(s + '|', end='')

	def printMinefield(self):
		border = '-' + '-' * 4 * (self.__cellCountX + 1)#на одну ячейку приходится 4 знака '-'
		print(border)
		print("|   |", end='')
		for i in range(self.__cellCountX):#вывод х-коориднат
			self.__printCell(i)
		print('\n' + border)
		for i in range(self.__cellCountY):
			print('|', end='')
			self.__printCell(i)
			for j in range(self.__cellCountX):
				if (self.isAlive()):
					self.__printCell(self.__userMinefield[i][j])
				else:
					self.__printCell(self.__minefield[i][j])
			print('\n' + border)


def getMinefieldParams():
	cmd = ""
	countCellX = None#Размер поля по Ох
	countCellY = None#Размер поля по Оу
	countMines = None#Количество мин
	success_input = False
	while (not(success_input)):
		print("Write width, height of the field and the number of mines: ", end='')
		line = input().split()
		data = []
		for i in range(0, 3):
			if (i < len(line)):
				data.append(line[i])
			else:
				data.append("")
		countCellX =data[0]
		countCellY = data[1]
		countMines = data[2]
		if (not(countCellX.isdigit()) or not(countCellY.isdigit()) or not(countMines.isdigit()) or int(countCellX) <= 0 or int(countCellY) <= 0 or int(countMines) <= 0):
			print("The numbers of the minefield size and mines must be integer and more than 0")
		else:
			if (int(countMines) >= int(countCellY)*int(countCellX)):#Если мин больше, чем ячеек поля
				print("The number of mines must be less then minefield size")
			else:
				success_input = True
	return [int(countCellX), int(countCellY), int(countMines), [], []]

def playMinefield(minefield):
	minefield.printMinefield()
	while (minefield.isAlive() and not(minefield.isWin())):
		print("Write x y Action: ", end='')
		line = input().split()#следующие 8 строк - обработка пользовательского ввода для устойчивости программы
		data = []
		for i in range(0, 3):
			if (i < len(line)):
				data.append(line[i])
			else:
				data.append("")
		x = data[0]
		y = data[1]
		action = data[2]
		if (x.isdigit() and y.isdigit() and minefield.isCorrectBounds(int(x), int(y))):
			if (action == "Open"):
				minefield.saveAction(x, y, action)#сохранение действия пользователя
				minefield.openPoint(int(x), int(y))#открытие клетки
				minefield.checkWin()#проверка условий выигрыша
				minefield.printMinefield()
			elif (action == "Flag"):
				minefield.saveAction(x, y, action)#сохранение действия пользователя
				minefield.setPointBomb(int(x), int(y))#установка или снятие флага у клетки
				minefield.checkWin()#проверка условий выигрыша
				minefield.printMinefield()
			else:
				print("The command '" + action + "' doesn't exists")
		else:
			print("Incorrect input coordinates")
	if (minefield.isAlive()):
		print("YOU WIN!")
	else:
		print("You lost the game.")

def getSavedData():
	f = open('SavedGame.txt', 'r')
	baseConfig = (f.readline()).split()
	readHashLines = 0
	bombHashCoords = []
	for line in f:#считываем из файла хеши координат бомб
		bombHashCoords.append(line.split())
		readHashLines+=1
		if (readHashLines == int(baseConfig[2])):#условие выхода - когда хеши координат всех бомб прочитаны из файла
			break
	bombCoords = []
	actions = []
	for i in range(int(baseConfig[1])):#проход по всем y координатам
		for j in range(int(baseConfig[0])):#проход по всем х координатам
			for k in bombHashCoords:
				if (str(hash(str(j))) == k[0] and str(hash(str(i))) == k[1]):
					bombCoords.append([j, i])
	for action in f:#считываем всю последовательность действий пользователя из файла
		action = action.split()
		actions.append([int(action[0]), int(action[1]), action[2]])
	f.close()
	return [int(baseConfig[0]), int(baseConfig[1]), int(baseConfig[2]), bombCoords, actions]

def main():
	print("MINESWEEPER.\nName of the action to open a cell - Open.\nName of the action to set the flag in the cell - Flag.")
	minefieldParams = []
	cmd = ""
	if (os.path.isfile('SavedGame.txt')):
		while (cmd != "y" and cmd != "n"):#цикл обработки ввода
			print("Do you want to continue the game?(y/n)")
			cmd = input()
		if (cmd == "y"):#считываем параметры игры из файла сохранения
			minefieldParams = getSavedData()
	if (cmd == "" or cmd == "n"):
		minefieldParams = getMinefieldParams()
	minefield = Minefield(minefieldParams[0], minefieldParams[1], minefieldParams[2], minefieldParams[3], minefieldParams[4])#создание объетка игрового поля
	playMinefield(minefield)#запуск игры
	if (os.path.isfile('SavedGame.txt')):#при окончании игры файл сохранения удаляется
		try:
			os.remove('SavedGame.txt')
		except:
			print("can't remove file with saved game")

if __name__ == "__main__":
	main()
	print("Press any key...")
	input()