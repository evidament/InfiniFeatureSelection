#include <stdio.h>
#include <string.h>

void write_data(float* iqr, float* sp, int size, int cols, float index){
    char buf[128];
    snprintf(buf, sizeof(buf), "%.1f", index);

    char* directory = "results/";
    char target[strlen(directory)+strlen(buf)+1];

    strcpy(target, directory);
    strcat(target, buf);

    FILE* fp = fopen (target, "w");
    int i;
    for(i=0; i<size; i++)
        if(iqr[i]>0.01 && sp[i]<2.0 && sp[i]>-1){
            int ind = index*size + i;
            int col1 = ind/cols;
            int col2 = ind%cols;

            fprintf (fp, "%i,%i,%.2f,%.2f\r\n", col1, col2, iqr[i], sp[i]);
        }
    fclose(fp);
}