from threading import Lock
from Common import *

class Model:

    def __init__(self,ravensProblem):

        self._figA = self.createFigure(ravensProblem.figures["A"])
        self._figB = self.createFigure(ravensProblem.figures["B"])
        self._figC = self.createFigure(ravensProblem.figures["C"])

        self._answers = []
        for i in range(1, 7, 1):
            self._answers.append(self.createFigure(ravensProblem.figures[str(i)]))

        self._objectsA = [ EmptyObject() ]
        self._objectsB = [ EmptyObject() ]
        self._objectsC = [ EmptyObject() ]
        self._objectsA += self._figA.getObjects()
        self._objectsB += self._figB.getObjects()
        self._objectsC += self._figC.getObjects()

        self._sizeA = len(self._objectsA)
        self._sizeB = len(self._objectsB)
        self._sizeC = len(self._objectsC)

        self._model = [[[Block() for k in range(len(self._objectsC))] for j in range(len(self._objectsB))] for i in range(len(self._objectsA))]

        idxA = 0
        for objectA in self._objectsA:
            idxB = 0
            for objectB in self._objectsB:
                idxC = 0
                for objectC in self._objectsC:
                    if not(idxA == 0 and idxB == 0 and idxC == 0):
                        block = Block(objectA, objectB, objectC, idxA, idxB, idxC, self._sizeA, self._sizeB, self._sizeC)
                        self._model[idxA][idxB][idxC] = block

                    idxC += 1

                idxB += 1

            idxA += 1

    def solve(self):
        blocks = []

        for i in range(self._sizeA):
            for j in range(self._sizeB):
                for k in range(self._sizeC):
                    block = self._model[i][j][k]

                    if block != {} and (i != 0 or j != 0 or k != 0):
                        blocks.append(block)

        # Order them based on score
        blocks = self.sortObjects(blocks)

        # Generator content
        generatedBlocks = []

        for block in blocks:
            if len(generatedBlocks) == 0:
                generatedBlocks.append(block)
            else:
                found = False

                for generatedBlock in generatedBlocks:
                    if (block.getIndexA() == generatedBlock.getIndexA() and block.getIndexA() != 0) or (block.getIndexB() == generatedBlock.getIndexB() and block.getIndexB() != 0) or (block.getIndexC() == generatedBlock.getIndexC() and block.getIndexC() != 0):
                        found = True

                if not found:
                    generatedBlocks.append(block)

        generatedObjects = []

        for generatedBlock in generatedBlocks:
            for generatedObject in generatedBlock.getGenerated():
                if type(generatedObject) is not EmptyObject:
                    generatedObjects.append(generatedObject)

        for answer in self._answers:
            answerObjects = answer.getObjects()
            if len(answerObjects) == len(generatedObjects):
                allMatch = True
                for generatedObject in generatedObjects:
                    if not self.checkGeneratedObject(generatedObject, answerObjects):
                        allMatch = False

                if allMatch:
                    return int(answer.getName())

        # Couldn't find a solution!
        return -1

    def sortObjects(self, blocks):
        for i in range(len(blocks)):
            for j in range(len(blocks) - i - 1):
                if self.shouldSwap(blocks[j], blocks[j + 1]):
                    temp = blocks[j]
                    blocks[j] = blocks[j + 1]
                    blocks[j + 1] = temp

        return blocks

    def shouldSwap(self, blockA, blockB):
        if blockA.getTotalScore() < blockB.getTotalScore():
            return True
        if blockA.getTotalScore() > blockB.getTotalScore():
            return True
        if blockA.getDownScore() < blockB.getDownScore() and blockA.getDownScore() < blockB.getRightScore():
            return True
        if blockA.getRightScore() < blockB.getDownScore() and blockA.getRightScore() < blockB.getRightScore():
            return True
        if blockA.getDownScore() > blockB.getDownScore() and blockA.getDownScore() > blockB.getRightScore():
            return False
        if blockA.getRightScore() > blockB.getDownScore() and blockA.getRightScore() > blockB.getRightScore():
            return False

        return False

    def checkGeneratedObject(self, generatedObject, answerObjects):
        for answerObject in answerObjects:
            transformations = Block().getTransformations(generatedObject, answerObject)
            score = Block().getScore(transformations, False, False)

            if score == 0:
                return True

        return False

    def createFigure(self, ravensFigure):
        lock = Lock()
        lock.acquire()

        self._createdObjects = []
        self._createdAttributes = []

        name = ravensFigure.name
        self._createdObjects = []
        for object in ravensFigure.objects:
            o = self.createObject(ravensFigure.objects[object])
            self._createdObjects.append(o)

        lock.release()

        return Figure(name, self._createdObjects)

    def createObject(self, ravensObject):
        lock = Lock()
        lock.acquire()

        name = ravensObject.name
        attributes = ravensObject.attributes

        self._createdAttributes = []
        for attr in ravensObject.attributes:
            if any(x == attr for x in self._createdAttributes):
                pass
            else:
                self._createdAttributes.append(Attribute(attr, attributes[attr]))

        lock.release()

        return Object(name, self._createdAttributes)