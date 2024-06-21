# an example of a BLS-12 curve with ate pairing

def frobenius_point(Q):
    return Q.curve()(Q[0].frobenius(), Q[1].frobenius())

def trace_point(Q, n):
    Qi = Q
    R = Qi
    for i in range(1, n):
        Qi = frobenius_point(Qi)
        R = R + Qi
    return R

def trace_zero(Q, n):
    return n*Q - trace_point(Q, n)

def params():
    global P, Q, r, t, p, E, Ep12, c, Fp
    # Define parameters for curve BLS12-381
    QQx.<x> = QQ[]
    rx = cyclotomic_polynomial(12)
    tx = x+1
    cx = (x-1)^2//3 # the cofactor
    px = cx*rx + tx - 1

    u = -0xd201000000010000
    p = ZZ(px(u))
    r = ZZ(rx(u))
    t = ZZ(tx(u))
    c = ZZ(cx(u))

    Fp = GF(p)
    a = Fp(0)
    b = Fp(4)
    E = EllipticCurve(Fp, [a, b])
    P = E(0x17F1D3A73197D7942695638C4FA9AC0FC3688C4F9774B905A14E3A3F171BAC586C55E83FF97A1AEFFB3AF00ADB22C6BB, 0x08B3F481E3AAA0F1A09E30ED741D8AE4FCF5E095D5D00AF600DB18CB2C04B3EDD03CC744A2888AE40CAA232946C5E7E1)

    # Define an extension of degree 12 with p = 3 mod 4
    # one can define a first level to be Fp2 with non residues \beta = -1, and upper extensions with \xi = 1+i
    Fpz.<z> = Fp[]
    Fp2.<i> = Fp.extension(z^2+1)
    xi = 1 + i

    Fp2s.<s> = Fp2[]
    Fq6.<j> = Fp2.extension(s^6 - xi)
    a0, a1 = xi.polynomial().list()
    Fp12.<w> = Fp.extension(z^12 -2*a0*z^6 + a0^2 + a1^2)

    Ep12 = E.base_extend(Fp12)
    c2 = Ep12.order() // (r^2)
    Q = Ep12(2578232507445644209705389149747005828621775158081381201632210272686879082618193252640606571991242713060396837669229*w^10 + 3641502873767573927654921472302126498413084341369125646993054932047178266436574334217899373184594062188088602487362*w^4, 2854492949579232990659640638483934487696261592466403263554955643994848614156095896608808611932084748408415472861752*w^9 + 3312048708305139342416502647182932316264562276543187680067676573003818389556499754216478047767612717461821747783399*w^3)

    # Test bilinearity
    k = randrange(r)
    assert Ep12(P).tate_pairing(k*Q, r, 12) == (Ep12(P).tate_pairing(Q, r, 12))^k
