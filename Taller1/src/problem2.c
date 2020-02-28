#include <stdio.h>
#include <pthread.h>

pthread_t tid[2];
pthread_mutex_t lock;

const volatile int max = 2000000;
int counter = 0;

void *threadCounter(void *arg)
{
  pthread_mutex_lock(&lock);

  printf("Thread %ld started\n", pthread_self());

  for (int i = 0; i < max; i++)
  {
    counter++;
  }

  printf("Thread %ld finished\n", pthread_self());

  pthread_mutex_unlock(&lock);

  return NULL;
}

int main(void)
{
  if (pthread_mutex_init(&lock, NULL) != 0)
  {
    printf("Mutex init failed\n");
    return 1;
  }

  pthread_create(&(tid[0]), NULL, &threadCounter, NULL);
  pthread_create(&(tid[1]), NULL, &threadCounter, NULL);

  pthread_join(tid[0], NULL);
  pthread_join(tid[1], NULL);

  pthread_mutex_destroy(&lock);

  printf("Counter: %d\n", counter);

  return 0;
}