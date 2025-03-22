# Writeup
WIP

TLDR: many possible solutions here, but common themes are
1. rewriting the long flag string in terms of the flag to dramatically reduce number of bits needed to be recovered.
2. knowing how to use crt to partial decryption for small primes
3. knowing how to recognise and handle when e mod phi isn't coprime to phi, or when the base doesn't generate the entire subgroup.

My solve script just rewrites equation, then takes tiny factors from each ct to solve in small subgroups. But lots of other options. (Factoring larger numbers, randcracking from the e values etc.)

Proper write coming soon(tm)