# Bytewords: Encoding binary data as English words

## BCR-2020-012

**© 2020 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: June 20, 2020<br/>
Revised: October 4, 2020

### Introduction

Schemes like [BIP39] and [SLIP39] (see Appendix) encode a binary string as a series of human-readable words. This proposal specifies a scheme "Bytewords" with similar ends but:

* Encodes a [CBOR] structure tagged with the data type [URTYPES], and is therefore self-describing.
* Uses a dictionary of exactly 256 English words with a uniform word size of 4 letters.
* Only two letters of each word (the first and last) are required to uniquely identify each byte value, making a minimal Bytewords encoding as efficient as hexadecimal (2 characters per byte) and yet less error prone.
* Additionally, words can be uniquely identified by their first three letters or last three letters.
* Representing each byte as a single word simplifies encoder and decoder architecture.
* Minimizing the number of letters for each word simplifies transfer to permanent media such as stamped metal.
* Using only ASCII letters (and a separator character, either space or hyphen) preserves compatibility with URI and QR code character sets.
* Provides a four-word sequence at the end as a checksum of the entire sequence.

### Word selection criteria

* All words are English.
* All words are exactly 4 ASCII letters.
* No proper names.
* Prefer words in common usage.
* Avoid homophones and near homophones.
* Prefer two-syllable words.
* Each word's first three letters must be a unique sequence (XXX-).
* Each word's last three letters must be a unique sequence (-XXX).
* Each word's first and last letters must be a unique sequence (X--X).
* The Damerau-Levenshtein distance between any two words is at least 2.
* Prefer words with positive connotations.
* Prefer words which are "interesting" (strong emotional valence) even if connotation is neutral or slightly negative.
* Avoid words with strong negative connotations.
* Represent initial letters somewhat equally when possible.
* Word list is sorted alphabetically.

### Word List

```
0x00: able acid also apex aqua arch atom aunt
0x08: away axis back bald barn belt beta bias
0x10: blue body brag brew bulb buzz calm cash
0x18: cats chef city claw code cola cook cost
0x20: crux curl cusp cyan dark data days deli
0x28: dice diet door down draw drop drum dull
0x30: duty each easy echo edge epic even exam
0x38: exit eyes fact fair fern figs film fish
0x40: fizz flap flew flux foxy free frog fuel
0x48: fund gala game gear gems gift girl glow
0x50: good gray grim guru gush gyro half hang
0x58: hard hawk heat help high hill holy hope
0x60: horn huts iced idea idle inch inky into
0x68: iris iron item jade jazz join jolt jowl
0x70: judo jugs jump junk jury keep keno kept
0x78: keys kick kiln king kite kiwi knob lamb
0x80: lava lazy leaf legs liar limp lion list
0x88: logo loud love luau luck lung main many
0x90: math maze memo menu meow mild mint miss
0x98: monk nail navy need news next noon note
0xa0: numb obey oboe omit onyx open oval owls
0xa8: paid part peck play plus poem pool pose
0xb0: puff puma purr quad quiz race ramp real
0xb8: redo rich road rock roof ruby ruin runs
0xc0: rust safe saga scar sets silk skew slot
0xc8: soap solo song stub surf swan taco task
0xd0: taxi tent tied time tiny toil tomb toys
0xd8: trip tuna twin ugly undo unit urge user
0xe0: vast very veto vial vibe view visa void
0xe8: vows wall wand warm wasp wave waxy webs
0xf0: what when whiz wolf work yank yawn yell
0xf8: yoga yurt zaps zero zest zinc zone zoom
```

#### Distribution of initial letters

| letter | count |
|--------|-------|
| a | 10 |
| b | 12 |
| c | 14 |
| d | 13 |
| e | 9 |
| f | 15 |
| g | 13 |
| h | 12 |
| i | 9 |
| j | 10 |
| k | 10 |
| l | 15 |
| m | 11 |
| n | 8 |
| o | 7 |
| p | 11 |
| q | 2 |
| r | 12 |
| s | 13 |
| t | 13 |
| u | 5 |
| v | 9 |
| w | 12 |
| x | 0 |
| y | 5 |
| z | 6 |

### Checksum

The CBOR body of an encoded Bytewords sequence is followed by a four-word (four byte, 32 bit) CRC32 checksum in network order (big-endian).

The choice to use a CRC32 hash of a Bytewords body is open for comment. This issue is being tracked [here](https://github.com/BlockchainCommons/Research/issues/23).

### Example/Test Vector

* A 16 byte (128-bit) cryptographic seed (`seed`) (tag #6.40300) [URTYPES] generated on May 13, 2020, in the CBOR diagnostic notation:

```
40300({
  1: h'c7098580125e2ab0981253468b2dbc52', / payload /
  2: 1(18394) / birthdate /
})
```

* Encoded as binary using [CBOR-PLAYGROUND]:

```
D9 9D6C                                 # tag(40300) seed
   A2                                   # map(2)
      01                                # unsigned(1) payload:
      50                                # bytes(16)
         C7098580125E2AB0981253468B2DBC52
      02                                # unsigned(2) birthdate:
      C1                                # tag(1) [CBOR-DATE]
         19 47DA                        # unsigned(18394)
```

* Body as a hex string:

```
d99d6ca20150c7098580125e2ab0981253468b2dbc5202c11947da
```

* CRC32 Checksum:

```
c904f40b
```

* Body with checksum appended:

```
d99d6ca20150c7098580125e2ab0981253468b2dbc5202c11947dac904f40b
```

* Bytewords:

```
tuna next jazz oboe acid good slot axis limp lava
brag holy door puff monk brag guru frog luau drop
roof grim also safe chef fuel twin solo aqua work
bald
```

* Bytewords (URI compatible):

```
tuna-next-jazz-oboe-acid-good-slot-axis-limp-lava-
brag-holy-door-puff-monk-brag-guru-frog-luau-drop-
roof-grim-also-safe-chef-fuel-twin-solo-aqua-work-
bald
```

* Bytewords (minimal encoding, only first and last letters of each word):

```
tantjzoeadgdstaslplabghydrpfmkbggufgludprfgmaosecffltnsoaawkbd
```

### Brutal Encoding

Unlike the "standard" encoding described above, where the encoded message is CBOR and is therefore self-describing, Bytewords can also be used to encode arbitrary byte sequences with no defined internal structure except for the last four words being the checksum. The advantage of this "brutal" encoding is brevity. The disadvantage is that it is up to the user to keep track of the type of information encoded and ensure that it is interpreted correctly.

For example, the seed payload used in the example above:

```
c7098580125e2ab0981253468b2dbc52
```

can be concatenated with the four-byte checksum of the payload as described above:

```
feac0dea
```

to yield:

```
c7098580125e2ab0981253468b2dbc52feac0dea
```

And then encoded as Bytewords:

```
slot axis limp lava brag holy door puff monk brag
guru frog luau drop roof grim zone plus belt wand
```

Or encoded as minimal Bytewords:

```
staslplabghydrpfmkbggufgludprfgmzepsbtwd
```

It is recommended that if Bytewords is used in the brutal encoding mode, that some other metadata, such as a URI scheme, be present to guide in interpreting the payload, e.g.:

```
my-seed:slot-axis-limp-lava-brag-holy-door-puff-monk-brag-guru-frog-luau-drop-roof-grim-zone-plus-belt-wand
```

or

```
my-seed:staslplabghydrpfmkbggufgludprfgmzepsbtwd
```

### References

* [URTYPES] [BCR-0006: Registry of Uniform Resource (UR) Types
](bcr-0006-urtypes.md)
* [BC32] [BCR-2020-004: The BC32 Data Encoding Format](bcr-2020-004-bc32.md)
* [BIP39] [BIP-0039: Mnemonic code for generating deterministic keys](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
* [BIP39WORDS] [BIP-0039 Multilingual Word Lists](https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md)
* [CBOR] [Concise Binary Object Representation (CBOR)](https://tools.ietf.org/html/rfc7049)
* [CBOR-DATE] [Concise Binary Object Representation (CBOR) Tags for Date](https://datatracker.ietf.org/doc/draft-ietf-cbor-date-tag/)
* [CBOR-PLAYGROUND] [CBOR Playground](http://cbor.me)
* [CRC32] [MSDN: 32-Bit CRC Algorithm](https://docs.microsoft.com/en-us/openspecs/office_protocols/ms-abs/06966aa2-70da-4bf9-8448-3355f277cd77)
* [SLIP39] [SLIP-0039: Shamir's Secret-Sharing for Mnemonic Codes](https://github.com/satoshilabs/slips/blob/master/slip-0039.md)
* [SLIP39WORDS] [SLIP-0039: Word List](https://github.com/satoshilabs/slips/blob/master/slip-0039/wordlist.txt)

## Appendix

### Analysis of BIP-39

In the case of BIP-39, the binary string is broken up into 11-bit words and encoded using a 2,048-word dictionary. The words are according the following criteria:

> An ideal wordlist has the following characteristics:
>
> a) smart selection of words
>
>    - the wordlist is created in such way that it's enough to type the first four letters to unambiguously identify the word
>
> b) similar words avoided
>
>    - word pairs like "build" and "built", "woman" and "women", or "quick" and "quickly" not only make remembering the sentence difficult, but are also more error prone and more difficult to guess
>
> c) sorted wordlists
>
>    - the wordlist is sorted which allows for more efficient lookup of the code words (i.e. implementations can use binary search instead of linear search)
>    - this also allows trie (a prefix tree) to be used, e.g. for better compression

In addition, BIP-39 word lists are available in several other languages, each of which was constructed by rules described in [BIP39WORDS].

### Analysis of SLIP-39

In the case of SLIP-39, the binary string is broken up into 10-bit words and encoded using a 1,024-word dictionary [SLIP39WORDS]. The words are according the following criteria:

>    * The wordlist is alphabetically sorted.
>    * No word is shorter than 4 letters.
>    * No word is longer than 8 letters.
>    * All words begin with a unique 4-letter prefix.
>    * The wordlist contains only common English words (+ the word "satoshi").
>    * The minimum Damerau-Levenshtein distance between any two words is at least 2.
>    * The similarity between the pronunciation of any two words has been minimized.

### Analysis of BC32

In the case of [BC32], the binary string is broken up into 5-bit letters and encoded using a limited 32-character subset of ASCII that is compatible both with QR Code alphanumeric mode and URI unreserved characters. Six characters (30 bits) of checksum are added at the end.

## Version History

### October 4, 2020:

* Fix for [https://github.com/BlockchainCommons/Research/issues/45](wordlist alphabetization error).
