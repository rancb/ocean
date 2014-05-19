
#include <stdio.h>
#include <stdlib.h>

void f2()
{
	printf("addsdsdsdsaaaaaaa\n");
}

int f(int a)
{
	printf("aaaaaaaa %d\n",a);
	return a+4;
}

int main()
{
	printf("aaaa\n");
	f(42);
	f2();
	f(44);
}
