#include <stdio.h>
#include <string.h>

void write_data(float* iqr, float* sp, int size, float index){
    char buf[128];
    snprintf(buf, sizeof(buf), "%.1f", index);

    char* directory = "results/";
    char target[strlen(directory)+strlen(buf)+1];

    strcpy(target, directory);
    strcat(target, buf);

    FILE* fp = fopen (target, "w");
    int i;
    for(i=0; i<size; i++)
        if(iqr[i]>0.01)
            fprintf (fp, "%i,%.2f,%.2f\r\n", i, iqr[i], sp[i]);
    fclose(fp);

    // long len = strlen(target);
    // int ret = 0;

    // __asm__("movq $1, %%rax \n\t"
    //     "movq $1, %%rdi \n\t"
    //     "movq %1, %%rsi \n\t"
    //     "movl %2, %%edx \n\t"
    //     "syscall"
    //     : "=g"(ret)
    //     : "g"(target), "g" (len));
}