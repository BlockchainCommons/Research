# Password Best Practices

What are the best practices for generating encryption keys from passwords?

Current best practices are to make key-derivation processes costly. Some algorithms such as PBKDF2 do so via [key stretching](https://en.wikipedia.org/wiki/Key_stretching), to dramatically increase the CPU resources required to generate a key from a password, making it more difficult to brute-force the key. Generally, this means: combine a password with both a fixed salt (for the site) and a unique salt and then either use a slow hasing algorithm or hash thousands of times.

Some algorithms such as Bcrypt and [Scrypt](https://datatracker.ietf.org/doc/html/rfc7914) instead require high memory resources, to sidestep GPU attacks.

* PHP still uses bcrypt as default for password hashing, but has support for Argon2.
* 7zip uses [SHA-256 executed 2<sup>18</sup> (262144) times](https://en.wikipedia.org/wiki/7z#Encryption) for the encryption of its data.
* This [overview](https://medium.com/analytics-vidhya/password-hashing-pbkdf2-scrypt-bcrypt-and-argon2-e25aaf41598e) suggests Argon2 or else Scrypt as the most robust current options.
* OWASP [suggests] Argon2id, then bcrypt.

* There's also discussion that long pass phrases are more secure than increasing key-derivation time, as per [this article](https://blog.benpri.me/blog/2019/01/13/why-you-shouldnt-be-using-bcrypt-and-scrypt/).
