/******* PowerStone Benchmark *******/

#ifdef STATIC_SIZE
unsigned long   src[1] = {0};
unsigned long   dst[1];
#else
unsigned long	src[1024] =
{
	0x00005678,0x12340000,0x02040608,0x00000001,
	0x12345678,0x12345678,0x12345678,0x12345678,
	0x00005678,0x12340000,0x02040608,0x00000001,
	0x12345678,0x12345678,0x12345678,0x12345678,
	0x00005678,0x12340000,0x02040608,0x00000001,
	0x12345678,0x12345678,0x12345678,0x12345678,
	0x00005678,0x12340000,0x02040608,0x00000001,
	0x12345678,0x12345678,0x12345678,0x12345678,
	0x00005678,0x12340000,0x02040608,0x00000001,
	0x12345678,0x12345678,0x12345678,0x12345678,
	0x00005678,0x12340000,0x02040608,0x00000001,
	0x10101010,0x12345678,0x10101010,0x12345678,
	0x00005678,0x12340000,0x02040608,0x00000001,
	0x10101010,0x12345678,0x10101010,0x12345678,
	0x00005678,0x12340000,0x02040608,0x00000001,
	0x10101010,0x12345678,0x10101010,0x12345678,
	0
};
unsigned long	dst[1024];
#endif

void blit(unsigned long saddr, unsigned long daddr, unsigned long n)
{
	int		d1, d2;
	unsigned long	*s, *d, x, y;
	unsigned long	soff, doff;

	s = (unsigned long *)((unsigned long)src + (saddr >> 5));
	d = (unsigned long *)((unsigned long)dst + (daddr >> 5));
	soff = saddr & 0x1f;
	doff = daddr & 0x1f;
	if (soff > doff)
	{	d1 = soff - doff;
		d2 = 32 - d1;
		y = *d & (0xffffffff << (32-doff));
		x = *s++ & ((unsigned)0xffffffff >> soff);
		y |= x << d1;
		for ( ; n >= 32 ; n -= 32, s++, d++)
		{	x = *s;
			*d = y | (x >> d2);
			y = x << d1;
		}
		x = *d & (0xffffffff << (32 - n + d1));
		*d = y | x;
	}
	else if (soff < doff)
	{	d1 = doff - soff;
		d2 = 32 - d1;
		y = *d & (0xffffffff << (32-doff));
		x = *s++ & ((unsigned)0xffffffff >> soff);
		for ( ; n >= 32 ; n -= 32, s++, d++)
		{	*d = y | (x >> d1);
			y = x << d2;
			x = *s;
		}
		x = *d & (0xffffffff << (32 - n + d1));
		*d = y | (x >> d1);
	}
	else
	{	if (soff)
		{	y = *d & (0xffffffff << (32-doff));
			x = *s++ & ((unsigned)0xffffffff >> soff);
			*d++ = x | y;
			n -= (32 - soff);
		}
		for ( ; n >= 32 ; n -= 32, s++, d++)
			*d = *s;
		if (n)
		{	y = *d & ((unsigned)0xffffffff >> doff);
			x = *s & (0xffffffff << (32-soff));
			*d = x | y;
		}
	}
}


int main()
{
    #ifdef TSIM_DISABLE_CACHE
    /*Now I can disable the caches*/
    #ifdef LEON3_CACHE
    asm("sta %g0, [%g0] 2");
    #else
    asm("sethi %hi(0xfd800000), %g1");
    asm("or %g1,%lo(0xfd800000),%g1");
    asm("sethi %hi(0x80000014), %g2");
    asm("or %g2,%lo(0x80000014),%g2");
    asm("st %g1, [%g2]");
    #endif
    #endif

    int i = 0;

	blit(17, 29, 1000*32);	/* bit blit */
	blit(29, 17, 1000*32);

    #ifdef SHORT_BENCH
    for(i = 0; i < 10; i++){
    #else
    for(i = 0; i < 1000; i++){
    #endif
        blit(17, 29, 1000*32);  /* bit blit */
        blit(29, 17, 1000*32);
    }

	return 0;
}