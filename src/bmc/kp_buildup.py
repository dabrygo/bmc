import unittest

def kp_step(n, chunk_size=5):
    if n % chunk_size == 1:
        return [n]

    # New Verse
    x = [n] 

    # Together
    n_chunks = (n-1) // chunk_size
    start = (chunk_size * n_chunks) + 1
    together = tuple(i for i in range(start, n+1))
    x.append(together)

    # Forwards and backwards
    forwards = tuple(i for i in range(start, n+1))
    backwards = tuple(i for i in range(n, start - 1, -1))
    fwd_and_bkwd = tuple([forwards, backwards])
    x.append(fwd_and_bkwd)

    if n > chunk_size and n % chunk_size == 0:
        all_in_order = tuple(i for i in range(1, n+1))
        x.append(all_in_order)

    return x

def kp(n):
    x = []
    for i in range(1, n+1):
        step = kp_step(i)
        new = []
        together = []
        forwards = []
        backwards = []
        all_in_order = []
        if len(step) == 1:
            new = step[0]
        elif len(step) == 3:
            new, together, fwd_and_bkwd = step
            forwards, backwards = fwd_and_bkwd
        elif len(step) == 4:
            new, together, fwd_and_bkwd, all_in_order = step
            forwards, backwards = fwd_and_bkwd
        else:
            raise ValueError
        x.append(new)
        x.extend(together)
        x.extend(forwards)
        x.extend(backwards)
        x.extend(all_in_order)
    return x


class TestKp(unittest.TestCase):
    def test_one(self):
        self.assertEqual(kp(1), [1])

    def test_two(self):
        self.assertEqual(
            kp(2),
            [1,
             2,
                 1, 2,
                 1, 2, 2, 1
            ]
        )

    def test_three(self):
        self.assertEqual(
            kp(3),
            [1,
             2,
                 1, 2,
                 1, 2, 2, 1,
             3,
                 1, 2, 3,
                 1, 2, 3, 3, 2, 1
             ]
        )

    def test_six(self):
        self.assertEqual(
            kp(6),
            [1,
             2,
                 1, 2,
                 1, 2, 2, 1,
             3,
                 1, 2, 3,
                 1, 2, 3, 3, 2, 1,
             4,
                 1, 2, 3, 4,
                 1, 2, 3, 4, 4, 3, 2, 1,
             5,
                 1, 2, 3, 4, 5,
                 1, 2, 3, 4, 5, 5, 4, 3, 2, 1,
             6,
             ]
        )

    def test_seven(self):
        self.assertEqual(
            kp(7),
            [1,
             2,
                 1, 2,
                 1, 2, 2, 1,
             3,
                 1, 2, 3,
                 1, 2, 3, 3, 2, 1,
             4,
                 1, 2, 3, 4,
                 1, 2, 3, 4, 4, 3, 2, 1,
             5,
                 1, 2, 3, 4, 5,
                 1, 2, 3, 4, 5, 5, 4, 3, 2, 1,
             6,
             7,
                 6, 7,
                 6, 7, 7, 6,
             ]
        )

    def test_ten(self):
        self.assertEqual(
            kp(10),
            [1,
             2,
                 1, 2,
                 1, 2, 2, 1,
             3,
                 1, 2, 3,
                 1, 2, 3, 3, 2, 1,
             4,
                 1, 2, 3, 4,
                 1, 2, 3, 4, 4, 3, 2, 1,
             5,
                 1, 2, 3, 4, 5,
                 1, 2, 3, 4, 5, 5, 4, 3, 2, 1,
             6,
             7,
                 6, 7,
                 6, 7, 7, 6,
             8,
                 6, 7, 8,
                 6, 7, 8, 8, 7, 6,
             9,
                 6, 7, 8, 9,
                 6, 7, 8, 9, 9, 8, 7, 6,
             10,
                 6, 7, 8, 9, 10,
                 6, 7, 8, 9, 10, 10, 9, 8, 7, 6,
             1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
             ]
        )

    def test_len_13(self):
        self.assertEqual(122, len(kp(13)))

class TestKpStep(unittest.TestCase):
    def test_one(self):
        self.assertEqual(kp_step(1), [1])

    def test_two(self):
        self.assertEqual(kp_step(2), [2, (1, 2), ((1, 2), (2,1))])

    def test_three(self):
        self.assertEqual(kp_step(3), [3, (1, 2, 3), ((1, 2, 3), (3, 2,1))])

    def test_five(self):
        self.assertEqual(kp_step(5), [5, (1, 2, 3, 4, 5), ((1, 2, 3, 4, 5), (5, 4, 3, 2,1))])
        
    def test_six(self):
        self.assertEqual(kp_step(6), [6])
        
    def test_seven(self):
        self.assertEqual(kp_step(7), [7, (6, 7), ((6, 7), (7, 6))])
        
    def test_eight(self):
        self.assertEqual(kp_step(8), [8, (6, 7, 8), ((6, 7, 8), (8, 7, 6))])
        
    def test_ten(self):
        self.assertEqual(
            kp_step(10),
            [10,
              (6, 7, 8, 9, 10),
              (
                  (6, 7, 8, 9, 10),
                  (10, 9, 8, 7, 6)
               ),
              (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
              ]
        )
          
    def test_eleven(self):
        self.assertEqual(kp_step(11), [11])

    def test_twelve(self):
        self.assertEqual(kp_step(12), [12, (11, 12), ((11, 12), (12, 11))])
               
    def test_fifteen(self):
        self.assertEqual(
            kp_step(15),
            [15,
              (11, 12, 13, 14, 15),
              (
                  (11, 12, 13, 14, 15),
                  (15, 14, 13, 12, 11)
               ),
              (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
              ]
        )


if __name__ == '__main__':
    unittest.main()
