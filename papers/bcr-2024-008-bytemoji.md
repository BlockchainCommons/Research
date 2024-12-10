# Bytemoji: Easy and quick digital object recognition using emojis

## BCR-2024-008

**© 2024 Blockchain Commons**

Authors: Wolf McNally, Christopher Allen<br/>
Date: December 7, 2024

### Introduction

Bytemoji is a curated set of 256 emojis that are chosen to be easily recognized and distinguished from each other, especially when used in combination. Bytemoji are intended to be used as a simple and quick way to visually identify objects in digital systems, for example, by converting a 32-bit hash (e.g., CRC-32 or truncated SHA-256) to its four corresponding Bytemojis.

Other ways to visually identify digital object include [ByteWords](bcr-2020-012-Bytewords.md), and [LifeHash](http://lifehash.info). Bytemoji combine the value of cryptographic hash visualization with easy display and handling as text.

Unlike ByteWords, Bytemoji are not intended to "round-trip" data between text and binary format, although this is technically possible.

### Example

Each line below represents a combination of four bytes, represented as Bytemojis.

💛 🚩 🐥 🫠<br/>
🧵 💀 🎂 🛟<br/>
💫 🤠 👆 😂<br/>
🪐 👔 👚 👻<br/>
🧸 🥚 🧀 🙀<br/>
👃 👄 🐬 🧄<br/>
🧦 🌽 🏠 🦆<br/>
🌐 🌭 🥺 🛑<br/>
🥁 🦞 🌹 🐢<br/>
😽 😐 🐺 🌀<br/>

#### Clustering

Although Bytemoji are chosen partly for their visual distinctness, they are not intended to be individually identifiable. Bytemoji should never be displayed in isolation: they should always displayed in clusters of four or more to represent cryptographic hashes. In addition, they should be clustered with other indicators of the digital object's unique identity, such as hex codes, ByteWords, or a LifeHash.

This clustering ensures sufficient visual distinction and reduces the risk of ambiguity, even if individual emojis may share some similar features. In this example, the Bytemojis, the ByteWords, and the raw hex representation are shown together, under the user's chosen name of the object:

```
**My First Cryptographic Seed**

🌊 😹 🌽 🐞
JUGS DELI GIFT WHEN
71 27 4d f1
```

This mix of modalities further increases the likelihood of accurate recognition and decreases the risk of confusion. It is also useful for accessibility, as it provides multiple ways to present the information via assistive technologies.

See our previous work on the [Object Identity Block (OIB)](bcr-2021-002-digest.md#object-identity-block) for more information on identifying digital objects.

### Selection Criteria

The byte sequences that encode emojis can become quite long and complex:

- Some emojis that render as a single glyph use several combining forms. For example, *“I am a witness”* takes 17 UTF-8 bytes!

👁️‍🗨️

- Some emojis are rendered as sequences of multiple glyphs, for example *"family: man, woman, girl, boy with various skin tones"* takes 28 UTF-8 bytes. Note that this is a *single* emoji!

👨🏿‍👩🏾‍👧🏽‍👦🏼

So to keep things simple while still providing a wide range of visual objects, we selected a set of 256 emojis that:

- All render as single glyphs.
- All have code points that serialize as 3 or 4 UTF-8 bytes.

In addition, we used these other selection criteria:

- All emojis are visually distinct, with maximally unique shapes and designs.
- All emojis must render on a wide range of platforms.
- Avoid emojis that are highly similar or could be easily confused.
- Avoid emojis that depend solely on color differences to be distinguished.
- Prefer emojis that read well at smaller sizes.
- Ensure that contrast is good when displayed on light or dark backgrounds.
- Exclude combining forms, skin tone modifiers, and gender modifiers.
- Ensure the set covers a wide range of themes and concepts.
- Prefer emojis with positive or neutral connotations.
- Avoid national, ideological, and controversial symbols.

### Bytemoji Table

|   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 😀 | 😂 | 😆 | 😉 | 🙄 | 😋 | 😎 | 😍 | 😘 | 😭 | 🫠 | 🥱 | 🤩 | 😶 | 🤨 | 🫥 |
| 1 | 🥵 | 🥶 | 😳 | 🤪 | 😵 | 😡 | 🤢 | 😇 | 🤠 | 🤡 | 🥳 | 🥺 | 😬 | 🤑 | 🙃 | 🤯 |
| 2 | 😈 | 👹 | 👺 | 💀 | 👻 | 👽 | 😺 | 😹 | 😻 | 😽 | 🙀 | 😿 | 🫶 | 🤲 | 🙌 | 🤝 |
| 3 | 👍 | 👎 | 👈 | 👆 | 💪 | 👄 | 🦷 | 👂 | 👃 | 🧠 | 👀 | 🤚 | 🦶 | 🍎 | 🍊 | 🍋 |
| 4 | 🍌 | 🍉 | 🍇 | 🍓 | 🫐 | 🍒 | 🍑 | 🍍 | 🥝 | 🍆 | 🥑 | 🥦 | 🍅 | 🌽 | 🥕 | 🫒 |
| 5 | 🧄 | 🥐 | 🥯 | 🍞 | 🧀 | 🥚 | 🍗 | 🌭 | 🍔 | 🍟 | 🍕 | 🌮 | 🥙 | 🍱 | 🍜 | 🍤 |
| 6 | 🍚 | 🥠 | 🍨 | 🍦 | 🎂 | 🪴 | 🌵 | 🌱 | 💐 | 🍁 | 🍄 | 🌹 | 🌺 | 🌼 | 🌻 | 🌸 |
| 7 | 💨 | 🌊 | 💧 | 💦 | 🌀 | 🌈 | 🌞 | 🌝 | 🌛 | 🌜 | 🌙 | 🌎 | 💫 | ⭐ | 🪐 | 🌐 |
| 8 | 💛 | 💔 | 💘 | 💖 | 💕 | 🏁 | 🚩 | 💬 | 💯 | 🚫 | 🔴 | 🔷 | 🟩 | 🛑 | 🔺 | 🚗 |
| 9 | 🚑 | 🚒 | 🚜 | 🛵 | 🚨 | 🚀 | 🚁 | 🛟 | 🚦 | 🏰 | 🎡 | 🎢 | 🎠 | 🏠 | 🔔 | 🔑 |
| A | 🚪 | 🪑 | 🎈 | 💌 | 📦 | 📫 | 📖 | 📚 | 📌 | 🧮 | 🔒 | 💎 | 📷 | ⏰ | ⏳ | 📡 |
| B | 💡 | 💰 | 🧲 | 🧸 | 🎁 | 🎀 | 🎉 | 🪭 | 👑 | 🫖 | 🔭 | 🛁 | 🏆 | 🥁 | 🎷 | 🎺 |
| C | 🏀 | 🏈 | 🎾 | 🏓 | ✨ | 🔥 | 💥 | 👕 | 👚 | 👖 | 🩳 | 👗 | 👔 | 🧢 | 👓 | 🧶 |
| D | 🧵 | 💍 | 👠 | 👟 | 🧦 | 🧤 | 👒 | 👜 | 🐱 | 🐶 | 🐭 | 🐹 | 🐰 | 🦊 | 🐻 | 🐼 |
| E | 🐨 | 🐯 | 🦁 | 🐮 | 🐷 | 🐸 | 🐵 | 🐔 | 🐥 | 🦆 | 🦉 | 🐴 | 🦄 | 🐝 | 🐛 | 🦋 |
| F | 🐌 | 🐞 | 🐢 | 🐺 | 🐍 | 🪽 | 🐙 | 🦑 | 🪼 | 🦞 | 🦀 | 🐚 | 🦭 | 🐟 | 🐬 | 🐳 |

### Reference Implementation

The current reference implementation is in the `bc-ur` Rust crate. The `bc-ur` crate is available on [crates.io](https://crates.io/crates/bc-ur) and [GitHub](https://github.com/blockchaincommons/bc-ur-rust/).

### Reference String

The following line contains all 256 Bytemojis in order, which may be used for testing and in further implementations:

```
😀😂😆😉🙄😋😎😍😘😭🫠🥱🤩😶🤨🫥🥵🥶😳🤪😵😡🤢😇🤠🤡🥳🥺😬🤑🙃🤯😈👹👺💀👻👽😺😹😻😽🙀😿🫶🤲🙌🤝👍👎👈👆💪👄🦷👂👃🧠👀🤚🦶🍎🍊🍋🍌🍉🍇🍓🫐🍒🍑🍍🥝🍆🥑🥦🍅🌽🥕🫒🧄🥐🥯🍞🧀🥚🍗🌭🍔🍟🍕🌮🥙🍱🍜🍤🍚🥠🍨🍦🎂🪴🌵🌱💐🍁🍄🌹🌺🌼🌻🌸💨🌊💧💦🌀🌈🌞🌝🌛🌜🌙🌎💫⭐🪐🌐💛💔💘💖💕🏁🚩💬💯🚫🔴🔷🟩🛑🔺🚗🚑🚒🚜🛵🚨🚀🚁🛟🚦🏰🎡🎢🎠🏠🔔🔑🚪🪑🎈💌📦📫📖📚📌🧮🔒💎📷⏰⏳📡💡💰🧲🧸🎁🎀🎉🪭👑🫖🔭🛁🏆🥁🎷🎺🏀🏈🎾🏓✨🔥💥👕👚👖🩳👗👔🧢👓🧶🧵💍👠👟🧦🧤👒👜🐱🐶🐭🐹🐰🦊🐻🐼🐨🐯🦁🐮🐷🐸🐵🐔🐥🦆🦉🐴🦄🐝🐛🦋🐌🐞🐢🐺🐍🪽🐙🦑🪼🦞🦀🐚🦭🐟🐬🐳
```

### Note on Emoji Rendering

The rendering of emojis can vary significantly between platforms. The Bytemoji set was chosen to be as platform-independent as possible and the entire set should be universally supported where emojis are supported, but some variation in appearance is to be expected.
