from exercise2.text_processor import TextProcessor
from itertools import chain


"""
This class is responsible for parsing and evaluating boolean queries.
The class provides methods to evaluate AND, OR, and NOT operators.
"""
class BooleanQueryParser:
    def __init__(self, inverted_index) -> None:
        self.inverted_index = inverted_index

        self._text_processor = TextProcessor()
        self._operators = ['and', 'or', 'not', '(', ')']

        self._and_operator = 'and'
        self._or_operator = 'or'
        self._not_operator = 'not'

    def AND(self, left_operand, right_operand) -> set:
        """
        Returns the intersection of two sets.
        """
        return left_operand.intersection(right_operand)
    
    def OR(self, left_operand: set, right_operand: set) -> set:
        """
        Returns the union of two sets.
        """
        return left_operand.union(right_operand)

    def NOT(self, operand) -> set:
        """
        Returns the set of documents that do not contain the term.
        """
        # Flatten the list of document IDs and convert to a set
        all_docs = set(chain.from_iterable(self.inverted_index.values()))
        return all_docs.difference(operand)
    
    def _shunting_yard(self, query: str) -> list:
        """
        Converts an infix boolean query to a postfix boolean query.
        source: https://fr.wikipedia.org/wiki/Algorithme_Shunting-yard
        """
        output = []
        stack = []

        for token in query:
            if token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            elif token in self._operators:
                while stack and stack[-1] != '(' and self._operators.index(token) <= self._operators.index(stack[-1]):
                    output.append(stack.pop())
                stack.append(token)
            else:
                output.append(token)

        while stack:
            output.append(stack.pop())

        return output
    
    def _evaluate_operator(self, operator: str, stack: list) -> None:
        """
        Evaluates a boolean operator and pushes the result to the stack.
        """
        if operator == self._and_operator:
            right_operand = stack.pop()
            left_operand = stack.pop()
            
            stack.append(self.AND(left_operand, right_operand))
        elif operator == self._or_operator:
            right_operand = stack.pop()
            left_operand = stack.pop()
            
            stack.append(self.OR(left_operand, right_operand))
        elif operator == self._not_operator:
            if not stack: 
                raise ValueError("Invalid NOT operator: Missing operand")
            
            operand = stack.pop()
            stack.append(self.NOT(operand))
        
    def _evaluate_postfix(self, query: list) -> set:
        """
        Evaluates a postfix boolean query and returns the set of documents that satisfy the query.
        """
        stack = []

        for token in query:
            if token not in self._operators:
                if token in self.inverted_index: stack.append(set(self.inverted_index[token]))
                else: stack.append(set())
            else: self._evaluate_operator(token, stack)

        return stack.pop()

    def evaluate_query(self, query: str) -> set:
        """
        Evaluates a boolean query and returns the set of documents that satisfy the query.
        """
        query = self._text_processor.pre_processing(query)
        if not query: return set()
        
        query = self._shunting_yard(query)
        return self._evaluate_postfix(query)