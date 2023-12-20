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

## Why is there a cycle?

We can begin by investigating one of the branches of broadcaster. We stop expanding when we reach one of `ft, jz, sz, ng`.

```
broadcaster -> pt, tp, gv, bv
&qq -> sr, pt, ch, lh, hj, pf, ft
%pt -> qq, pf - 1
%pf -> hv
%hv -> qq, hj - 4
%hj -> ch
%ch -> xt
%xt -> qq, lh - 32
%lh -> sr
%sr -> vr
%vr -> xq, qq - 256
%xq -> qq, rr - 512
%rr -> qq, tr - 1024
%tr -> qq     - 2048
```

It looks like all the flip flops are linked together. This means that the flip flops represents a binary number and each button press will increment the number by 1. 

```
pt (off)    pt(on)     pt(off)    pt(on)     pt(off)
pf (off) -> pf(off) -> pf(on)  -> pf(on)  -> pf(off) ...
hv (off)    hv(off)    hv(off)    hv(off)    hv(on)
```
First, we send a low to pt. pt turns on, and sends a high signal to pf, which does nothing. 
In the next press, pt turns off, sending a low to pf, which turns pf on. This then repeats.

Remember that a conjunction `&` needs all its inputs to be high before it can output a low signal. If we consider all the qq sources to be a 1, we get the binary number, `0b111100100101`, or 3877 in decimal. That equals the cycle length of ft! 

We see that ft only has one source and that is qq. So ft will only output a high when qt outputs a low. This means that ft outputs a high every 3877 presses.

But what is the line `&qq -> sr, pt, ch, lh, hj, pf, ft` doing? 

If we mark the flip flops with the destinations of qq, we get:

```
broadcaster -> pt, tp, gv, bv
&qq -> sr, pt, ch, lh, hj, pf, ft
%pt -> qq, pf #
%pf -> hv     #
%hv -> qq, hj
%hj -> ch     #
%ch -> xt     #
%xt -> qq, lh 
%lh -> sr     #
%sr -> vr     #
%vr -> xq, qq
%xq -> qq, rr
%rr -> qq, tr
%tr -> qq
```
That is clearly the two's complement of 3877. So after we reach 3877, qq sends a low signal to all the flip flops representing the two's complement of 3877. This is essentially binary addition. Adding a number with its complement overflows the sum to zero.

We can investigate another branch `ng`.
```
&vm -> ng, hz, sn, gv, nv
%gv -> vm, kq #
%kq -> vm, nv 
%nv -> mb     #
%mb -> vm, qg
%qg -> vm, sn
%sn -> nk     #
%nk -> vk, vm
%vk -> vm, hz
%hz -> mp     #
%mp -> vm, nn
%nn -> cv, vm 
%cv -> vm
```
and find that the binary represents `0b111011011011` or 3803 in decimal, representing the cycle length of ng. All the other branches are the same.

To summarise, the machine broadcasts into 4 counters, incrementing each counter by 1. Each counter has a target value. Once a counter reaches its target value, it outputs a high signal to `rx` and resets to 0. Only when all the counters reach their target value simultaneously will `rx` output a low value. This will happen at their LCM.