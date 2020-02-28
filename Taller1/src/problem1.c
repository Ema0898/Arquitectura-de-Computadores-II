#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>

int arr1[100];
int arr2[100];

const volatile int arrSize = 100;

pthread_t tid[3];

void *threadArr1(void *arg)
{
  int arrCounter = 0;

  while (arrCounter < arrSize)
  {
    arr1[arrCounter] = rand() % 256;

    arrCounter++;

    usleep(5000);
  }

  return NULL;
}

void *threadArr2(void *arg)
{
  int arrCounter = 0;

  while (arrCounter < arrSize)
  {
    arr2[arrCounter] = rand() % 256;

    arrCounter++;

    usleep(10000);
  }

  return NULL;
}

void *thread3(void *arg)
{
  int arrCounter = 0;

  while (arrCounter < arrSize)
  {
    usleep(15000);
    int and = arr1[arrCounter] & arr2[arrCounter];
    printf("Position %d, arr1 = %d, arr2 = %d, ", arrCounter, arr1[arrCounter], arr2[arrCounter]);
    printf("AND OP = decimal: %d, char: %c\n", and, (char)and);

    arrCounter++;
  }

  return NULL;
}

int main()
{
  srand(time(NULL));

  memset(arr1, 0, arrSize);
  memset(arr2, 0, arrSize);

  pthread_create(&(tid[0]), NULL, &threadArr1, NULL);
  pthread_create(&(tid[1]), NULL, &threadArr2, NULL);
  pthread_create(&(tid[2]), NULL, &thread3, NULL);

  pthread_join(tid[0], NULL);
  pthread_join(tid[1], NULL);
  pthread_join(tid[2], NULL);

  return 0;
}