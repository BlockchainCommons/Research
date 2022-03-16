# Crypto Files
The following is a discussion of files used with cryptography, covering both file names and file formats. It's not intended as a specification, but instead a survey of current methodologies. We are seeking discussion of this and other elements related to crypto-files, to create a community specification at some point in the future.
## File Names

### Data Files

[Gordian Seed Tool](https://github.com/BlockchainCommons/GordianSeedTool-iOS) outputs a variety of individual text and image data. They follow a consistent name scheme to allow easy sorting and lookup of data.

#### Seed Data Files
The general format for a seed file name is:

`Seed Id - Seed Name - (optionally) Request or Response - Type - (usually) Format.filetype`

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

### SSKR Share Files

If SSKR shares are instead exported to individual files, per share, the format is:

`Seed Id - [group # _ Share #] - Checksum Words -Type - Format.filetype`

* **Seed ID** — The first 7 digits of the SHA256 digest of the object.
* **Group #** — Number of Share Group (usually "group1").
* **Share #** — Share number "of" total shares in group.
* **Checksum Words** — Bytewords for the final four words, which are checksums, in the SSKR share.
* * **Type** — The type of object, in this case "SSKR" for the shares of a Seed. 
* **Format** — Output format, including ""ByteWords" or "UR". Note that URs can be encoded as plain text (with a ".txt" suffix) or a QR code (with a ".jpg" suffix.

**Examples:**
```
ffa11a8-[group1_1of3]-TRIP HAWK LUNG BELT-SSKR-ByteWords.txt
ffa11a8-[group1_1of3]-TRIP HAWK LUNG BELT-SSKR-UR.png
ffa11a8-[group1_1of3]-TRIP HAWK LUNG BELT-SSKR-UR.txt
ffa11a8-[group1_2of3]-CASH FIZZ MEMO PLAY-SSKR-ByteWords.txt
ffa11a8-[group1_2of3]-CASH FIZZ MEMO PLAY-SSKR-UR.png
ffa11a8-[group1_2of3]-CASH FIZZ MEMO PLAY-SSKR-UR.txt
ffa11a8-[group1_3of3]-ZERO CATS IRIS ROCK-SSKR-ByteWords.txt
ffa11a8-[group1_3of3]-ZERO CATS IRIS ROCK-SSKR-UR.png
ffa11a8-[group1_3of3]-ZERO CATS IRIS ROCK-SSKR-UR.txt
```
### Key Data Files

The general format for a key file name is:



Derivation-Request-PublicHDKey-[48h_0h_0h_2h]-UR.txt

ffa11a8-5db8946-Address from Yinmn Blue Acid Exam-Address-[604b93f2]-Lifehash.png
ffa11a8-5db8946-Address from Yinmn Blue Acid Exam-Address-[604b93f2]-Name.txt
ffa11a8-5db8946-Address from Yinmn Blue Acid Exam-Address-[604b93f2].png
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Account-0-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Output-[604b93f2_legacy_0_frs22d0f]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Output-[604b93f2_legacymultisig_0_vwnxudyw]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Output-[604b93f2_nested_0_cmyxclfa]-UR.png
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Output-[604b93f2_nested_0_cmyxclfa]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Output-[604b93f2_nested_0_cmyxclfa].txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Output-[604b93f2_nestedmultisig_0_ycs6cu6j]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Output-[604b93f2_segwit_0_ncwysjuk]-UR.png
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Output-[604b93f2_segwit_0_ncwysjuk]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Output-[604b93f2_segwitmultisig_0_wmsu2266]-UR.png
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Output-[604b93f2_segwitmultisig_0_wmsu2266]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Output-[604b93f2_segwitmultisig_0_wmsu2266].txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Output-[604b93f2_taproot_0_nay7kr6q]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-PrivateHDKey-[604b93f2]-Base58.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-PrivateHDKey-[604b93f2]-Lifehash.png
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-PrivateHDKey-[604b93f2]-Name.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-PrivateHDKey-[604b93f2]-UR.png
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-PrivateHDKey-[604b93f2]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Request-PrivateHDKey-[604b93f2]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Response-PrivateHDKey-[604b93f2]-UR.png
ffa11a8-5db8946-HDKey from Yinmn Blue Acid Exam-Response-PrivateHDKey-[604b93f2]-UR.txt
ffa11a8-607bf2a-HDKey from Yinmn Blue Acid Exam-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-Base58.txt
ffa11a8-607bf2a-HDKey from Yinmn Blue Acid Exam-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-Detail.txt
ffa11a8-607bf2a-HDKey from Yinmn Blue Acid Exam-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-Identifier-Hex.txt
ffa11a8-607bf2a-HDKey from Yinmn Blue Acid Exam-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-Lifehash.png
ffa11a8-607bf2a-HDKey from Yinmn Blue Acid Exam-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-Name.txt
ffa11a8-607bf2a-HDKey from Yinmn Blue Acid Exam-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-UR.png
ffa11a8-607bf2a-HDKey from Yinmn Blue Acid Exam-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-UR.txt
ffa11a8-607bf2a-HDKey from Yinmn Blue Acid Exam-Request-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-UR.txt
ffa11a8-607bf2a-HDKey from Yinmn Blue Acid Exam-Response-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-UR.txt

Notes from Wolf:
```
And exporting a key derived from that seed gives the following filename:
1c907cb-07bc595-HDKey from TestSeed-PrivateHDKey-[94b193eb_48h_0h_0h_2h]-3fb97f42-UR.txt
(seedID-keyID-name-type-[masterFingerprint_path]-fingerprint-format)
An Address derived from the seed:
1c907cb-07bc595-Address from TestSeed-Address-[94b193eb_48h_0h_0h_2h]-3fb97f42.txt
(seedID-keyID-name-type-[masterFingerprint_path]-fingerprint)
A ur:crypto-response returning the same seed:
1c907cb-TestSeed-Response-Seed-UR.txt
(seedID-name-type-format)
A printed PDF of an exported key:
1c907cb-c04e2df-HDKey from TestSeed-PrivateHDKey-[94b193eb_84h_0h_0h]-f168af3e.pdf
```
