import os

class SparseMatrix:
    def __init__(self, matrix_file):
        self.numRows = 0
        self.numCols = 0
        self.elements = []
        matrix_file = os.path.abspath(matrix_file)
        with open(matrix_file, 'r') as file:
            lines = file.readlines()

        if len(lines) < 2:
            raise ValueError("Invalid input file format.")

        # Read number of rows
        first_line = lines[0].strip()
        if not first_line.startswith("rows="):
            raise ValueError("Invalid format for number of rows.")
        self.numRows = int(first_line.split("=")[1])

        # Read number of columns
        second_line = lines[1].strip()
        if not second_line.startswith("cols="):
            raise ValueError("Invalid format for number of columns.")
        self.numCols = int(second_line.split("=")[1])

        # Read elements
        for line in lines[2:]:
            line = line.strip()
            if line.startswith("(") and line.endswith(")"):
                elements = line[1:-1].split(",")
                if len(elements) != 3:
                    raise ValueError("Invalid format for matrix element.")
                row = int(elements[0].strip())
                col = int(elements[1].strip())
                value = int(elements[2].strip())
                self.elements.append((row, col, value))

    def getElement(self, row, col):
        for elem in self.elements:
            if elem[0] == row and elem[1] == col:
                return elem[2]
        return 0

    def setElement(self, row, col, value):
        for i, elem in enumerate(self.elements):
            if elem[0] == row and elem[1] == col:
                self.elements[i] = (row, col, value)
                return
        self.elements.append((row, col, value))

    def addMatrices(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions do not match for addition.")

        result = SparseMatrix('')
        
        # Add elements from self
        for elem in self.elements:
            row, col, value = elem
            result.setElement(row, col, result.getElement(row, col) + value)

        # Add elements from other
        for elem in other.elements:
            row, col, value = elem
            result.setElement(row, col, result.getElement(row, col) + value)

        return result

    def subtractMatrices(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions do not match for subtraction.")

        result = SparseMatrix('')
        
        # Add elements from self
        for elem in self.elements:
            row, col, value = elem
            result.setElement(row, col, result.getElement(row, col) + value)

        # Subtract elements from other
        for elem in other.elements:
            row, col, value = elem
            result.setElement(row, col, result.getElement(row, col) - value)

        return result

    def multiplyMatrices(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrix dimensions do not match for multiplication.")

        result = SparseMatrix('')
        
        for elemA in self.elements:
            rowA, colA, valueA = elemA
            for elemB in other.elements:
                rowB, colB, valueB = elemB
                if colA == rowB:
                    new_value = result.getElement(rowA, colB) + (valueA * valueB)
                    result.setElement(rowA, colB, new_value)

        return result

    def printMatrix(self):
        for i in range(self.numRows):
            for j in range(self.numCols):
                print(self.getElement(i, j), end=" ")
            print()


try:
    current_dir = os.getcwd() 
    matrixFile1 = os.path.join(current_dir, "dsa/sparse_matrix/sample_inputs/easy_sample_01_2.txt")
    matrixFile2 = os.path.join(current_dir, "dsa/sparse_matrix/sample_inputs/easy_sample_01_3.txt")

    A = SparseMatrix(matrixFile1)
    B = SparseMatrix(matrixFile2)

    print("Matrix A:")
    A.printMatrix()

    print("\nMatrix B:")
    B.printMatrix()

    C = A.addMatrices(B)
    print("\nMatrix A + B:")
    C.printMatrix()

    D = A.subtractMatrices(B)
    print("\nMatrix A - B:")
    D.printMatrix()

    E = A.multiplyMatrices(B)
    print("\nMatrix A * B:")
    E.printMatrix()

except ValueError as e:
    print(f"Error: {e}")
