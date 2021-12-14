import numpy as np

class PuzzleSolver(object):

    def solve_puzzle(self, a, b, c):
        """Solve an analogy puzzle.
        
        Arguments:
            a {str} -- is to
            b {str} -- like
            c {str} -- is to
        
        Returns:
            str -- Token that solves the puzzle
        """
        # to implement
        path = "./datasets/word_embeddings/" 

        embeddings = np.load(path + "glove_word_embeddings.npy")

        fd = open(path + "words.txt", "r")
        words = fd.read().splitlines()

        # find word indices 
        # take the corresponding word embeddings
        idx = {"a": words.index(a), "b": words.index(b), "c": words.index(c)}

        a = embeddings[idx["a"]]   
        b = embeddings[idx["b"]]   
        c = embeddings[idx["c"]]   

        # compute w_b - w_a + w_c
        analogy = b - a + c

        # find closest representation (according to cosine similarity)      
        norm_e = embeddings / np.reshape(np.linalg.norm(embeddings, axis=1), (-1, 1))
        norm_a = analogy / np.linalg.norm(analogy)

        cosine_similarity = np.sum(norm_a * norm_e, axis=1)

        # assign a,b,c a high negative value (so we don't choose them as maximum)
        cosine_similarity[list(idx.values())] = -99999
       
        # find the maximum 
        x = words[cosine_similarity.argmax()]

        return x


def test_solve_puzzle(puzzle_solver):
    # This test shall pass!
    assert puzzle_solver.solve_puzzle("man", "king", "woman") == "queen"


if __name__ == "__main__":
    config = {}
    puzzle_solver = PuzzleSolver()
    test_solve_puzzle(puzzle_solver)
