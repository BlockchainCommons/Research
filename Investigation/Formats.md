# Formats

This is a catalog of various formats for blockchain-related things that we might want to publish or even specify in the future or for compatibility in projects like Gordian Seed Tool.

## Seed Formats

* QR Code of Recovery Words
   * See https://github.com/BlockchainCommons/GordianSeedTool-iOS/issues/66
   * Numbered lists of words and bare words have both been used
* QR Code, Encrypting Recovery Words
   * See https://github.com/BlockchainCommons/GordianSeedTool-iOS/issues/67#issuecomment-1055827481
   * See https://anderson-arlen.github.io/cryptoseed/
   * "Your recovery seed is encrypted with the Cipher Block Chaining (CBC) mode of the Advanced Encryption Standard with a 256 bit key length. Your key is generated using a password of your choice and a random salt, hashed 1 million times with pbkdf2 (sha512). Encrypting the same data with the same key will yield a different result every time."
* 7zip of Backup
   * See https://github.com/BlockchainCommons/GordianSeedTool-iOS/issues/138#issuecomment-1048477394
   * For Foundation Devices, Backup is Encrypted with 6 Bytewords separated by spaces
   * ColdCard uses a similar methodology
