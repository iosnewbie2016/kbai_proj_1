import uuid
from enum import Enum

class Figure:
    def __init__(self, name, objects):
        self._name = name
        self._objects = objects

    def getName(self):
        return self._name

    def getObjects(self):
        return self._objects

class IBaseObject:
    def __init__(self, name, attributes):
        self._name = name
        self._attributes = attributes

    def getName(self):
        return self._name

    def getAttribute(self,name):
        for attribute in self._attributes:
                if attribute.getName() == name:
                    return attribute.getValue()
        return -1

    def getAttributes(self):
        return self._attributes

    def getAttributeNames(self):
        names = []
        for attribute in self._attributes:
            names.append(attribute.getName())

        return set(names)

    def transform(self,transformations,addAttributes):
        raise NotImplementedError()

class EmptyObject(IBaseObject):
    def __init__(self):
        super().__init__("NULL", [])

    def transform(self,transformations,addAttributes):
        for transformation in transformations:
            if isinstance(transformation, AddTransformation):
                return [ Object(str(uuid.uuid4()), addAttributes) ]
            elif isinstance(transformation, (NoTransformation,DeleteTransformation)):
                return [ EmptyObject() ]
            else:
                raise IllegalTransformationError("Illegal change transformation!")

        return [ EmptyObject() ]

class IllegalTransformationError(Exception):
    pass

class Object(IBaseObject):
    def __init__(self, name, attributes):
        super().__init__(name, attributes)

    def transform(self,transformations,addAttributes):
        newAttributes = self.getAttributes()

        for transformation in transformations:
            if type(transformation) is AddTransformation:
                object1 = Object(str(uuid.uuid4()), [])
                object2 = Object(str(uuid.uuid4()), addAttributes)
                return [ object1, object2 ]
            elif type(transformation) is DeleteTransformation or type(transformation) is NoTransformation:
                return [ EmptyObject() ]
            else:
                attribute = transformation.getAttribute()
                attributeValue = transformation.getUpdatedValue()

                operation = transformation.getOperation()

                if operation == Operation.ADD:
                    newAttributes.append(Attribute(attribute, attributeValue))
                elif operation == Operation.DELETE:
                    newAttributes.remove(Attribute(attribute, attributeValue))
                elif operation == Operation.CHANGE:
                    if attribute == "angle":
                        originalAngle = int(transformation.getOriginalValue())
                        updatedAngle = int(transformation.getUpdatedValue())

                        foundAttr = False
                        for attr in newAttributes:
                            if attr.getName() == attribute:
                                currentAngle = int(attr.getValue())
                                foundAttr = True
                                break

                        if foundAttr:
                            horizontalReflection = reflectHorizontalAngle(originalAngle)
                            verticalReflection = reflectVerticalAngle(originalAngle)

                            if horizontalReflection == updatedAngle:
                                resultAngle = reflectHorizontalAngle(currentAngle)
                            elif verticalReflection == updatedAngle:
                                resultAngle = reflectVerticalAngle(currentAngle)
                            else:
                                change = updatedAngle - originalAngle
                                resultAngle = currentAngle + change

                            for attr in newAttributes:
                                if attr.getName() == attribute:
                                    newAttributes.remove(attr)
                                    newAttributes.append(Attribute(attribute, str(resultAngle)))

                    elif attribute == "alignment":
                        originalAlignment = transformation.getOriginalValue()
                        updatedAlignment = transformation.getUpdatedValue()

                        foundAttr = False
                        for attr in newAttributes:
                            if attr.getName() == attribute:
                                currentAlignment = attr.getValue()
                                foundAttr = True
                                break

                        if foundAttr:
                            horizontalReflection = reflectHorizontalAlignment(originalAlignment)
                            verticalReflection = reflectVerticalAlignment(originalAlignment)
                            doubleReflection = reflectVerticalAlignment(horizontalReflection)

                            if updatedAlignment == horizontalReflection:
                                resultAlignment = reflectHorizontalAlignment(currentAlignment)
                            elif updatedAlignment == reflectVerticalAlignment:
                                resultAlignment = reflectVerticalAlignment(currentAlignment)
                            elif updatedAlignment == doubleReflection:
                                resultAlignment = reflectHorizontalAlignment(reflectVerticalAlignment(currentAlignment))
                            else:
                                resultAlignment = currentAlignment

                            for attr in newAttributes:
                                if attr.getName() == attribute:
                                    newAttributes.remove(attr)
                                    newAttributes.append(Attribute(attribute, resultAlignment))
                    else:
                        for attr in newAttributes:
                            if attr.getName() == attribute:
                                newAttributes.remove(attr)
                                newAttributes.append(Attribute(attribute, attributeValue))

        return [ Object(str(uuid.uuid4()), newAttributes) ]

def reflectVerticalAngle(angle):
    vertical = int(angle) * -1
    if vertical < 0:
        return vertical + 360

    return vertical


def reflectHorizontalAngle(angle):
    horizontal = 180 - int(angle)
    if horizontal < 0:
        return horizontal + 360

    return horizontal


def reflectVerticalAlignment(alignment):
    if "left" in alignment:
        return alignment.replace("left", "right")

    if "right" in alignment:
        return alignment.replace("right", "left")

    return alignment


def reflectHorizontalAlignment(alignment):
    if "top" in alignment:
        return alignment.replace("top", "bottom")

    if "bottom" in alignment:
        return alignment.replace("bottom", "top")

    return alignment

class Attribute:
    def __init__(self, name, value):
        self._name = name
        self._value = value

    def getName(self):
        return self._name

    def getValue(self):
        return self._value

class IBaseTransformation:
    def getOperation(self):
        raise NotImplementedError

    def getAttribute(self):
        raise NotImplementedError

    def getOriginalValue(self):
        raise NotImplementedError

    def getUpdatedValue(self):
        raise NotImplementedError


class NoTransformation(IBaseTransformation):
    def getOperation(self):
        return {}

    def getAttribute(self):
        return {}

    def getOriginalValue(self):
        return {}

    def getUpdatedValue(self):
        return {}

class AddTransformation(IBaseTransformation):
    def getOperation(self):
        return {}

    def getAttribute(self):
        return {}

    def getOriginalValue(self):
        return {}

    def getUpdatedValue(self):
        return {}

class DeleteTransformation(IBaseTransformation):
    def getOperation(self):
        return {}

    def getAttribute(self):
        return {}

    def getOriginalValue(self):
        return {}

    def getUpdatedValue(self):
        return {}

class ChangeTransformation(IBaseTransformation):
    def getOperation(self):
        return self._operation

    def getAttribute(self):
        return self._attribute

    def getOriginalValue(self):
        return self._originalValue

    def getUpdatedValue(self):
        return self._updatedValue

    def withOperation(self, operation):
        self._operation = operation
        return self

    def forAttribute(self, attribute):
        self._attribute = attribute
        return self

    def withOriginalValue(self, value):
        self._originalValue = value
        return self

    def withUpdatedValue(self, value):
        self._updatedValue = value
        return self

class Block:
    def __init__(self,base={},right={},down={},idxA=0,idxB=0,idxC=0,sizeA=0,sizeB=0,sizeC=0):
        self._base = base
        self._right = right
        self._down = down

        self._idxA = idxA
        self._idxB = idxB
        self._idxC = idxC

        self._sizeA = sizeA
        self._sizeB = sizeB
        self._sizeC = sizeC

        self._generated = []

        if base != {} and right != {} and down != {}:
            self._rightTransformations = self.getTransformations(base, right)
            self._rightScore = self.getScore(self._rightTransformations, self._sizeB > self._sizeA, self._sizeB < self._sizeA)

            self._downTransformations = self.getTransformations(base, down)
            self._downScore = self.getScore(self._downTransformations, self._sizeC > self._sizeA, self._sizeC < self._sizeA)

            try:
                self._generated = self._right.transform(self._downTransformations, self._down.getAttributes())
            except Exception:
                pass

            if self._generated == []:
                try:
                    self._generated = self._down.transform(self._rightTransformations, self._right.getAttributes())

                except Exception:
                    self._generated = []

    def getTransformations(self,original, updated):
        transformations = []

        if isinstance(original, EmptyObject) and isinstance(updated, EmptyObject):
            transformations.append(NoTransformation())
        elif isinstance(original, EmptyObject):
            transformations.append(AddTransformation())
        elif isinstance(updated, EmptyObject):
            transformations.append(DeleteTransformation())
        else:
            originalAttributeNames = original.getAttributeNames()
            updatedAttributeNames = updated.getAttributeNames()

            deletedAttributeNames = originalAttributeNames - updatedAttributeNames
            addedAttributeNames = updatedAttributeNames - originalAttributeNames
            potentiallyChangedAttributeNames = originalAttributeNames.intersection(updatedAttributeNames)

            for attribute in deletedAttributeNames:
                transformations.append(ChangeTransformation().withOperation(Operation.DELETE).forAttribute(attribute))

            for attribute in addedAttributeNames:
                transformations.append(
                    ChangeTransformation().withOperation(Operation.ADD).forAttribute(attribute).withUpdatedValue(
                        updated.getAttribute(attribute)))

            for attribute in potentiallyChangedAttributeNames:
                originalValue = original.getAttribute(attribute)
                updatedValue = updated.getAttribute(attribute)

                if originalValue != updatedValue:
                    if attribute == "inside" or attribute == "above":
                        if len(originalValue.split(',')) != len(updatedValue.split(',')):
                            transformations.append(ChangeTransformation().withOperation(Operation.CHANGE).forAttribute(
                                attribute).withOriginalValue(originalValue).withUpdatedValue(updatedValue))
                    else:
                        transformations.append(ChangeTransformation().withOperation(Operation.CHANGE).forAttribute(
                            attribute).withOriginalValue(originalValue).withUpdatedValue(updatedValue))

        return transformations

    def getScore(self,transformations, objectsAdded, objectsDeleted):
        score = 0

        if len(transformations) == 0:
            return score

        for transformation in transformations:
            if type(transformation) is AddTransformation:
                if objectsAdded:
                    score += 5
                else:
                    score += 30
            elif type(transformation) is DeleteTransformation:
                if objectsDeleted:
                    score += 5
                else:
                    score += 30
            elif type(transformation) is NoTransformation:
                if not (objectsAdded or objectsDeleted):
                    score += 30
                else:
                    score += 5
            else:
                attribute = transformation.getAttribute()

                if attribute != {} and ("inside" in attribute or "above" in attribute):
                    score += 4
                else:
                    score += 5

        return score

    def getIndexA(self):
        return self._idxA

    def getIndexB(self):
        return self._idxB

    def getIndexC(self):
        return self._idxC

    def getRightScore(self):
        return self._rightScore

    def getDownScore(self):
        return self._downScore

    def getTotalScore(self):
        return self._downScore + self._rightScore

    def getGenerated(self):
        return self._generated

    def __lt__(self, other):
        if self.getTotalScore() < other.getTotalScore():
            return -1
        if self.getTotalScore() > other.getTotalScore():
            return 1
        if self.getDownScore() < other.getDownScore() and self.getDownScore() < other.getRightScore():
                return -1
        if self.getRightScore() < other.getDownScore() and self.getRightScore() < other.getRightScore():
                return -1
        if self.getDownScore() > other.getDownScore() and self.getDownScore() > other.getRightScore():
                return 1
        if self.getRightScore() > other.getDownScore() and self.getRightScore() > other.getRightScore():
                return 1

        return 0


class Operation(Enum):
    ADD = 1
    DELETE = 2
    CHANGE = 3