
with open("output.txt", "r") as f:
    data = f.read()

flaglen = 18

# nasty parsing hack. Don't use on untrusted output.txt
exec(data)

mods = [p_0, p_1]
vals = [f_0, f_1]

fullvalue = crt(vals,mods)
print(int(fullvalue).bit_length())
from Crypto.Util.number import long_to_bytes

fullmod = prod(mods)
suffix_bits = int.from_bytes(b"01111101", "big")

prefix_bits = bin(int.from_bytes(b'DDC{', "big"))
prefix_bits_int = int.from_bytes(prefix_bits.encode(), "big")
prefix_bits_int_shifted = prefix_bits_int * (2 ** (8*8 * (flaglen - 4)))


f = b'\x30' * (flaglen - 5) * 8 + b'\x00'*8 

normalised = int.from_bytes(f, "big")

target_for_subsetsum = int(fullvalue) - suffix_bits - prefix_bits_int_shifted - normalised
target_for_subsetsum = int(int(target_for_subsetsum) % fullmod)

bits_to_check = []
weights = []
for i in range(flaglen-4):
    for j in range(8):
        idx = (64)*i + 8*j
        if idx < 64:
            continue
        if j == 7:
            continue
        weights += [2**idx]

print(len(weights))

print("starting subset sum")

##############
#from https://github.com/josephsurin/lattice-based-cryptanalysis/blob/main/lbc_toolkit/problems/knapsack.sage


import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from sage.modules.free_module_integer import IntegerLattice

def subset_sum(weights, targets, modulus=None, N=None, lattice_reduction=None, verbose=False):
    r"""
    Returns the solution of the subset sum problem with the given ``weights``
    and ``targets``. Supports multiple knapsacks as well as the modular case
    with the ``modulus`` argument. The implementation follows the algorithm
    as described in [1].

    INPUT:

    - ``weights`` -- A list of integer weights `a_1, \ldots, a_n`, or a list
    of lists `a_{1, 1}, \ldots, a_{k, n}` for the multiple subset sum problem
    with `k` different subset sums.

    - ``targets`` -- The integer target `s`, or a list of targets
    `s_1, \ldots, s_j` for the multiple subset sum problem case.

    - ``modulus`` -- (optional) The modulus `M`.

    - ``N`` -- (optional) The scaling factor `N` as described in [1].
    (Default: `\lceil \sqrt{(n+1)/4} \rceil`)

    OUTPUT:

    A solution to the given subset sum problem as a list representing the `e_i`
    such that

    .. MATH::

        \sum_{i=1}^n e_i a_{j, i} = s_j

    for all `1 \leq j \leq k`.

    If no solution could be found, None is returned.

    REFERENCES:

    [1] Yanbin Pan and Feng Zhang. *Solving low-density multiple subset sum problems with SVP oracle.*
    In Journal of Systems Science and Complexity, p. 228--242. Springer, 2016.
    https://link.springer.com/article/10.1007/s11424-015-3324-9
    """

    verbose = (lambda *a: print('[subset_sum]', *a)) if verbose else lambda *_: None

    if type(weights[0]) is list:
        k = len(weights)
        n = len(weights[0])
    else:
        k = 1
        n = len(weights)
        weights = [weights]
        targets = [targets]

    if modulus is not None:
        density = n / (k * log(modulus, 2))
    else:
        density = n / (k * log(max(flatten(weights)), 2))
    verbose('Density:', round(density.n(), 4))

    N = N or ceil(sqrt((n+1)/4))
    B = 2 * Matrix.identity(n)
    B = B.augment(vector([0] * n))
    for j in range(k):
        B = B.augment(vector([N * a for a in weights[j]]))
    if modulus is not None:
        B = B.stack(Matrix.zero(k, n + 1).augment(N * modulus * Matrix.identity(k)))
    B = B.stack(vector([1] * (n + 1) + [N * s for s in targets]))

    verbose('Lattice dimensions:', B.dimensions())
    lattice_reduction_timer = cputime()
    if lattice_reduction:
        B = lattice_reduction(B)
    else:
        B = B.LLL()
    verbose(f'Lattice reduction took {cputime(lattice_reduction_timer):.3f}s')

    for row in B:
        if row[n] < 0:
            sol = [(x + 1)//2 for x in row[:n]]
        else:
            sol = [(1 - x)//2 for x in row[:n]]
        if any(x not in [0, 1] for x in sol):
            continue
        for j in range(k):
            t = sum(e * a for e, a in zip(sol, weights[j]))
            tj = targets[j]
            if modulus > 0:
                t %= modulus
                tj %= modulus
            if t != tj:
                break
        else:
            return sol
        
    return None

def modular_subset_sum(weights, target, M):
    print('Modular Subset Sum Example')
    sol = subset_sum(weights, target, modulus=M, lattice_reduction=lambda B: IntegerLattice(B).BKZ(block_size=30), verbose=True)
    assert sol
    print('  Found  solution:', sol, end='\n\n')
    return sol


result = modular_subset_sum(weights, target_for_subsetsum, fullmod )

result = result[::-1]

for i in range(13):
    result.insert(i*8, 0)
    
res = int("".join([str(x) for x in result]),2)

flag_inside = res.to_bytes(13,'big')

flag = b'DDC{' + flag_inside + b'}'

print(flag)
assert binarify(flag) % p_0 == f_0
assert binarify(flag) % p_1 == f_1

print(flag)

exit()
