# Negative Zero: An Unstable Phantom Across System Boundaries

## BCR-2025-002

**© 2025 Blockchain Commons**

Author: Wolf McNally\
Date: April 25, 2024

## Introduction

IEEE-754 floating point computations allow for the result *negative zero*, `-0.0`. In these environments, the expression `-1 / Infinity` typically results in negative zero.

However, all these environments treat zero and negative zero as identical for the purposes of numeric comparison, i.e., `0.0 == -0.0`. The value of negative zero is therefore an artifact of no common use (similar to IEEE-754 NaN payloads). If you’re a numerical purist, please refer to Endnote 1.

dCBOR abstracts away the value `-0.0` in numeric reduction, serializing it as `0x00`. Some have proposed that this is inconsistent behavior. In fact, the opposite is true: allowing `-0.0` to survive encoding across the serialization and language barriers I describe below is what *breaks* consistency. As I’ll show below, treating all forms of zero as `0` is the only path to deterministic, interoperable numeric representations.

An existence proof for my argument would be to find common systems that:

- Do not have a concept of “negative zero” or always treat zero as uniquely *unsigned*,
- May produce negative zero internally, but normalize it in such a way that code cannot recover it,
- Treat negative zero *inconsistently* so that its behavior cannot be relied upon as deterministic.

Below is the result of my survey. It confirms that systems that do *not* normalize `-0.0` to `0` may break determinism in applications that require it.

Many common languages like C, C++, Rust, Java, Go, etc. are IEEE-754 environments, and all provide a way to detect the sign bit. When formatting and printing floating point values as text, they may not all format `-0.0` as negative by default. So even though they may exhibit inconsistent *display* behavior, they still provide a clear internal distinction between zero and negative zero. As such, I won’t be dealing with them further here.

## JavaScript/JSON interoperability

While JavaScript can *produce* `-0`, and `JSON.parse()` will *decode* `-0`, `JSON.stringify()` will not *encode* `-0`. This is inconsistent behavior, and cannot be relied upon for deterministic behavior unless extra steps are taken.

This silent flattening by `JSON.stringify()`—combined with JavaScript’s internal ability to produce `-0`—means `-0` is an unstable phantom: visible in memory, erased on the wire. No application depending on it can behave predictably across serialization boundaries.

```
: -1 / Infinity
  -0

: JSON.parse("-0.0");
  -0

: JSON.stringify(-1 / Infinity)
  '0'

: JSON.stringify(0.0);
  '0'

: JSON.stringify(-0.0);
  '0'

: JSON.parse(JSON.stringify(-1 / Infinity));
  0

: JSON.parse(JSON.stringify(-0.0))
  0
```

## Mathematica

Mathematica treats zero as a unique, unsigned value.

```
In[1]:= -1 / Infinity
Out[1]= 0

In[2]:= -0.0
Out[2]= 0.

In[3]:= N[-0.0]
Out[3]= 0.

In[4]:= Sign[-0.0]
Out[4]= 0

In[5]:= Sign[0.0]
Out[5]= 0

In[6]:= Sign[-1.0]
Out[6]= -1

In[7]:= Sign[-1/Infinity]
Out[7]= 0

In[8]:= Sign[N[-0.0]]
Out[8]= 0
```

## MATLAB/Octave

MATLAB and Octave (an open source MATLAB-like environment) use IEEE-754 internally, but normalize all presentations of zero *except hex* to present as unsigned. So the environment *hides* the sign bit of negative zero, requiring a *backdoor* way such as bit manipulation to distinguish between the negative and positive zeros. Nonetheless, as these two representations of zero have different binary values, they break determinism.

```
x = -1 / Inf;
disp(x);
  0
disp(sign(x));
  0
format hex
disp(x);
  8000000000000000
u = typecast(x, 'uint64');
signBit = bitget(u, 64);
format default
disp(signBit);
  1
```

## R

Like Mathematica, R treats zero as a unique, unsigned value.

```
x <- -1 / Inf
print(x)                     # 0
print(identical(x, -0.0))    # TRUE
print(identical(x, 0.0))     # TRUE
print(sign(x))               # 0
print(identical(0.0, -0.0))  # TRUE
```

## SQL

All implementations of SQL, even if they use IEEE-754 internally, normalize negative zero to zero:

```
MariaDB [(none)]> SELECT 0.0, SIGN(0.0), -0.0, SIGN(-0.0);
+-----+-----------+------+------------+
| 0.0 | SIGN(0.0) | -0.0 | SIGN(-0.0) |
+-----+-----------+------+------------+
| 0.0 |         0 |  0.0 |          0 |
+-----+-----------+------+------------+
1 row in set (0.000 sec)
```

## Conclusion

The only form of zero that survives cleanly across serialization, inter-language calls, and memory models is `0`. Any system that permits `-0.0` to be encoded introduces a trapdoor of non-determinism.

Therefore, dCBOR is correct to normalize `-0.0` to `0x00`: Determinism demands it.

## Endnote 1

While the sign bit in the IEEE-754 floating-point representation of zero can technically encode information potentially useful in certain niche numerical analysis contexts (e.g., indicating limit directionality or handling branch cuts in complex functions), its practical necessity and consistent implementation across diverse systems are questionable. Notably, highly sophisticated mathematical environments such as Mathematica and R, designed for complex computations, deliberately treat zero as a unique, unsigned value, lacking any concept of negative zero. Their ability to perform advanced mathematics without preserving or relying on a distinct `-0.0` strongly suggests that this artifact is neither universally required nor fundamental, even in demanding computational fields. Furthermore, as demonstrated in the main text, the handling of `-0.0` is inconsistent across system boundaries, particularly during serialization (e.g., `JSON.stringify()` behavior). Attempting to maintain the `-0.0` distinction in a generalized, interoperable format thus introduces a fragile dependency and a clear risk of non-determinism. Consequently, for robust formats like dCBOR that prioritize deterministic and canonical representations essential for interoperability and verification, normalizing `-0.0` to the single, unambiguous value of `0` is the necessary approach to ensure predictable behavior and avoid reliance on this non-universally supported and inconsistently handled artifact.

---

I am the author of this paper. Thoughts?
