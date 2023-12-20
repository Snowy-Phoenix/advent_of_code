## Part 2 Solution:

Part 2 was solved using a bit of reverse engineering.

Consider the line containing `rx`:
`&xm -> rx`

We can expand this further by checking all the lines containing `xm`. Since `xm` is a conjunction module, this means all its source must send a high signal. From my input, the sources were:
```
&ft -> xm
&jz -> xm
&sv -> xm
&ng -> xm
```

In order for rx to receive a low pulse, `ft, jz, sz, ng` must all send a high pulse. We could repeatedly press the button and determine when they would send a high signal.

```
ng: 3803
ft: 3877
sv: 3889
jz: 3917
ng: 7606
ft: 7754
sv: 7778
jz: 7834
ng: 11409
ft: 11631
sv: 11667
jz: 11751
...
```

We see that all of these follow a predictable cycle! The cycle lengths is also equal to the first iteration these modules output high! Hence, the LCM of all of the modules will give us the first iteration we send a low to `rx`. 

We note that all of these are coprime, so the answer is simply multiplying all the cycle lengths together.