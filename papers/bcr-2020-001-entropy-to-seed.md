# Uniformly Translating Entropy into Cryptographic Seeds
## BCR-2020-001

**© 2020 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: April 8, 2020<br/>
Revised: June 25, 2020

---

A simple scheme for uniformly translating human-provided entropy into a cryptographic seed is proposed. The goal is to suggest an approach that is easy to understand and to code in various programming languages, in order to maximize compatibility between implementations over time.

Existing third-party tools do *not* use this proposed system and instead use a variety of idiosyncratic approaches. It would be helpful if implementers standardized on a single approach.

**NOTE**: The strength of the resulting seed is still only as strong as the number of bits of entropy provided, and the method used to generate it. This proposal does not address this possible weakness one way or the other.

Any human-generated or entered entropy can be represented as an array of bytes. Entropy is generated and then entered in *input form units*:

* Binary digits (coin tosses)
* Decimal digits
* Die rolls
* Playing cards drawn from a shuffled deck
* Arbitrary integers in the range [0-255].

After each input form unit is syntax-checked, it is transformed into a binary representation in an array:

* Bits "011010" would translate to the byte array {0x00, 0x01, 0x01, 0x00, 0x01, 0x00}.
* Die rolls "123456" would translate to the byte array {0x01, 0x02, 0x03, 0x04, 0x05, 0x06}.
* The integers "36 24 51 58 71 47" would translate to the byte array {0x24, 0x18, 0x33, 0x3a, 0x47, 0x2f}.
* Playing cards use a simple function to convert the letter representation to an integer in [0-51]:
	* Suits are most-significant and have values: {"c": 0, "d": 1, "h": 2, "s": 3}
	* Ranks are least-significant and have values: {"a": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "t": 9, "j": 10, "q": 11, "k": 12}
	* So the binary representation of a card is `suit * 13 + rank`. So for example 5♥ would be: 2 * 13 + 4 = 30.
	* Card values are case-insensitive and can be entered or displayed in any case. If they are stored as text, canonically they are stored in lower case.

Once you have the byte array, perform SHA256 on it and use the resulting digest as a seed for a HKDF_SHA256-based RNG. Arbitrary amounts of random numbers can then be generated and used as seeds for other purposes like HD key derivation.

**⚠️ Warning:** The authors note that the seed used as input to this RNG algorithm should be used only once.

Benefits:

* The entire 8-bit range can be used for the entropy.
* There is no complex math or bit packing to do.
* Although entropy should be randomly generated, any UTF-8 string could be used if desired
* Bits("011010"), Base10("011010") and Ints("0 1 1 0 1 0") all represent the same entropy, simplifying the human interpretation of the syntax of an entropy string.
