#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

/* This simple program demonstrates the deadlock phenomenon. */
pthread_mutex_t m1 = PTHREAD_MUTEX_INITIALIZER,
                m2 = PTHREAD_MUTEX_INITIALIZER;

void *func1(void *arg) {
    pthread_mutex_lock(&m1);
    // sleep to make sure the other thread locks the other mutex
    sleep(1);
    pthread_mutex_lock(&m2);
    puts("Thread running.");
    pthread_mutex_unlock(&m2);
    pthread_mutex_unlock(&m1);
    return NULL;
}

void *func2(void *arg) {
    pthread_mutex_lock(&m2);
    // sleep to make sure the other thread locks the other mutex
    sleep(1);
    pthread_mutex_lock(&m1);
    puts("Thread running.");
    pthread_mutex_unlock(&m1);
    pthread_mutex_unlock(&m2);
    return NULL;
}

int main() {
    pthread_t t1, t2;
    int a = pthread_create(&t1, NULL, func1, NULL);
    int b = pthread_create(&t2, NULL, func2, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
}
