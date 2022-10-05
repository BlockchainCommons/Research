# Blockchain Commons Research

![](images/logos/bcc-research-screen.jpg)

This repository contains research and proposals of interest to the blockchain community.

## Contents

| Number                    | Title         | Version | Owner                                                  |
|---------------------------|---------------|---------|----------------------------------------------|
| [BCR-2020-001](papers/bcr-2020-001-entropy-to-seed.md) | Uniformly Translating Entropy into Cryptographic Seeds | 1.0.0 | Wolf McNally |
| [BCR-2020-002](papers/bcr-2020-002-bech32-seed-format.md) | Bech32 Encoding for Cryptographic Seeds | 1.0.0 | Wolf McNally |
| [BCR-2020-003](papers/bcr-2020-003-uri-binary-compatibility.md) | Encoding Binary Compatibly with URI Reserved Characters  | 1.0.0 | Wolf McNally |
| [BCR-2020-004](papers/bcr-2020-004-bc32.md) | The BC32 Data Encoding Format  | 1.0.0 | Wolf McNally |
| [BCR-2020-005](papers/bcr-2020-005-ur.md) | Uniform Resources (UR): Encoding Structured Binary Data for Transport in URIs and QR Codes  | 2.0.1 | Wolf McNally |
| [BCR-2020-006](papers/bcr-2020-006-urtypes.md) | Registry of Uniform Resource (UR) Types  | 1.0.0 | Wolf McNally |
| [BCR-2020-007](papers/bcr-2020-007-hdkey.md) | UR Type Definition for Hierarchical Deterministic (HD) Keys  | 1.0.0 | Wolf McNally |
| [BCR-2020-008](papers/bcr-2020-008-eckey.md) | UR Type Definition for Elliptic Curve (EC) Keys  | 1.0.0 | Wolf McNally |
| [BCR-2020-009](papers/bcr-2020-009-address.md) | UR Type Definition for Cryptocurrency Addresses  | 1.0.0 | Wolf McNally |
| [BCR-2020-010](papers/bcr-2020-010-output-desc.md) | UR Type Definition for Bitcoin Output Descriptors | 1.0.0 | Wolf McNally |
| [BCR-2020-011](papers/bcr-2020-011-sskr.md) | UR Type Definition for Sharded Secret Key Reconstruction (SSKR) | 1.0.1 | Wolf McNally |
| [BCR-2020-012](papers/bcr-2020-012-bytewords.md) | Bytewords: Encoding binary data as English words | 1.0.0 | Wolf McNally |
| [BCR-2020-013](papers/bcr-2020-013-crc32-cbor-tag.md) | CRC-32 Checksums in CBOR | 1.0.0 | Wolf McNally |
| [BCR-2020-014](papers/bcr-2020-014-urs-on-epaper.md) | URs on E-paper display | 1.0.0 | Gorazd Kovacic |
| [BCR-2020-015](papers/bcr-2020-015-account.md) | UR Type Definition for BIP44 Accounts | 1.0.0 | Craig Raw |
| [BCR-2021-001](papers/bcr-2021-001-request.md) | UR Type Definitions for Transactions Between Airgapped Devices | 1.0.0 | Wolf McNally |
| [BCR-2021-002](papers/bcr-2021-002-digest.md) | Digests for Digital Objects | 1.0.0 | Wolf McNally |
| [BCR-2022-001](papers/bcr-2022-001-secure-message.md) | Secure Messages | 1.0.0 | Wolf McNally |
| [BCR-2022-002](papers/bcr-2022-002-cid-common-identifier.md) | CID: Common Identifier | 0.1.0 | Wolf McNally |


_Also see our [Testimony](https://github.com/BlockchainCommons/Testimony/blob/master/README.md) and our [Wallet Improvement Proposals](https://github.com/BlockchainCommons/wips/blob/master/README.md)._

### BCR Number

Please number all Bitcoin Research BCRs with a four-digit number representing the current year (`YYYY`) followed by a three-digit sequence number for that year (`SSS`). For example: `bcr-2020-001` is the first BCR for 2020, `bcr-2020-017` is the 17th, and `bcr-2021-001` is the first BCR for 2021.

_Note that the sequence number reverts to 001 at the start of each year._

### BCR Title

Please be sure that your title is concise, yet informative.

### BCR Version

When updating BCRs, please use [semantic versioning](https://semver.org/) for your version number.

Most briefly: your version number should be of the form X.Y.Z, where `X` is the major number ("0" for a BCR in progress; "1" for a fully drafted BCR; and "2" or higher for a new version that has introduced a backward-incompatible change), `Y` is the minor number (for a backward-compatible new feature), and `Z` is the patch number (for fixing typos and making other clarifications that don't fundamentally change what the BCR means).

But please consult the semantic versioning document for more information and adjust appropriately for the fact that these are textual BCRs, not software.

### BCR Owner

Please list the person primarily responsible for the BCR, and moving it forward, as the owner. If there are multiple authors, they should be listed on the BCR itself, not on this overview.

## Origin, Authors, Copyright & Licenses

Unless otherwise noted (either in this [/README.md](./README.md) or in the file's header comments) the contents of this repository are Copyright © 2020 by Blockchain Commons, LLC, and are [licensed](./LICENSE) under the [spdx:BSD-2-Clause Plus Patent License](https://spdx.org/licenses/BSD-2-Clause-Patent.html).

## Financial Support

This research is a project of [Blockchain Commons](https://www.blockchaincommons.com/). We are proudly a "not-for-profit" social benefit corporation committed to open source & open development. Our work is funded entirely by donations and collaborative partnerships with people like you. Every contribution will be spent on building open tools, technologies, and techniques that sustain and advance blockchain and internet security infrastructure and promote an open web.

To financially support further development of this research and other projects, please consider becoming a Patron of Blockchain Commons through ongoing monthly patronage as a [GitHub Sponsor](https://github.com/sponsors/BlockchainCommons). You can also support Blockchain Commons with bitcoins at our [BTCPay Server](https://btcpay.blockchaincommons.com/).

## Contributing

We encourage public contributions through issues and pull requests! Please review [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our development process. All contributions to this repository require a GPG signed [Contributor License Agreement](./CLA.md).

### Discussions

The best place to talk about Blockchain Commons and its projects is in our GitHub Discussions areas.

[**Gordian Developer Community**](https://github.com/BlockchainCommons/Gordian-Developer-Community/discussions). For standards and open-source developers who want to talk about interoperable wallet specifications, please use the Discussions area of the [Gordian Developer Community repo](https://github.com/BlockchainCommons/Gordian-Developer-Community/discussions). This is where you talk about Gordian specifications such as [Gordian Envelope](https://github.com/BlockchainCommons/BCSwiftSecureComponents/blob/master/Docs/00-INTRODUCTION.md), [bc-shamir](https://github.com/BlockchainCommons/bc-shamir), [Sharded Secret Key Reconstruction](https://github.com/BlockchainCommons/bc-sskr), and [bc-ur](https://github.com/BlockchainCommons/bc-ur) as well as the larger [Gordian Architecture](https://github.com/BlockchainCommons/Gordian/blob/master/Docs/Overview-Architecture.md), its [Principles](https://github.com/BlockchainCommons/Gordian#gordian-principles) of independence, privacy, resilience, and openness, and its macro-architectural ideas such as functional partition (including airgapping, the original name of this community).

[**Blockchain Commons Discussions**](https://github.com/BlockchainCommons/Community/discussions). For developers, interns, and patrons of Blockchain Commons, please use the discussions area of the [Community repo](https://github.com/BlockchainCommons/Community) to talk about general Blockchain Commons issues, the intern program, or topics other than those covered by the [Gordian Developer Community](https://github.com/BlockchainCommons/Gordian-Developer-Community/discussions) or the 
[Gordian User Community](https://github.com/BlockchainCommons/Gordian/discussions).
### Other Questions & Problems

As an open-source, open-development community, Blockchain Commons does not have the resources to provide direct support of our projects. Please consider the discussions area as a locale where you might get answers to questions. Alternatively, please use this repository's [issues](./issues) feature. Unfortunately, we can not make any promises on response time.

If your company requires support to use our projects, please feel free to contact us directly about options. We may be able to offer you a contract for support from one of our contributors, or we might be able to point you to another entity who can offer the contractual support that you need.

### Credits

The following people directly contributed to this repository. You can add your name here by getting involved. The first step is learning how to contribute from our [CONTRIBUTING.md](./CONTRIBUTING.md) documentation.

| Name              | Role                | Github                                            | Email                                 | GPG Fingerprint                                    |
| ----------------- | ------------------- | ------------------------------------------------- | ------------------------------------- | -------------------------------------------------- |
| Christopher Allen | Principal Architect | [@ChristopherA](https://github.com/ChristopherA) | \<ChristopherA@LifeWithAlacrity.com\> | FDFE 14A5 4ECB 30FC 5D22  74EF F8D3 6C91 3574 05ED |
| Wolf McNally      | Contributor        | [@WolfMcNally](https://github.com/wolfmcnally)    | \<Wolf@WolfMcNally.com\>              | 9436 52EE 3844 1760 C3DC  3536 4B6C 2FCF 8947 80AE |

## Responsible Disclosure

We want to keep all of our software safe for everyone. If you have discovered a security vulnerability, we appreciate your help in disclosing it to us in a responsible manner. We are unfortunately not able to offer bug bounties at this time.

We do ask that you offer us good faith and use best efforts not to leak information or harm any user, their data, or our developer community. Please give us a reasonable amount of time to fix the issue before you publish it. Do not defraud our users or us in the process of discovery. We promise not to bring legal action against researchers who point out a problem provided they do their best to follow the these guidelines.

### Reporting a Vulnerability

Please report suspected security vulnerabilities in private via email to ChristopherA@BlockchainCommons.com (do not use this email for support). Please do NOT create publicly viewable issues for suspected security vulnerabilities.

The following keys may be used to communicate sensitive information to developers:

| Name              | Fingerprint                                        |
| ----------------- | -------------------------------------------------- |
| Christopher Allen | FDFE 14A5 4ECB 30FC 5D22  74EF F8D3 6C91 3574 05ED |

You can import a key by running the following command with that individual’s fingerprint: `gpg --recv-keys "<fingerprint>"` Ensure that you put quotes around fingerprints that contain spaces.
