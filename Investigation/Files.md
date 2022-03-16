# Crypto Files
The following is a discussion of files used with cryptography, covering both file names and file formats. It's not intended as a specification, but instead a survey of current methodologies. We are seeking discussion of this and other elements related to crypto-files, to create a community specification at some point in the future.
## File Names

### Data Files

[Gordian Seed Tool](https://github.com/BlockchainCommons/GordianSeedTool-iOS) outputs a variety of individual text and image data. They follow a consistent name scheme to allow easy sorting and lookup of data.

#### Seed Data Files
The general format for a seed file name is:

* **Seed ID** — The first 7 digits of the SHA256 digest of the object.
* **Seed Name** — Randomlly created or user-selected name for object.
* **Request or Response** (optional) — Whether the file is a `ur:crypto-request` or `ur:crypto-response`.
* **Type** — The type of object, in this case, "Lifehash" for a visual hash, "Seed" for Seed data, "Seed-Identifier" for the identifier for a Seed, "Seed-Name" for the name of a seed, or "SSKR" for the shares of a Seed. 
* **Format** (optional) - Output format, including "BIP39", "ByteWords", "Hex", or "UR". Note that URs can be encoded as plain text (with a ".txt" suffix) or a QR code (with a ".jpg" suffix. Unformatted text (such as "Seed-Name") and unformatted graphics (such as "Lifehash") do not have a Format.

**Examples:**
```
ffa11a8-Yinmn Blue Acid Exam-Request-Seed-UR.png
ffa11a8-Yinmn Blue Acid Exam-Request-Seed-UR.txt
ffa11a8-Yinmn Blue Acid Exam-Response-Seed-UR.png
ffa11a8-Yinmn Blue Acid Exam-Response-Seed-UR.txt
ffa11a8-Yinmn Blue Acid Exam-Seed-BIP39.txt
ffa11a8-Yinmn Blue Acid Exam-Seed-ByteWords.txt
ffa11a8-Yinmn Blue Acid Exam-Seed-Hex.txt
ffa11a8-Yinmn Blue Acid Exam-Seed-Identifier-Hex.txt
ffa11a8-Yinmn Blue Acid Exam-Seed-Lifehash.png
ffa11a8-Yinmn Blue Acid Exam-Seed-Name.txt
ffa11a8-Yinmn Blue Acid Exam-Seed-UR.png
ffa11a8-Yinmn Blue Acid Exam-Seed-UR.txt
ffa11a8-Yinmn Blue Acid Exam-SSKR-ByteWords.txt
ffa11a8-Yinmn Blue Acid Exam-SSKR-UR.txt
```

Notes from Wolf:
```
And exporting a key derived from that seed gives the following filename:
1c907cb-07bc595-HDKey from TestSeed-PrivateHDKey-[94b193eb_48h_0h_0h_2h]-3fb97f42-UR.txt
(seedID-keyID-name-type-[masterFingerprint_path]-fingerprint-format)
An SSKR share from a backup of the same seed:
1c907cb-[group1_1of3]-GRAY COLA LION EYES-SSKR-UR.txt
(seedID-[group_share]-name-type-format)
An Address derived from the seed:
1c907cb-07bc595-Address from TestSeed-Address-[94b193eb_48h_0h_0h_2h]-3fb97f42.txt
(seedID-keyID-name-type-[masterFingerprint_path]-fingerprint)
A ur:crypto-response returning the same seed:
1c907cb-TestSeed-Response-Seed-UR.txt
(seedID-name-type-format)
A printed PDF of an exported key:
1c907cb-c04e2df-HDKey from TestSeed-PrivateHDKey-[94b193eb_84h_0h_0h]-f168af3e.pdf
```
