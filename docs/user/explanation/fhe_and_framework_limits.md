# FHE and **Concrete Numpy** Limits

## FHE limits

FHE used to be an impossible thing to imagine, twenty years ago. Then, with advances due to [Craig Gentry](https://crypto.stanford.edu/craig/), this became a dream come true. And, even more recently, with several generations of new scheme, FHE became practical.

### Speed

However, one still has to consider that FHE is slow, as compared to the vanilla implementations. With the different HW pluggins that can be added to **Concrete**, an important speed factor can be achieved.

### Multiplying by constants

In the scheme used in **Concrete Numpy**, namely [TFHE](https://tfhe.github.io/tfhe/), multiplications by constants is only defined for integer constants. Notably, one can't multiply by floats. As float multiplication is very usual in the data science (think of weights of dense layers, for example), this could be a problem, but quantization is at our rescue. See [this](quantization.md) section for more details.

### Achieving computations of not-linear functions

For most FHE scheme but TFHE, the application of a non-linear function is complicated and slow, if not impossible. Typically, this is a blocker, since activation functions _are_ non-linear. However, in the **Concrete Numpy** package, we use an operation called _programmable bootstrapping_ (described in this [white paper](https://whitepaper.zama.ai)), which allows to apply any table lookup: by quantizing the non-linear function, any function can thus be replaced.

## Limits of this project

Since this is an early version of the product, not everything is done, to say the least. What we wanted to tackle first was the cryptographic complexities. This is why we concentrated on the cryptographic part, and let some engineering problems for later.

### Currently executing locally

As of today, the execution of the FHE program is done locally. Notably, in the current version, there is no client (on which we encrypt the private data, or decrypt the returned result) or server (on which the computation is done completely over encrypted data), but a single host. As explained in [this section](future_features.md), this limit will be removed in the next version, such that **Concrete Numpy** can be used in production.

### Currently slow

As we explained, we wanted to focus first on cryptographic challenges. Performance has been postponed, and will be tackled in the next release.

### Currently restricted to 7 bits computations

For the moment, we can only perform computations with 7 bits or less. Furthermore, the exactness of computations is only ensured for 6 bits or less; for 7 bits, the computations are exact with a probability close to 90%. Of course, we are working on increasing this limit, and making the probability of a wrong computation as close to 0% as possible. Don't hesitate to look at our [quantization](quantization.md) section to know how to use smaller integers.

