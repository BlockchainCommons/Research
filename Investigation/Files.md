# Crypto Files
The following is a discussion of files used with cryptography, covering both file names and file formats. It's not intended as a specification, but instead a survey of current methodologies. We are seeking discussion of this and other elements related to crypto-files, to create a community specification at some point in the future.

## File Names

### Colcard: Backup Files

[pending]

### Passport: Backup Files

[Passport](https://foundationdevices.com/passport/) Backup Files have file name format of:

`Master Fingerprint - backup - Backup #.7z`

* **Master Fingerprint** — The Hash 160 of the master public key.
* **Backup #** — The incrementing number of the backup.

**Example:**
```
604b93f2-backup-1.7z
```

Passport Backup Files uncompress to:
``passport-backup.txt``

### Gordian Seed Tool: Data Files

[Gordian Seed Tool](https://github.com/BlockchainCommons/GordianSeedTool-iOS) outputs a variety of individual text and image data. They follow a consistent name scheme to allow easy sorting and lookup of data.

#### Seed Data Files
The general format for a seed file name is:

`Seed Id - Seed Name - (optionally) Request or Response - Type - Format.filetype`

* **Seed ID** — The first 7 digits of the SHA256 digest of the object.
* **Seed Name** — Randomly created or user-selected name for object. Space separated.
* **Request or Response** (optional) — Whether the file is a `ur:crypto-request` or `ur:crypto-response`.
* **Type** — The type of object, in this case, "Seed" for a Seed or "SSKR" for the shares of a Seed. 
* **Format** — Output format, including "BIP39", "ByteWords", "Hex", "Identifier-Hex", "Lifehash", "Name" or "UR". Note that URs can be encoded as plain text (with a ".txt" suffix) or a QR code (with a ".jpg" suffix). 

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

`Seed Id - [Group # _ Share #] - Checksum Words - Type - Format.filetype`

* **Seed ID** — The first 7 digits of the SHA256 digest of the object.
* **Group #** — Number of Share Group (usually "group1").
* **Share #** — Share number "of" total shares in group.
* **Checksum Words** — Bytewords for the final four words, which are checksums in the SSKR share. Space separated.
* **Type** — The type of object, in this case "SSKR" for the shares of a Seed. 
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
`Seed Id - Key ID - HDKey from Seed Name - (optionally) Request or Response - Type - [Derivation Path] - Format.filetype`

* **Seed ID** — The first 7 digits of the SHA256 digest of the object.
* **Key ID** — The first 7 digits of the SHA256 digest of the object.
* **HDKey from Seed Name** — The prefix "HDKey from" prepended to randomly created or user-selected name for seed. Space separated.
* **Request or Response** (optional) — Whether the file is a `ur:crypto-request` or `ur:crypto-response`.
* **Type** — The type of object, in this case "PrivateHDKey" or "PublicHDKey".
* **Derivation Path** — [Master Fingerprint (optionally) _ Path] _ (optionally) Fingerprint
   * **Master Fingerprint** — The Hash 160 of the master public key.
   * **Path** — The derivation path, using "h" for hardened. Underscore separated. Not used for Master Key.
   * **Fingerprint** — The Hash 160 of the derived key. Not used for Master Key.
* **Format** — Output format, including "Base58", "Detail", "Identifier-Hex", "Lifehash", "Name" "UR". Note that URs can be encoded as plain text (with a ".txt" suffix) or a QR code (with a ".jpg" suffix). 

**Examples of Master Keys:**
```
ffa11a8-5db8946-HDKey from Yinmn Blue Puff-PrivateHDKey-[604b93f2]-Base58.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Puff-PrivateHDKey-[604b93f2]-UR.txt
ffa11a8-bcab0a2-HDKey from Yinmn Blue Puff-PublicHDKey-[604b93f2]-Base58.txt
ffa11a8-bcab0a2-HDKey from Yinmn Blue Puff-PublicHDKey-[604b93f2]-Lifehash.png
ffa11a8-bcab0a2-HDKey from Yinmn Blue Puff-PublicHDKey-[604b93f2]-Name.txt
ffa11a8-bcab0a2-HDKey from Yinmn Blue Puff-PublicHDKey-[604b93f2]-UR.png
ffa11a8-bcab0a2-HDKey from Yinmn Blue Puff-PublicHDKey-[604b93f2]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Puff-Request-PrivateHDKey-[604b93f2]-UR.txt
```

**Examples of Other Key Derivations:**

```
ffa11a8-607bf2a-HDKey from Yinmn Blue Puff-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-Base58.txt
ffa11a8-607bf2a-HDKey from Yinmn Blue Puff-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-Lifehash.png
ffa11a8-607bf2a-HDKey from Yinmn Blue Puff-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-UR.txt
ffa11a8-607bf2a-HDKey from Yinmn Blue Puff-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-UR.png
ffa11a8-607bf2a-HDKey from Yinmn Blue Puff-Request-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-UR.txt
ffa11a8-607bf2a-HDKey from Yinmn Blue Puff-Response-PublicHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-UR.txt
ffa11a8-8183ac1-HDKey from Yinmn Blue Puff-PrivateHDKey-[604b93f2_84h_0h_0h]_fac272cd-Base58.txt
ffa11a8-8183ac1-HDKey from Yinmn Blue Puff-PrivateHDKey-[604b93f2_84h_0h_0h]_fac272cd-Lifehash.png
ffa11a8-8183ac1-HDKey from Yinmn Blue Puff-PrivateHDKey-[604b93f2_84h_0h_0h]_fac272cd-UR.png
ffa11a8-db9b01e-HDKey from Yinmn Blue Puff-PublicHDKey-[604b93f2_84h_0h_0h]_fac272cd-Base58.txt
ffa11a8-db9b01e-HDKey from Yinmn Blue Puff-PublicHDKey-[604b93f2_84h_0h_0h]_fac272cd-UR.png
ffa11a8-db9b01e-HDKey from Yinmn Blue Puff-PublicHDKey-[604b93f2_84h_0h_0h]_fac272cd-UR.txt
ffa11a8-dc0c061-HDKey from Yinmn Blue Puff-PrivateHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-Base58.txt
ffa11a8-dc0c061-HDKey from Yinmn Blue Puff-PrivateHDKey-[604b93f2_48h_0h_0h_2h]_9ff1237f-Lifehash.png
```

### Address Data Files

The general format for an address file name is:
`Seed Id - Key ID - Address from Seed Name - Type - [Derivation Path] - (optionally)Format.filetype`

* **Seed ID** — The first 7 digits of the SHA256 digest of the object.
* **Key ID** — The first 7 digits of the SHA256 digest of the object.
* **Address from Seed Name** — The prefix "Address from" prepended to randomly created or user-selected name for seed. Space separated.
* **Type** — The type of object, in this case "Address".
* **Derivation Path** — [Master Fingerprint (optionally) _ Path] _ (optionally) Fingerprint
   * **Master Fingerprint** — The Hash 160 of the master public key.
   * **Path** — The derivation path, using "h" for hardened. Underscore separated. Not used for Master Key.
   * **Fingerprint** — The Hash 160 of the derived key. Not used for Master Key.
* **Format** — Output format, including "Lifehash" or "Name". If there is no Format, this is a plain address, either formatted in hex (as a .txt file) or in a QR (as a .png file).

**Examples of Master Key Addresses:**
```
ffa11a8-5db8946-Address from Yinmn Blue Puff-Address-[604b93f2]-Lifehash.png
ffa11a8-5db8946-Address from Yinmn Blue Puff-Address-[604b93f2]-Name.txt
ffa11a8-5db8946-Address from Yinmn Blue Puff-Address-[604b93f2].png
ffa11a8-5db8946-Address from Yinmn Blue Puff-Address-[604b93f2].txt
```

**Examples of Other Addresses:**
```
ffa11a8-8183ac1-Address from Yinmn Blue Puff-Address-[604b93f2_84h_0h_0h]_fac272cd.txt
ffa11a8-dc0c061-Address from Yinmn Blue Puff-Address-[604b93f2_48h_0h_0h_2h]_9ff1237f-Lifehash.png
ffa11a8-dc0c061-Address from Yinmn Blue Puff-Address-[604b93f2_48h_0h_0h_2h]_9ff1237f-Name.txt
ffa11a8-dc0c061-Address from Yinmn Blue Puff-Address-[604b93f2_48h_0h_0h_2h]_9ff1237f.txt
```
### Output Data Files

Output data files contain a descriptor for a specific key derivation. They are derived from the master key. The general format for output file names is:

`Seed Id - Key ID - HDKey from Seed Name - Type - [Master Fingprint _ Descriptor Type _ Account # _ Output Type _ Descriptor Checksum] - Format.filetype`

* **Seed ID** — The first 7 digits of the SHA256 digest of the object.
* **Key ID** — The first 7 digits of the SHA256 digest of the object.
* **HDKey from Seed Name** — The prefix "HDKey from" prepended to randomly created or user-selected name for seed. Space separated.
* **Type** — The type of object, in this case "Output".
* **Master Fingerprint** — The Hash 160 of the master public key.
* **Account #** — The number of the account.
* **Output Type — A textual descriptor of the derivation path, currently: "legacy", "legacymultisig", "nested", "nestedmultisig", "segwit", "segwitmultisig", or "taproot".
* **Descriptor Checksum** — A [checksum for the descriptor](https://github.com/bitcoin/bitcoin/blob/master/doc/descriptors.md#checksums), as can also be described by `bitcoin-cli getdescriptorinfo`.
* **Format** — Output format, which is "UR". Formatted as textual UR (in a .txt file) or as a QR (in a .png file).

**Examples:**
```
ffa11a8-5db8946-HDKey from Yinmn Blue Puff-Output-[604b93f2_legacy_0_frs22d0f]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Puff-Output-[604b93f2_legacymultisig_0_vwnxudyw]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Puff-Output-[604b93f2_nested_0_cmyxclfa]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Puff-Output-[604b93f2_nestedmultisig_0_ycs6cu6j]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Puff-Output-[604b93f2_segwit_0_ncwysjuk]-UR.png
ffa11a8-5db8946-HDKey from Yinmn Blue Puff-Output-[604b93f2_segwit_0_ncwysjuk]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Puff-Output-[604b93f2_segwitmultisig_0_wmsu2266]-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Puff-Output-[604b93f2_taproot_0_nay7kr6q]-UR.txt
```

### Account Data Files

Account data files contain several popular output descriptors. The general format for account file names is:

`Seed Id - Key ID - HDKey from Seed Name - Type - Account # - Format.filetype`

* **Seed ID** — The first 7 digits of the SHA256 digest of the object.
* **Key ID** — The first 7 digits of the SHA256 digest of the object.
* **HDKey from Seed Name** — The prefix "HDKey from" prepended to randomly created or user-selected name for seed. Space separated.
* **Type** — The type of object, in this case "Account".
* **Account #** — The number of the account.
* **Format** — Output format, which is "UR". Formatted as textual UR inas a .txt file) or as a QR (in a .png file).

**Examples:**
```
ffa11a8-5db8946-HDKey from Yinmn Blue Puff-Account-0-UR.txt
ffa11a8-5db8946-HDKey from Yinmn Blue Puff-Account-1-UR.txt
```

## Encryption

### Coldcard: Backup Files

[pending]

### Passport: Backup Files

Passport backup files are 7zipped and encrypted with six space-separated Bytewords.

## Contents

### Coldcard: Backup Files

[pending]

### Passport: Backup Files

Passport backup files contains a variety of key-value information in a plain text format:
```
# Passport backup file! DO NOT CHANGE.

# Private Key Details: Bitcoin
mnemonic = "fly mule excess resource treat plunge nose soda reflect adult ramp planet"
chain = "BTC"
xfp = "604B93F2"
xprv = "xprv9s21ZrQH143K4Mnjc7E8rpSMf8JB1XWmojYf7Ndk6zcNSbUYBsvTqJcdzTok1XwYcgytn5CRxtwhHu93NNXNQwGUbBqL3AHHZZrtKpEvmww"
xpub = "xpub661MyMwAqRbcGqsCi8m9DxP6DA8fQzEdAxUFum3MfL9MKPogjREiP6w7qjaeHuDUGuVmgCFf5iMntcyVoHsEFMKoxo7UxMpmafjeQofQezj"
raw_secret = "8059f2293a5bce7d4de59e71b4207ac5d2"

# Firmware Version (informational):
fw_version = "1.0.8"
fw_date = "December 29, 2021"

# User Preferences:
setting.backup_num = 4
setting.backup_quiz = true
setting.chain = "BTC"
setting.next_addrs = {"0/None": 0, "0/7": 1}
setting.terms_ok = 1
setting.validated_ok = 1
setting.wallet_prog = {"deriv_path": "m/84'/0'/0'", "export_mode": "qr", "acct_info": [{"acct": 0, "deriv": "m/84'/0'/0'", "fmt": 7}], "sig_type": "single-sig", "exported": true, "addr_type": 7, "verified": false, "multisig_id": null, "acct_num": 0, "next_addr": 0, "sw_wallet": "BlueWallet"}
setting.words = true

# EOF
```

### Gordian Seed Tool: Data Files

Gordian Seed Tool contents are simple datums with data Type and Format specified in the filename. UR format content is in addition self-identifying, whether saved as a `ur:` text string or a QR code.
