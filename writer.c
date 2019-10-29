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
        if(iqr[i]>0.01 && sp[i]<2.0 && sp[i]>-1)
            fprintf (fp, "%i,%.2f,%.2f\r\n", i, iqr[i], sp[i]);
    fclose(fp);
}